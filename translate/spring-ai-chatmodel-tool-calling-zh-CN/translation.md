---
title: Spring AI：ChatModel 工具调用
description: 直接使用 ChatModel 提供工具定义、手动驱动阻塞与流式循环，并理解默认工具覆盖和上下文合并规则。
sidebar:
  label: ChatModel 工具调用
  order: 4
---

`ChatModel` 是面向聊天模型提供方的底层请求与响应接口。它接收工具定义、将定义发送给模型，并返回模型响应。**响应中的工具调用请求不会自动执行，调用方需要自行处理。**

大多数应用应使用 [ChatClient](/frameworks/spring-ai/tools/tool-calling/)：它通过 [ToolCallingAdvisor](/frameworks/spring-ai/tools/tool-calling-advisor/) 驱动工具调用循环，可以组合记忆、可观测性等 Advisor，并提供自动配置扩展点。本文适合明确需要底层控制的场景。

<a id="when-to-use"></a>

## 什么时候直接使用 ChatModel

- 不需要 Advisor 处理链，包括记忆 Advisor、可观测性 Advisor 和 `ToolCallingAdvisor`。
- 要接入自行管理循环的编排器，例如领域工作流引擎或非 Spring 的 Agent 框架。
- 要基于 Spring AI 构建基础设施，例如自定义 `ChatClient` 实现，或封装自己的高层 API。

普通聊天、RAG、Agent 工作流和使用大量工具的助手，优先选择 `ChatClient`。

<a id="no-internal-tool-execution"></a>

## ChatModel 不执行工具

`ChatModel.call(prompt)` 和 `ChatModel.stream(prompt)` 返回模型原始响应，其中可能包含工具调用请求。工具执行和携带结果再次调用模型，都由调用方负责。

