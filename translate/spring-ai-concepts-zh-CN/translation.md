---
title: Spring AI：AI 核心概念
description: 简明理解模型、提示词、Embedding、Token、结构化输出、RAG、工具调用与响应评估。
sidebar:
  label: AI 核心概念
  order: 2
---

理解 Spring AI，可以先掌握这条主线：**用提示词描述任务，用模型生成结果，用企业数据和工具补充能力，再评估输出是否可靠。**

## 模型：处理什么，生成什么

AI 模型从训练数据中学习规律，用于预测或生成内容。不同模型的输入、输出不同：语言模型处理文本和代码，多模态模型可处理图像、音频等，嵌入模型则将内容转换为向量。

下图按输入、模型类型和输出划分常见能力。选择模型时，先确认它是否支持任务需要的数据类型。

![模型类型对照：语言、图像、音频及 Embedding 模型的输入与输出](/images/frameworks/spring-ai/spring-ai-model-types-zh.svg)

Spring AI 支持语言、图像、音频及嵌入相关模型。使用预训练模型时，应用开发者可以直接集成已有能力，无需先掌握完整的机器学习或模型训练流程。

## 提示词：不只是一个字符串

提示词（Prompt）向模型说明任务、上下文和输出要求。聊天请求通常由多条带角色的消息组成：

- **System**：设定模型行为与交互背景。
- **User**：提供用户的问题或任务。

与通过 SQL 查询数据不同，使用提示词需要像与人交谈一样表达意图。组织和改进提示词的方法称为**提示词工程（Prompt Engineering）**：通过调整指令、上下文和表达方式改善输出，并反复验证效果。

### 提示词模板

模板把固定指令与动态输入分开。例如：

```text
Tell me a {adjective} joke about {content}.
```

