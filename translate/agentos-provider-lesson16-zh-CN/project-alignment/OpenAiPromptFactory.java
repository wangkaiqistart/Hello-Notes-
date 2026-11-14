import java.time.Duration;
import java.util.List;
import java.util.Map;
import org.springframework.ai.chat.messages.Message;
import org.springframework.ai.chat.prompt.Prompt;
import org.springframework.ai.openai.OpenAiChatOptions;
import org.springframework.ai.tool.ToolCallback;

public final class OpenAiPromptFactory {
    public static Prompt create(
            List<Message> messages, String model, String reasoningEffort,
            Integer maxOutputTokens, Duration requestTimeout,
            List<ToolCallback> tools, Map<String, Object> toolContext) {
        if (model == null || model.isBlank()) {
            throw new IllegalArgumentException("Model is required");
        }
        var options = OpenAiChatOptions.builder()
                .model(model)
                .reasoningEffort(reasoningEffort)
                .maxCompletionTokens(maxOutputTokens)
                .timeout(requestTimeout)
                .toolCallbacks(List.copyOf(tools))
                .toolContext(Map.copyOf(toolContext))
                .build();
        return new Prompt(List.copyOf(messages), options);
    }
}
