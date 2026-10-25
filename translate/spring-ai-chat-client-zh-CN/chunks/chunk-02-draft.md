## call() 的返回值

选择 `call()` 后，可以按需要获取不同形式的结果：

| 方法 | 返回内容 |
| --- | --- |
| `String content()` | 回答的文本内容。 |
| `ChatResponse chatResponse()` | 模型响应，包含生成结果及 Token 用量等元数据。 |
| `ChatClientResponse chatClientResponse()` | 模型响应与 `ChatClient` 执行上下文，可读取 Advisor 使用的附加数据，例如 RAG 检索到的文档。 |

`entity(...)` 系列方法将返回文本映射为 Java 对象：

| 方法 | 用途 |
| --- | --- |
| `entity(ParameterizedTypeReference<T> type)` | 指定集合等泛型类型。 |
| `entity(Class<T> type)` | 指定具体 Java 类型。 |
| `entity(StructuredOutputConverter<T> structuredOutputConverter)` | 使用指定转换器将文本转为对象。 |
| `entity(ParameterizedTypeReference<T> type, Consumer<EntityParamSpec> spec)` | 泛型映射，并配置 `EntityParamSpec`。 |
| `entity(Class<T> type, Consumer<EntityParamSpec> spec)` | 具体类型映射，并配置 `EntityParamSpec`。 |
| `entity(StructuredOutputConverter<T> converter, Consumer<EntityParamSpec> spec)` | 使用指定转换器，并配置 `EntityParamSpec`。 |

`responseEntity(...)` 系列方法同时返回完整的 `ChatResponse` 和映射后的 Java 对象，适合既要读取元数据、生成结果，又要获取结构化对象的场景。这里的 `ResponseEntity` 是 Spring AI 的结果容器。

| 方法 | 用途 |
| --- | --- |
| `responseEntity(Class<T> type)` | 返回模型响应与指定类型的对象。 |
| `responseEntity(Class<T> type, Consumer<EntityParamSpec> spec)` | 同上，并配置 `EntityParamSpec`。 |
| `responseEntity(ParameterizedTypeReference<T> type)` | 返回模型响应与泛型对象，例如集合。 |
| `responseEntity(ParameterizedTypeReference<T> type, Consumer<EntityParamSpec> spec)` | 同上，并配置 `EntityParamSpec`。 |
| `responseEntity(StructuredOutputConverter<T> structuredOutputConverter)` | 返回模型响应与指定转换器生成的对象。 |
| `responseEntity(StructuredOutputConverter<T> converter, Consumer<EntityParamSpec> spec)` | 同上，并配置 `EntityParamSpec`。 |

