### Core Components

- `AugmentedToolCallbackProvider<T>` — wraps tool objects or providers, augmenting all tools with the specified record type.

- `AugmentedToolCallback<T>` — wraps individual `ToolCallback` instances.

- `AugmentedArgumentEvent<T>` — contains `toolDefinition()`, `rawInput()`, and `arguments()` for consumers.

- `ToolInputSchemaAugmenter` — low-level utility for schema manipulation.

The `removeExtraArgumentsAfterProcessing` option (default `true`) controls whether augmented arguments are passed to the original tool. Set it to `false` if the tool can ignore extra fields and you want them preserved in the input.

## User-Controlled Tool Execution

The auto-registered loop covers most cases, but some scenarios genuinely need you to own each iteration:

- Gating tool execution on an external approval step.

- Forwarding intermediate progress to an SSE or WebSocket endpoint.

- Applying conditional logic between turns.

- Stopping the loop based on a side-channel signal.

Opt out per call by setting `AdvisorParams.toolCallingAdvisorAutoRegister(false)` on the request. You become responsible for detecting tool calls in the `ChatResponse` and executing them via `ToolCallingManager`:

```java
ChatClient chatClient = ...
ToolCallingManager toolCallingManager = ToolCallingManager.builder().build();

ToolCallback[] tools = ToolCallbacks.from(new WeatherTools());
ChatOptions chatOptions = ToolCallingChatOptions.builder().toolCallbacks(tools).build();

String question = "What is the weather in Amsterdam and Paris?";

// ToolCallingAdvisor disabled — no tool loop runs automatically
ChatClientResponse response = chatClient.prompt()
    .user(question)
    .options(chatOptions)
    .advisors(AdvisorParams.toolCallingAdvisorAutoRegister(false))
    .call()
    .chatClientResponse();

Prompt prompt = new Prompt(List.of(new UserMessage(question)), chatOptions);

// Drive the loop yourself — each iteration is observable and interruptible
while (response.chatResponse() != null && response.chatResponse().hasToolCalls()) {
    ToolExecutionResult result = toolCallingManager.executeToolCalls(prompt, response.chatResponse());
    prompt = new Prompt(result.conversationHistory(), chatOptions);
    response = chatClient.prompt()
        .messages(result.conversationHistory())
        .options(chatOptions)
        .advisors(AdvisorParams.toolCallingAdvisorAutoRegister(false))
        .call()
        .chatClientResponse();
}
```

