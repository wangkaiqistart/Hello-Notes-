Advisors API 用于拦截、修改和增强模型交互，把常见的生成式 AI 处理模式封装为可复用组件。例如，在调用前补充对话历史或检索资料，在调用后记录日志、检查或转换结果。

这些处理独立于具体模型，有助于跨模型复用。通过 [ChatClient](/frameworks/spring-ai/core/chat-client/) 配置现有 Advisor：

```java
ChatMemory chatMemory = ... // 初始化对话记忆存储
VectorStore vectorStore = ... // 初始化向量存储

var chatClient = ChatClient.builder(chatModel)
    .defaultAdvisors(
        MessageChatMemoryAdvisor.builder(chatMemory).build(), // 对话记忆 Advisor
        QuestionAnswerAdvisor.builder(vectorStore).build()    // RAG Advisor
    )
    .build();

var conversationId = "678";

String response = this.chatClient.prompt()
    // 运行时设置 Advisor 参数
    .advisors(advisor -> advisor.param(ChatMemory.CONVERSATION_ID, conversationId))
    .user(userText)
    .call()
	.content();
```

建议在构建客户端时通过 `defaultAdvisors()` 注册默认 Advisor，在单次调用中传入会话 ID 等运行时参数。示例中的 `...` 代表需要自行初始化的组件。

