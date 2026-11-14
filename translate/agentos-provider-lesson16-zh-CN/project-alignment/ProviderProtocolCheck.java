import com.sun.net.httpserver.HttpServer;
import io.micrometer.observation.ObservationRegistry;
import java.net.InetSocketAddress;
import java.nio.charset.StandardCharsets;
import java.time.Duration;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.concurrent.atomic.AtomicInteger;
import org.springframework.ai.chat.messages.UserMessage;
import org.springframework.ai.tool.ToolCallback;
import org.springframework.ai.tool.definition.ToolDefinition;
import tools.jackson.databind.JsonNode;
import tools.jackson.databind.ObjectMapper;

/** Local-only protocol check. All requests use a fake credential and a loopback server. */
public final class ProviderProtocolCheck {
    private static void check(boolean condition, String label) {
        if (!condition) throw new AssertionError(label);
    }

    public static void main(String[] args) throws Exception {
        var requests = new ArrayList<String>();
        var paths = new ArrayList<String>();
        var status = new AtomicInteger(200);
        var executions = new AtomicInteger();
        var server = HttpServer.create(new InetSocketAddress("127.0.0.1", 0), 0);
        server.createContext("/", exchange -> {
            paths.add(exchange.getRequestURI().getPath());
            requests.add(new String(exchange.getRequestBody().readAllBytes(), StandardCharsets.UTF_8));
            String body = status.get() == 200 ? """
                {"id":"local-response","object":"chat.completion","created":1,"model":"actual-test-model",
                 "choices":[{"index":0,"message":{"role":"assistant","content":null,
                   "tool_calls":[{"id":"call_1","type":"function","function":{"name":"probe","arguments":"{\\\"value\\\":\\\"ok\\\"}"}}]},
                   "finish_reason":"tool_calls"}],
                 "usage":{"prompt_tokens":11,"completion_tokens":3,"total_tokens":14}}
                """ : "{\"error\":{\"message\":\"local temporary failure\",\"type\":\"server_error\"}}";
            exchange.getResponseHeaders().add("Content-Type", "application/json");
            var bytes = body.getBytes(StandardCharsets.UTF_8);
            exchange.sendResponseHeaders(status.get(), bytes.length);
            exchange.getResponseBody().write(bytes);
            exchange.close();
        });
        server.start();
        try {
            ToolCallback tool = new ToolCallback() {
                public ToolDefinition getToolDefinition() {
                    return ToolDefinition.builder().name("probe").description("Local protocol probe")
                        .inputSchema("{\"type\":\"object\",\"properties\":{\"value\":{\"type\":\"string\"}},\"required\":[\"value\"],\"additionalProperties\":false}")
                        .build();
                }
                public String call(String input) { executions.incrementAndGet(); return "ok"; }
            };
            var prompt = OpenAiPromptFactory.create(List.of(new UserMessage("probe")),
                "requested-test-model", "low", 64, Duration.ofSeconds(5), List.of(tool),
                Map.of("private_turn_context", "not-for-model"));
            var baseUrl = "http://127.0.0.1:" + server.getAddress().getPort();
            var model = OpenAiConnectionFactory.create(baseUrl + "/v1", "local-test-key",
                Duration.ofSeconds(5), ObservationRegistry.NOOP);
            var response = model.call(prompt);
            check(paths.equals(List.of("/v1/chat/completions")), "API prefix and one physical call");
            JsonNode request = new ObjectMapper().readTree(requests.getFirst());
            check(request.get("model").asString().equals("requested-test-model"), "Agent model");
            check(request.get("reasoning_effort").asString().equals("low"), "reasoning effort");
            check(request.get("max_completion_tokens").asInt() == 64, "output budget");
            check(!request.has("temperature") && !request.has("max_tokens"), "unsupported options absent");
            check(request.get("tools").size() == 1, "tool schema present");
            check(!requests.getFirst().contains("private_turn_context")
                && !requests.getFirst().contains("not-for-model"), "ToolContext remains local");
            check(response.getResult() != null && response.getResult().getOutput().getToolCalls().size() == 1,
                "tool-only response retained");
            check(response.getResult().getOutput().getToolCalls().getFirst().id().equals("call_1"), "call ID");
            check(response.getMetadata().getModel().equals("actual-test-model"), "actual response model");
            check(response.getMetadata().getUsage().getTotalTokens() == 14, "usage retained");
            check(executions.get() == 0, "ChatModel never executed callback");

            var rootModel = OpenAiConnectionFactory.create(baseUrl, "local-test-key",
                Duration.ofSeconds(5), ObservationRegistry.NOOP);
            rootModel.call(prompt);
            check(paths.getLast().equals("/chat/completions"), "explicit root URL not appended with v1");

            int before = requests.size();
            status.set(503);
            boolean failed = false;
            try { model.call(prompt); } catch (RuntimeException expected) { failed = true; }
            check(failed && requests.size() - before == 1, "503 causes no SDK retry");
            before = requests.size();
            boolean rejected = false;
            try {
                OpenAiPromptFactory.create(List.of(new UserMessage("probe")), " ", "low", 64,
                    Duration.ofSeconds(5), List.of(tool), Map.of());
            } catch (IllegalArgumentException expected) { rejected = true; }
            check(rejected && requests.size() == before, "blank model rejected before HTTP");
            check(executions.get() == 0, "callback never executed");
            System.out.println("PASS: snippets compile; 3 local HTTP calls; Agent options, tool-only response, metadata, URL prefix, zero SDK retries, local ToolContext, blank-model rejection");
        } finally { server.stop(0); }
    }
}
