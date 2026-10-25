`ChatResponse` 不仅包含模型回答，还携带提供方返回的调用指标，例如词元（Token）用量和限流额度。Spring AI 用三个类型提供统一访问方式：

| 类型                   | 用途                                                    |
| ---------------------- | ------------------------------------------------------- |
| `ChatResponseMetadata` | 响应级元数据入口，可读取响应 ID、模型、用量和限流信息。 |
| `RateLimit`            | 请求数与 Token 的限额、剩余额度和重置时间。             |
| `Usage`                | 本次交互的输入、输出、总 Token 数及提供方原生用量信息。 |

提供方通常按一定周期统计请求数或 Token 消耗，并按服务计划设置限额。具体规则见所用服务，例如 OpenAI 的[限流说明](https://platform.openai.com/docs/guides/rate-limits?context=tier-free)和[套餐](https://openai.com/pricing#language-models)。

## ChatResponseMetadata：响应元数据入口

通过模型 API 获取响应时，Spring AI 会创建相应的 `ChatResponseMetadata`。从 `ChatResponse.getMetadata()` 读取：

```java
ChatResponse response = chatModel.call(prompt);

ChatResponseMetadata metadata = response.getMetadata();

String id = metadata.getId();
String model = metadata.getModel();
RateLimit rateLimit = metadata.getRateLimit();
Usage usage = metadata.getUsage();
PromptMetadata promptMetadata = metadata.getPromptMetadata();
```

这些指标可用于监控与用量报表，也可作为应用限流或调整提示词长度的依据。

## RateLimit：限额与剩余额度

`RateLimit` 提供模型服务在响应中返回的限流信息：

```java
interface RateLimit {

	Long getRequestsLimit();

	Long getRequestsRemaining();

	Duration getRequestsReset();

	Long getTokensLimit();

	Long getTokensRemaining();

	Duration getTokensReset();

}
```

| 方法组                                          | 含义                                          |
| ----------------------------------------------- | --------------------------------------------- |
| `getRequestsLimit()` / `getRequestsRemaining()` | 当前周期的请求数上限与剩余可用请求数。        |
| `getRequestsReset()`                            | 距离请求数额度重置的时长，类型为 `Duration`。 |
| `getTokensLimit()` / `getTokensRemaining()`     | 当前周期的 Token 上限与剩余额度。             |
| `getTokensReset()`                              | 距离 Token 额度重置的时长。                   |

例如，读取剩余 Token 额度：

```java
RateLimit rateLimit = metadata.getRateLimit();

Long tokensRemaining = rateLimit.getTokensRemaining();

// 根据限流元数据执行相应处理
```

[OpenAI 等服务](https://platform.openai.com/docs/guides/rate-limits/rate-limits-in-headers)会在 REST API 的 HTTP 响应头中返回限流信息；对应模型实现将这些响应头映射到 `RateLimit` 后，应用才能通过该接口读取。

**各模型实现的支持程度不同。**没有可用限流信息时，`getRateLimit()` 返回 `EmptyRateLimit`，其访问方法返回 **0，而非 `null`**。可通过 `rateLimit instanceof EmptyRateLimit` 区分“没有限流数据”和“真实剩余额度为零”。

## Usage：Token 用量

从 `ChatResponseMetadata.getUsage()` 获取用量，核心接口如下：

```java
interface Usage {

	Integer getPromptTokens();

	Integer getCompletionTokens();

	default Integer getTotalTokens() { ... }

	Object getNativeUsage();

}
```

| 方法                    | 含义                                                                            |
| ----------------------- | ------------------------------------------------------------------------------- |
| `getPromptTokens()`     | 处理输入提示词消耗的 Token 数。                                                 |
| `getCompletionTokens()` | 生成输出消耗的 Token 数。                                                       |
| `getTotalTokens()`      | 输入与输出 Token 的总数；Spring AI 提供默认计算方式，提供方也可能直接返回总数。 |
| `getNativeUsage()`      | 提供方原生用量对象，用于读取统一接口以外的明细。                                |

### 使用 ChatModel 读取用量

下面的 OpenAI 示例先读取标准指标，再检查原生对象的类型，以读取音频、缓存、推理与预测 Token 等明细：

```java
@SpringBootConfiguration
public class Configuration {

	@Bean
	public OpenAiChatModel openAiChatModel() {
		return OpenAiChatModel.builder()
			.options(OpenAiChatOptions.builder()
				.apiKey(System.getenv("OPENAI_API_KEY"))
				.build())
			.build();
	}

}

@Service
public class ChatService {

	private final OpenAiChatModel chatModel;

	public ChatService(OpenAiChatModel chatModel) {
		this.chatModel = chatModel;
	}

	public void demonstrateUsage() {
		// 创建提示词
		Prompt prompt = new Prompt("What is the weather like today?");

		// 获取聊天响应
		ChatResponse response = this.chatModel.call(prompt);

		// 读取用量信息
		Usage usage = response.getMetadata().getUsage();

		// 读取标准用量指标
		System.out.println("Prompt Tokens: " + usage.getPromptTokens());
		System.out.println("Completion Tokens: " + usage.getCompletionTokens());
		System.out.println("Total Tokens: " + usage.getTotalTokens());

		// 读取 OpenAI 原生用量，查看更细的 Token 分类
		if (usage.getNativeUsage() instanceof com.openai.models.completions.CompletionUsage nativeUsage) {

			// 输入 Token 明细
			nativeUsage.promptTokensDetails().ifPresent(details -> {
				System.out.println("Prompt Tokens Details:");
				details.audioTokens().ifPresent(tokens -> System.out.println("- Audio Tokens: " + tokens));
				details.cachedTokens().ifPresent(tokens -> System.out.println("- Cached Tokens: " + tokens));
			});

			// 输出 Token 明细
			nativeUsage.completionTokensDetails().ifPresent(details -> {
				System.out.println("Completion Tokens Details:");
				details.reasoningTokens().ifPresent(tokens -> System.out.println("- Reasoning Tokens: " + tokens));
				details.acceptedPredictionTokens().ifPresent(tokens -> System.out.println("- Accepted Prediction Tokens: " + tokens));
				details.audioTokens().ifPresent(tokens -> System.out.println("- Audio Tokens: " + tokens));
				details.rejectedPredictionTokens().ifPresent(tokens -> System.out.println("- Rejected Prediction Tokens: " + tokens));
			});
		}
	}
}
```

### 使用 ChatClient 读取用量

通过 `.call().chatResponse()` 获取完整响应，再访问用量：

```java
ChatResponse response = chatClient.prompt("What is the weather like today?")
		.call()
		.chatResponse();

Usage usage = response.getMetadata().getUsage();
```

如果仅调用 `.content()`，得到的是回答字符串；需要元数据时，按上例获取 `ChatResponse`。调用方式见 [ChatClient API](/frameworks/spring-ai/core/chat-client/)。

## 提示词缓存用量

对于支持提示词缓存的提供方，`Usage` 提供统一方法，无需先转换为提供方专用类型：

```java
Usage usage = response.getMetadata().getUsage();

// 通过统一接口读取缓存指标
Long cacheReadTokens = usage.getCacheReadInputTokens();
Long cacheWriteTokens = usage.getCacheWriteInputTokens();

if (cacheReadTokens != null && cacheReadTokens > 0) {
	System.out.println("Cache hit: " + cacheReadTokens + " tokens read from cache");
}
if (cacheWriteTokens != null && cacheWriteTokens > 0) {
	System.out.println("Cache write: " + cacheWriteTokens + " tokens written to cache");
}
```

- `getCacheReadInputTokens()`：从缓存读取的输入 Token 数。
- `getCacheWriteInputTokens()`：写入缓存的输入 Token 数。

不支持提示词缓存的提供方返回 `null`。表中的读写指标支持情况如下：

| 提供方        | 缓存读取 Token                    | 缓存写入 Token                     |
| ------------- | --------------------------------- | ---------------------------------- |
| Anthropic     | 支持                              | 支持（`cacheCreationInputTokens`） |
| AWS Bedrock   | 支持                              | 支持                               |
| OpenAI        | 支持（`cachedTokens`）            | 不支持                             |
| Google Gemini | 支持（`cachedContentTokenCount`） | 不支持                             |
| DeepSeek      | 不支持                            | 不支持                             |
| Mistral       | 不支持                            | 不支持                             |
| Ollama        | 不支持                            | 不支持                             |
| Qxotic jinfer | 支持                              | 不支持                             |

需要提供方特有的缓存明细，例如 Gemini 按模态划分的缓存统计，可通过 `getNativeUsage()` 获取原生对象。

## 多步流程的累计用量

工具调用循环等多步流程中，返回响应的 `getUsage()` 统计本次交互中**所有模型调用的累计用量**，不只是最后一次调用。

例如，模型发起一次工具调用，应用执行工具并将结果交回模型，通常至少会调用模型两次；最终的 `Usage` 会累计这些调用：

```java
ChatResponse response = chatClient.prompt("What is the weather in Paris?")
		.tools(new WeatherTools())
		.call()
		.chatResponse();

// 工具调用循环中所有模型调用的累计用量
Usage usage = response.getMetadata().getUsage();
int totalTokens = usage.getTotalTokens();
```

累计计算由 `org.springframework.ai.support.UsageCalculator` 完成，包括标准 Token 计数，以及 `getCacheReadInputTokens()`、`getCacheWriteInputTokens()` 两项统一缓存指标。

**提供方原生用量对象无法跨响应合并。**累计多个模型调用后，`getNativeUsage()` 返回 `null`；仅单次模型调用的响应保留原生对象。需要原生用量明细时，应从单次 `ChatModel` 调用的响应中读取。