Spring AI 1.x 中，各 `ChatModel` 有自己的内部工具循环；2.0 已移除这一机制。迁移说明见[工具调用从 1.x 升级到 2.0](https://docs.spring.io/spring-ai/reference/upgrade-notes.html#tool-calling-1x-to-2x)。

<a id="passing-tools"></a>

## 向 ChatModel 提供工具

使用 `ToolCallingChatOptions.toolCallbacks(...)` 传入 `List<ToolCallback>` 或 `ToolCallback[]`。对于包含 `@Tool` 方法的对象，先通过 `ToolCallbacks.from(...)` 转换为回调。

<a id="per-request-tools"></a>

### 请求级工具

```java
ChatModel chatModel = ...
ToolCallback[] tools = ToolCallbacks.from(new DateTimeTools());

ChatOptions chatOptions = ToolCallingChatOptions.builder()
    .toolCallbacks(tools)
    .build();

Prompt prompt = new Prompt("What day is tomorrow?", chatOptions);
ChatResponse response = chatModel.call(prompt);
```

这段代码只把工具定义发送给模型。如果响应要求调用工具，应用还需按后文的手动循环执行工具。

<a id="default-tools"></a>

### 模型默认工具

部分 `ChatModel` 构建器允许设置默认选项。默认工具会应用于每次请求，除非被请求级选项覆盖：

```java
ToolCallback[] dateTimeTools = ToolCallbacks.from(new DateTimeTools());

ChatModel chatModel = OllamaChatModel.builder()
    .ollamaApi(OllamaApi.builder().build())
    .options(OllamaChatOptions.builder()
        .toolCallbacks(dateTimeTools)
        .build())
    .build();
```

Ollama 示例使用提供方专用的 `OllamaChatOptions`；运行前还需连接实际服务并选择支持工具调用的型号。

默认工具会随该模型实例的每次请求发送。只将应始终可用的工具设为默认；高风险或有破坏性的工具通常应按请求注册。

<a id="override-semantics"></a>

### 覆盖规则

模型默认选项和请求级选项都设置了工具时，**请求级工具列表整体替换默认列表**：

```java
ChatModel chatModel = OllamaChatModel.builder()
    .ollamaApi(OllamaApi.builder().build())
    .options(OllamaChatOptions.builder()
        .toolCallbacks(defaultTools)  // 5 个默认工具
        .build())
    .build();

ChatOptions runtimeOptions = ToolCallingChatOptions.builder()
    .toolCallbacks(otherTool)          // 1 个工具
    .build();

ChatResponse response = chatModel.call(new Prompt("...", runtimeOptions));
// 模型只看到 otherTool，默认工具列表已被整体替换。
```

如果单次请求需要“默认工具加一个额外工具”，需显式合并：

```java
List<ToolCallback> combined = new ArrayList<>(Arrays.asList(defaultTools));
combined.add(otherTool);

ChatOptions runtimeOptions = ToolCallingChatOptions.builder()
    .toolCallbacks(combined)
    .build();
```

这与 `ChatClient` 不同：`ChatClient.tools(...)` 会追加到 `.defaultTools(...)`，详见[向 ChatClient 提供工具](/frameworks/spring-ai/tools/tool-calling/#passing-tools)。

<a id="driving-the-loop-manually"></a>

## 手动驱动工具循环

模型返回工具调用请求后，应用执行工具，把结果加入消息历史，再次调用模型。这正是 `ToolCallingAdvisor` 为 `ChatClient` 自动完成的流程；直接使用 `ChatModel` 时由应用编写。

<a id="blocking-loop"></a>

### 阻塞调用

```java
ChatModel chatModel = ...
ToolCallingManager toolCallingManager = ToolCallingManager.builder().build();

ToolCallback[] tools = ToolCallbacks.from(new WeatherTools());
ChatOptions chatOptions = ToolCallingChatOptions.builder()
    .toolCallbacks(tools)
    .build();

Prompt prompt = new Prompt("What is the weather in Amsterdam and Paris?", chatOptions);
ChatResponse response = chatModel.call(prompt);

while (response.hasToolCalls()) {
    ToolExecutionResult result = toolCallingManager.executeToolCalls(prompt, response);

    if (result.returnDirect()) {
        // 全部被调用工具均直接返回时，不再调用模型。
        return result.conversationHistory();
    }

    prompt = new Prompt(result.conversationHistory(), chatOptions);
    response = chatModel.call(prompt);
}

String finalAnswer = response.getResult().getOutput().getText();
```

关键对象与方法：

- `ToolCallingManager`：执行工具调用。Spring Boot 自动配置默认实现 `DefaultToolCallingManager`；未使用自动配置时，可调用 `ToolCallingManager.builder().build()` 创建。
- `response.hasToolCalls()`：判断模型是否请求了至少一个工具调用。
- `executeToolCalls(prompt, response)`：找到所请求的工具、执行并返回 `ToolExecutionResult`。
- `result.returnDirect()`：本轮所调用的工具全部设置了 `returnDirect = true` 时才为 `true`。
- `result.conversationHistory()`：包含原有消息、助手的工具调用请求，以及工具响应。下一次模型请求使用这份消息列表。

<a id="streaming-loop"></a>

### 流式调用

流式响应需要先聚合每次迭代的分片，再判断是否有完整的工具调用请求。聚合的同时，可以把原始分片转发给 SSE 等下游订阅者：

```java
ChatModel chatModel = ...
ToolCallingManager toolCallingManager = ToolCallingManager.builder().build();

ToolCallback[] tools = ToolCallbacks.from(new WeatherTools());
ChatOptions chatOptions = ToolCallingChatOptions.builder()
    .toolCallbacks(tools)
    .build();

Prompt prompt = new Prompt("What is the weather in Amsterdam and Paris?", chatOptions);

while (true) {
    AtomicReference<ChatResponse> aggregated = new AtomicReference<>();

    new MessageAggregator().aggregate(
        chatModel.stream(prompt).doOnNext(chunk -> forwardToSse(chunk)),
        aggregated::set
    ).blockLast();

    ChatResponse response = aggregated.get();
    if (response == null || !response.hasToolCalls()) {
        break;
    }

    ToolExecutionResult result = toolCallingManager.executeToolCalls(prompt, response);
    if (result.returnDirect()) {
        forwardToSse(ChatResponse.builder()
            .generations(ToolExecutionResult.buildGenerations(result))
            .build());
        break;
    }
    prompt = new Prompt(result.conversationHistory(), chatOptions);
}
```

直接返回时，示例将工具结果转换成 `ChatResponse` 后交给 `forwardToSse(...)`，避免只退出循环却漏掉结果。

示例通过 `MessageAggregator` 聚合 `ChatResponse`，使用 `blockLast()` 等待本次迭代完成。它演示的是逐次等待的手动循环；`forwardToSse(...)` 由应用实现。

如果希望保留完整的 Advisor 组合能力，见 [ChatClient 的用户控制流式调用](/frameworks/spring-ai/tools/tool-calling-advisor/#user-controlled-streaming)。

<a id="tool-context"></a>

## 工具上下文

工具上下文用于把非模型数据传给工具方法，使用方式与 `ChatClient` 一致，通过 `ToolCallingChatOptions` 设置：

```java
ChatOptions chatOptions = ToolCallingChatOptions.builder()
    .toolCallbacks(ToolCallbacks.from(new CustomerTools()))
    .toolContext(Map.of("tenantId", "acme"))
    .build();

Prompt prompt = new Prompt("Tell me about customer 42", chatOptions);
chatModel.call(prompt);
```

默认选项与请求级选项都设置了 `toolContext` 时，两份 Map 会合并，同名键以请求级值为准。注意，这与整体替换的 `toolCallbacks` 不同。

上下文不会作为工具输入参数发送给模型；工具方法如何读取它，见[工具上下文](/frameworks/spring-ai/tools/tool-calling/#tool-context)。这段代码仍只完成模型请求，实际执行工具时才会用到上下文。

<a id="return-direct"></a>

## 直接返回工具结果

`ToolCallingManager.executeToolCalls(...)` 会处理工具的 `returnDirect` 标志，手动循环需检查返回值：

```java
ToolExecutionResult result = toolCallingManager.executeToolCalls(prompt, response);

if (result.returnDirect()) {
    // 跳过下一次模型调用，把工具结果交给调用方。
    return result.conversationHistory();
}
```

模型在同一次迭代中请求多个工具时，只有 **所有被调用工具** 都设置 `returnDirect = true`，`result.returnDirect()` 才为 `true`。此时跳过下一次模型调用，由应用把工具结果返回给调用方。声明方式见[直接返回](/frameworks/spring-ai/tools/tool-calling/#return-direct)。

<a id="see-also"></a>

## 相关文档

- [工具调用](/frameworks/spring-ai/tools/tool-calling/)：推荐的 ChatClient 接入路径。
- [ToolCallingAdvisor](/frameworks/spring-ai/tools/tool-calling-advisor/)：ChatClient 的工具循环实现。
- [ChatClient 用户控制流式调用](/frameworks/spring-ai/tools/tool-calling-advisor/#user-controlled-streaming)：保留 Advisor 处理链的手动循环方式。
- [工具调用升级说明](https://docs.spring.io/spring-ai/reference/upgrade-notes.html#tool-calling-1x-to-2x)。

来源：[ChatModel 工具调用](https://docs.spring.io/spring-ai/reference/api/tools/chatmodel-tool-calling.html)。文档版本：2.0.2；核验日期：2026-10-26。