Advisor 也参与[可观测性](https://docs.spring.io/spring-ai/reference/observability/index.html)，可以查看执行指标和追踪。具体应用见[问答 Advisor](https://docs.spring.io/spring-ai/reference/api/retrieval-augmented-generation.html#_questionansweradvisor)与[对话记忆](https://docs.spring.io/spring-ai/reference/api/chat-memory.html)。

## 核心组件与执行流程

API 分为同步和流式两组：

| 场景   | Advisor         | 处理链               | 响应                       |
| ------ | --------------- | -------------------- | -------------------------- |
| 非流式 | `CallAdvisor`   | `CallAdvisorChain`   | `ChatClientResponse`       |
| 流式   | `StreamAdvisor` | `StreamAdvisorChain` | `Flux<ChatClientResponse>` |

`ChatClientRequest` 携带尚可增强的 `Prompt`，`ChatClientResponse` 携带模型响应；两者都包含上下文，用于在链中传递状态。

Advisor 的关键方法是 `adviseCall()` 与 `adviseStream()`，可用于检查或增强请求、继续调用下游、检查或修改响应，或抛出异常报告处理错误。`getOrder()` 决定顺序，`getName()` 提供标识名称。

下图保留各接口的继承与聚合关系：重点看同步、流式两条分支，以及 Advisor 与对应处理链的方法区别。

[![Advisors API 类型关系：Advisor 继承 Ordered，分为 CallAdvisor 与 StreamAdvisor，由相应 Chain 继续调用下游](/images/frameworks/spring-ai/advisors-api-classes-zh.svg)](/images/frameworks/spring-ai/advisors-api-classes-zh.svg)

类名和方法名保留 API 原名，图例已中文化；点击可查看大图。

框架按 `getOrder()` 创建有序链，并在末端加入负责模型调用的内部 Advisor。一次交互的流程如下：

1. 根据用户请求构建 `ChatClientRequest`，初始化 Advisor 上下文。
2. 各 Advisor 依次处理请求，可修改或增强内容。也可以不调用下游而短路，此时必须自行提供响应。
3. 框架的内部 Advisor 将请求交给 `ChatModel`。
4. 模型响应沿处理链返回，包装为带上下文的 `ChatClientResponse`。
5. 各 Advisor 可以检查或修改返回结果。
6. 客户端按所选终结方法获取模型响应或其他结果。

下图对应这六步：请求从左侧向下进入模型，响应从右侧向上返回。

[![Advisor 六步流程：构建请求、调用前处理、请求模型、模型响应、调用后处理、提取结果](/images/frameworks/spring-ai/advisors-flow-zh.svg)](/images/frameworks/spring-ai/advisors-flow-zh.svg)

黄色内部节点连接 Advisor 链与聊天模型；点击可查看大图。

### Advisor 顺序

**`order` 越小，请求处理越早，响应处理越晚。**处理链类似嵌套调用：最先进入的 Advisor 最后退出。

| 配置                              | 请求阶段       | 响应阶段       |
| --------------------------------- | -------------- | -------------- |
| 接近 `Ordered.HIGHEST_PRECEDENCE` | 靠前执行       | 靠后执行       |
| 接近 `Ordered.LOWEST_PRECEDENCE`  | 靠后执行       | 靠前执行       |
| 相同 `order`                      | 不保证相互顺序 | 不保证相互顺序 |

Spring `Ordered` 的含义如下：

```java
public interface Ordered {

    /**
     * 最高优先级常量。
     * @see java.lang.Integer#MIN_VALUE
     */
    int HIGHEST_PRECEDENCE = Integer.MIN_VALUE;

    /**
     * 最低优先级常量。
     * @see java.lang.Integer#MAX_VALUE
     */
    int LOWEST_PRECEDENCE = Integer.MAX_VALUE;

    /**
     * 获取当前对象的顺序值。
     * <p>值越大，优先级越低。
     * 最小值对应最高优先级，类似于
     * Servlet 的 {@code load-on-startup}。
     * <p>顺序值相同时，
     * 相应对象的排序位置不确定。
     * @return 顺序值
     * @see #HIGHEST_PRECEDENCE
     * @see #LOWEST_PRECEDENCE
     */
    int getOrder();
}
```

如果希望某项处理在请求和响应两侧都最先执行，应拆成两个 Advisor，分别设置顺序；需要共享状态时通过上下文传递。

## API 接口

主要接口位于 `org.springframework.ai.chat.client.advisor.api`。

`Advisor` 继承 `Ordered`，并要求提供名称：

```java
public interface Advisor extends Ordered {

	String getName();

}
```

同步接口负责单个完整响应：

```java
public interface CallAdvisor extends Advisor {

	ChatClientResponse adviseCall(
		ChatClientRequest chatClientRequest, CallAdvisorChain callAdvisorChain);

}
```

流式接口返回响应流：

```java
public interface StreamAdvisor extends Advisor {

	Flux<ChatClientResponse> adviseStream(
		ChatClientRequest chatClientRequest, StreamAdvisorChain streamAdvisorChain);

}
```

在实现中，通过对应 Chain 调用下一个 Advisor：

```java
public interface CallAdvisorChain extends AdvisorChain {

	/**
	 * 使用指定请求调用 {@link CallAdvisorChain} 中的下一个 {@link CallAdvisor}。
	 *
	 */
	ChatClientResponse nextCall(ChatClientRequest chatClientRequest);

	/**
	 * 返回链创建时包含的全部 {@link CallAdvisor} 实例。
	 *
	 */
	List<CallAdvisor> getCallAdvisors();

}
```

```java
public interface StreamAdvisorChain extends AdvisorChain {

	/**
	 * 使用指定请求调用 {@link StreamAdvisorChain} 中的下一个 {@link StreamAdvisor}。
	 *
	 */
	Flux<ChatClientResponse> nextStream(ChatClientRequest chatClientRequest);

	/**
	 * 返回链创建时包含的全部 {@link StreamAdvisor} 实例。
	 *
	 */
	List<StreamAdvisor> getStreamAdvisors();

}
```

`getCallAdvisors()`、`getStreamAdvisors()` 返回链创建时包含的相应 Advisor 列表。

## 实现自定义 Advisor

可以实现 `CallAdvisor`、`StreamAdvisor`，或同时实现两者。同步处理实现 `adviseCall()`，流式处理实现 `adviseStream()`；继续执行下游时分别调用 `nextCall()`、`nextStream()`。

### 日志 Advisor

以下示例在调用下游前记录请求，返回后记录响应，只观察数据，不修改内容，并同时支持两种调用方式：

```java
public class SimpleLoggerAdvisor implements CallAdvisor, StreamAdvisor {

	private static final Logger logger = LoggerFactory.getLogger(SimpleLoggerAdvisor.class);

	@Override
	public String getName() {
		return this.getClass().getSimpleName();
	}

	@Override
	public int getOrder() {
		return 0;
	}


	@Override
	public ChatClientResponse adviseCall(ChatClientRequest chatClientRequest, CallAdvisorChain callAdvisorChain) {
		logRequest(chatClientRequest);

		ChatClientResponse chatClientResponse = callAdvisorChain.nextCall(chatClientRequest);

		logResponse(chatClientResponse);

		return chatClientResponse;
	}

	@Override
	public Flux<ChatClientResponse> adviseStream(ChatClientRequest chatClientRequest,
			StreamAdvisorChain streamAdvisorChain) {
		logRequest(chatClientRequest);

		Flux<ChatClientResponse> chatClientResponses = streamAdvisorChain.nextStream(chatClientRequest);

		return new ChatClientMessageAggregator().aggregateChatClientResponse(chatClientResponses, this::logResponse);
	}

	private void logRequest(ChatClientRequest request) {
		logger.debug("request: {}", request);
	}

	private void logResponse(ChatClientResponse chatClientResponse) {
		logger.debug("response: {}", chatClientResponse);
	}

}
```

- `getName()` 返回名称；示例使用类名。
- `getOrder()` 返回顺序值；越小越早处理请求。
- `ChatClientMessageAggregator` 将流中的响应汇总给日志回调，便于观察完整回答。该回调只读，不能用它修改响应；调用方仍接收原有响应流。

### 重读策略：Re2

论文 [Re-Reading Improves Reasoning in Large Language Models](https://arxiv.org/pdf/2309.06275) 提出重读策略：在输入中再次呈现同一问题。

```text
{Input_Query}
Read the question again: {Input_Query}
```

可以通过 `BaseAdvisor` 的 `before()` 增强用户消息，再由 `after()` 原样返回结果：

```java
public class ReReadingAdvisor implements BaseAdvisor {

	private static final String DEFAULT_RE2_ADVISE_TEMPLATE = """
			{re2_input_query}
			Read the question again: {re2_input_query}
			""";

	private final String re2AdviseTemplate;

	private int order = 0;

	public ReReadingAdvisor() {
		this(DEFAULT_RE2_ADVISE_TEMPLATE);
	}

	public ReReadingAdvisor(String re2AdviseTemplate) {
		this.re2AdviseTemplate = re2AdviseTemplate;
	}

	@Override
	public ChatClientRequest before(ChatClientRequest chatClientRequest, AdvisorChain advisorChain) {
		String augmentedUserText = PromptTemplate.builder()
			.template(this.re2AdviseTemplate)
			.variables(Map.of("re2_input_query", chatClientRequest.prompt().getUserMessage().getText()))
			.build()
			.render();

		return chatClientRequest.mutate()
			.prompt(chatClientRequest.prompt().augmentUserMessage(augmentedUserText))
			.build();
	}

	@Override
	public ChatClientResponse after(ChatClientResponse chatClientResponse, AdvisorChain advisorChain) {
		return chatClientResponse;
	}

	@Override
	public int getOrder() {
		return this.order;
	}

	public ReReadingAdvisor withOrder(int order) {
		this.order = order;
		return this;
	}

}
```

`before()` 读取原问题、渲染模板并构建新请求；`withOrder()` 调整执行顺序。该策略的实际收益应结合所用模型与任务评估。

### 内置 Advisor

| 类别       | Advisor                        | 用途                                                                             |
| ---------- | ------------------------------ | -------------------------------------------------------------------------------- |
| 对话记忆   | `MessageChatMemoryAdvisor`     | 读取历史记录并作为消息集合加入提示词，保留对话结构；需确认模型支持相应消息形式。 |
| 对话记忆   | `VectorStoreChatMemoryAdvisor` | 从向量存储检索相关历史，加入提示词的系统文本。                                   |
| 问答与 RAG | `QuestionAnswerAdvisor`        | 通过向量存储实现基础 Naive RAG。                                                 |
| 问答与 RAG | `RetrievalAugmentationAdvisor` | 使用 `org.springframework.ai.rag` 组件构建模块化 RAG 流程。                      |
| 重读策略   | `ReReadingAdvisor`             | 在输入阶段应用 Re2 策略。                                                        |
| 工具调用   | `ToolCallingAdvisor`           | 在链中执行工具循环：运行工具并回传结果，直到无需继续调用工具。                   |
| 内容防护   | `SafeGuardAdvisor`             | 简单的内容防护，用于限制有害或不当内容。                                         |

除非明确禁用，`ChatClient` 会自动注册 `ToolCallingAdvisor`，即使没有静态工具配置，也能处理其他 Advisor 在运行时加入的工具。`ToolAdvisor` 标记接口用于识别已有工具处理能力，避免再自动添加第二个工具 Advisor。

完整循环见[递归 Advisors](/frameworks/spring-ai/core/advisors-recursive/#toolcallingadvisor工具调用循环)，自动注册与禁用方式见 [ChatClient：工具调用](/frameworks/spring-ai/core/chat-client/#工具调用)。

### 流式与非流式

非流式 Advisor 处理完整请求和响应；流式 Advisor 仍接收一个请求，但响应通过 `Flux` 逐步传递。

下图对比两条路径：左侧返回单个 `ChatClientResponse`，右侧返回 `Flux<ChatClientResponse>`。

[![非流式和流式 Advisor 对比：同步响应为单个对象，流式响应为 Flux，二者使用各自的处理链](/images/frameworks/spring-ai/advisors-non-stream-vs-stream-zh.svg)](/images/frameworks/spring-ai/advisors-non-stream-vs-stream-zh.svg)

两条路径都按请求进入、响应返回的方向执行；点击可查看大图。

以下代码展示流式处理的结构，在下游调用前后插入逻辑：

```java
@Override
public Flux<ChatClientResponse> adviseStream(ChatClientRequest chatClientRequest, StreamAdvisorChain chain) {

    return  Mono.just(chatClientRequest)
            .publishOn(Schedulers.boundedElastic())
            .map(request -> {
                // 可在阻塞或非阻塞线程调用的场景中使用。
                // 调用下游前的处理
            })
            .flatMapMany(request -> chain.nextStream(request))
            .map(response -> {
                // 下游返回后的处理
            });
}
```

### 实践建议

- 每个 Advisor 聚焦单一职责，便于组合与复用。
- 需要跨 Advisor 传递状态时，使用上下文。
- 按应用需要支持同步与流式路径，避免只实现一侧却用于另一侧。
- 明确每个 Advisor 的顺序，检查前一个步骤的输出是否满足后续步骤要求。

## 历史 API 迁移

以下是来源保留的历史变更，阅读旧文章或迁移旧代码时再对照；当前实现以 2.0.2 API 为准。

### Advisor 接口演变

| 版本   | 变化                                                                                                    |
| ------ | ------------------------------------------------------------------------------------------------------- |
| 1.0 M2 | 使用 `RequestAdvisor` 与 `ResponseAdvisor`，分别在 `ChatModel.call()` / `stream()` 前后执行。           |
| 1.0 M3 | 改为 `CallAroundAdvisor` 与 `StreamAroundAdvisor`；移除原 `ResponseAdvisor` 中的 `StreamResponseMode`。 |
| 1.0.0  | `CallAroundAdvisor` → `CallAdvisor`；`StreamAroundAdvisor` → `StreamAdvisor`；对应 Chain 同步改名。     |
| 1.0.0  | `AdvisedRequest` → `ChatClientRequest`；`AdvisedResponse` → `ChatClientResponse`。                      |

### 上下文 Map 的历史变化

- **1.0 M2**：上下文作为独立方法参数，是沿链传递的可变 Map。
- **1.0 M3**：上下文并入当时的 `AdvisedRequest` / `AdvisedResponse` record，改为不可变 Map；历史 API 用 `updateContext()` 创建包含变更的新不可修改 Map。

上面的 `updateContext()` 是旧版迁移说明，不能直接当作当前 `ChatClientRequest` 的方法使用。
