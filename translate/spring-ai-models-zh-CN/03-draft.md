---
title: Spring AI：模型概览
description: 区分聊天、Embedding 与其他专用模型，理解统一模型 API 的作用，并按任务查阅提供方文档。
sidebar:
  label: 模型概览
  order: 1
---

Spring AI 通过统一的模型 API 封装不同提供方的服务，让应用以相近的方式组织请求和读取响应；需要专有能力时，仍可使用提供方特有的选项。

本小节精选模型章节中与当前学习最相关的内容：先区分模型类型，再掌握[聊天模型](/frameworks/spring-ai/models/chat-model/)与 [Embedding 模型](/frameworks/spring-ai/models/embedding-model/)。各提供方的安装、配置和完整参数按需查阅，不逐家展开。

## 按任务选择模型类型

| 任务 | 模型类型 | 当前学习重点 |
| --- | --- | --- |
| 聊天、内容生成、基于上下文回答 | 聊天模型 | 掌握 `ChatModel`；业务侧通常使用 `ChatClient`。 |
| 把文本变成向量，进行语义检索 | Embedding 模型 | 掌握 `EmbeddingModel`，为 RAG 做准备。 |
| 根据描述生成图片 | 图像模型 | 有图片生成需求时再学。 |
| 将录音转成文字 | 语音转写模型 | 有语音输入需求时再学。 |
| 将文字转成语音 | 语音合成模型 | 有播报需求时再学。 |
| 检测内容是否属于不当或风险类别 | 内容审核模型 | 根据产品审核需求选用。 |

**多模态是模型的能力，不是与聊天模型并列的另一套固定类型。** 支持图片输入的聊天模型，仍通过聊天接口处理文字与图片；“看懂图片”和“生成图片”也应分别确认。输入方式见[多模态](/frameworks/spring-ai/core/multimodality/)。

## 统一 API 统一了什么

Spring AI 的通用抽象围绕请求、选项和响应展开：

| 抽象 | 职责 |
| --- | --- |
| `Model` | 定义同步模型调用。 |
| `ModelRequest` / `ModelOptions` | 表达输入和调用选项。 |
| `ModelResponse` / `ModelResult` | 表达整体响应与其中的结果。 |
| `StreamingModel` | 定义流式调用；是否可用需看具体模型接口和实现。 |

聊天模型使用 `Prompt → ChatResponse`，Embedding 模型使用 `EmbeddingRequest → EmbeddingResponse`。应用通常使用这些具体 API，不必从通用接口手写实现。

统一 API 可以减少切换服务时的业务代码改动，但**不保证参数、模态、工具调用、结构化输出或生成效果完全相同**。更换模型时仍需验证实际任务。

## 接入时先确认这几件事

1. **任务与型号**：需要聊天还是 Embedding，具体型号是否支持所需能力。
2. **运行方式**：云 API 还是本地推理；延迟、资源与部署条件是否合适。
3. **接入配置**：匹配当前 Spring AI 版本的依赖、认证、地址、区域和模型名称。
4. **调用限制**：输入长度、输出上限、媒体限制、请求频率与计费方式。
5. **响应与异常**：是否需要流式响应、用量统计、超时与重试。

先接入一个聊天模型。进入 RAG 阶段再选择一个 Embedding 模型，两者可以来自不同提供方。

## 按需查询的文档入口

| 需求 | 文档 |
| --- | --- |
| 对比聊天模型适配能力 | [Chat Models Comparison](https://docs.spring.io/spring-ai/reference/api/chat/comparison.html) |
| 找聊天模型的接入配置 | [Chat Models](https://docs.spring.io/spring-ai/reference/api/chatmodel.html#_available_implementations) |
| 找 Embedding 提供方实现 | [Embedding Models](https://docs.spring.io/spring-ai/reference/api/embeddings.html#available-implementations) |
| 生成图片 | [Image Models](https://docs.spring.io/spring-ai/reference/api/imageclient.html) |
| 语音转文字 | [Transcription API](https://docs.spring.io/spring-ai/reference/api/audio/transcriptions.html) |
| 文字转语音 | [Text-To-Speech API](https://docs.spring.io/spring-ai/reference/api/audio/speech.html) |
| 内容审核 | [Moderation Models](https://docs.spring.io/spring-ai/reference/api/moderation.html) |

本地笔记保留稳定概念和常用 API。模型清单、Starter 名称、完整配置键和提供方专有参数，以你使用版本的文档为准。

来源：[Spring AI API：AI Model API](https://docs.spring.io/spring-ai/reference/api/index.html#_ai_model_api)及模型导航分类，精选整理；接入检查项为工程建议。文档版本：2.0.2；核验日期：2026-10-25。
