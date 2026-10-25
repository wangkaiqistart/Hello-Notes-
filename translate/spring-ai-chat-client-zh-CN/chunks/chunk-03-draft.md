## Advisors

[Advisors API](https://docs.spring.io/spring-ai/reference/api/advisors.html) 用于拦截、修改和增强模型交互。常见用途是在用户问题之外补充上下文：

- **业务资料**：提供模型未训练过的私有数据，并将这些资料作为回答的优先依据。
- **对话历史**：聊天模型 API 本身无状态；要让后续回答参考前文，需要随请求提供历史消息。

### 在 ChatClient 中配置 Advisor

`AdvisorSpec` 支持设置参数，并将一个或多个 Advisor 加入处理链：

```java
interface AdvisorSpec {
    AdvisorSpec param(String k, Object v);
    AdvisorSpec params(Map<String, Object> p);
    AdvisorSpec advisors(Advisor... advisors);
    AdvisorSpec advisors(List<Advisor> advisors);
}
```

Advisor 的执行顺序会影响结果：前一个 Advisor 对提示词或上下文的修改，会传递给后续 Advisor。配置时应关注各 Advisor 的 `order`，不能仅凭添加顺序判断执行先后。

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

上述组合先通过 `MessageChatMemoryAdvisor` 补充对话历史，再由 `QuestionAnswerAdvisor` 执行检索增强。进一步用法见 [Question Answer Advisor](https://docs.spring.io/spring-ai/reference/api/retrieval-augmented-generation.html#_questionansweradvisor)。

**每次使用记忆 Advisor，都必须通过 `.param()` 提供 `ChatMemory.CONVERSATION_ID`；缺失时会抛出 `IllegalArgumentException`。**

### 检索增强生成

完整流程见 [RAG](https://docs.spring.io/spring-ai/reference/api/retrieval-augmented-generation.html) 文档。

### 日志

`SimpleLoggerAdvisor` 记录 `ChatClient` 的请求与响应，便于调试。将它加入 Advisor 链，并安排在靠后的位置：

```java
ChatResponse response = ChatClient.create(chatModel).prompt()
        .advisors(new SimpleLoggerAdvisor())
        .user("Tell me a joke?")
        .call()
        .chatResponse();
```

将相应包的日志级别设为 `DEBUG`：

```properties
logging.level.org.springframework.ai.chat.client.advisor=DEBUG
```

上例用于 `application.properties`；使用 `application.yaml` 时，改为等价的 YAML 配置。

可通过以下构造方法定制请求、响应的日志内容和执行顺序：

```java
SimpleLoggerAdvisor(
    Function<ChatClientRequest, String> requestToString,
    Function<ChatResponse, String> responseToString,
    int order
)
```

例如：

```java
SimpleLoggerAdvisor customLogger = new SimpleLoggerAdvisor(
    request -> "Custom request: " + request.prompt().getUserMessage(),
    response -> "Custom response: " + response.getResult(),
    0
);
```

生产环境应避免将敏感信息写入日志。模型与向量存储交互的指标和追踪，见[可观测性](https://docs.spring.io/spring-ai/reference/observability/index.html)文档。

### 工具调用

除非明确禁用，`ChatClient` 会自动注册 `ToolCallingAdvisor`。即使当前请求没有静态配置工具，其他 Advisor 在运行时动态加入的工具也能被处理。

```java
String response = ChatClient.builder(chatModel)
    .build()
    .prompt("What day is tomorrow?")
    .tools(new DateTimeTools())   // 自动注册 ToolCallingAdvisor
    .call()
    .content();
```

默认顺序为 `Ordered.HIGHEST_PRECEDENCE + 300`。

#### 禁用自动注册

**全局禁用**：设置以下属性，关闭自动配置客户端的工具 Advisor 自动注册：

```properties
spring.ai.chat.client.tool-calling.enabled=false
```

工具定义仍会发送给模型，但模型返回的工具调用不会自动执行。此时可使用[用户控制的工具执行](https://docs.spring.io/spring-ai/reference/api/tools.html#user-controlled-tool-execution)自行驱动调用循环。

**单次调用禁用**：使用 `AdvisorParams.toolCallingAdvisorAutoRegister(false)`：

```java
chatClient.prompt("What day is tomorrow?")
    .tools(new DateTimeTools())
    .advisors(AdvisorParams.toolCallingAdvisorAutoRegister(false))
    .call()
    .content();
```

如果链中已经有自定义 `ToolCallingAdvisor`，或其他实现了 `ToolAdvisor` 的 Advisor，自动注册也会被抑制，避免重复添加。例如：

```java
chatClient.prompt("What day is tomorrow?")
    .tools(new DateTimeTools())
    .advisors(customAdvisor)    // customAdvisor 实现 ToolAdvisor，抑制自动注册
    .call()
    .content();
```

#### 定制默认 ToolCallingAdvisor

Spring Boot 通过 `spring.ai.chat.client.tool-calling.*` 属性控制自动配置：

| 属性 | 默认值 | 作用 |
| --- | --- | --- |
| `spring.ai.chat.client.tool-calling.enabled` | `true` | 设为 `false` 时禁用自动注册；仍发送工具定义，但不自动执行工具调用。 |
| `spring.ai.chat.client.tool-calling.advisor-order` | `Ordered.HIGHEST_PRECEDENCE + 300` | 设置工具 Advisor 在处理链中的位置。 |

**调整执行顺序**：

```properties
spring.ai.chat.client.tool-calling.advisor-order=0
```

需要在工具循环内反复执行的 Advisor，其 `order` 应大于工具 Advisor；每次用户请求只执行一次的 Advisor，其 `order` 应小于工具 Advisor。默认值由 `ToolCallingAdvisor.DEFAULT_ORDER` 定义。

**自行控制工具执行**：若要观察每轮工具调用，例如向界面发送中间结果，可在单次请求中使用 `AdvisorParams.toolCallingAdvisorAutoRegister(false)` 关闭自动注册，再自行驱动循环。完整示例见[使用 ChatClient 控制工具执行](https://docs.spring.io/spring-ai/reference/api/tools.html#user-controlled-tool-execution)。

**提供自定义 Builder Bean**：需要指定 `ToolCallingManager` 等组件时，可声明 `ToolCallingAdvisor.Builder<?>` Bean。自动配置使用 `@ConditionalOnMissingBean`，因此会优先使用自定义 Bean：

```java
@Bean
ToolCallingAdvisor.Builder<?> toolCallingAdvisorBuilder(ToolCallingManager myToolCallingManager) {
    return ToolCallingAdvisor.builder()
        .toolCallingManager(myToolCallingManager)
        .advisorOrder(Ordered.LOWEST_PRECEDENCE);
}
```

自动配置的 `ChatClient.Builder` 会使用这个工具 Advisor Builder。

**不使用 Spring Boot 自动配置**：直接向 `ChatClient.builder()` 传入预先配置的 Builder：

```java
ToolCallingManager customManager = ToolCallingManager.builder()
    // 自定义解析器、异常处理器等
    .build();

ChatClient chatClient = ChatClient
    .builder(chatModel, observationRegistry, null, null,
            ToolCallingAdvisor.builder().toolCallingManager(customManager))
    .build();

// 注册工具的请求会在自动添加的 Advisor 中使用 customManager
chatClient.prompt("What day is tomorrow?")
    .tools(new DateTimeTools())
    .call()
    .content();
```

#### ToolAdvisor 标记接口

`ToolAdvisor` 表明处理链已经具备工具执行能力。自定义 Advisor 实现该接口后，`ChatClient` 不会再自动添加第二个 `ToolCallingAdvisor`。详见[扩展工具调用循环](https://docs.spring.io/spring-ai/reference/api/tools.html#extending-the-loop)。

## 对话记忆

`ChatMemory` 提供添加、读取和清空会话消息的能力。当前内置的记忆实现是 `MessageWindowChatMemory`。

`MessageWindowChatMemory` 默认保留最多 **20 条消息**，不是 20 轮对话。超过上限时淘汰旧消息，同时保留系统消息；加入新的系统消息时，旧的系统消息会被移除。

底层存储由 `ChatMemoryRepository` 提供，可选实现包括：

- `InMemoryChatMemoryRepository`
- `JdbcChatMemoryRepository`
- `CassandraChatMemoryRepository`
- `Neo4jChatMemoryRepository`
- `MongoChatMemoryRepository`
- `RedisChatMemoryRepository`

所有记忆 Advisor 都要求每次调用显式提供会话 ID：`.advisors(a -> a.param(ChatMemory.CONVERSATION_ID, conversationId))`。**没有默认会话 ID**，缺失时会抛出 `IllegalArgumentException`。完整配置见[对话记忆](https://docs.spring.io/spring-ai/reference/api/chat-memory.html)文档。

### MemoryAdvisor 标记接口

`BaseChatMemoryAdvisor` 继承了 `MemoryAdvisor` 标记接口。`DefaultChatClient` 在自动注册逻辑中使用该标记识别下游记忆 Advisor。

自定义记忆 Advisor 若没有继承 `BaseChatMemoryAdvisor`，但需要参与这类识别，应实现 `MemoryAdvisor`。

## 实现说明

`ChatClient` 同时涉及命令式与响应式调用。按本文 2.0.2 版本的实现说明，需要注意：

- 自定义模型实现的 HTTP 客户端时，应同时配置 `RestClient` 和 `WebClient`。
- 流式调用依赖响应式栈。命令式应用若需流式响应，也要引入相应依赖，例如 `spring-boot-starter-webflux`。
- 非流式调用依赖 Servlet 栈。响应式应用也需要相应依赖，例如 `spring-boot-starter-web`，并考虑部分调用会阻塞。
- 工具调用采用命令式执行，会形成阻塞流程，也可能造成 Micrometer 观测不完整或中断。例如，`ChatClient` span 与工具调用 span 不能连通，前者可能保持未完成状态。
- 内置 Advisor 在普通调用中执行阻塞操作，在流式调用中执行非阻塞操作。流式调用使用的 Reactor `Scheduler` 可通过各 Advisor 的 Builder 配置。

<!-- 审校说明：保留全部代码块，仅翻译注释；将日志配置明确为 properties 写法，避免误贴到 YAML；Advisor 顺序说明补明 order，避免把添加顺序当成唯一排序依据。 -->