这些带 `Consumer<EntityParamSpec>` 的重载支持配置校验等行为，详见 [EntityParamSpec](https://docs.spring.io/spring-ai/reference/api/chatclient.html#_entityparamspec)。

**`call()` 本身只选择同步调用方式，不会立即执行模型请求。** 调用 `content()`、`chatResponse()`、`responseEntity()` 等取结果的方法时，才会实际调用模型。需要流式响应时，改用 `stream()`。

## stream() 的返回值

选择 `stream()` 后，可获取以下响应流：

| 方法 | 返回内容 |
| --- | --- |
| `Flux<String> content()` | 模型逐步生成的文本片段。 |
| `Flux<ChatResponse> chatResponse()` | 包含元数据的模型响应。 |
| `Flux<ChatClientResponse> chatClientResponse()` | 包含模型响应和客户端执行上下文的响应，可读取 Advisor 使用的附加数据。 |

## 消息元数据

`ChatClient` 支持为用户消息和系统消息添加元数据（Metadata）。元数据随消息传递，为下游处理提供附加信息；具体如何使用取决于模型适配器和消息消费者。

### 为用户消息添加元数据

使用 `metadata()` 逐项添加，或一次传入一个 `Map`：

```java
// 逐项添加元数据
String response = chatClient.prompt()
    .user(u -> u.text("What's the weather like?")
        .metadata("messageId", "msg-123")
        .metadata("userId", "user-456")
        .metadata("priority", "high"))
    .call()
    .content();

// 一次添加多项元数据
Map<String, Object> userMetadata = Map.of(
    "messageId", "msg-123",
    "userId", "user-456",
    "timestamp", System.currentTimeMillis()
);

String response = chatClient.prompt()
    .user(u -> u.text("What's the weather like?")
        .metadata(userMetadata))
    .call()
    .content();
```

### 为系统消息添加元数据

系统消息使用相同方式：

```java
// 为系统消息添加元数据
String response = chatClient.prompt()
    .system(s -> s.text("You are a helpful assistant.")
        .metadata("version", "1.0")
        .metadata("model", "gpt-4"))
    .user("Tell me a joke")
    .call()
    .content();
```

### 默认元数据

在 `ChatClient.Builder` 中设置默认消息及其元数据：

```java
@Configuration
class Config {
    @Bean
    ChatClient chatClient(ChatClient.Builder builder) {
        return builder
            .defaultSystem(s -> s.text("You are a helpful assistant")
                .metadata("assistantType", "general")
                .metadata("version", "1.0"))
            .defaultUser(u -> u.text("Default user context")
                .metadata("sessionId", "default-session"))
            .build();
    }
}
```

### 元数据校验

元数据必须满足以下条件：

- 键不能为 `null` 或空字符串。
- 值不能为 `null`。
- 批量传入 `Map` 时，键和值同样不能为 `null`。

以下调用会抛出 `IllegalArgumentException`：

```java
// 键为 null，会抛出 IllegalArgumentException
chatClient.prompt()
    .user(u -> u.text("Hello")
        .metadata(null, "value"))  // 无效的键
    .call()
    .content();

// 值为 null，同样会抛出 IllegalArgumentException
chatClient.prompt()
    .user(u -> u.text("Hello")
        .metadata("key", null))    // 无效的值
    .call()
    .content();
```

### 读取元数据

元数据保存在生成的 `UserMessage` 和 `SystemMessage` 中，通过消息的 `getMetadata()` 方法读取。处理 Advisor 链或检查对话历史时，可以用它获取消息附带的信息。

## 默认配置

在 `@Configuration` 类中设置默认系统提示词后，每次调用只需提供用户输入，减少重复配置。

### 默认系统提示词

下面的客户端默认以海盗口吻回答：

```java
@Configuration
class Config {

    @Bean
    ChatClient chatClient(ChatClient.Builder builder) {
        return builder.defaultSystem("You are a friendly chat bot that answers question in the voice of a Pirate")
                .build();
    }

}
```

通过 `@RestController` 调用它：

```java
@RestController
class AIController {

	private final ChatClient chatClient;

	AIController(ChatClient chatClient) {
		this.chatClient = chatClient;
	}

	@GetMapping("/ai/simple")
	public Map<String, String> completion(@RequestParam(value = "message", defaultValue = "Tell me a joke") String message) {
		return Map.of("completion", this.chatClient.prompt().user(message).call().content());
	}
}
```

使用 curl 访问接口，示例结果如下：

```bash
❯ curl localhost:8080/ai/simple
{"completion":"Why did the pirate go to the comedy club? To hear some arrr-rated jokes! Arrr, matey!"}
```

### 带参数的默认系统提示词

把口吻写成占位符，即可在调用时指定：

```java
@Configuration
class Config {

    @Bean
    ChatClient chatClient(ChatClient.Builder builder) {
        return builder.defaultSystem("You are a friendly chat bot that answers question in the voice of a {voice}")
                .build();
    }

}
```

```java
@RestController
class AIController {
	private final ChatClient chatClient;

	AIController(ChatClient chatClient) {
		this.chatClient = chatClient;
	}

	@GetMapping("/ai")
	Map<String, String> completion(@RequestParam(value = "message", defaultValue = "Tell me a joke") String message, String voice) {
		return Map.of("completion",
				this.chatClient.prompt()
						.system(sp -> sp.param("voice", voice))
						.user(message)
						.call()
						.content());
	}

}
```

使用 HTTPie 指定 `voice` 参数，示例结果如下：

```
http localhost:8080/ai voice=='Robert DeNiro'
{
    "completion": "You talkin' to me? Okay, here's a joke for ya: Why couldn't the bicycle stand up by itself? Because it was two tired! Classic, right?"
}
```

### 其他默认配置

`ChatClient.Builder` 还支持以下默认值：

| 方法 | 用途 |
| --- | --- |
| `defaultOptions(ChatOptions chatOptions)` | 配置通用模型选项，或 `OpenAiChatOptions` 等模型专用选项；具体能力参见对应类型的 JavaDoc。 |
| `defaultTools(Object... tools)` | 为每次请求注册默认工具，支持混合传入 `ToolCallback`、`ToolCallbackProvider`，以及包含 `@Tool` 方法的 POJO。 |
| `defaultToolContext(Map<String, Object> toolContext)` | 设置工具执行的默认上下文。 |
| `defaultSystem(String text)`、`defaultSystem(Resource text)`、`defaultSystem(Consumer<PromptSystemSpec> systemSpecConsumer)` | 设置默认系统消息。 |
| `defaultUser(String text)`、`defaultUser(Resource text)`、`defaultUser(Consumer<UserSpec> userSpecConsumer)` | 设置默认用户消息；使用 `Consumer` 可同时配置文本和参数。 |
| `defaultTemplateRenderer(TemplateRenderer templateRenderer)` | 设置提示词模板的默认渲染器。 |
| `defaultAdvisors(Advisor... advisor)`、`defaultAdvisors(List<Advisor> advisors)` | 配置默认 Advisor 链，例如通过 `QuestionAnswerAdvisor` 为提示词补充检索上下文，实现 RAG。 |
| `defaultAdvisors(Consumer<AdvisorSpec> advisorSpecConsumer)` | 使用 Lambda 配置多个 Advisor 及相关参数。 |

单次调用时，可使用不带 `default` 前缀的对应方法覆盖默认配置：

- `options(ChatOptions.Builder optionsCustomizer)`
- `tools(Object... tools)`
- `toolContext(Map<String, Object> toolContext)`
- `messages(Message... messages)`、`messages(List<Message> messages)`
- `system(String text)`、`system(Resource text)`、`system(Consumer<PromptSystemSpec> systemSpecConsumer)`
- `user(String text)`、`user(Resource text)`、`user(Consumer<UserSpec> userSpecConsumer)`
- `templateRenderer(TemplateRenderer templateRenderer)`
- `advisors(Advisor... advisor)`、`advisors(List<Advisor> advisors)`
- `advisors(Consumer<AdvisorSpec> advisorSpecConsumer)`

下图展示默认配置与单次请求配置的合并，以及合并后的请求通过 Advisor 链交给模型的过程。

![ChatClient 配置合并：默认配置与单次请求配置合并，形成请求并经过 Advisor 链调用模型](/images/frameworks/spring-ai/chat-client-options-merging-zh.svg)

## 基于现有配置创建客户端

`mutate()` 会基于现有设置返回一个 `ChatClient.Builder`：

- 对 `ChatClient` 调用：复制客户端的默认设置。
- 对 `ChatClientRequestSpec` 调用：复制当前请求的设置。

可以据此构建派生客户端，复用配置后再按需调整。
