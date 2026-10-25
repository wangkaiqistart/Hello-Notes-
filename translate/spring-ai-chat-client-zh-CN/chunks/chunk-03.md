## Advisors

The [Advisors API](https://docs.spring.io/spring-ai/reference/api/advisors.html) provides a flexible and powerful way to intercept, modify, and enhance AI-driven interactions in your Spring applications.

A common pattern when calling an AI model with user text is to append or augment the prompt with contextual data.

This contextual data can be of different types. Common types include:

- **Your own data**: This is data the AI model hasn’t been trained on. Even if the model has seen similar data, the appended contextual data takes precedence in generating the response.

- **Conversational history**: The chat model’s API is stateless. If you tell the AI model your name, it won’t remember it in subsequent interactions. Conversational history must be sent with each request to ensure previous interactions are considered when generating a response.

### Advisor Configuration in ChatClient

The ChatClient fluent API provides an `AdvisorSpec` interface for configuring advisors. This interface offers methods to add parameters, set multiple parameters at once, and add one or more advisors to the chain.

```java
interface AdvisorSpec {
    AdvisorSpec param(String k, Object v);
    AdvisorSpec params(Map<String, Object> p);
    AdvisorSpec advisors(Advisor... advisors);
    AdvisorSpec advisors(List<Advisor> advisors);
}
```

The order in which advisors are added to the chain is crucial, as it determines the sequence of their execution.
Each advisor modifies the prompt or the context in some way, and the changes made by one advisor are passed on to the next in the chain.

```java
ChatClient.builder(chatModel)
    .build()
    .prompt()
    .advisors(a -> a
        .advisors(
            MessageChatMemoryAdvisor.builder(chatMemory).build(),
            QuestionAnswerAdvisor.builder(vectorStore).build()
        )
        .param(ChatMemory.CONVERSATION_ID, conversationId))
    .user(userText)
    .call()
    .content();
```

In this configuration, the `MessageChatMemoryAdvisor` will be executed first, adding the conversation history to the prompt. Then, the `QuestionAnswerAdvisor` will perform its search based on the user’s question and the added conversation history, potentially providing more relevant results.

`ChatMemory.CONVERSATION_ID` must be supplied via `.param()` on every call that uses a memory advisor. Omitting it throws an `IllegalArgumentException` at runtime.

[Learn about Question Answer Advisor](https://docs.spring.io/spring-ai/reference/api/retrieval-augmented-generation.html#_questionansweradvisor)

### Retrieval Augmented Generation

Refer to the [Retrieval Augmented Generation](https://docs.spring.io/spring-ai/reference/api/retrieval-augmented-generation.html) guide.

### Logging

The `SimpleLoggerAdvisor` is an advisor that logs the `request` and `response` data of the `ChatClient`. This can be useful for debugging and monitoring your AI interactions.

Spring AI supports observability for LLM and vector store interactions.
Refer to the [Observability](https://docs.spring.io/spring-ai/reference/observability/index.html) guide for more information.

To enable logging, add the `SimpleLoggerAdvisor` to the advisor chain when creating your ChatClient. It’s recommended to add it toward the end of the chain:

```java
ChatResponse response = ChatClient.create(chatModel).prompt()
        .advisors(new SimpleLoggerAdvisor())
        .user("Tell me a joke?")
        .call()
        .chatResponse();
```

To see the logs, set the logging level for the advisor package to `DEBUG`:

```
logging.level.org.springframework.ai.chat.client.advisor=DEBUG
```

Add this to your `application.properties` or `application.yaml` file.

You can customize what data from `AdvisedRequest` and `ChatResponse` is logged by using the following constructor:

```java
SimpleLoggerAdvisor(
    Function<ChatClientRequest, String> requestToString,
    Function<ChatResponse, String> responseToString,
    int order
)
```

Example usage:

```java
SimpleLoggerAdvisor customLogger = new SimpleLoggerAdvisor(
    request -> "Custom request: " + request.prompt().getUserMessage(),
    response -> "Custom response: " + response.getResult(),
    0
);
```

This allows you to tailor the logged information to your specific needs.

Be cautious about logging sensitive information in production environments.

### Tool Calling

The `ChatClient` always auto-registers a `ToolCallingAdvisor` in the advisor chain unless auto-registration is explicitly disabled (see below). This ensures that tools injected dynamically at runtime by another advisor are handled correctly, even when no static tools are configured on the call.

```java
String response = ChatClient.builder(chatModel)
    .build()
    .prompt("What day is tomorrow?")
    .tools(new DateTimeTools())   // ToolCallingAdvisor is auto-registered
    .call()
    .content();
```

The `ToolCallingAdvisor` is registered at `Ordered.HIGHEST_PRECEDENCE + 300` by default.

#### Disabling Auto-Registration

##### Globally (all calls)

Set `spring.ai.chat.client.tool-calling.enabled=false` to disable auto-registration for every call made from the auto-configured `ChatClient`:

```properties
spring.ai.chat.client.tool-calling.enabled=false
```

When this property is set, tools are still sent to the AI model as definitions, but tool calls in the response are not executed automatically. Use [user-controlled tool execution](https://docs.spring.io/spring-ai/reference/api/tools.html#user-controlled-tool-execution) to drive the loop yourself.

##### Per call

You can disable auto-registration for a single call using `AdvisorParams.toolCallingAdvisorAutoRegister(false)`:

```java
chatClient.prompt("What day is tomorrow?")
    .tools(new DateTimeTools())
    .advisors(AdvisorParams.toolCallingAdvisorAutoRegister(false))
    .call()
    .content();
```

Or you can provide your own `ToolCallingAdvisor` (or any other advisor implementing `ToolAdvisor`) — in that case auto-registration is suppressed automatically because the chain already contains a `ToolAdvisor`.

You can pass a custom advisor via `.advisors()`:

```java
chatClient.prompt("What day is tomorrow?")
    .tools(new DateTimeTools())
    .advisors(customAdvisor)    // auto-registration suppressed
    .call()
    .content();
```

#### Customizing the Default ToolCallingAdvisor

The `spring.ai.chat.client.tool-calling.*` properties control the auto-configured `ToolCallingAdvisor`:

| Property | Default | Description |
| --- | --- | --- |
| `spring.ai.chat.client.tool-calling.enabled` | `true` | Set to `false` to disable `ToolCallingAdvisor` auto-registration for all calls. Tools are still sent to the model, but tool calls are not executed automatically. |
| `spring.ai.chat.client.tool-calling.advisor-order` | `Ordered.HIGHEST_PRECEDENCE + 300` | Position of the auto-registered `ToolCallingAdvisor` in the advisor chain. |

##### Spring Boot: advisor order property

The simplest way to tune the auto-registered advisor is through the `spring.ai.chat.client.tool-calling.advisor-order` property. It controls where in the advisor chain the `ToolCallingAdvisor` is inserted:

```properties
spring.ai.chat.client.tool-calling.advisor-order=0
```

The value must be lower than the order of any advisor that should run *inside* the tool-call loop (i.e., repeated on every iteration), and higher than any advisor that should run *outside* it (i.e., executed only once per user request). The default is `ToolCallingAdvisor.DEFAULT_ORDER`.

##### Spring Boot: user-controlled tool execution

To observe each iteration of the tool-calling loop — for example to forward intermediate chunks to a UI — disable the auto-registered advisor per-call and drive the loop yourself using `AdvisorParams.toolCallingAdvisorAutoRegister(false)`. See [User-Controlled Tool Execution — With ChatClient](https://docs.spring.io/spring-ai/reference/api/tools.html#user-controlled-tool-execution) for a complete example.

##### Spring Boot: custom `ToolCallingAdvisor.Builder` bean

For deeper customization — for example to supply a custom `ToolCallingManager` — declare a `ToolCallingAdvisor.Builder<?>` bean. Spring Boot’s `@ConditionalOnMissingBean` on the auto-configured bean means your bean takes precedence:

```java
@Bean
ToolCallingAdvisor.Builder<?> toolCallingAdvisorBuilder(ToolCallingManager myToolCallingManager) {
    return ToolCallingAdvisor.builder()
        .toolCallingManager(myToolCallingManager)
        .advisorOrder(Ordered.LOWEST_PRECEDENCE);
}
```

The `ChatClient.Builder` bean is then automatically wired with this custom builder.

##### Without Spring Boot

When not using Spring Boot auto-configuration, pass a pre-configured `ToolCallingAdvisor.Builder` directly to `ChatClient.builder()`:

```java
ToolCallingManager customManager = ToolCallingManager.builder()
    // custom resolver, exception processor, etc.
    .build();

ChatClient chatClient = ChatClient
    .builder(chatModel, observationRegistry, null, null,
            ToolCallingAdvisor.builder().toolCallingManager(customManager))
    .build();

// Every prompt that registers tools will use customManager in the auto-registered advisor
chatClient.prompt("What day is tomorrow?")
    .tools(new DateTimeTools())
    .call()
    .content();
```

#### ToolAdvisor Marker Interface

`ToolAdvisor` is a marker interface that signals to the `ChatClient` that the advisor chain already handles tool execution. Implementing this interface on a custom advisor prevents the auto-registration of a second `ToolCallingAdvisor`.

For more details see [Extending the Loop: Custom ToolAdvisor](https://docs.spring.io/spring-ai/reference/api/tools.html#extending-the-loop).

## Chat Memory

The interface `ChatMemory` represents a storage for chat conversation memory. It provides methods to add messages to a conversation, retrieve messages from a conversation, and clear the conversation history.

There is currently one built-in implementation: `MessageWindowChatMemory`.

`MessageWindowChatMemory` is a chat memory implementation that maintains a window of messages up to a specified maximum size (default: 20 messages). When the number of messages exceeds this limit, older messages are evicted, but system messages are preserved. If a new system message is added, all previous system messages are removed from memory. This ensures that the most recent context is always available for the conversation while keeping memory usage bounded.

The `MessageWindowChatMemory` is backed by the `ChatMemoryRepository` abstraction which provides storage implementations for the chat conversation memory. There are several implementations available, including the `InMemoryChatMemoryRepository`, `JdbcChatMemoryRepository`, `CassandraChatMemoryRepository`, `Neo4jChatMemoryRepository`, `MongoChatMemoryRepository`, and `RedisChatMemoryRepository`.

The `ChatMemory.CONVERSATION_ID` parameter is **required** for all memory advisors. It must be supplied on every call via `.advisors(a → a.param(ChatMemory.CONVERSATION_ID, conversationId))`. Omitting it throws an `IllegalArgumentException`. There is no default conversation ID.

For more details and usage examples, see the [Chat Memory](https://docs.spring.io/spring-ai/reference/api/chat-memory.html) documentation.

### MemoryAdvisor Marker Interface

`MemoryAdvisor` is a marker interface extended by `BaseChatMemoryAdvisor`. `DefaultChatClient` uses this marker to detect downstream memory advisors in the auto-registration logic.

Custom memory advisors that do not extend `BaseChatMemoryAdvisor` but should participate in this detection should implement `MemoryAdvisor`.

## Implementation Notes

The combined use of imperative and reactive programming models in `ChatClient` is a unique aspect of the API. Often an application will be either reactive or imperative, but not both.

- When customizing the HTTP client interactions of a Model implementation, both the RestClient and the WebClient must be configured.

- Streaming is only supported via the Reactive stack. Imperative applications must include the Reactive stack for this reason (e.g. spring-boot-starter-webflux).

- Non-streaming is only supportive via the Servlet stack. Reactive applications must include the Servlet stack for this reason (e.g. spring-boot-starter-web) and expect some calls to be blocking.

- Tool calling is imperative, leading to blocking workflows. This also results in partial/interrupted Micrometer observations (e.g. the ChatClient spans and the tool calling spans are not connected, with the first one remaining incomplete for that reason).

- The built-in advisors perform blocking operations for standards calls, and non-blocking operations for streaming calls. The Reactor Scheduler used for the advisor streaming calls can be configured via the Builder on each Advisor class.
