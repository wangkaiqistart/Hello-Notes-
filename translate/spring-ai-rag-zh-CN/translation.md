---
title: Spring AI：检索增强生成（RAG）
description: 两种 RAG Advisor 的接入、过滤和模板，以及查询转换、扩展、文档检索与后处理的完整模块参考。
sidebar:
  label: 检索增强生成（RAG）
  order: 1
---

检索增强生成（Retrieval Augmented Generation，RAG）用于弥补大语言模型在长篇内容处理、事实准确性和上下文理解方面的局限。

Spring AI 采用模块化架构支持 RAG：既可以自行组合模块构建流程，也可以通过 [Advisor API](/frameworks/spring-ai/core/advisors/#核心组件与执行流程) 使用现成流程。

:::note
RAG 的基本原理见[AI 核心概念：先检索，再生成](/frameworks/spring-ai/concepts/#rag先检索再生成)。
:::

:::tip[阅读路线]
先掌握两种 Advisor 的区别、检索参数和空上下文行为，再按问题选择查询重写、扩展或重排序。所有模块示例都保留在后半篇供查阅，不需要一次配齐。
:::

本篇处理**提问时**的链路：用户查询 → 检索文档 → 补入提示词 → 模型回答。资料的读取、切分和入库见 [ETL 管道](/frameworks/spring-ai/rag/document-ingestion/)，向量模型基础见 [Embedding 模型](/frameworks/spring-ai/models/embedding-model/)。

| 需求                                 | 选择                           | 依赖                             |
| ------------------------------------ | ------------------------------ | -------------------------------- |
| 已有向量库，快速接入基础文档问答     | `QuestionAnswerAdvisor`        | `spring-ai-vector-store-advisor` |
| 需要组合查询转换、扩展、检索和后处理 | `RetrievalAugmentationAdvisor` | `spring-ai-rag`                  |

示例假设 `ChatModel`、[`ChatClient` 或 `ChatClient.Builder`](/frameworks/spring-ai/core/chat-client/#创建-chatclient) 已配置，并且 [`VectorStore`](/frameworks/spring-ai/rag/vector-stores/#api-overview) 中已有文档。代码中的相似度阈值与 Top-K 都是示例值，应按数据和模型进行[评估测试](/frameworks/spring-ai/engineering/evaluation/#_relevancy_evaluator)；添加 Advisor 不会自动导入资料，也不会自动生成可核验的来源引用。

<a id="_advisors"></a>

## 一、RAG Advisor（重点掌握）

Spring AI 通过 `Advisor` API 提供常见 RAG 流程的开箱即用支持。

使用 `QuestionAnswerAdvisor` 或 `VectorStoreChatMemoryAdvisor`，需要添加 `spring-ai-vector-store-advisor` 依赖：

```xml
<dependency>
   <groupId>org.springframework.ai</groupId>
   <artifactId>spring-ai-vector-store-advisor</artifactId>
</dependency>
```

<a id="_questionansweradvisor"></a>

### QuestionAnswerAdvisor

向量数据库可以存储模型原本不了解的资料。用户提问时，`QuestionAnswerAdvisor` 会先检索与问题相关的文档，再把检索结果追加到用户文本中，为模型生成回答提供上下文。

假设资料已经加载到 `VectorStore`，把 `QuestionAnswerAdvisor` 传给 `ChatClient` 即可执行 RAG：

```java
ChatResponse response = ChatClient.builder(chatModel)
        .build().prompt()
        .advisors(QuestionAnswerAdvisor.builder(vectorStore).build())
        .user(userText)
        .call()
        .chatResponse();
```

这里会对向量数据库中的全部文档执行相似度检索。若要限制检索范围，可以在 [`SearchRequest`](/frameworks/spring-ai/rag/vector-stores/#_searchrequest_builder) 中使用类似 SQL 的[元数据过滤表达式](/frameworks/spring-ai/rag/vector-stores/#metadata-filters)；同一表达式可跨 `VectorStore` 实现使用。

过滤条件既可以在创建 `QuestionAnswerAdvisor` 时配置，作为默认检索条件，也可以在运行时按请求传入；请求条件会覆盖默认过滤条件。

下面把相似度阈值设为 `0.8`，最多返回 `6` 条结果：

```java
var qaAdvisor = QuestionAnswerAdvisor.builder(vectorStore)
        .searchRequest(SearchRequest.builder().similarityThreshold(0.8d).topK(6).build())
        .build();
```

<a id="_dynamic_filter_expressions"></a>

#### 动态过滤表达式

通过 Advisor 上下文参数 `FILTER_EXPRESSION`，可以在运行时更新 `SearchRequest` 的过滤表达式：

```java
ChatClient chatClient = ChatClient.builder(chatModel)
    .defaultAdvisors(QuestionAnswerAdvisor.builder(vectorStore)
        .searchRequest(SearchRequest.builder().build())
        .build())
    .build();

// Update filter expression at runtime
String content = chatClient.prompt()
    .user("Please answer my question XYZ")
    .advisors(a -> a.param(QuestionAnswerAdvisor.FILTER_EXPRESSION, "type == 'Spring'"))
    .call()
    .content();
```

`FILTER_EXPRESSION` 会根据本次传入的表达式动态筛选检索结果。

<a id="_custom_template"></a>

#### 自定义模板

`QuestionAnswerAdvisor` 默认使用内置模板，把检索文档补充到用户问题中。通过构建器的 `.promptTemplate()` 方法传入自定义 `PromptTemplate`，可以调整合并方式。

:::note
这里的 `PromptTemplate` 控制 Advisor 如何合并检索上下文与用户查询。`ChatClient.templateRenderer()` 则控制 Advisor 执行**之前**，初始用户提示词和系统提示词的渲染，两者作用阶段不同。详见 [ChatClient 提示词模板](/frameworks/spring-ai/core/chat-client/#提示词模板)。
:::

自定义 `PromptTemplate` 可以使用任意 `TemplateRenderer` 实现；默认使用基于 StringTemplate 引擎的 `StTemplateRenderer`，渲染器与占位符的用法见 [PromptTemplate](/frameworks/spring-ai/core/prompts/#prompttemplate将模板转换为提示词)。模板必须包含两个占位符：

- `query`：接收用户问题。
- `question_answer_context`：接收检索上下文。

```java
PromptTemplate customPromptTemplate = PromptTemplate.builder()
    .renderer(StTemplateRenderer.builder().startDelimiterToken('<').endDelimiterToken('>').build())
    .template("""
            <query>

            Context information is below.

			---------------------
			<question_answer_context>
			---------------------

			Given the context information and no prior knowledge, answer the query.

			Follow these rules:

			1. If the answer is not in the context, just say that you don't know.
			2. Avoid statements like "Based on the context..." or "The provided information...".
            """)
    .build();

    String question = "Where does the adventure of Anacletus and Birba take place?";

    QuestionAnswerAdvisor qaAdvisor = QuestionAnswerAdvisor.builder(vectorStore)
        .promptTemplate(customPromptTemplate)
        .build();

    String response = ChatClient.builder(chatModel).build()
        .prompt(question)
        .advisors(qaAdvisor)
        .call()
        .content();
```

:::note
旧版的 `userTextAdvise()` 自定义入口已由 `.promptTemplate()` 取代；2.0.2 的 Builder 已不提供 `userTextAdvise()`，新代码使用 `.promptTemplate()`。
:::

<a id="_retrievalaugmentationadvisor"></a>

### RetrievalAugmentationAdvisor

Spring AI 提供一组 [RAG 模块](#modules)，可以组合成自定义流程。`RetrievalAugmentationAdvisor` 基于这些模块，为常见 RAG 流程提供现成的 Advisor 实现。

查询转换、扩展和文档后处理分别对应构建器的 `queryTransformers(...)`、`queryExpander(...)`、`documentPostProcessors(...)`。其中只有 `documentRetriever(...)` 必填，其余模块按需要配置。

使用它需要添加 `spring-ai-rag` 依赖：

```xml
<dependency>
   <groupId>org.springframework.ai</groupId>
   <artifactId>spring-ai-rag</artifactId>
</dependency>
```

<a id="_sequential_rag_flows"></a>

#### 顺序式 RAG 流程

<a id="_naive_rag"></a>

##### 基础 RAG（Naive RAG）

配置文档检索器即可建立“检索 → 补充上下文 → 生成回答”的基本流程：

```java
Advisor retrievalAugmentationAdvisor = RetrievalAugmentationAdvisor.builder()
        .documentRetriever(VectorStoreDocumentRetriever.builder()
                .similarityThreshold(0.50)
                .vectorStore(vectorStore)
                .build())
        .build();

String answer = chatClient.prompt()
        .advisors(retrievalAugmentationAdvisor)
        .user(question)
        .call()
        .content();
```

默认情况下，`RetrievalAugmentationAdvisor` 不接受空的检索上下文；未检索到内容时，会通过提示词要求模型不要回答。这仍会调用模型；若业务要求严格拒答，应在应用层检测检索结果并决定是否继续生成。可以按下面的方式允许空上下文：

```java
Advisor retrievalAugmentationAdvisor = RetrievalAugmentationAdvisor.builder()
        .documentRetriever(VectorStoreDocumentRetriever.builder()
                .similarityThreshold(0.50)
                .vectorStore(vectorStore)
                .build())
        .queryAugmenter(ContextualQueryAugmenter.builder()
                .allowEmptyContext(true)
                .build())
        .build();

String answer = chatClient.prompt()
        .advisors(retrievalAugmentationAdvisor)
        .user(question)
        .call()
        .content();
```

`VectorStoreDocumentRetriever` 支持通过 `FilterExpression` 按元数据筛选结果。可以在创建检索器时配置，也可以通过 Advisor 上下文参数 `FILTER_EXPRESSION` 按请求传入：

```java
Advisor retrievalAugmentationAdvisor = RetrievalAugmentationAdvisor.builder()
        .documentRetriever(VectorStoreDocumentRetriever.builder()
                .similarityThreshold(0.50)
                .vectorStore(vectorStore)
                .build())
        .build();

String answer = chatClient.prompt()
        .advisors(retrievalAugmentationAdvisor)
        .advisors(a -> a.param(VectorStoreDocumentRetriever.FILTER_EXPRESSION, "type == 'Spring'"))
        .user(question)
        .call()
        .content();
```

详见 [VectorStoreDocumentRetriever](#_vectorstoredocumentretriever)。

<a id="_advanced_rag"></a>

##### 进阶 RAG（Advanced RAG）

在检索前加入查询重写，将用户的原始表述转换为更适合检索的查询，再执行相似度搜索：

```java
Advisor retrievalAugmentationAdvisor = RetrievalAugmentationAdvisor.builder()
        .queryTransformers(RewriteQueryTransformer.builder()
                .chatClientBuilder(chatClientBuilder.build().mutate())
                .build())
        .documentRetriever(VectorStoreDocumentRetriever.builder()
                .similarityThreshold(0.50)
                .vectorStore(vectorStore)
                .build())
        .build();

String answer = chatClient.prompt()
        .advisors(retrievalAugmentationAdvisor)
        .user(question)
        .call()
        .content();
```

还可以使用 `DocumentPostProcessor`，在文档传给模型之前执行检索后处理，例如按查询相关性重排序、移除无关或重复文档，或压缩各文档内容以减少噪声与冗余。

<a id="modules"></a>

## 二、模块参考（按需深入）

Spring AI 的模块化 RAG 架构借鉴了论文《[Modular RAG: Transforming RAG Systems into LEGO-like Reconfigurable Frameworks](https://arxiv.org/abs/2407.21059)》中的模块化设计。

| 阶段       | 主要职责                                                     | 本篇实现                                                                                                      |
| ---------- | ------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------- |
| 检索前处理 | 把追问、含糊查询或跨语言查询转为适合检索的形式；扩展多个查询 | `CompressionQueryTransformer`、`RewriteQueryTransformer`、`TranslationQueryTransformer`、`MultiQueryExpander` |
| 检索       | 查找文档，合并多查询或多来源结果                             | `VectorStoreDocumentRetriever`、`ConcatenationDocumentJoiner`                                                 |
| 检索后处理 | 重排序、去噪、去重、压缩文档                                 | `DocumentPostProcessor` 扩展点                                                                                |
| 生成       | 将文档内容补入查询，交给模型回答                             | `ContextualQueryAugmenter`                                                                                    |

<a id="_pre_retrieval"></a>

### 检索前处理

检索前处理模块负责处理用户查询，以改善检索结果。

<a id="_query_transformation"></a>

#### 查询转换

查询转换组件将输入查询改写为更适合检索的形式，处理表达不清、术语歧义、词汇复杂或语言不受支持等问题。

:::note
使用 `QueryTransformer` 时，若模型提供方支持 temperature，建议为相应的 `ChatClient.Builder` 配置较低值，例如 `0.0`，让转换结果更稳定。部分模型的默认 temperature 对查询转换而言偏高，可能影响检索效果；具体支持范围和默认值取决于提供方。
:::

<a id="_compressionquerytransformer"></a>

##### CompressionQueryTransformer

`CompressionQueryTransformer` 使用大语言模型，将对话历史与追问压缩成一条包含对话要点、可独立理解的查询。

它适合对话历史较长、追问依赖前文的场景。

```java
Query query = Query.builder()
        .text("And what is its second largest city?")
        .history(new UserMessage("What is the capital of Denmark?"),
                new AssistantMessage("Copenhagen is the capital of Denmark."))
        .build();

QueryTransformer queryTransformer = CompressionQueryTransformer.builder()
        .chatClientBuilder(chatClientBuilder)
        .build();

Query transformedQuery = queryTransformer.transform(query);
```

可以通过构建器的 `promptTemplate()` 自定义该组件使用的提示词。

<a id="_rewritequerytransformer"></a>

##### RewriteQueryTransformer

`RewriteQueryTransformer` 使用大语言模型重写用户查询，使其更适合向量存储、Web 搜索引擎等目标系统。

它适合查询冗长、含义模糊，或包含可能干扰检索的无关信息的场景。

```java
Query query = new Query("I'm studying machine learning. What is an LLM?");

QueryTransformer queryTransformer = RewriteQueryTransformer.builder()
        .chatClientBuilder(chatClientBuilder)
        .build();

Query transformedQuery = queryTransformer.transform(query);
```

可以通过构建器的 `promptTemplate()` 自定义该组件使用的提示词。

<a id="_translationquerytransformer"></a>

##### TranslationQueryTransformer

`TranslationQueryTransformer` 使用大语言模型，将查询翻译为文档嵌入模型支持的目标语言。查询已经使用目标语言，或无法识别其语言时，均原样返回。

当嵌入模型主要针对某种语言训练，而用户使用另一种语言提问时，可以使用这个组件。

```java
Query query = new Query("Hvad er Danmarks hovedstad?");

QueryTransformer queryTransformer = TranslationQueryTransformer.builder()
        .chatClientBuilder(chatClientBuilder)
        .targetLanguage("english")
        .build();

Query transformedQuery = queryTransformer.transform(query);
```

可以通过构建器的 `promptTemplate()` 自定义该组件使用的提示词。

<a id="_query_expansion"></a>

#### 查询扩展

查询扩展组件把一条查询扩展成多条查询：既可以通过不同表述改善表达不清的查询，也可以把复杂问题拆分成较简单的子查询。

<a id="_multiqueryexpander"></a>

##### MultiQueryExpander

`MultiQueryExpander` 使用大语言模型生成语义角度不同的查询变体，从多个视角补充上下文，提高找到相关结果的机会。

```java
MultiQueryExpander queryExpander = MultiQueryExpander.builder()
    .chatClientBuilder(chatClientBuilder)
    .numberOfQueries(3)
    .build();
List<Query> queries = queryExpander.expand(new Query("How to run a Spring Boot app?"));
```

默认会把原始查询包含在扩展结果中。可以通过构建器的 `includeOriginal` 关闭这一行为：

```java
MultiQueryExpander queryExpander = MultiQueryExpander.builder()
    .chatClientBuilder(chatClientBuilder)
    .includeOriginal(false)
    .build();
```

可以通过构建器的 `promptTemplate()` 自定义该组件使用的提示词。

<a id="_retrieval"></a>

### 检索

检索模块负责查询向量存储等数据系统，取回最相关的文档。

<a id="_document_search"></a>

#### 文档搜索

文档搜索组件从搜索引擎、向量存储、数据库或知识图谱等底层数据源中检索 `Document`。

<a id="_vectorstoredocumentretriever"></a>

##### VectorStoreDocumentRetriever

`VectorStoreDocumentRetriever` 从向量存储中检索与输入查询语义相似的文档，支持元数据过滤、相似度阈值和 Top-K 限制。

```java
DocumentRetriever retriever = VectorStoreDocumentRetriever.builder()
    .vectorStore(vectorStore)
    .similarityThreshold(0.73)
    .topK(5)
    .filterExpression(new FilterExpressionBuilder()
        .eq("genre", "fairytale")
        .build())
    .build();
List<Document> documents = retriever.retrieve(new Query("What is the main character of the story?"));
```

过滤表达式可以是固定的，也可以通过 `Supplier` 动态生成：

```java
DocumentRetriever retriever = VectorStoreDocumentRetriever.builder()
    .vectorStore(vectorStore)
    .filterExpression(() -> new FilterExpressionBuilder()
        .eq("tenant", TenantContextHolder.getTenantIdentifier())
        .build())
    .build();
List<Document> documents = retriever.retrieve(new Query("What are the KPIs for the next semester?"));
```

也可以通过 `Query` 的 `FILTER_EXPRESSION` 上下文参数，传入本次请求专用的过滤表达式。若同时存在请求级和检索器级过滤条件，请求级条件优先，覆盖检索器条件，不会自动将两者用 AND 合并。

**工程判断**：租户过滤必须来自服务端可信的身份上下文。若允许请求传入其他筛选条件，应在服务端显式组合必要的租户限制，避免覆盖掉数据隔离条件。示例中的 `TenantContextHolder` 是应用自定义的上下文工具，并非 Spring AI 自动提供的授权机制。

```java
Query query = Query.builder()
    .text("Who is Anacletus?")
    .context(Map.of(VectorStoreDocumentRetriever.FILTER_EXPRESSION, "location == 'Whispering Woods'"))
    .build();
List<Document> retrievedDocuments = documentRetriever.retrieve(query);
```

<a id="_document_join"></a>

#### 文档合并

文档合并组件将多个查询、多个数据源取回的文档合并为一个集合，也可以在合并过程中处理重复文档及倒数排名等排序策略。

<a id="_concatenationdocumentjoiner"></a>

##### ConcatenationDocumentJoiner

`ConcatenationDocumentJoiner` 将多个查询、多个数据源的检索结果拼接成一个文档集合。按文档 ID 去重，重复 ID 保留遍历时先遇到的文档；各文档分数保持不变，最终按分数降序排列，空分数按 `0.0` 处理。

```java
Map<Query, List<List<Document>>> documentsForQuery = ...
DocumentJoiner documentJoiner = new ConcatenationDocumentJoiner();
List<Document> documents = documentJoiner.join(documentsForQuery);
```

<a id="_post_retrieval"></a>

### 检索后处理

检索后处理模块负责加工已检索到的文档，以改善生成结果。

<a id="_document_post_processing"></a>

#### 文档后处理

文档后处理组件根据查询处理检索结果，应对 _lost-in-the-middle_（模型容易忽略长上下文中间的信息）、模型上下文长度限制，以及检索信息中的噪声与冗余等问题。

例如，可以按查询相关性重排序，移除无关或重复文档，或压缩文档内容。

[Qxotic jinfer](https://docs.spring.io/spring-ai/reference/api/embeddings/jinfer-embeddings.html#reranking) 集成提供 `JinferDocumentPostProcessor`，可以使用本地重排序模型调整检索结果的顺序。

<a id="_generation"></a>

### 生成

生成模块根据用户查询和检索到的文档生成最终回答。

<a id="_query_augmentation"></a>

#### 查询增强

查询增强组件将额外数据补充到输入查询中，为大语言模型回答问题提供必要上下文。

<a id="_contextualqueryaugmenter"></a>

##### ContextualQueryAugmenter

`ContextualQueryAugmenter` 使用传入文档的内容增强用户查询。

```java
QueryAugmenter queryAugmenter = ContextualQueryAugmenter.builder().build();
```

默认不允许检索上下文为空；如果为空，会通过提示词要求模型不要回答用户问题。

启用 `allowEmptyContext` 后，即使检索上下文为空，也允许模型生成回答：

```java
QueryAugmenter queryAugmenter = ContextualQueryAugmenter.builder()
        .allowEmptyContext(true)
        .build();
```

可以通过构建器的 `promptTemplate()` 和 `emptyContextPromptTemplate()`，分别自定义常规上下文与空上下文使用的提示词。

来源：[Spring AI Retrieval Augmented Generation](https://docs.spring.io/spring-ai/reference/api/retrieval-augmented-generation.html)。文档版本：2.0.2；核验日期：2026-11-01。
