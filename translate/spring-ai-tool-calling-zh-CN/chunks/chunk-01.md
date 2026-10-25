Source: https://docs.spring.io/spring-ai/reference/api/tools.html
Retrieved: 2026-10-26
Version: 2.0.2

# Tool Calling

*Tool calling* — the ability for an AI model to invoke application-defined functions and act on their results — is the essential building block of agentic AI systems. A model that can only generate text is a chatbot; a model that can discover information, take action, and loop until a goal is reached is an agent.

![The agent loop](https://docs.spring.io/spring-ai/reference/_images/tools/spring-ai-agent-loop.png)

Tools are used for two broad purposes:

- **Information retrieval** — augmenting the model’s knowledge with data from databases, web services, file systems, or search engines. Examples: fetching the current weather, querying customer records, looking up the latest news.

- **Taking action** — executing operations in your system. Examples: sending an email, booking a flight, updating a record, triggering a workflow.

Although we speak of "tool calling" as a model capability, it is the application that owns the tool calling logic. The model can request a tool call and provide input arguments; the application is responsible for executing the tool and returning the result. The model never receives direct access to the APIs behind your tools — a critical security consideration.

## Architecture Overview

Spring AI 2.0 makes the tool calling loop a first-class, composable component of the `ChatClient’s advisor chain. The flow at a glance:

- You define tools ([Defining Tools](https://docs.spring.io/spring-ai/reference/api/tools.html#defining-tools)) and pass them to `ChatClient`.

- `ChatClient` auto-registers a `ToolCallingAdvisor` ([The Tool Calling Loop](https://docs.spring.io/spring-ai/reference/api/tools.html#the-tool-calling-loop)) that drives the loop.

- The model decides which tools to call; `ToolCallingManager` executes them; the loop continues until the model produces a response without tool calls.

- Other advisors in the chain — memory, observability, retries, custom logic — compose with the loop through a single dial: **advisor ordering** ([Memory and the Tool Loop](https://docs.spring.io/spring-ai/reference/api/tools.html#memory-and-the-tool-loop)).

|  | This architecture replaces the per-`ChatModel` tool execution loops of Spring AI 1.x. Calling `ChatModel` directly is still supported for low-level use cases — see [ChatModel Tool Calling](https://docs.spring.io/spring-ai/reference/api/tools/chatmodel-tool-calling.html). |
| --- | --- |

|  | Check the [Chat Model Comparisons](https://docs.spring.io/spring-ai/reference/api/chat/comparison.html) to see which models support tool calling. |
| --- | --- |

## Quick Start

Define a tool by annotating a method with `@Tool`:

```java
import org.springframework.ai.tool.annotation.Tool;
import org.springframework.context.i18n.LocaleContextHolder;

class DateTimeTools {

    @Tool(description = "Get the current date and time in the user's timezone")
    String getCurrentDateTime() {
        return LocalDateTime.now().atZone(LocaleContextHolder.getTimeZone().toZoneId()).toString();
    }

    @Tool(description = "Set a user alarm for the given time, provided in ISO-8601 format")
    void setAlarm(String time) {
        LocalDateTime alarmTime = LocalDateTime.parse(time, DateTimeFormatter.ISO_DATE_TIME);
        System.out.println("Alarm set for " + alarmTime);
    }
}
```

Pass the tools to `ChatClient` via `.tools()` and ask a question that requires them:

```java
ChatModel chatModel = ...

String response = ChatClient.create(chatModel)
        .prompt("Can you set an alarm 10 minutes from now?")
        .tools(new DateTimeTools())
        .call()
        .content();
```

The model decides to call `getCurrentDateTime()`, then `setAlarm(…​)` with the computed time. Spring AI handles the full round-trip automatically.

## Defining Tools

Spring AI offers three ways to define tools, from highest-level to most explicit:

| Style | Use when | Section |
| --- | --- | --- |
| Declarative `@Tool` | You own the method and want minimal ceremony | [Declarative](https://docs.spring.io/spring-ai/reference/api/tools.html#declarative-tool) |
| `MethodToolCallback` | You need programmatic control over a method-backed tool | [Programmatic: Method](https://docs.spring.io/spring-ai/reference/api/tools.html#method-tool-callback) |
| `FunctionToolCallback` | You want to expose a `Function` / `Supplier` / `Consumer` lambda or method reference | [Programmatic: Function](https://docs.spring.io/spring-ai/reference/api/tools.html#function-tool-callback) |

All three produce `ToolCallback` instances that flow through the same loop. You can mix styles freely.

### Declarative: @Tool

Annotate any method — public, package-private, private; static or instance — with `@Tool`:

```java
class WeatherTools {

    @Tool(description = "Get the current weather for a given city")
    public String getWeather(String city) {
        return weatherService.fetch(city);
    }
}
```

The `@Tool` annotation supports:

- `name` — the tool name. Defaults to the method name. Must be unique within the tool set provided to a model.

- `description` — what the tool does and when to use it. Strongly recommended; without it the model has no guidance on when to call the tool.

- `returnDirect` — return the result directly to the caller instead of feeding it back to the model. See [Return Direct](https://docs.spring.io/spring-ai/reference/api/tools.html#return-direct).

- `resultConverter` — the `ToolCallResultConverter` to use. See [Result Conversion](https://docs.spring.io/spring-ai/reference/api/tools.html#result-conversion).

|  | For AOT compilation (GraalVM native image), the class containing the `@Tool` methods must be a Spring bean (e.g. `@Component`). Otherwise, annotate it with `@RegisterReflection(memberCategories = MemberCategory.INVOKE_DECLARED_METHODS)`. |
| --- | --- |

Add `@ToolParam` to describe individual parameters:

```java
class WeatherTools {

    @Tool(description = "Get the weather for a city at a specific time")
    public String getWeather(
            @ToolParam(description = "City name") String city,
            @ToolParam(description = "Time in ISO-8601 format", required = false) String at) {
        return weatherService.fetch(city, at);
    }
}
```

By default all parameters are required. `@ToolParam(required = false)` or `@Nullable` makes a parameter optional. See [JSON Schema](https://docs.spring.io/spring-ai/reference/api/tools.html#json-schema) for the full schema customization options.

### Programmatic: MethodToolCallback

For dynamic tool registration — when you don’t control the source class, or you want to build the tool definition at runtime — use `MethodToolCallback`:

```java
Method method = ReflectionUtils.findMethod(WeatherTools.class, "getWeather", String.class);

MethodToolCallback callback = MethodToolCallback.builder()
    .toolDefinition(ToolDefinitions.builder(method)
        .description("Get the current weather for a given city")
        .build())
    .toolMethod(method)
    .toolObject(new WeatherTools())
    .build();
```

The `toolObject` is required for instance methods, optional for static methods. See [Tool Specification Reference](https://docs.spring.io/spring-ai/reference/api/tools.html#tool-specification-reference) for the full builder API.

### Programmatic: FunctionToolCallback

For tools backed by a `Function`, `Supplier`, `Consumer`, or `BiFunction` — including lambdas and method references — use `FunctionToolCallback`:

```java
FunctionToolCallback callback = FunctionToolCallback.builder("currentWeather", weatherService::getWeather)
    .description("Get the weather in location")
    .inputType(WeatherRequest.class)
    .build();
```

The factory takes a name and the function reference. The builder sets the description and the input type (used for JSON schema generation).

### ToolCallback Beans

Spring AI automatically discovers `ToolCallback` beans in the application context and exposes them through the `ToolCallbackResolver` for name-based lookup. Define a tool once as a `@Bean` and inject it where needed:

```java
@Configuration(proxyBeanMethods = false)
class WeatherToolsConfig {

    @Bean
    ToolCallback currentWeather(WeatherService weatherService) {
        return FunctionToolCallback.builder("currentWeather", weatherService::getWeather)
            .description("Get the weather in location")
            .inputType(WeatherRequest.class)
            .build();
    }
}
```

Inject and pass the bean to `ChatClient`:

```java
@Autowired ToolCallback currentWeather;

ChatClient.create(chatModel)
    .prompt("What's the weather in Copenhagen?")
    .tools(currentWeather)
    .call()
    .content();
```

|  | Spring AI 2.0 removes the `SpringBeanToolCallbackResolver` pattern where bare `Function` beans were resolved by name via `toolNames(…​)`. Tools must now be registered as explicit `ToolCallback` beans. See [Upgrading Tool Calling from 1.x to 2.0](https://docs.spring.io/spring-ai/reference/upgrade-notes.html#tool-calling-1x-to-2x). |
| --- | --- |

## Passing Tools to ChatClient

`ChatClient` exposes two methods for providing tools:

```java
// Per call — tools available only for this single request
chatClient.prompt(...)
    .tools(new WeatherTools(), currentWeather)
    .call();

// As defaults — tools available on every request built from this client
ChatClient client = ChatClient.builder(chatModel)
    .defaultTools(new WeatherTools(), currentWeather)
    .build();
```

Both methods are **heterogeneous**: they accept `@Tool`-annotated POJO instances, `ToolCallback` instances, `ToolCallbackProvider` instances, and arrays or collections of any of these. You can mix styles in a single call.

Per-call `.tools(…​)` **appends** to the client’s defaults — it does not replace them. The final tool list sent to the model is the union of `.defaultTools(…​)` and any `.tools(…​)` added at the call site.

|  | Default tools are shared across every request built from the same `ChatClient.Builder`. They are useful for tools that should always be available, but they can also be dangerous if used carelessly — risk-tier and destructive tools should typically be added per call, not as defaults. |
| --- | --- |

|  | Tools registered via `ToolCallingChatOptions.toolCallbacks(…​)` on the underlying `ChatModel` **are** overridden by the request-level tool list. See [ChatModel Tool Calling](https://docs.spring.io/spring-ai/reference/api/tools/chatmodel-tool-calling.html) for the precedence rules. |
| --- | --- |

## The Tool Calling Loop

When you call `.call()` or `.stream()` on a `ChatClient` request, the request flows through the advisor chain. `ToolCallingAdvisor` — auto-registered by `DefaultChatClient` — owns the tool execution lifecycle:

![Tool Calling Advisor Flow](https://docs.spring.io/spring-ai/reference/_images/tools/spring-ai-tool-calling-advisor-flow.png)

- The advisor sends the request to the model with all registered tool definitions included.

- The model decides whether to call any tools and returns a response.

- If the response contains tool calls, the advisor:

- Hands them to `ToolCallingManager`, which finds the matching `ToolCallback` and executes it.

- Appends the tool results to the conversation history.

- Sends the updated history back to the model.

- Steps 2–3 repeat until the model produces a response without tool calls; that response is returned to the caller.

Both blocking (`.call()`) and streaming (`.stream()`) modes are fully supported.

`ToolCallingAdvisor` is a **recursive advisor** — it re-enters the downstream advisor chain on each iteration of the loop. The same mechanism drives structured-output validation retries and any other looped advisor pattern. See [Recursive Advisors](https://docs.spring.io/spring-ai/reference/api/advisors-recursive.html) for the underlying pattern.

`DefaultChatClient` enforces that **exactly one `ToolAdvisor` is present** in the chain. Attempting to register a second one fails with an explicit error.

For the full `ToolCallingAdvisor` builder API, hook methods, and configuration options, see [ToolCallingAdvisor](https://docs.spring.io/spring-ai/reference/api/tools/tool-calling-advisor.html).

## Memory and the Tool Loop

Where you place `MessageChatMemoryAdvisor` relative to `ToolCallingAdvisor` (default order `HIGHEST_PRECEDENCE + 300`) determines how much conversation context the memory store captures.

### Outside the Loop (default)

`MessageChatMemoryAdvisor’s default order is `HIGHEST_PRECEDENCE + 200` — lower than `ToolCallingAdvisor`, which places it **outside** the loop. The memory advisor:

- Loads history once before the loop starts.

- Persists only the final user message and the final assistant message after the loop completes.

- Never sees tool call requests or tool response messages.

This is the safe default and works with every `ChatMemoryRepository` implementation. It also matches the behavior of Spring AI 1.x, where the tool loop was internal to each `ChatModel` and memory could not observe tool messages.

```java
var chatClient = ChatClient.builder(chatModel)
    .defaultAdvisors(MessageChatMemoryAdvisor.builder(chatMemory).build())  // outside the loop by default
    .build();
```

### Inside the Loop

To give the model the full tool transcript on subsequent turns — so it can reason about what was already tried, which tools were called, and what they returned — place the memory advisor **inside** the loop by giving it an order greater than `ToolCallingAdvisor.DEFAULT_ORDER`:

```java
var chatMemoryAdvisor = MessageChatMemoryAdvisor.builder(chatMemory)
    .order(BaseAdvisor.HIGHEST_PRECEDENCE + 400)  // inside (after) ToolCallingAdvisor
    .build();

var chatClient = ChatClient.builder(chatModel)
    .defaultAdvisors(chatMemoryAdvisor)
    .build();
```

To avoid duplicate writes, `ToolCallingAdvisor’s internal conversation history must be disabled when a memory advisor sits inside the loop. With the auto-registered `ToolCallingAdvisor`**, this is automatic** — `DefaultChatClient` detects any `MemoryAdvisor` inside the loop and disables internal history with no additional configuration. If you construct a `ToolCallingAdvisor` manually, call `.disableInternalConversationHistory()` on the builder yourself.

|  | Disabling internal history only changes what’s forwarded to the rest of the chain each round — [tool call limits](https://docs.spring.io/spring-ai/reference/api/tools.html#tool-call-limits) still see the complete history for the current turn regardless, so limits keep working correctly with a memory advisor nested inside the loop. |
| --- | --- |

![ChatMemoryAdvisor inside the ToolCallingAdvisor loop](https://docs.spring.io/spring-ai/reference/_images/tools/spring-ai-tool-calling-with-inside-memory.png)

### Backend Compatibility

Not every `ChatMemoryRepository` can persist tool messages. The repository has to know how to serialize `ToolResponseMessage` and tool call request messages alongside ordinary user and assistant turns — and most current implementations only model the latter.

As of 2.0, the built-in repositories that support the full message set are:

- [InMemoryChatMemoryRepository](https://docs.spring.io/spring-ai/reference/api/chat-memory.html#_in_memory_repository)

- [RedisChatMemoryRepository](https://docs.spring.io/spring-ai/reference/api/chat-memory.html#_redischatmemoryrepository)

- [Neo4jChatMemoryRepository](https://docs.spring.io/spring-ai/reference/api/chat-memory.html#_neo4j_chatmemoryrepository)

Any of them is safe inside the loop.

|  | For JDBC-backed persistence with full tool-message support — plus event-sourced history, turn-aware compaction, and multi-agent branch isolation — see the [spring-ai-session](https://spring-ai-community.github.io/spring-ai-session/latest/) community project. It is designed for exactly this scenario and is planned for inclusion in Spring AI 2.1. |
| --- | --- |

## Scaling to Hundreds of Tools

The default `ToolCallingAdvisor` sends all registered tool definitions to the model on every request. With a small tool library this is fine. At 30+ tools — or in multi-server MCP setups where a session may aggregate hundreds of tool definitions — it creates context bloat, accuracy degradation, and unnecessary token cost.

`ToolSearchToolCallingAdvisor` is a drop-in replacement that implements the **progressive tool disclosure** pattern: it indexes the full tool set once per session and injects only a built-in `toolSearchTool` the model uses to retrieve relevant tools by natural language query. Only discovered tools are included in subsequent requests.

Enable it with a single property:

```properties
spring.ai.chat.client.tool-search-advisor.enabled=true
```

See [Tool Search Tool](https://docs.spring.io/spring-ai/reference/api/tools/tool-search-tool.html) for the full configuration, indexing strategies, session-ID semantics, and tuning options.

## MCP Tools

The [Model Context Protocol](https://modelcontextprotocol.io/) (MCP) is a standardized way for AI applications to consume tools, resources, and prompts from remote servers. Spring AI integrates MCP from both directions: your application can consume tools from MCP servers, and it can expose its own tools to MCP clients.

### Consuming MCP Server Tools

Add the MCP client starter and configure connections to one or more MCP servers:

```xml
<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>spring-ai-starter-mcp-client</artifactId>
</dependency>
```

```properties
spring.ai.mcp.client.stdio.connections.my-server.command=npx
spring.ai.mcp.client.stdio.connections.my-server.args=-y,@modelcontextprotocol/server-everything
```

Auto-configuration connects to all configured servers, discovers their tools, and exposes them as a `SyncMcpToolCallbackProvider` bean (or `AsyncMcpToolCallbackProvider` for the async client type).

|  | MCP providers are deliberately **not** auto-registered with the `ChatClient` — they implement `ToolCallbackProvider`, but listing tools eagerly would force a network round-trip to every connected MCP server at startup. Inject the provider and wire it explicitly: |
| --- | --- |

```java
@Autowired SyncMcpToolCallbackProvider mcpTools;

// Once, as default tools for every request
ChatClient chatClient = ChatClient.builder(chatModel)
    .defaultTools(mcpTools)
    .build();

// Or per call
chatClient.prompt()
    .user("Search the web for the latest Spring AI release notes")
    .tools(mcpTools)
    .call()
    .content();
```

Tool callback auto-configuration is enabled by default and can be turned off with `spring.ai.mcp.client.toolcallback.enabled=false`. See [MCP Client Boot Starter](https://docs.spring.io/spring-ai/reference/api/mcp/mcp-client-boot-starter-docs.html) for the full configuration surface — transports, security, filtering, name-prefix generation.

### Exposing Spring Tools as an MCP Server

Going the other direction — exposing your Spring beans as MCP tools — is a matter of using `@McpTool` (instead of `@Tool`) and adding the MCP server starter:

```xml
<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>spring-ai-starter-mcp-server-webmvc</artifactId>
</dependency>
```

```java
@Component
public class WeatherTools {

    @McpTool(description = "Get the current weather for a given city")
    public String getWeather(
            @McpToolParam(description = "City name") String city) {
        return weatherService.fetch(city);
    }
}
```

Auto-configuration scans for `@McpTool`-annotated beans, generates JSON schemas for their parameters, and registers them with the MCP server. See [MCP Server Boot Starter](https://docs.spring.io/spring-ai/reference/api/mcp/mcp-server-boot-starter-docs.html) for transport, security, and observability options.

### Combining Local and MCP Tools

Local `@Tool` methods and remote MCP tools share the same `ToolCallback` interface — the model and the `ToolCallingAdvisor` don’t distinguish between them. `.tools(…​)` and `.defaultTools(…​)` accept both types in a single call, so you can mix freely:

```java
chatClient.prompt()
    .tools(new LocalTools(), mcpTools)
    .call()
    .content();
```

A few things to be aware of in hybrid setups:

- **Name conflicts are only handled within the MCP side.** `DefaultMcpToolNamePrefixGenerator` prefixes duplicates across MCP servers, but it doesn’t know about local `@Tool` methods. If a local tool and a remote MCP tool share a name, you need to rename one of them yourself, or use an `McpToolFilter` to drop the remote one.

- **Restrict what’s exposed.** MCP tools come from external sources whose surface you don’t fully control. An `McpToolFilter` bean lets you select which tools enter the namespace based on server identity, tool name, or description — useful for limiting the blast radius of a chatty or untrusted MCP server.

|  | A name conflict between two tool sources is only caught when the merged list goes through `ChatClient`. `.tools(…​)` and `.defaultTools(…​)` validate the full merged list and throw `IllegalStateException` if any two callbacks share a name, so a conflict here fails the request instead of running the wrong tool. That validation does not run if you call `ChatModel.call()`/`.stream()` directly, or build your own tool-calling loop, with a hand-assembled `ToolCallingChatOptions`. On that path, tool execution resolves by name only: whichever callback comes first in the merged list wins, silently, with no error or log. A remote MCP tool that happens to share a name with a trusted local tool can therefore execute in its place. If you combine local and MCP tools outside `ChatClient`, either keep the sources namespaced so their names can’t collide (see [Tool Name Prefix Generation](https://docs.spring.io/spring-ai/reference/api/mcp/mcp-client-boot-starter-docs.html#mcp-tool-name-prefix-generation)), or call `ToolCallingChatOptions.validateToolCallbacks(…​)` yourself on the merged list before use. |
| --- | --- |

## Tool Argument Augmentation

Spring AI provides a utility for dynamic augmentation of tool input schemas with additional arguments. This lets you capture extra information from the model — such as reasoning, confidence, or metadata — without modifying the underlying tool implementation. The model sees the augmented schema and fills in the extra fields; your code receives them via a consumer; the original tool receives only its expected arguments, unchanged.

Common use cases:

- **Inner thinking / reasoning** — capture the model’s step-by-step reasoning before executing a tool.

- **Memory enhancement** — extract insights to store in long-term memory.

- **Analytics & tracking** — collect metadata, user intent, or usage patterns.

- **Multi-agent coordination** — pass agent identifiers or coordination signals.

![Tool Argument Augmentation](https://docs.spring.io/spring-ai/reference/_images/tools/spring-ai-tool-arg-augmenter.png)

### Quick Start

Define the augmented arguments as a Java record:

```java
public record AgentThinking(
    @ToolParam(description = "Your reasoning for calling this tool", required = true)
    String innerThought,

    @ToolParam(description = "Confidence level (low, medium, high)", required = false)
    String confidence
) {}
```

Wrap your tools with `AugmentedToolCallbackProvider`:

```java
AugmentedToolCallbackProvider<AgentThinking> provider = AugmentedToolCallbackProvider
    .<AgentThinking>builder()
    .toolObject(new WeatherTools())     // wrap the original tools
    .argumentType(AgentThinking.class)  // augmentation schema type
    .argumentConsumer(event -> {        // optional consumer of augmented content
        AgentThinking thinking = event.arguments();
        log.info("Tool: {} | Reasoning: {}", event.toolDefinition().name(), thinking.innerThought());
    })
    .removeExtraArgumentsAfterProcessing(true)
    .build();

ChatClient chatClient = ChatClient.builder(chatModel)
    .defaultTools(provider)
    .build();
```

The LLM sees the augmented schema with your additional fields. Your consumer receives the `AgentThinking` record; the original tool receives only its expected arguments.