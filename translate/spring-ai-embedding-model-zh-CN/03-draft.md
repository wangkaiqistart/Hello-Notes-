---
title: Spring AI：Embedding 模型
description: 理解 EmbeddingModel 如何生成文本向量，掌握常用方法、请求响应结构，以及维度和向量空间的一致性。
sidebar:
  label: Embedding 模型
  order: 3
---

**嵌入（Embedding）**是内容的数值表示。嵌入模型把内容转换为浮点数数组，也就是向量；数组长度称为**维度**。通过比较同一向量空间中的向量，可以衡量内容的语义相似程度。

Embedding 技术可处理文字、图片等内容，本文精选 `EmbeddingModel` 的文本 API，为后续语义检索与 RAG 做准备。各提供方的配置和完整类定义保留官网入口。

## EmbeddingModel 负责什么

`EmbeddingModel` 将文本转换成向量，便于语义检索、分类等后续处理。它本身不存储文档，不执行完整检索，也不生成问答答案。

在常见文本 RAG 中，三类组件分工如下：

| 组件 | 作用 |
| --- | --- |
| `EmbeddingModel` | 将文档内容或用户问题转换为向量。 |
| `VectorStore` | 保存文档与向量，并进行相似度检索。 |
| `ChatModel` | 结合检索到的资料生成回答。 |

聊天模型与 Embedding 模型可以来自不同提供方；但用于同一检索空间的文档向量和查询向量必须相互兼容。

## 常用方法

| 方法 | 返回值 | 用途 |
| --- | --- | --- |
| `embed(String)` | `float[]` | 将一段文本转换为向量。 |
| `embed(Document)` | `float[]` | 对文档内容进行向量化。 |
| `embed(List<String>)` | `List<float[]>` | 批量转换多段文本。 |
| `embedForResponse(List<String>)` | `EmbeddingResponse` | 同时获取向量和响应元数据。 |
| `call(EmbeddingRequest)` | `EmbeddingResponse` | 显式传递输入列表与 Embedding 选项。 |
| `dimensions()` | `int` | 获取向量维度；默认实现可能调用远端接口。 |

假设已配置并注入 `embeddingModel`，转换一段文本：

```java
float[] vector = embeddingModel.embed("How do I track my order?");
int dimensions = vector.length;
```

这里直接读取已有向量的长度，无需为确认维度额外发起模型请求。[`dimensions()` 的 API 说明](https://docs.spring.io/spring-ai/docs/2.0.2/api/org/springframework/ai/embedding/EmbeddingModel.html#dimensions())明确提醒：默认实现会通过 Embedding 调用获取维度，不应将其当作一定免费的本地属性读取。

批量转换：

```java
List<float[]> vectors = embeddingModel.embed(List.of(
    "Where is my order?",
    "How can I cancel an order?"
));
```

需要响应元数据时：

```java
EmbeddingResponse response = embeddingModel.embedForResponse(
    List.of("How do I track my order?")
);
float[] vector = response.getResults().get(0).getOutput();
```

这些示例是方法用法片段，需要应用提供对应模型 Bean；并非完整启动项目。

## 请求、响应和 Document 的边界

`EmbeddingModel` 继承 `Model<EmbeddingRequest, EmbeddingResponse>`：

- `EmbeddingRequest`：输入文本列表与可选 `EmbeddingOptions`。
- `EmbeddingResponse`：一组 `Embedding` 结果及响应元数据。
- `Embedding`：对应某一输入的向量、索引与结果元数据。

`getEmbeddingContent(Document)` 控制从文档中提取哪些内容参与向量化。默认取 `Document.getText()`；支持 `MetadataMode` 的实现可以按配置将元数据拼入文本。这会影响嵌入结果，不能默认“传入 Document 就只嵌入正文”。

## 工程上先记住三点

1. **维度匹配**：输出向量维度必须与向量存储的配置一致。
2. **向量空间一致**：文档入库和问题查询使用兼容的嵌入模型与配置。维度相同不代表不同模型的向量就能直接比较。
3. **更换模型需处理旧索引**：模型或影响向量的配置改变后，应评估重新嵌入文档、重建或迁移索引，避免混用新旧向量。

这些是检索工程的实践要求。此阶段先理解“文本如何变成向量”，文档切分、批量入库、Top-K 和过滤条件放到后续 RAG 笔记中实践。

## 按需查询

- [Embedding Model API 完整文档](https://docs.spring.io/spring-ai/reference/api/embeddings.html)
- [提供方实现列表](https://docs.spring.io/spring-ai/reference/api/embeddings.html#available-implementations)
- 常见接入入口：[OpenAI](https://docs.spring.io/spring-ai/reference/api/embeddings/openai-embeddings.html)、[Ollama](https://docs.spring.io/spring-ai/reference/api/embeddings/ollama-embeddings.html)、[Google GenAI](https://docs.spring.io/spring-ai/reference/api/embeddings/google-genai-embeddings-text.html)、[Mistral AI](https://docs.spring.io/spring-ai/reference/api/embeddings/mistralai-embeddings.html)。

模型名称、输出维度是否可调、批量大小、输入长度和计费规则，接入时查对应版本的提供方文档。

来源：[Embeddings Model API](https://docs.spring.io/spring-ai/reference/api/embeddings.html)，精选整理，补充最小调用片段与工程提示；返回类型和维度行为参考 [2.0.2 API](https://docs.spring.io/spring-ai/docs/2.0.2/api/org/springframework/ai/embedding/EmbeddingModel.html)。核验日期：2026-10-25。
