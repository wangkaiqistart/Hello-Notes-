---
title: Spring AI：ChatClient API
description: 配置模型依赖、application.yml 与 API 密钥，使用 ChatClient 完成同步与流式调用，并学习结构化输出、模板、Advisor 和对话记忆。
sidebar:
  label: ChatClient API
  order: 4
---

import { TabItem, Tabs } from '@astrojs/starlight/components';

`ChatClient` 提供与 AI 模型交互的链式 API，同时支持同步调用和流式响应。

请求以 [Prompt](https://docs.spring.io/spring-ai/reference/api/prompt.html#_prompt) 为输入，包含一组消息和调用选项：

- **用户消息**：用户输入的问题或任务。
- **系统消息**：约束模型的行为、背景和回答方式。
- **模板变量**：运行时替换的占位符，用于组合动态内容。
- **调用选项**：模型名称、控制输出随机性的 `temperature` 等参数。

`ChatClient` 同时涉及命令式与响应式编程，使用时还需关注文末的[实现说明](#实现说明)。

## 运行前配置

以下配置适用于 **Spring AI 2.0.2 + Spring Boot 4.0.x / 4.1.x**。先按[快速入门](/frameworks/spring-ai/getting-started/quickstart/)导入 BOM，并准备 Web 项目，再添加模型 Starter：

```xml
<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>spring-ai-starter-model-openai</artifactId>
</dependency>
```

在 `src/main/resources/application.yml` 中选择一种配置：

<Tabs>
  <TabItem label="OpenAI">

```yaml
spring:
  ai:
    openai:
      api-key: ${OPENAI_API_KEY}
      chat:
        model: gpt-4o-mini
```

  </TabItem>
  <TabItem label="DeepSeek（兼容接口）">

```yaml
spring:
  ai:
    openai:
      base-url: https://api.deepseek.com
      api-key: ${DEEPSEEK_API_KEY}
      chat:
        model: deepseek-chat
```

  </TabItem>
</Tabs>

在 IDEA 的 **Run → Edit Configurations → Environment variables** 中设置对应的 `OPENAI_API_KEY` 或 `DEEPSEEK_API_KEY`，模型名按账号可用型号调整。DeepSeek 使用 OpenAI 兼容接口，因此沿用同一个 Starter。

Spring AI 2.0.x 使用 `chat.model`，旧的 `chat.options.model` 已弃用。后续使用 `.stream()` 时，再添加 `spring-boot-starter-webflux`。

配置参考：[OpenAI Chat](https://docs.spring.io/spring-ai/reference/api/chat/openai-chat.html)。

## 创建 ChatClient

通过 `ChatClient.Builder` 创建客户端。可以注入 Spring Boot 为 [ChatModel](https://docs.spring.io/spring-ai/reference/api/chatmodel.html) 自动配置的 Builder，也可以手动构建。

### 使用自动配置的 ChatClient.Builder

Spring AI 提供原型作用域的 `ChatClient.Builder` Bean，可直接注入业务类。下面的接口接收用户输入并返回字符串：

```java
@RestController
class MyController {

    private final ChatClient chatClient;

    public MyController(ChatClient.Builder chatClientBuilder) {
        this.chatClient = chatClientBuilder.build();
    }

    @GetMapping("/ai")
    String generation(String userInput) {
        return this.chatClient.prompt()
            .user(userInput)
            .call()
            .content();
    }
}
```

`.user(userInput)` 设置用户消息，`.call()` 选择同步调用方式，`.content()` 触发模型调用并取得字符串回答。仅调用 `.call()` 不会立即执行模型请求。

### 使用多个聊天模型

多模型常用于任务分流、服务故障回退、A/B 测试，以及让用户选择模型。例如，复杂推理使用能力更强的模型，简单任务使用响应更快、费用更低的模型。

Spring AI 默认自动配置一个 `ChatClient.Builder` Bean。根据底层模型是否相同，可采用以下方式。

#### 同一模型类型创建多个 ChatClient

Builder 使用原型作用域，每个注入点都会获得新实例，因此可以分别设置默认值：

```java
@Configuration
class ChatClientConfig {

    @Bean
    ChatClient defaultChatClient(ChatClient.Builder builder) {
        return builder.build();
    }

    @Bean
    ChatClient customChatClient(ChatClient.Builder builder) {
        return builder.defaultSystem("You are a helpful assistant.").build();
    }
}
```

#### 为不同模型类型创建 ChatClient

直接调用 `ChatClient.create(chatModel)` 或 `ChatClient.builder(chatModel)` 会绕过自动配置的 Builder，不能自动继承其中的可观测性配置和 `ChatClientBuilderCustomizer`。

需要保留这些能力时，注入 `ChatClientBuilderConfigurer`，让它应用已注册的 Customizer，并显式传入可观测性等依赖：

```java
import io.micrometer.observation.ObservationRegistry;
import org.springframework.ai.anthropic.AnthropicChatModel;
import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.chat.client.advisor.ToolCallingAdvisor;
import org.springframework.ai.chat.client.advisor.observation.AdvisorObservationConvention;
import org.springframework.ai.chat.client.observation.ChatClientObservationConvention;
import org.springframework.ai.chat.model.ChatModel;
import org.springframework.ai.model.chat.client.autoconfigure.ChatClientBuilderConfigurer;
import org.springframework.ai.openai.OpenAiChatModel;
import org.springframework.beans.factory.ObjectProvider;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Primary;

@Configuration
public class ChatClientConfig {

    @Bean
    @Primary
    public ChatClient openAiChatClient(OpenAiChatModel chatModel, ChatClientBuilderConfigurer configurer,
            ObjectProvider<ObservationRegistry> observationRegistry,
            ObjectProvider<ChatClientObservationConvention> chatClientObservationConvention,
            ObjectProvider<AdvisorObservationConvention> advisorObservationConvention,
            ObjectProvider<ToolCallingAdvisor.Builder<?>> toolCallingAdvisorBuilder) {
        return buildChatClient(chatModel, configurer, observationRegistry,
                chatClientObservationConvention, advisorObservationConvention, toolCallingAdvisorBuilder);
    }

    @Bean
    public ChatClient anthropicChatClient(AnthropicChatModel chatModel, ChatClientBuilderConfigurer configurer,
            ObjectProvider<ObservationRegistry> observationRegistry,
            ObjectProvider<ChatClientObservationConvention> chatClientObservationConvention,
            ObjectProvider<AdvisorObservationConvention> advisorObservationConvention,
            ObjectProvider<ToolCallingAdvisor.Builder<?>> toolCallingAdvisorBuilder) {
        return buildChatClient(chatModel, configurer, observationRegistry,
                chatClientObservationConvention, advisorObservationConvention, toolCallingAdvisorBuilder);
    }

    private ChatClient buildChatClient(ChatModel chatModel, ChatClientBuilderConfigurer configurer,
            ObjectProvider<ObservationRegistry> observationRegistry,
            ObjectProvider<ChatClientObservationConvention> chatClientObservationConvention,
            ObjectProvider<AdvisorObservationConvention> advisorObservationConvention,
            ObjectProvider<ToolCallingAdvisor.Builder<?>> toolCallingAdvisorBuilder) {
        ChatClient.Builder builder = ChatClient.builder(chatModel,
                observationRegistry.getIfUnique(() -> ObservationRegistry.NOOP),
                chatClientObservationConvention.getIfUnique(),
                advisorObservationConvention.getIfUnique(),
                toolCallingAdvisorBuilder.getIfAvailable());
        return configurer.configure(builder).build();
    }
}
```

#### 单模型与多模型的配置差异

**自动配置多个模型提供方时，删除 `spring.ai.model.chat`，分别配置各自的密钥和模型名。** 如果固定为 `openai`，其他提供方的 `ChatModel` 不会自动注册，即使已经引入对应 Starter。

DeepSeek 有两种接法，依赖、配置前缀和注入类型需要对应：

| 接法              | Starter                            | 配置前缀             | 注入类型            |
| ----------------- | ---------------------------------- | -------------------- | ------------------- |
| OpenAI 兼容接口   | `spring-ai-starter-model-openai`   | `spring.ai.openai`   | `OpenAiChatModel`   |
| DeepSeek 专用接口 | `spring-ai-starter-model-deepseek` | `spring.ai.deepseek` | `DeepSeekChatModel` |

例如，将上例的 Anthropic 换成 DeepSeek 时，替换对应 Starter 和模型类型，并将客户端命名为 `deepSeekChatClient`。保留 OpenAI 配置，并在现有 YAML 中合并以下配置：

```yaml
spring:
  ai:
    deepseek:
      api-key: ${DEEPSEEK_API_KEY}
      chat:
        model: deepseek-chat
```

密钥放在 `deepseek.api-key`，模型名放在 `deepseek.chat.model`。

这里的 `@Primary` 只选择默认的 **ChatClient**。多个 `ChatModel` 存在时，如果还需注入 `ChatClient.Builder`，可在上面的配置类中添加以下方法，明确使用 OpenAI 客户端的配置（需导入 `Qualifier` 和 `Scope`）：

```java
@Bean
@Scope("prototype")
ChatClient.Builder chatClientBuilder(
        @Qualifier("openAiChatClient") ChatClient client) {
    return client.mutate();
}
```

配置依据：[DeepSeek](https://docs.spring.io/spring-ai/reference/api/chat/deepseek-chat.html) 与对应版本的自动配置源码。

业务组件可通过 `@Qualifier` 选择客户端：

```java
@Configuration
public class ChatClientExample {

    @Bean
    CommandLineRunner cli(
            @Qualifier("openAiChatClient") ChatClient openAiChatClient,
            @Qualifier("anthropicChatClient") ChatClient anthropicChatClient) {

        return args -> {
            var scanner = new Scanner(System.in);
            ChatClient chat;

            // 选择模型
            System.out.println("\nSelect your AI model:");
            System.out.println("1. OpenAI");
            System.out.println("2. Anthropic");
            System.out.print("Enter your choice (1 or 2): ");

            String choice = scanner.nextLine().trim();

            if (choice.equals("1")) {
                chat = openAiChatClient;
                System.out.println("Using OpenAI model");
            } else {
                chat = anthropicChatClient;
                System.out.println("Using Anthropic model");
            }

            // 使用选定的客户端
            System.out.print("\nEnter your question: ");
            String input = scanner.nextLine();
            String response = chat.prompt(input).call().content();
            System.out.println("ASSISTANT: " + response);

            scanner.close();
        };
    }
}
```

#### 连接多个 OpenAI 兼容端点

可以分别构建 `OpenAiChatModel`，连接提供 OpenAI 兼容 API 的不同服务。下面的模型名沿用来源示例，使用时需替换为提供方当前支持的模型：

```java
@Service
public class MultiModelService {

    private static final Logger logger = LoggerFactory.getLogger(MultiModelService.class);

    public void multiClientFlow() {
        try {
            // 为 Groq（Llama3）创建模型
            OpenAiChatModel groqModel = OpenAiChatModel.builder()
                .options(OpenAiChatOptions.builder()
                    .baseUrl("https://api.groq.com/openai/v1")
                    .apiKey(System.getenv("GROQ_API_KEY"))
                    .model("llama3-70b-8192")
                    .temperature(0.5)
                    .build())
                .build();

            // 为 GPT-4 创建模型
            OpenAiChatModel gpt4Model = OpenAiChatModel.builder()
                .options(OpenAiChatOptions.builder()
                    .baseUrl("https://api.openai.com")
                    .apiKey(System.getenv("OPENAI_API_KEY"))
                    .model("gpt-4")
                    .temperature(0.7)
                    .build())
                .build();

            // 向两个模型发送相同问题
            String prompt = "What is the capital of France?";

            String groqResponse = ChatClient.builder(groqModel).build().prompt(prompt).call().content();
            String gpt4Response = ChatClient.builder(gpt4Model).build().prompt(prompt).call().content();

            logger.info("Groq (Llama3) response: {}", groqResponse);
            logger.info("OpenAI GPT-4 response: {}", gpt4Response);
        }
        catch (Exception e) {
            logger.error("Error in multi-client flow", e);
        }
    }
}
```

## ChatClient 链式 API

使用 `prompt(...)` 开始构建请求，有三个重载：

| 方法                     | 用途                                             |
| ------------------------ | ------------------------------------------------ |
| `prompt()`               | 从空请求开始，继续设置用户消息、系统消息等内容。 |
| `prompt(Prompt prompt)`  | 传入通过底层 API 构造的 `Prompt`。               |
| `prompt(String content)` | 直接传入用户消息文本。                           |

## ChatClient 的响应

通过链式 API，可以取得完整模型响应、Java 对象或流式内容。

### 返回 ChatResponse

[ChatResponse](https://docs.spring.io/spring-ai/reference/api/chatmodel.html#ChatResponse) 包含模型生成结果和响应元数据。一份响应可以包含多个 [Generation](https://docs.spring.io/spring-ai/reference/api/chatmodel.html#Generation)，每个生成结果也可带有元数据。

元数据中的 Token 用量可用于统计调用成本。托管模型通常按 Token 计费，具体切分和计费规则取决于模型与提供方。

在 `.call()` 后调用 `.chatResponse()`，可取得完整响应：

```java
ChatResponse chatResponse = chatClient.prompt()
    .user("Tell me a joke")
    .call()
    .chatResponse();
```

### 返回 Java 对象

`entity()` 可将模型返回的文本映射为 Java 对象。例如定义一个 record：

```java
record ActorFilms(String actor, List<String> movies) {}
```

然后直接映射模型输出：

```java
ActorFilms actorFilms = chatClient.prompt()
    .user("Generate the filmography for a random actor.")
    .call()
    .entity(ActorFilms.class);
```

对于 `List<ActorFilms>` 等泛型类型，使用 `ParameterizedTypeReference`：

```java
List<ActorFilms> actorFilms = chatClient.prompt()
    .user("Generate the filmography of 5 movies for Tom Hanks and Bill Murray.")
    .call()
    .entity(new ParameterizedTypeReference<List<ActorFilms>>() {});
```

#### 可靠性配置：EntityParamSpec

`entity()` 的各类重载都可额外接收 `Consumer<EntityParamSpec>`。下面两项能力相互独立，也可以组合：

- `validateSchema()`：按目标类型的 Schema 校验 JSON，失败时携带错误信息自动重试。
- `useProviderStructuredOutput()`：将 Schema 作为提供方 API 的约束传递，而非仅通过提示词描述格式。

```java
ActorFilms actorFilms = chatClient.prompt()
    .user("Generate the filmography for a random actor.")
    .call()
    .entity(ActorFilms.class, spec -> spec
        .useProviderStructuredOutput()
        .validateSchema());
```

支持范围、限制和底层转换器 API，见[结构化输出](https://docs.spring.io/spring-ai/reference/api/structured-output.html)。

### 流式响应

使用 `.stream().content()` 取得 `Flux<String>`，在订阅后接收模型生成的文本片段：

```java
Flux<String> output = chatClient.prompt()
    .user("Tell me a joke")
    .stream()
    .content();
```

需要同时接收响应元数据时，可使用 `.stream().chatResponse()`，其返回类型为 `Flux<ChatResponse>`。

当前版本的流式 API 尚未提供直接返回 Java 对象的便捷方法。可以先聚合文本，再使用[结构化输出转换器](https://docs.spring.io/spring-ai/reference/api/structured-output/converters.html) 显式转换：

```java
var converter = new BeanOutputConverter<>(new ParameterizedTypeReference<List<ActorFilms>>() {});

Flux<String> flux = chatClient.prompt()
    .user(u -> u.text("""
                        Generate the filmography for a random actor.
                        {format}
                      """)
            .param("format", converter.getFormat()))
    .stream()
    .content();

String content = flux.collectList().block().stream().collect(Collectors.joining());

List<ActorFilms> actorFilms = converter.convert(content);
```

这里的 `block()` 用于命令式代码中等待并汇总流式结果。

## 提示词模板

用户消息和系统消息都可以使用模板，在运行时替换变量：

```java
String answer = ChatClient.create(chatModel).prompt()
    .user(u -> u
            .text("Tell me the names of 5 movies whose soundtrack was composed by {composer}")
            .param("composer", "John Williams"))
    .call()
    .content();
```

`ChatClient` 通过 `PromptTemplate` 处理文本，并委托 `TemplateRenderer` 渲染变量。默认实现 `StTemplateRenderer` 基于 Terence Parr 开发的 [StringTemplate](https://www.stringtemplate.org/) 引擎；不需要模板处理时，可使用 `NoOpTemplateRenderer`。

通过 `.templateRenderer()` 设置的渲染器只影响客户端链中的 `.user()`、`.system()` 等文本。`QuestionAnswerAdvisor` 等 Advisor 内部使用的模板有独立的[定制机制](https://docs.spring.io/spring-ai/reference/api/retrieval-augmented-generation.html#_custom_template)，不受此设置影响，详见 [Advisor 说明](https://docs.spring.io/spring-ai/reference/api/retrieval-augmented-generation.html#_questionansweradvisor)。

可以实现 `TemplateRenderer` 以使用其他模板引擎，也可以调整 `StTemplateRenderer`。默认占位符使用 `{}`；提示词包含 JSON 时，可改用其他分隔符以避免冲突，例如 `<` 与 `>`：

```java
String answer = ChatClient.create(chatModel).prompt()
    .user(u -> u
            .text("Tell me the names of 5 movies whose soundtrack was composed by <composer>")
            .param("composer", "John Williams"))
    .templateRenderer(StTemplateRenderer.builder().startDelimiterToken('<').endDelimiterToken('>').build())
    .call()
    .content();
```

## call() 的返回值

选择 `call()` 后，可以按需要获取不同形式的结果：

| 方法                                      | 返回内容                                                                                   |
| ----------------------------------------- | ------------------------------------------------------------------------------------------ |
| `String content()`                        | 回答的文本内容。                                                                           |
| `ChatResponse chatResponse()`             | 模型响应，包含生成结果及 Token 用量等元数据。                                              |
| `ChatClientResponse chatClientResponse()` | 模型响应与 `ChatClient` 执行上下文，可读取 Advisor 使用的附加数据，例如 RAG 检索到的文档。 |

`entity(...)` 系列方法将返回文本映射为 Java 对象：

| 方法                                                                             | 用途                                       |
| -------------------------------------------------------------------------------- | ------------------------------------------ |
| `entity(ParameterizedTypeReference<T> type)`                                     | 指定集合等泛型类型。                       |
| `entity(Class<T> type)`                                                          | 指定具体 Java 类型。                       |
| `entity(StructuredOutputConverter<T> structuredOutputConverter)`                 | 使用指定转换器将文本转为对象。             |
| `entity(ParameterizedTypeReference<T> type, Consumer<EntityParamSpec> spec)`     | 泛型映射，并配置 `EntityParamSpec`。       |
| `entity(Class<T> type, Consumer<EntityParamSpec> spec)`                          | 具体类型映射，并配置 `EntityParamSpec`。   |
| `entity(StructuredOutputConverter<T> converter, Consumer<EntityParamSpec> spec)` | 使用指定转换器，并配置 `EntityParamSpec`。 |

`responseEntity(...)` 系列方法同时返回完整的 `ChatResponse` 和映射后的 Java 对象，适合既要读取元数据、生成结果，又要获取结构化对象的场景。这里的 `ResponseEntity` 是 Spring AI 的结果容器。

| 方法                                                                                     | 用途                                 |
| ---------------------------------------------------------------------------------------- | ------------------------------------ |
| `responseEntity(Class<T> type)`                                                          | 返回模型响应与指定类型的对象。       |
| `responseEntity(Class<T> type, Consumer<EntityParamSpec> spec)`                          | 同上，并配置 `EntityParamSpec`。     |
| `responseEntity(ParameterizedTypeReference<T> type)`                                     | 返回模型响应与泛型对象，例如集合。   |
| `responseEntity(ParameterizedTypeReference<T> type, Consumer<EntityParamSpec> spec)`     | 同上，并配置 `EntityParamSpec`。     |
| `responseEntity(StructuredOutputConverter<T> structuredOutputConverter)`                 | 返回模型响应与指定转换器生成的对象。 |
| `responseEntity(StructuredOutputConverter<T> converter, Consumer<EntityParamSpec> spec)` | 同上，并配置 `EntityParamSpec`。     |

这些带 `Consumer<EntityParamSpec>` 的重载支持配置校验等行为，详见 [EntityParamSpec](#可靠性配置entityparamspec)。

**`call()` 本身只选择同步调用方式，不会立即执行模型请求。** 调用 `content()`、`chatResponse()`、`responseEntity()` 等取结果的方法时，才会实际调用模型。需要流式响应时，改用 `stream()`。

## stream() 的返回值

选择 `stream()` 后，可获取以下响应流：

| 方法                                            | 返回内容                                                              |
| ----------------------------------------------- | --------------------------------------------------------------------- |
| `Flux<String> content()`                        | 模型逐步生成的文本片段。                                              |
| `Flux<ChatResponse> chatResponse()`             | 包含元数据的模型响应。                                                |
| `Flux<ChatClientResponse> chatClientResponse()` | 包含模型响应和客户端执行上下文的响应，可读取 Advisor 使用的附加数据。 |

## 消息元数据

`ChatClient` 支持为用户消息和系统消息添加元数据（Metadata）。元数据随消息传递，为下游处理提供附加信息；具体如何使用取决于模型适配器和消息消费者。

### 为用户消息添加元数据

使用 `metadata()` 逐项添加，或一次传入一个 `Map`。下面展示两种独立写法：

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

| 方法                                                                                                                         | 用途                                                                                                        |
| ---------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| `defaultOptions(ChatOptions chatOptions)`                                                                                    | 配置通用模型选项，或 `OpenAiChatOptions` 等模型专用选项；具体能力参见对应类型的 JavaDoc。                   |
| `defaultTools(Object... tools)`                                                                                              | 为每次请求注册默认工具，支持混合传入 `ToolCallback`、`ToolCallbackProvider`，以及包含 `@Tool` 方法的 POJO。 |
| `defaultToolContext(Map<String, Object> toolContext)`                                                                        | 设置工具执行的默认上下文。                                                                                  |
| `defaultSystem(String text)`、`defaultSystem(Resource text)`、`defaultSystem(Consumer<PromptSystemSpec> systemSpecConsumer)` | 设置默认系统消息。                                                                                          |
| `defaultUser(String text)`、`defaultUser(Resource text)`、`defaultUser(Consumer<UserSpec> userSpecConsumer)`                 | 设置默认用户消息；使用 `Consumer` 可同时配置文本和参数。                                                    |
| `defaultTemplateRenderer(TemplateRenderer templateRenderer)`                                                                 | 设置提示词模板的默认渲染器。                                                                                |
| `defaultAdvisors(Advisor... advisor)`、`defaultAdvisors(List<Advisor> advisors)`                                             | 配置默认 Advisor 链，例如通过 `QuestionAnswerAdvisor` 为提示词补充检索上下文，实现 RAG。                    |
| `defaultAdvisors(Consumer<AdvisorSpec> advisorSpecConsumer)`                                                                 | 使用 Lambda 配置多个 Advisor 及相关参数。                                                                   |

单次调用时，可使用不带 `default` 前缀的对应方法调整默认配置。具体采用覆盖还是合并，由相应 API 决定；例如，模型选项会保留本次未指定的默认项：

- `options(ChatOptions.Builder optionsCustomizer)`
- `tools(Object... tools)`
- `toolContext(Map<String, Object> toolContext)`
- `messages(Message... messages)`、`messages(List<Message> messages)`
- `system(String text)`、`system(Resource text)`、`system(Consumer<PromptSystemSpec> systemSpecConsumer)`
- `user(String text)`、`user(Resource text)`、`user(Consumer<UserSpec> userSpecConsumer)`
- `templateRenderer(TemplateRenderer templateRenderer)`
- `advisors(Advisor... advisor)`、`advisors(List<Advisor> advisors)`
- `advisors(Consumer<AdvisorSpec> advisorSpecConsumer)`

这里的增量配置由 `ChatClient` 处理。直接调用 `ChatModel.call()` 或 `ChatModel.stream()` 时，`Prompt` 中非空的选项会作为完整配置使用；选项为 `null` 时才使用模型默认值，详见 [ChatModel](https://docs.spring.io/spring-ai/reference/api/chatmodel.html)。

下图展示默认配置与单次请求配置的合并，以及合并后的请求通过 Advisor 链交给模型的过程。

[![ChatClient 配置合并与调用链：模型选项合并为请求，经过 Advisor 调用模型，响应沿相反方向返回](/images/frameworks/spring-ai/chat-client-options-merging-zh.svg)](/images/frameworks/spring-ai/chat-client-options-merging-zh.svg)

图中 Advisor 数量仅为示意；点击图片可查看大图。

## 基于现有配置创建客户端

`mutate()` 会基于现有设置返回一个 `ChatClient.Builder`：

- 对 `ChatClient` 调用：复制客户端的默认设置。
- 对 `ChatClientRequestSpec` 调用：复制当前请求的设置。

可以据此构建派生客户端，复用配置后再按需调整。

## Advisors

[Advisors API](/frameworks/spring-ai/core/advisors/) 用于拦截、修改和增强模型交互。常见用途是在用户问题之外补充上下文：

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

上述组合由 `MessageChatMemoryAdvisor` 补充对话历史，`QuestionAnswerAdvisor` 执行检索增强。若希望先补充历史、再检索，应让记忆 Advisor 的 `order` 小于检索 Advisor。进一步用法见 [Question Answer Advisor](https://docs.spring.io/spring-ai/reference/api/retrieval-augmented-generation.html#_questionansweradvisor)。

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

| 属性                                               | 默认值                             | 作用                                                                |
| -------------------------------------------------- | ---------------------------------- | ------------------------------------------------------------------- |
| `spring.ai.chat.client.tool-calling.enabled`       | `true`                             | 设为 `false` 时禁用自动注册；仍发送工具定义，但不自动执行工具调用。 |
| `spring.ai.chat.client.tool-calling.advisor-order` | `Ordered.HIGHEST_PRECEDENCE + 300` | 设置工具 Advisor 在处理链中的位置。                                 |

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

来源：[Spring AI Chat Client API](https://docs.spring.io/spring-ai/reference/api/chatclient.html)。文档版本：2.0.2；核验日期：2026-10-25。本文为简明中文译述；示例中的类型名与局部变量不一致已校正。
