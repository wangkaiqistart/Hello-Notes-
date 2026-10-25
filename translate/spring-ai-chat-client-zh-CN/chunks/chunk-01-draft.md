`ChatClient` 提供与 AI 模型交互的链式 API，同时支持同步调用和流式响应。

请求以 [Prompt](https://docs.spring.io/spring-ai/reference/api/prompt.html#_prompt) 为输入，包含一组消息和调用选项：

- **用户消息**：用户输入的问题或任务。
- **系统消息**：约束模型的行为、背景和回答方式。
- **模板变量**：运行时替换的占位符，用于组合动态内容。
- **调用选项**：模型名称、控制输出随机性的 `temperature` 等参数。

`ChatClient` 同时涉及命令式与响应式编程，使用时还需关注文末的[实现说明](https://docs.spring.io/spring-ai/reference/api/chatclient.html#_implementation_notes)。

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

这里的 `@Primary` 选择默认的 **ChatClient**。如果容器中有多个 `ChatModel`，自动配置 Builder 时仍需消除模型注入歧义：给选定的 **ChatModel** 标注 `@Primary`，或自行提供 `ChatClient.Builder` Bean。两种类型的默认候选需要分别处理。

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

可以分别构建 `OpenAiChatModel`，连接提供 OpenAI 兼容 API 的不同服务：

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

| 方法 | 用途 |
| --- | --- |
| `prompt()` | 从空请求开始，继续设置用户消息、系统消息等内容。 |
| `prompt(Prompt prompt)` | 传入通过底层 API 构造的 `Prompt`。 |
| `prompt(String content)` | 直接传入用户消息文本。 |

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

<!-- 审校记录：开头将 call() 立即发送请求的简化说法澄清为选择同步方式，content() 等取结果方法触发执行；区分 ChatClient 与 ChatModel 的 @Primary；流式转换示例统一 ActorsFilms 为 ActorFilms，并将 this.chatClient/this.converter/this.flux/this.content 统一为局部变量。省略来源将一个 Token 近似为 3/4 个英文单词的估算，改为按模型与提供方规则解释。 -->
