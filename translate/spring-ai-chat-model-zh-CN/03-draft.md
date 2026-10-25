---
title: Spring AI：聊天模型
description: 精选 ChatModel 的同步与流式调用、Prompt 和 ChatOptions、响应结构，以及与 ChatClient 的职责区别。
sidebar:
  label: 聊天模型
  order: 2
---

`ChatModel` 是 Spring AI 与聊天模型交互的底层抽象，负责把提示词转换成提供方请求，并将返回结果转换为 `ChatResponse`。本文精选核心接口与调用规则，提供方配置和完整类定义通过文末链接查询。

## ChatModel 与 ChatClient 的关系

| 组件 | 职责 | 何时使用 |
| --- | --- | --- |
| `ChatModel` | 提供统一模型调用，处理提供方请求和响应转换。 | 需要直接控制 `Prompt`、完整响应或底层集成时。 |
| `StreamingChatModel` | 以 `Flux<ChatResponse>` 返回响应流。 | 直接消费模型流式结果时。 |
| `ChatClient` | 在模型之上提供链式 API、Advisors 等应用能力。 | 编写常规聊天、RAG 与工具调用业务时。 |

`ChatModel` 继承 `StreamingChatModel`。具体实现和所选型号是否支持流式仍需确认。已经学过 [ChatClient API](/frameworks/spring-ai/core/chat-client/) 后，本篇重点理解它下面的模型层，无需再背一遍完整接口源码。

## 一次请求和响应包含什么

调用关系是：`Prompt → ChatModel → ChatResponse`。

- `Prompt`：消息列表，以及可选的 `ChatOptions`。
- `Message`：文本、元数据和对话角色；支持媒体的消息还可携带 `Media`。
- `ChatResponse`：完整模型响应，包含结果集合及响应元数据。
- `Generation`：某个生成结果，包含 `AssistantMessage` 和该结果的元数据。

`ChatResponse.getResults()` 返回结果列表，`getResult()` 取首个结果。需要回答文本时继续读取 `getOutput().getText()`；若结果是工具调用或媒体输出，应读取相应结构。

消息角色见[提示词](/frameworks/spring-ai/core/prompts/)，Token 用量、限流与缓存指标见[响应元数据](/frameworks/spring-ai/core/chat-response-metadata/)。

## 同步调用与流式调用

假设 `chatModel` 已由应用配置并注入，同步调用返回完整响应：

```java
Prompt prompt = new Prompt("Explain Spring AI in one sentence.");
ChatResponse response = chatModel.call(prompt);
String text = response.getResult().getOutput().getText();
```

流式调用返回 `Flux<ChatResponse>`：

```java
Flux<ChatResponse> responses = chatModel.stream(prompt);
```

流中的元素代表逐步到达的响应，不应把每个元素都当成完整回答。常规文本消费也可以使用 `chatClient.prompt().user(...).stream().content()`，具体见 [ChatClient 流式调用](/frameworks/spring-ai/core/chat-client/)。

## ChatOptions：通用选项与专有选项

常用选项包括 `model`、`temperature`、`maxTokens`、`topP`、`topK`、停止序列，以及重复惩罚相关参数。不同模型支持的参数、范围和含义可能不同，不必一次配齐。

来源区分了两种运行时配置方式：

| 调用入口 | 配置规则 |
| --- | --- |
| 直接 `ChatModel.call(prompt)` / `stream(prompt)` | `Prompt` 未提供选项时使用模型默认值；提供选项时，应按来源约定准备完整选项，不依赖逐字段补齐。 |
| `ChatClient` 链式 API | 支持增量定制默认选项，单次请求只设置需要修改的字段。 |

例如，在 `ChatClient` 中只调整本次请求的温度：

```java
String text = chatClient.prompt()
    .user("Explain Spring AI in one sentence.")
    .options(options -> options.temperature(0.2))
    .call()
    .content();
```

这个例子要求所选模型支持 `temperature`。默认参数、请求级覆盖与提供方专有选项的关系，见 [ChatClient 参数配置](/frameworks/spring-ai/core/chat-client/)。

## 需要时再查的内容

接入某一家服务时，再阅读其 Starter、认证、模型名称、完整参数与特有功能。切换提供方时，即使业务仍使用 `ChatModel`，也要重新核对流式、多模态、工具调用和结构化输出能力。

- [Chat Model API 完整文档](https://docs.spring.io/spring-ai/reference/api/chatmodel.html)
- [聊天模型能力对比](https://docs.spring.io/spring-ai/reference/api/chat/comparison.html)
- 常见接入入口：[OpenAI](https://docs.spring.io/spring-ai/reference/api/chat/openai-chat.html)、[DeepSeek](https://docs.spring.io/spring-ai/reference/api/chat/deepseek-chat.html)、[Ollama](https://docs.spring.io/spring-ai/reference/api/chat/ollama-chat.html)、[Anthropic](https://docs.spring.io/spring-ai/reference/api/chat/anthropic-chat.html)、[Google GenAI](https://docs.spring.io/spring-ai/reference/api/chat/google-genai-chat.html)。其他实现从完整文档导航进入。

准备学习 RAG 时，再读 [Embedding 模型](/frameworks/spring-ai/models/embedding-model/)。

来源：[Chat Model API](https://docs.spring.io/spring-ai/reference/api/chatmodel.html)，精选整理，示例按核心方法补充。文档版本：2.0.2；核验日期：2026-10-25。