The same pattern applies to the streaming API, where each iteration’s chunk `Flux` can be forwarded to a subscriber while being aggregated with `ChatClientMessageAggregator`. See [User-Controlled Streaming](https://docs.spring.io/spring-ai/reference/api/tools/tool-calling-advisor.html#user-controlled-streaming) for the full streaming variant.

To disable auto-registration globally for every call from an auto-configured `ChatClient`, set:

```properties
spring.ai.chat.client.tool-calling.enabled=false
```

|  | Driving the loop yourself outside the framework also bypasses observability, advisor composition, and the single-`ToolAdvisor` invariant. For most needs — including streaming intermediate progress to a UI — placing a custom advisor **inside** the loop (see [Extending the Loop](https://docs.spring.io/spring-ai/reference/api/tools.html#extending-the-loop)) is simpler and more composable than full opt-out. |
| --- | --- |

## Extending the Loop: Custom ToolAdvisor

The tool loop is not a black box. `ToolCallingAdvisor` exposes hook methods at well-defined points, and `DefaultChatClient’s auto-configuration accepts custom implementations transparently. This is the same extension point that `ToolSearchToolCallingAdvisor` uses to implement progressive tool disclosure.

`ToolAdvisor` is a marker interface: any custom tool call advisor must implement it so that `DefaultChatClient` recognizes it, enforces the single-advisor constraint, and registers it in place of the default.

### Hook Methods

The base `ToolCallingAdvisor` exposes four pairs of protected hook methods (one each for the call and stream paths):

| Hook | When it fires |
| --- | --- |
| `doInitializeLoop` / `doInitializeLoopStream` | Once, before the first iteration |
| `doBeforeCall` / `doBeforeStream` | Before each iteration |
| `doAfterCall` / `doAfterStream` | After each iteration |
| `doFinalizeLoop` / `doFinalizeLoopStream` | Once, after the loop ends |

`ToolSearchToolCallingAdvisor` uses `doInitializeLoop` to index the tool set and augment the system message, and `doBeforeCall` to inject only the tools discovered so far. Any custom subclass follows the same pattern.

Common use cases for a custom loop:

- **Approval gate** — pause before executing a destructive tool and wait for human confirmation.

- **Observability** — emit structured events for each tool call to a side channel.

- **Budget enforcement** — count tokens or LLM calls per session and abort if limits are exceeded.

- **Custom tool resolution** — resolve tools from a dynamic source not available at startup.

### Auto-Configuration Integration

Custom `ToolAdvisor` implementations plug into the auto-configuration system without requiring any manual `ChatClient` wiring. The extension point is the `ToolCallingAdvisor.Builder<?>` bean.

`ChatClientAutoConfiguration` declares a default `ToolCallingAdvisor.Builder<?>` bean guarded by `@ConditionalOnMissingBean`. To replace it, register your own `ToolCallingAdvisor.Builder<?>` bean — typed as the base `ToolCallingAdvisor.Builder<?>` — in an auto-configuration that runs **before** `ChatClientAutoConfiguration`:

```java
@AutoConfiguration(beforeName = "org.springframework.ai.model.chat.client.autoconfigure.ChatClientAutoConfiguration")
@ConditionalOnProperty(prefix = "my.advisor", name = "enabled", havingValue = "true")
public class MyToolAdvisorAutoConfiguration {

    @Bean
    @ConditionalOnMissingBean
    ToolCallingAdvisor.Builder<?> toolCallingAdvisorBuilder(ToolCallingManager toolCallingManager) {
        return MyCustomToolCallingAdvisor.builder()
            .toolCallingManager(toolCallingManager);
    }
}
```

`ChatClient.Builder` then uses your custom builder to auto-register your advisor transparently. `ToolSearchToolCallingAdvisor’s auto-configuration uses exactly this mechanism.

For the full `ToolCallingAdvisor` builder API and hook signatures, see [ToolCallingAdvisor](https://docs.spring.io/spring-ai/reference/api/tools/tool-calling-advisor.html).

## Tool Specification Reference

The sections above cover the common paths for defining and using tools. This reference covers the underlying interfaces and customization points.

### ToolCallback

The `ToolCallback` interface models a tool: it carries the definition the model sees and the execution logic invoked when the model calls it.

```java
public interface ToolCallback {

    /** Definition used by the AI model to decide when and how to call the tool. */
    ToolDefinition getToolDefinition();

    /** Metadata controlling how the tool is handled (e.g. return-direct). */
    ToolMetadata getToolMetadata();

    /** Execute with the given JSON input and return the result. */
    String call(String toolInput);

    /** Execute with the given input and tool context. */
    String call(String toolInput, ToolContext toolContext);
}
```

Spring AI provides `MethodToolCallback` and `FunctionToolCallback` as built-in implementations. Implement `ToolCallback` directly when you need full control — for example, to proxy a remote tool source (as MCP integration does).

### ToolDefinition

`ToolDefinition` is the contract the model sees: name, description, and input schema.

```java
public interface ToolDefinition {

    /** Unique tool name within the tool set provided to the model. */
    String name();

    /** Description used by the model to decide when to call the tool. */
    String description();

    /** JSON schema of the tool's input parameters. */
    String inputSchema();
}
```

Build one with `ToolDefinition.builder()`:

```java
ToolDefinition toolDefinition = ToolDefinition.builder()
    .name("currentWeather")
    .description("Get the weather in location")
    .inputSchema("""
        {
            "type": "object",
            "properties": {
                "location": { "type": "string" },
                "unit": { "type": "string", "enum": ["C", "F"] }
            },
            "required": ["location", "unit"]
        }
    """)
    .build();
```

For method-based tools, `ToolDefinitions.from(method)` generates a definition automatically. The class is annotated with `@Tool`? The annotation’s name and description override the method-name defaults.

### JSON Schema

The input schema tells the model how to call the tool. Spring AI’s `JsonSchemaGenerator` produces the schema from a method or function’s parameter list and supports several customization annotations.

**Parameter descriptions**

Use any of these (Spring AI’s annotation has highest precedence):

- `@ToolParam(description = "…​")` — Spring AI

- `@JsonClassDescription(description = "…​")` — Jackson

- `@JsonPropertyDescription(description = "…​")` — Jackson

- `@Schema(description = "…​")` — Swagger

```java
class CustomerTools {

    @Tool(description = "Update customer information")
    void updateCustomerInfo(
            Long id,
            String name,
            @ToolParam(description = "Email address, RFC 5322 format", required = false) String email) {
        // ...
    }
}
```

**Required vs optional**

By default every parameter is required. Make a parameter optional via (in order of precedence):

- `@ToolParam(required = false)` — Spring AI

- `@JsonProperty(required = false)` — Jackson

- `@Schema(required = false)` — Swagger

- `@Nullable` — Spring Framework / JSpecify

|  | Defining the correct required status is critical for reducing hallucinations. A parameter marked required forces the model to provide a value; an optional one lets it omit. If you mark a parameter required but the model has no way to determine its value, it will make one up. |
| --- | --- |

### Tool Context

`ToolContext` lets you pass non-model data (tenant IDs, user IDs, request scope) to tool methods. The data is **not** sent to the model — it’s purely for the tool’s internal use.

![Tool Context](https://docs.spring.io/spring-ai/reference/_images/tools/tool-context.jpg)

The chat request carries the tool definitions plus the tool context, and Spring AI sends only the tool definitions to the model (1).
The model decides to call a tool and returns the tool call requests to Spring AI (2), which dispatches them to the matching tool (3).
The tool context is handed directly to the tool at invocation time (3"), so it reaches the tool without ever passing through the model.
The tool returns its result to Spring AI (4), which sends that result back to the model (5), and the model’s final answer is returned as the chat response (6).

In the example below, the `Map.of("tenantId", "acme")` passed to `.toolContext()` is the tool context from step (1), and `getCustomerInfo` reads it through its `ToolContext` parameter at step (3") — the `tenantId` reaches the tool without ever being exposed to the model.

```java
class CustomerTools {

    @Tool(description = "Retrieve customer information")
    Customer getCustomerInfo(Long id, ToolContext toolContext) {
        return customerRepository.findById(id, toolContext.getContext().get("tenantId"));
    }
}

String response = ChatClient.create(chatModel)
        .prompt("Tell me more about the customer with ID 42")
        .tools(new CustomerTools())
        .toolContext(Map.of("tenantId", "acme"))
        .call()
        .content();
```

If `toolContext` is set both as a default and at the call site, the two maps are merged; runtime values take precedence over defaults.

### Return Direct

By default, the result of a tool call is sent back to the model so it can continue the conversation. With `returnDirect = true`, the result bypasses the model and is returned directly to the caller — useful when the tool’s output is the final answer (e.g. a RAG retrieval) and the extra round-trip would add latency without value.

![Returning tool call results directly to the caller](https://docs.spring.io/spring-ai/reference/_images/tools/return-direct.jpg)

For declarative tools:

```java
@Tool(description = "Retrieve customer information", returnDirect = true)
Customer getCustomerInfo(Long id) { ... }
```

For programmatic tools, set `returnDirect` via `ToolMetadata`:

```java
ToolMetadata toolMetadata = ToolMetadata.builder()
    .returnDirect(true)
    .build();
```

|  | If the model requests multiple tool calls in a single round, `returnDirect` is only honored if **all** the called tools have `returnDirect = true`. Otherwise the results are sent back to the model. |
| --- | --- |

### Result Conversion

Tool results are converted to a `String` (the format the model expects) by a `ToolCallResultConverter`:

```java
@FunctionalInterface
public interface ToolCallResultConverter {
    String convert(Object result, Type returnType);
}
```

The default `DefaultToolCallResultConverter` uses Jackson to serialize the result. Configure a custom converter on the `@Tool` annotation (`resultConverter`) or via `ToolMetadata`.

### Method Tool Limitations

Certain types are not supported as method parameters or return values when using `MethodToolCallback`:

- `Optional` — use `@Nullable` or `@ToolParam(required = false)` instead.

- Asynchronous types (`CompletableFuture`, `Future`).

- Reactive types (`Flow`, `Mono`, `Flux`).

- Functional types (`Function`, `Supplier`, `Consumer`).

These types are not serializable to the model and have no schema representation that the model can interpret.

### Exception Handling

When a tool throws, the exception is wrapped in `ToolExecutionException` and handed to the `ToolExecutionExceptionProcessor`:

```java
@FunctionalInterface
public interface ToolExecutionExceptionProcessor {
    String process(ToolExecutionException exception);
}
```

The processor has two choices: produce an error message that the framework feeds back to the model (so the model can recover or apologize), or re-throw the exception so the caller handles it.

The default `DefaultToolExecutionExceptionProcessor`:

- Sends the message of any `RuntimeException` back to the model.

- Always re-throws checked exceptions and `Error`s.

Configure via property:

| Property | Description | Default |
| --- | --- | --- |
| `spring.ai.tools.throw-exception-on-error` | If `true`, all tool errors are thrown for the caller to handle. If `false`, errors are sent back to the model as messages. | `false` |

Or by replacing the bean:

```java
@Bean
ToolExecutionExceptionProcessor toolExecutionExceptionProcessor() {
    return new DefaultToolExecutionExceptionProcessor(true);
}
```

|  | If you implement your own `ToolCallback`, throw `ToolExecutionException` from `call()` when execution fails — that’s what the processor expects. |
| --- | --- |

### Tool Call Limits

`DefaultToolCallingManager` caps how many times a tool can be called within a turn, to guard against runaway loops:

```java
ToolCallingManager toolCallingManager = ToolCallingManager.builder()
    .maxCallsPerTool(40)                           // per-tool default
    .maxCallsPerTool("search", 10)                  // override for one tool
    .excludeToolFromLimit("getCurrentWeather")      // no limit for this tool
    .maxTotalToolCalls(150)                         // cap across all tools combined
    .onLimitExceeded(ToolCallLimitBehavior.THROW)   // or RETURN_ERROR_RESPONSE
    .build();
```

These defaults (`DefaultToolCallingManager.DEFAULT_MAX_CALLS_PER_TOOL` / `DEFAULT_MAX_TOTAL_TOOL_CALLS`) apply even without calling these methods. Use `unlimitedCallsPerTool()` / `unlimitedTotalToolCalls()` to disable a cap entirely.

#### Counting

Counts are scoped to the current turn only: only `ToolResponseMessage` entries from the last `UserMessage` onward are tallied, so history replayed by a `ChatMemory` advisor outside the loop never inflates the count for a new turn. Nothing is cached on the manager itself — counts are recomputed from `prompt.getInstructions()` on every call, so a single `ToolCallingManager` instance stays safe to share across concurrent requests. This also means disabling `ToolCallingAdvisor’s internal conversation history (see [Inside the Loop](https://docs.spring.io/spring-ai/reference/api/tools.html#inside-the-loop)) has no effect on limit counting — it always sees the complete turn history regardless of what’s trimmed for the rest of the chain.

#### Behavior When a Limit Is Exceeded

`DefaultToolCallingManager` throws `ToolCallLimitExceededException`, carrying the tool name (`null` for a total-limit breach), the limit that was hit, and the partial `ToolExecutionResult` already executed in the current batch, so no completed work is discarded. `ToolCallingAdvisor` catches it and returns the breach as the final response - a single `Generation` (via `ex.buildGeneration()`), never one generation per tool call, so a successful call earlier in a parallel batch can’t hide the breach from callers reading only the first result. Its finish reason is `ToolCallLimitExceededException.FINISH_REASON`, and any tool calls that did succeed earlier in the batch are preserved under the `METADATA_PARTIAL_TOOL_RESPONSES` metadata key instead of being discarded.

With `onLimitExceeded(ToolCallLimitBehavior.RETURN_ERROR_RESPONSE)`, the manager instead skips the call and synthesizes an error `ToolResponse` — the same mechanism used for `ToolExecutionException` — so the model is told the limit was reached and the conversation continues instead of terminating. This is also the option to reach for if you call `ToolCallingManager.executeToolCalls(…​)` directly instead of going through `ToolCallingAdvisor`.

Configure via properties:

| Property | Description | Default |
| --- | --- | --- |
| `spring.ai.tools.limits.max-calls-per-tool-default` | Max calls to one tool per turn. `-1` disables. | `40` |
| `spring.ai.tools.limits.max-calls-per-tool.<name>` | Per-tool override; `-1` exempts that tool. | — |
| `spring.ai.tools.limits.excluded-tools` | Tool names exempt from the per-tool limit. | — |
| `spring.ai.tools.limits.max-total-tool-calls` | Max tool calls across all tools per turn. `-1` disables. | `150` |
| `spring.ai.tools.limits.on-limit-exceeded` | `THROW` or `RETURN_ERROR_RESPONSE`. | `THROW` |

## Tool Resolution

Most of the time, tools are passed explicitly via `.tools(…​)` and `.defaultTools(…​)`. For more dynamic scenarios — name-based resolution at runtime — Spring AI uses `ToolCallbackResolver`:

```java
public interface ToolCallbackResolver {

    @Nullable
    ToolCallback resolve(String toolName);
}
```

By default, `StaticToolCallbackResolver` is auto-configured with all `ToolCallback` beans in the application context, plus tools produced by `ToolCallbackProvider` beans (with the exception of MCP providers, which are excluded to avoid eager listing — see [Consuming MCP Server Tools](https://docs.spring.io/spring-ai/reference/api/tools.html#consuming-mcp-server-tools)).

Replace the resolver with a custom bean if you need a different strategy (database-backed, classpath-scanned, remote):

```java
@Bean
ToolCallbackResolver toolCallbackResolver(List<ToolCallback> toolCallbacks) {
    return new StaticToolCallbackResolver(toolCallbacks);
}
```

The resolver is used internally by `ToolCallingManager` to support both [advisor-controlled execution](https://docs.spring.io/spring-ai/reference/api/tools.html#the-tool-calling-loop) and [user-controlled execution](https://docs.spring.io/spring-ai/reference/api/tools.html#user-controlled-tool-execution).

To enable the behavior — where a tool known to the resolver, but not attached to the request may be resolved by name and executed — enable the resolution fallback:

```properties
spring.ai.tools.resolution.fallback.enabled=true
```

| Property | Description | Default |
| --- | --- | --- |
| `spring.ai.tools.resolution.fallback.enabled` | If `true`, a requested tool that is absent from the request’s tool callbacks may be resolved by name through the `ToolCallbackResolver` and executed. If `false`, only the tools attached to the request can be executed. | `false` |

When constructing a `ToolCallingManager` directly, the same switch is available on the builder via `.resolutionFallbackEnabled(true)` (default `false`).

|  | Enabling the resolution fallback makes every tool reachable through the resolver executable whenever the model names it, regardless of what a request attached — including risk-tier and destructive tools. Enable it only when you fully control which tools the resolver exposes. |
| --- | --- |

## Observability

Spring AI emits Micrometer observations for tool calls under the `spring.ai.tool` name. Each observation captures:

- Tool name and definition metadata.

- Execution duration.

- Tracing context (when a `Tracer` is available).

See [Tool Calling Observability](https://docs.spring.io/spring-ai/reference/observability/index.html#_tool_calling) for the full attribute reference.

Tool call arguments and results can optionally be exported as span attributes; this is disabled by default for sensitivity reasons. See [Tool Call Arguments and Result Data](https://docs.spring.io/spring-ai/reference/observability/index.html#_tool_call_arguments_and_result_data) to enable it.

### Logging

All main operations log at `DEBUG`. Enable with:

```properties
logging.level.org.springframework.ai=DEBUG
```

## ChatModel Tool Calling

For users who want to drive `ChatModel` directly — without `ChatClient` and without `ToolCallingAdvisor` — Spring AI supports a low-level tool calling path. This is the right choice when you need full control over the request/response cycle and don’t need the advisor chain’s composition features.

See [ChatModel Tool Calling](https://docs.spring.io/spring-ai/reference/api/tools/chatmodel-tool-calling.html) for the API, precedence rules between default and runtime tools, and worked examples.

|  | The per-`ChatModel` internal tool execution loop of Spring AI 1.x has been removed. Calling `ChatModel` with tools sends the tool definitions to the model and returns the model’s response — tool calls in that response are **not** executed automatically. You drive the loop yourself, or use `ChatClient` (which auto-registers `ToolCallingAdvisor` for you). |
| --- | --- |