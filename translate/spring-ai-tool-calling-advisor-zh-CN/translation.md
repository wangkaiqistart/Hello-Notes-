---
title: Spring AI：工具调用 Advisor
description: 理解 ToolCallingAdvisor 的构建选项、处理链顺序、钩子扩展、流式观察和单工具 Advisor 约束。
sidebar:
  label: 工具调用 Advisor
  order: 2
---

`ToolCallingAdvisor` 是 Spring AI 2.0 中负责工具执行生命周期的递归 Advisor。`DefaultChatClient` 会自动注册它，由它驱动请求与响应循环，直到模型返回不含工具调用的响应。

本篇介绍构建器 API、配置项、钩子方法与扩展方式。循环原理见[工具调用循环](/frameworks/spring-ai/tools/tool-calling/#the-tool-calling-loop)，通用递归机制见[递归 Advisors](/frameworks/spring-ai/core/advisors/)。

<a id="overview"></a>

## 概览

`ToolCallingAdvisor` 实现 `CallAdvisor`、`StreamAdvisor` 和 `ToolAdvisor` 标记接口。`DefaultChatClient` 通过这个标记确保处理链中至多有一个工具 Advisor，详见[单个 ToolAdvisor 约束](/frameworks/spring-ai/tools/tool-calling-advisor/#single-tooladvisor-invariant)。

`ToolCallingAdvisor.DEFAULT_ORDER` 默认是 `Ordered.HIGHEST_PRECEDENCE + 300`。它大于 `MessageChatMemoryAdvisor` 的默认值 `HIGHEST_PRECEDENCE + 200`，因此默认的记忆 Advisor 位于工具循环外。具体行为见[记忆与工具循环](/frameworks/spring-ai/tools/tool-calling/#memory-and-the-tool-loop)。

<a id="builder"></a>

## 构建器

通过 `ToolCallingAdvisor.builder()` 创建实例：

```java
var toolCallingAdvisor = ToolCallingAdvisor.builder()
    .toolCallingManager(toolCallingManager)
    .advisorOrder(BaseAdvisor.HIGHEST_PRECEDENCE + 300)
    .build();

var chatClient = ChatClient.builder(chatModel)
    .defaultAdvisors(toolCallingAdvisor)
    .build();
```

多数应用不需要手动构建：`DefaultChatClient` 会自动注册默认实例。只有需要修改默认设置，或使用自定义子类替换时，才需要自行创建。

<a id="builder-options"></a>

### 构建器选项

| 选项                                                               | 作用                                                                                                                                                         | 默认值                                                               |
| ------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------- |
| `toolCallingManager(ToolCallingManager)`                           | 指定执行工具调用的 `ToolCallingManager`。                                                                                                                    | 自动创建的实例                                                       |
| `toolExecutionEligibilityChecker(ToolExecutionEligibilityChecker)` | 判断模型响应是否需要触发下一次工具调用迭代。默认检查 `chatResponse.hasToolCalls()`；可加入提供方特有的结束原因判断。                                         | `chatResponse → chatResponse != null && chatResponse.hasToolCalls()` |
| `advisorOrder(int)`                                                | 设置在处理链中的顺序，范围为 `BaseAdvisor.HIGHEST_PRECEDENCE` 至 `BaseAdvisor.LOWEST_PRECEDENCE`；它决定其他 Advisor 在循环内还是循环外执行。                | `HIGHEST_PRECEDENCE + 300`                                           |
| `conversationHistoryEnabled(boolean)`                              | 是否在循环内部维护历史。为 `true` 时，每次模型调用都带上之前的工具调用与结果；为 `false` 时，只转交最新消息，适合循环内已有 `MemoryAdvisor` 管理历史的情况。 | `true`                                                               |
| `disableInternalConversationHistory()`                             | `conversationHistoryEnabled(false)` 的快捷方法。                                                                                                             | —                                                                    |

<a id="checker"></a>

### ToolExecutionEligibilityChecker

`ToolExecutionEligibilityChecker` 是函数式接口：

```java
@FunctionalInterface
public interface ToolExecutionEligibilityChecker {
    boolean isToolCallResponse(@Nullable ChatResponse chatResponse);
}
```

默认只要响应含有工具调用，就进入下一次迭代。需要按提供方的规则判断时，可以自定义：

```java
ToolExecutionEligibilityChecker strictChecker = response ->
    response != null
        && response.hasToolCalls()
        && response.getResult() != null
        && "tool_calls".equals(response.getResult().getMetadata().getFinishReason());

var advisor = ToolCallingAdvisor.builder()
    .toolExecutionEligibilityChecker(strictChecker)
    .build();
```

<a id="conversation-history"></a>

### 内部历史的行为

默认情况下，`ToolCallingAdvisor` 在循环内维护完整历史，包括用户消息、模型响应、工具调用请求和工具结果。后续每次迭代都会把完整历史发送给模型。

当记忆 Advisor 位于循环外时，这样的分工正合适：外层记忆只看到最终的用户与助手交互，循环内的迭代历史由 `ToolCallingAdvisor` 自行管理。

以下情况应调用 `disableInternalConversationHistory()`：

- 把 `MemoryAdvisor` 放入循环内，由它维护每次迭代的历史。
- 自行驱动循环，只需要向后转交最新消息。

```java
var toolCallingAdvisor = ToolCallingAdvisor.builder()
    .disableInternalConversationHistory()  // 循环内的记忆 Advisor 负责维护历史
    .advisorOrder(BaseAdvisor.HIGHEST_PRECEDENCE + 300)
    .build();

var chatMemoryAdvisor = MessageChatMemoryAdvisor.builder(chatMemory)
    .order(BaseAdvisor.HIGHEST_PRECEDENCE + 400)  // 位于循环内
    .build();

var chatClient = ChatClient.builder(chatModel)
    .defaultAdvisors(chatMemoryAdvisor, toolCallingAdvisor)
    .build();
```

使用自动注册的 `ToolCallingAdvisor` 时，`DefaultChatClient` 会检测循环内的 `MemoryAdvisor`，并自动关闭内部历史。只有手动构建 `ToolCallingAdvisor` 时，才需要显式调用这个方法。详见[循环内的记忆](/frameworks/spring-ai/tools/tool-calling/#inside-the-loop)。

这里展示的是构建配置；实际请求使用记忆 Advisor 时，仍须显式传入 `ChatMemory.CONVERSATION_ID`，见[对话记忆](/frameworks/spring-ai/core/chat-memory/)。

<a id="hooks"></a>

## 钩子方法

`ToolCallingAdvisor` 在循环的固定阶段提供 `protected` 钩子。子类可以覆盖它们定制行为，无需重新实现整个循环。

阻塞调用与响应式流式调用各有一组对应方法。需要兼容两种模式的子类，应覆盖相关的成对钩子。

<a id="call-hooks"></a>

### 阻塞调用钩子

```java
protected ChatClientRequest doInitializeLoop(
        ChatClientRequest chatClientRequest, CallAdvisorChain callAdvisorChain);

protected ChatClientRequest doBeforeCall(
        ChatClientRequest chatClientRequest, CallAdvisorChain callAdvisorChain);

protected ChatClientResponse doAfterCall(
        ChatClientResponse chatClientResponse, CallAdvisorChain callAdvisorChain);

protected ChatClientResponse doFinalizeLoop(
        ChatClientResponse chatClientResponse, CallAdvisorChain callAdvisorChain);

protected List<Message> doGetNextInstructionsForToolCall(
        ChatClientRequest chatClientRequest,
        ChatClientResponse chatClientResponse,
        ToolExecutionResult toolExecutionResult);
```

| 钩子                               | 执行时机与用途                                                                                                                                                                                                                     |
| ---------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `doInitializeLoop`                 | 第一次迭代前执行一次；初始化会话索引、缓存或增强提示词。                                                                                                                                                                           |
| `doBeforeCall`                     | 每次迭代前执行；增删工具、修改选项或补充本次上下文，返回的请求会发送给模型。                                                                                                                                                       |
| `doAfterCall`                      | 每次模型响应后执行；记录本次观测数据，或在判断是否继续前转换响应。                                                                                                                                                                 |
| `doFinalizeLoop`                   | 循环结束后执行一次；汇总指标、清理会话状态或处理最终结果。                                                                                                                                                                         |
| `doGetNextInstructionsForToolCall` | 决定下一次迭代的消息。启用内部历史时返回完整历史，关闭时只返回系统消息和最新工具结果。它只影响向后续链路转交的消息；[工具调用次数限制](/frameworks/spring-ai/tools/tool-calling/#tool-call-limits)始终根据当前轮次的完整历史计算。 |

<a id="stream-hooks"></a>

### 流式调用钩子

```java
protected ChatClientRequest doInitializeLoopStream(
        ChatClientRequest chatClientRequest, StreamAdvisorChain streamAdvisorChain);

protected ChatClientRequest doBeforeStream(
        ChatClientRequest chatClientRequest, StreamAdvisorChain streamAdvisorChain);

protected ChatClientResponse doAfterStream(
        ChatClientResponse chatClientResponse, StreamAdvisorChain streamAdvisorChain);

protected Flux<ChatClientResponse> doFinalizeLoopStream(
        Flux<ChatClientResponse> chatClientResponseFlux, StreamAdvisorChain streamAdvisorChain);

protected List<Message> doGetNextInstructionsForToolCallStream(
        ChatClientRequest chatClientRequest,
        ChatClientResponse chatClientResponse,
        ToolExecutionResult toolExecutionResult);
```

流式方法与阻塞方法语义对应。`doAfterStream` 处理本次迭代各响应块聚合后的结果，`doFinalizeLoopStream` 则可以转换整个输出 `Flux`。

<a id="subclass-example"></a>

### 子类示例

`ToolSearchToolCallingAdvisor` 是现成的扩展示例：它覆盖 `doInitializeLoop` / `doInitializeLoopStream`，在会话开始时建立工具索引并增强系统消息；覆盖 `doBeforeCall` / `doBeforeStream`，每次只注入已经发现的工具。其余循环逻辑沿用基类。

下面展示一个记录工具调用意图的自定义子类：

```java
public class MyAuditingToolCallingAdvisor extends ToolCallingAdvisor {

    private final AuditService audit;

    private MyAuditingToolCallingAdvisor(
            ToolCallingManager manager,
            ToolExecutionEligibilityChecker checker,
            int order,
            boolean historyEnabled,
            AuditService audit) {
        super(manager, checker, order, historyEnabled);
        this.audit = java.util.Objects.requireNonNull(audit);
    }

    @Override
    protected ChatClientResponse doAfterCall(
            ChatClientResponse response, CallAdvisorChain chain) {
        if (response.chatResponse() == null || response.chatResponse().getResult() == null) {
            return response;
        }
        var toolCalls = response.chatResponse().getResult().getOutput().getToolCalls();
        for (var call : toolCalls) {
            audit.recordIntent(call.name(), call.arguments());
        }
        return response;
    }

    public static Builder<?> builder() {
        return new Builder<>();
    }

    public static class Builder<T extends Builder<T>> extends ToolCallingAdvisor.Builder<T> {

        private AuditService audit;

        public T audit(AuditService audit) {
            this.audit = audit;
            return self();
        }

        @Override
        protected Builder<?> newCopy() {
            return new Builder<>();
        }

        @Override
        public Builder<?> copy() {
            Builder<?> copy = (Builder<?>) super.copy();
            copy.audit = this.audit;
            return copy;
        }

        @Override
        public MyAuditingToolCallingAdvisor build() {
            // 通过 protected getter 读取 ToolCallingAdvisor.Builder 的继承字段。
            return new MyAuditingToolCallingAdvisor(
                getToolCallingManager(),
                getToolExecutionEligibilityChecker(),
                getAdvisorOrder(),
                isConversationHistoryEnabled(),
                audit);
        }
    }
}
```

`AuditService` 由应用提供；示例仅记录模型提出的调用意图，不代表工具已成功执行。构造器和 Builder 的复制方法需一起保留。

自引用泛型 `Builder<T extends Builder<T>>` 使子类构建器能连续调用继承的设置方法，同时保留子类类型。示例通过 `newCopy()` 和 `copy()` 保留子类类型及自定义审计字段，以支持 `DefaultChatClient` 对单次请求的调整。

<a id="single-tooladvisor-invariant"></a>

## 单个 ToolAdvisor 约束

`ToolAdvisor` 是标记接口。`DefaultChatClient` 据此确保一条处理链中至多有一个工具 Advisor，避免叠加两个工具循环后重复执行工具。

- 自动注册的 `ToolCallingAdvisor` 占用这个位置。
- 显式注册自定义 `ToolAdvisor`（例如自定义子类）后，`DefaultChatClient` 跳过默认注册，改用该实例。
- 同时注册两个自定义 `ToolAdvisor` 时，构建处理链会立即失败，并给出明确错误。

关闭自动注册且未显式配置工具 Advisor 时，处理链可以没有 `ToolAdvisor`，由应用自行执行工具。

在 Spring Boot 应用中替换默认实现，可通过自动配置注册子类，详见[自定义 ToolAdvisor 的自动配置集成](/frameworks/spring-ai/tools/tool-calling/#custom-tool-advisor-autoconfig)。

<a id="user-controlled-streaming"></a>

## 手动控制流式工具执行

[手动控制工具执行](/frameworks/spring-ai/tools/tool-calling/#user-controlled-tool-execution)介绍了阻塞模式，本节对应流式模式。

手动驱动 `.stream()` 循环时，每次迭代都会产生一个响应块 `Flux`。使用 `ChatClientMessageAggregator` 聚合结果，以判断是否包含工具调用；同时仍可把原始响应块转发给下游，例如 SSE 接口：

```java
ChatClient chatClient = ...
ToolCallingManager toolCallingManager = ToolCallingManager.builder().build();

ToolCallback[] tools = ToolCallbacks.from(new WeatherTools());
ChatOptions chatOptions = ToolCallingChatOptions.builder().toolCallbacks(tools).build();

String question = "What is the weather in Amsterdam and Paris?";
Prompt prompt = new Prompt(List.of(new UserMessage(question)), chatOptions);

AtomicReference<ChatClientResponse> ref = new AtomicReference<>();

new ChatClientMessageAggregator().aggregateChatClientResponse(
    chatClient.prompt()
        .messages(prompt.getInstructions())
        .options(chatOptions.mutate())
        .advisors(AdvisorParams.toolCallingAdvisorAutoRegister(false))
        .stream()
        .chatClientResponse()
        .doOnNext(chunk -> forwardToSse(chunk)),  // 同时向侧通道推送
    ref::set
).blockLast();

ChatClientResponse response = ref.get();

while (response.chatResponse() != null && response.chatResponse().hasToolCalls()) {
    ToolExecutionResult result = toolCallingManager.executeToolCalls(prompt, response.chatResponse());
    if (result.returnDirect()) {
        response = response.mutate()
            .chatResponse(ChatResponse.builder()
                .generations(ToolExecutionResult.buildGenerations(result))
                .build())
            .build();
        break;
    }
    prompt = new Prompt(result.conversationHistory(), chatOptions);

    AtomicReference<ChatClientResponse> nextRef = new AtomicReference<>();
    new ChatClientMessageAggregator().aggregateChatClientResponse(
        chatClient.prompt()
            .messages(result.conversationHistory())
            .options(chatOptions.mutate())
            .advisors(AdvisorParams.toolCallingAdvisorAutoRegister(false))
            .stream()
            .chatClientResponse()
            .doOnNext(chunk -> forwardToSse(chunk)),
        nextRef::set
    ).blockLast();

    response = nextRef.get();
}
```

这段示例使用 `blockLast()` 等待一次迭代完成，并非完全非阻塞的编排。`forwardToSse(...)` 由应用实现；直接返回工具的结果保存在最终的 `response` 中，可由应用读取并推送。

这种写法较长。多数情况下更适合[把自定义 Advisor 放进循环内](/frameworks/spring-ai/tools/tool-calling-advisor/#observing-the-tool-calling-loop)：保留框架管理的循环，只拦截响应块流。

<a id="observing-the-tool-calling-loop"></a>

## 观察工具调用循环

向界面推送中间进度、记录工具审计事件、采集每次迭代指标等场景，通常不需要关闭自动注册或自行驱动循环。把自定义 Advisor 的 `order` 设为大于 `ToolCallingAdvisor.DEFAULT_ORDER`，即可在循环内执行：

```java
public class ToolCallObservingAdvisor implements CallAdvisor, StreamAdvisor {

    private static final org.slf4j.Logger log =
        org.slf4j.LoggerFactory.getLogger(ToolCallObservingAdvisor.class);

    private final Consumer<ChatClientResponse> observer;

    public ToolCallObservingAdvisor(Consumer<ChatClientResponse> observer) {
        this.observer = java.util.Objects.requireNonNull(observer);
    }

    @Override
    public String getName() {
        return "ToolCallObservingAdvisor";
    }

    @Override
    public int getOrder() {
        return Ordered.HIGHEST_PRECEDENCE + 400;  // 位于 ToolCallingAdvisor（偏移量 300）的循环内
    }

    @Override
    public ChatClientResponse adviseCall(ChatClientRequest request, CallAdvisorChain chain) {
        // 每次迭代的请求包含之前迭代产生的 ToolResponseMessage
        request.prompt().getInstructions().forEach(msg -> log.debug("Message: {}", msg));
        ChatClientResponse response = chain.nextCall(request);
        observer.accept(response);
        return response;
    }

    @Override
    public Flux<ChatClientResponse> adviseStream(ChatClientRequest request, StreamAdvisorChain chain) {
        // 观察每个响应块，包括工具调用请求
        return chain.nextStream(request).doOnNext(observer);
    }
}
```

将观察 Advisor 与自动注册的 `ToolCallingAdvisor` 一起使用：

```java
var chatClient = ChatClient.builder(chatModel)
    .defaultAdvisors(new ToolCallObservingAdvisor(chunk -> forwardToSse(chunk)))
    .build();

String response = chatClient.prompt()
    .user("What is the weather in Amsterdam and Paris?")
    .tools(new WeatherTools())
    .call()
    .content();
```

`ToolCallObservingAdvisor` 会在每次迭代执行。主调用方仍只收到最终回答，因为 `ToolCallingAdvisor` 会从对外返回的流中过滤工具调用响应块。

<a id="return-direct"></a>

## 直接返回工具结果

工具的 `ToolMetadata.returnDirect` 为 `true` 时，`ToolCallingAdvisor` 会：

1. 正常执行工具。
2. 检查 `ToolExecutionResult` 的 `returnDirect` 标记。
3. 结束循环。
4. 直接向调用方返回 `ChatResponse`，其中生成结果的内容是工具输出。

工具结果不会再发送给模型，省去一次模型往返。适用于工具输出本身就是最终答案（例如某些 RAG 检索结果），或工具执行后应终止推理循环的场景。

同一次迭代包含多个工具调用时，只有**所有工具**都设置了 `returnDirect = true`，才会直接返回；否则结果仍发送给模型，循环继续。标记的声明方式见[直接返回](/frameworks/spring-ai/tools/tool-calling/#return-direct)。

<a id="opting-out"></a>

## 关闭自动注册

对自动配置的 `ChatClient` 全局关闭 `ToolCallingAdvisor` 自动注册：

```properties
spring.ai.chat.client.tool-calling.enabled=false
```

只对某次调用关闭：

```java
chatClient.prompt("What day is tomorrow?")
    .tools(new DateTimeTools())
    .advisors(AdvisorParams.toolCallingAdvisorAutoRegister(false))
    .call()
    .content();
```

关闭后，`.tools(...)` 提供的工具定义仍会发送给模型，但响应中的工具调用**不会自动执行**。应用进入[手动控制模式](/frameworks/spring-ai/tools/tool-calling/#user-controlled-tool-execution)。

<a id="see-also"></a>

## 相关阅读

- [工具调用循环](/frameworks/spring-ai/tools/tool-calling/#the-tool-calling-loop)：理解整体机制。
- [记忆与工具循环](/frameworks/spring-ai/tools/tool-calling/#memory-and-the-tool-loop)：区分循环内外的执行顺序。
- [扩展工具循环](/frameworks/spring-ai/tools/tool-calling/#extending-the-loop)：自定义子类的自动配置扩展点。
- [工具搜索](/frameworks/spring-ai/tools/tool-search-tool/)：通过 `ToolSearchToolCallingAdvisor` 渐进暴露工具。
- [递归 Advisors](/frameworks/spring-ai/core/advisors/)：理解底层递归模式。
- [Advisors](/frameworks/spring-ai/core/advisors/)：了解完整的处理链机制。

来源：[工具调用 Advisor](https://docs.spring.io/spring-ai/reference/api/tools/tool-calling-advisor.html)。文档版本：2.0.2；核验日期：2026-10-26。