Spring AI 使用 [StringTemplate](https://www.stringtemplate.org/) 处理模板，通过 `java.util.Map` 提供模板变量。渲染时将 `adjective` 和 `content` 替换为实际值，生成供模型使用的提示词；这类似 Spring MVC 的视图渲染。

## Embedding：内容的向量表示

**嵌入（Embedding）是文本、图像或视频等内容的数值表示**，用于表达内容之间的关系。嵌入模型将内容转换为浮点数数组，也就是向量；数组的长度称为**向量维度**。

通过比较向量的距离或相似度，应用可以查找语义相近的内容，支持语义搜索、分类、推荐和 RAG。在高维语义空间中，含义相近的内容通常对应位置相近的向量。下图展示了内容经嵌入模型转换为向量的过程。

![Embedding 流程：文本和图像经嵌入模型转换为浮点向量，并在向量空间中表达内容之间的关系](/images/frameworks/spring-ai/spring-ai-embeddings-zh.svg)

应用开发先理解“内容 → 向量 → 相似度检索”即可，不必从底层数学推导开始。

## Token：长度、费用和上下文限制

**词元（Token）是模型处理文本的基本单位**：输入文本先被切分为 Token，模型生成的 Token 再转换为输出文本。Token 不等于单词或汉字，具体如何切分取决于模型的分词器。下图用 `cl100k_base` 分词器展示中英文切分：每个彩色片段代表一个 Token，`·` 表示空格。

![Token 切分示例：中文“这是一个测试。”切成 5 个 Token，英文“ChatGPT generates tokens.”切成 6 个 Token；使用 cl100k_base 分词器](/images/frameworks/spring-ai/spring-ai-tokens-zh.svg)

需要关注两件事：

- **费用**：托管模型通常按输入和输出 Token 用量计费，具体价格取决于服务商。
- **上下文窗口**：一次调用能够容纳的内容有上限，需要为问题、历史消息、参考资料和输出预留空间。

长文档通常需要切分、检索或分阶段处理。上下文容量随模型版本而异，以具体模型文档为准。

## 结构化输出：让结果能被程序使用

模型返回的文本即使符合 JSON 格式，也仍是字符串，需要解析后才能作为程序中的数据结构使用。仅在提示词中要求 JSON，也不能保证格式始终正确。

下图所示的**提示词驱动转换方式**分为两步：调用前提供格式要求，调用后把返回文本转换为目标数据结构。为得到所需格式，可能需要多次与模型交互。

![结构化输出转换：在调用模型前补充格式指令，将模型返回的文本转换为结构化结果](/images/frameworks/spring-ai/spring-ai-structured-output-zh.svg)

Spring AI 提供[结构化输出](https://docs.spring.io/spring-ai/reference/api/structured-output.html)能力，便于映射为 Java 对象。应用仍需处理解析失败和字段校验。

## 把企业数据和 API 接入模型

模型的训练知识有时间和范围限制，也不会天然拥有企业的私有数据。常见补充方式有三种：

| 方式                          | 做法                     | 特点                                         |
| ----------------------------- | ------------------------ | -------------------------------------------- |
| 微调（Fine-tuning）           | 使用训练数据调整模型权重 | 需要训练资源和专业能力，是否支持取决于模型。 |
| 提示词填充（Prompt Stuffing） | 将相关资料放进提示词     | 不改变模型权重，但受上下文窗口限制。         |
| 工具调用（Tool Calling）      | 将业务服务注册为工具     | 获取实时信息，或由应用执行外部系统中的操作。 |

提示词填充把用户问题和参考资料一起交给模型。RAG 在此基础上增加检索步骤，先找出相关资料，再补充到提示词中。下图展示了问题与资料如何组合成新的提示词。

![提示词填充流程：将用户问题与参考资料合并为提示词，再发送给聊天模型](/images/frameworks/spring-ai/spring-ai-prompt-stuffing-zh.svg)

### RAG：先检索，再生成

检索增强生成（Retrieval Augmented Generation，RAG）将检索到的相关文档片段加入提示词，为回答提供依据。基于向量检索的典型流程包含两个阶段：

1. **文档入库**：读取文档 → 切分内容 → 生成向量 → 写入向量数据库。
2. **运行时问答**：接收问题 → 检索相关片段 → 将问题与片段组成提示词 → 由模型生成回答。

切分时尽量保留语义边界，避免拆断段落、表格或方法实现，并控制片段大小，为其他上下文留出空间。下图上半部分是入库的 ETL（提取、转换、加载）流程，下半部分是检索与生成流程。

![Spring AI RAG 架构：离线读取和切分文档写入向量库，运行时检索片段并补充到提示词中生成回答](/images/frameworks/spring-ai/spring-ai-rag-zh.svg)

Spring AI 的 [ETL Pipeline](https://docs.spring.io/spring-ai/reference/api/etl-pipeline.html) 负责文档处理；[ChatClient 的 RAG 能力](https://docs.spring.io/spring-ai/reference/api/chatclient.html#_retrieval_augmented_generation)可通过 `QuestionAnswerAdvisor` 等方式接入检索上下文。

### 工具调用：由应用执行实际操作

模型本身不能直接访问或修改外部系统的数据。工具调用允许模型提出调用请求，由应用执行服务，并把结果返回给模型。在 Spring AI 中，可用 `@Tool` 标注业务方法，注册后将工具定义随请求提供给模型；同一次请求也可提供多个工具。

一次典型调用包含六步：

1. 应用向模型提供工具定义：名称、描述和输入参数结构。
2. 模型决定调用工具时，返回工具名称和参数。
3. 应用根据工具名称找到工具，并使用参数执行调用。
4. 应用接收并处理执行结果。
5. 应用将工具结果回传模型。
6. 模型结合工具结果生成最终回答。

下图中的编号对应上述步骤，重点看清模型发出请求、应用执行工具、结果回传模型的边界。

![工具调用流程：请求携带工具定义，模型按需提出调用，Spring AI 分派执行并回传结果，模型生成回答](/images/frameworks/spring-ai/spring-ai-tool-calling-zh.svg)

Spring AI 负责协调工具调用对话，具体用法见[工具调用文档](https://docs.spring.io/spring-ai/reference/api/tools.html)。

## 评估：回答是否符合问题和依据

评估需要判断生成的回答是否符合用户意图和问题上下文，常用指标包括：

- **相关性**：是否回答了用户的问题。
- **连贯性**：表达是否清楚，前后是否一致。
- **事实正确性**：是否与已知事实和参考资料相符。

预训练模型也可以辅助评估：将用户问题、模型回答和参考资料提交给模型，判断回答是否与资料一致。向量数据库中的相关内容也可作为补充依据，帮助判断回答的相关性。

Spring AI 提供 `Evaluator` API，支持基础评估策略，详见[响应评估与测试](https://docs.spring.io/spring-ai/reference/api/testing.html)。

来源：[Spring AI Concepts](https://docs.spring.io/spring-ai/reference/concepts.html)。文档版本：2.0.2；核验日期：2026-10-25。本文为简明中文译述。
