---
title: Spring AI：向量存储
description: VectorStore 与只读检索接口、SearchRequest、批处理、元数据过滤、删除和文档版本管理，并说明各后端子页的阅读顺序。
sidebar:
  label: 向量存储总览
  order: 1
---

向量数据库用于保存向量并进行相似度检索，是 AI 应用中常见的数据组件。

与关系型数据库常见的精确匹配查询不同，向量检索查找的是与查询向量相似的向量。向量表示与语义相似的关系见 [AI 核心概念：Embedding](/frameworks/spring-ai/concepts/#embedding内容的向量表示)；余弦、欧几里得和内积度量可对照 [Redis 的距离度量说明](/frameworks/spring-ai/rag/vector-stores/redis/#_distance_metrics)，具体分数换算取决于后端实现。

向量数据库可以把自有资料接入 AI 应用：先将资料写入向量库；用户提问时，先检索相关文档，再把文档作为上下文，与问题一起交给模型。这就是[检索增强生成（RAG）](/frameworks/spring-ai/rag/retrieval-and-generation/)。

下面介绍 Spring AI 统一的向量存储接口、不同后端的实现和基本用法。末尾的向量原理入口进一步解释相似度检索。

:::tip[阅读路线]
先看 [API 概览](#api-overview)、[基本读写](#_example_usage)和[元数据过滤](#metadata-filters)，用一种后端完成写入与检索；批处理、自动截断、删除与版本管理保留作完整参考。

后端学习范围确定为 **PGvector → Milvus → Redis → S3 Vector Store → Elasticsearch（ES）**。[PGvector](/frameworks/spring-ai/rag/vector-stores/pgvector/) 衔接已有 [RAG](/frameworks/spring-ai/rag/retrieval-and-generation/) 和[评估测试](/frameworks/spring-ai/engineering/evaluation/)中的 `pgVectorStore` 示例；再读 [Milvus](/frameworks/spring-ai/rag/vector-stores/milvus/)、[Redis](/frameworks/spring-ai/rag/vector-stores/redis/)、[S3 Vector Store](/frameworks/spring-ai/rag/vector-stores/s3-vector-store/) 和 [Elasticsearch（ES）](/frameworks/spring-ai/rag/vector-stores/elasticsearch/)。其他实现只保留查询入口。
:::

<a id="api-overview"></a>

## 一、API 概览（重点掌握）

Spring AI 通过 `VectorStore` 统一访问向量数据库，并提供只读接口 `VectorStoreRetriever`。

<a id="_vectorstoreretriever_interface"></a>

### VectorStoreRetriever：只读检索接口

`VectorStoreRetriever` 只暴露文档检索方法：

```java
@FunctionalInterface
public interface VectorStoreRetriever {

    List<Document> similaritySearch(SearchRequest request);

    default List<Document> similaritySearch(String query) {
        return this.similaritySearch(SearchRequest.builder().query(query).build());
    }
}
```

这是一个函数式接口，适合只需要查询、不需要修改数据的组件。通过收窄接口，调用方只接触检索所需的方法。不过，这只是应用接口层面的限制，不能代替数据库权限控制。

<a id="_vectorstore_interface"></a>

### VectorStore：读写接口

`VectorStore` 继承 `VectorStoreRetriever`，并增加写入和删除能力：

```java
public interface VectorStore extends DocumentWriter, VectorStoreRetriever {

    default String getName() {
		return this.getClass().getSimpleName();
	}

    void add(List<Document> documents);

    void delete(List<String> idList);

    void delete(Filter.Expression filterExpression);

    default void delete(String filterExpression) { ... }

    default <T> Optional<T> getNativeClient() {
		return Optional.empty();
	}
}
```

`VectorStore` 同时支持添加、删除和相似度检索，也能作为 [ETL 管道](/frameworks/spring-ai/rag/document-ingestion/#vectorstore) 的写入端。以上为接口节选，`...` 表示省略的实现，不是可直接编译的完整源码。

<a id="_searchrequest_builder"></a>

### SearchRequest：构建检索请求

下面保留构建器及字段的参考节选，省略了部分方法体；实际使用时通过 `SearchRequest.builder()` 创建请求。

```java
public class SearchRequest {

	public static final double SIMILARITY_THRESHOLD_ACCEPT_ALL = 0.0;

	public static final int DEFAULT_TOP_K = 4;

	private String query = "";

	private int topK = DEFAULT_TOP_K;

	private double similarityThreshold = SIMILARITY_THRESHOLD_ACCEPT_ALL;

	@Nullable
	private Filter.Expression filterExpression;

    public static Builder from(SearchRequest originalSearchRequest) {
		return builder().query(originalSearchRequest.getQuery())
			.topK(originalSearchRequest.getTopK())
			.similarityThreshold(originalSearchRequest.getSimilarityThreshold())
			.filterExpression(originalSearchRequest.getFilterExpression());
	}

	public static class Builder {

		private final SearchRequest searchRequest = new SearchRequest();

		public Builder query(String query) {
			Assert.notNull(query, "Query can not be null.");
			this.searchRequest.query = query;
			return this;
		}

		public Builder topK(int topK) {
			Assert.isTrue(topK >= 0, "TopK should be positive.");
			this.searchRequest.topK = topK;
			return this;
		}

		public Builder similarityThreshold(double threshold) {
			Assert.isTrue(threshold >= 0 && threshold <= 1, "Similarity threshold must be in [0,1] range.");
			this.searchRequest.similarityThreshold = threshold;
			return this;
		}

		public Builder similarityThresholdAll() {
			this.searchRequest.similarityThreshold = 0.0;
			return this;
		}

		public Builder filterExpression(@Nullable Filter.Expression expression) {
			this.searchRequest.filterExpression = expression;
			return this;
		}

		public Builder filterExpression(@Nullable String textExpression) {
			this.searchRequest.filterExpression = (textExpression != null)
					? new FilterExpressionTextParser().parse(textExpression) : null;
			return this;
		}

		public SearchRequest build() {
			return this.searchRequest;
		}

	}

	public String getQuery() {...}
	public int getTopK() {...}
	public double getSimilarityThreshold() {...}
	public Filter.Expression getFilterExpression() {...}
}
```

写入前，先把数据封装为 `Document`。它可以承载 PDF、Word 等数据源提取出的文本，以及文件名等键值形式的元数据。

写入向量库时，嵌入（Embedding）模型把文本转换为 `float[]`，也就是嵌入向量。常见的向量表示技术包括 [Word2Vec](https://en.wikipedia.org/wiki/Word2vec)、[GloVe](<https://en.wikipedia.org/wiki/GloVe_(machine_learning)>)、[BERT](<https://en.wikipedia.org/wiki/BERT_(language_model)>)，也可以使用 OpenAI 的 `text-embedding-ada-002` 等文本嵌入模型，将词、句子或段落转换成向量。

**生成向量是 [`EmbeddingModel`](/frameworks/spring-ai/models/embedding-model/) 的职责，向量数据库负责存储和检索。** Spring AI 的具体 `VectorStore` 实现会在写入和查询过程中协调这些步骤。

`similaritySearch` 根据查询文本检索相似文档，可通过以下参数控制结果：

- `k`：最多返回多少个相似文档，通常称为 Top-K 或 K 近邻（KNN）检索。
- `threshold`：范围为 `0` 到 `1` 的相似度阈值，越接近 `1` 要求越相似。例如设为 `0.75`，只保留满足该阈值要求的结果；具体分数与底层后端的计算方式有关。
- `Filter.Expression`：通过链式 DSL（领域专用语言）构建过滤条件，类似 SQL 的 `WHERE`，但过滤对象是 `Document` 的元数据键值。
- `filterExpression`：基于 ANTLR4 的字符串 DSL。例如有 `country`、`year`、`isActive` 元数据时，可使用 `country == 'UK' && year >= 2020 && isActive == true`。

| 参数                  | 默认值 | 初读重点                                                 |
| --------------------- | ------ | -------------------------------------------------------- |
| `topK`                | `4`    | 最多返回的文档数，过滤后可能更少。                       |
| `similarityThreshold` | `0.0`  | 默认不按相似度阈值排除结果；分数换算与后端距离度量有关。 |
| `filterExpression`    | 无     | 限定元数据范围，不过滤任意正文。                         |

过滤语法详见[元数据过滤](#metadata-filters)。Top-K 与阈值的实际效果可结合 [RAG 评估测试](/frameworks/spring-ai/engineering/evaluation/#_relevancy_evaluator)检查；使用 S3 时，还需留意该版本的[阈值处理与正文回填边界](/frameworks/spring-ai/rag/vector-stores/s3-vector-store/#s3-properties)。

<a id="_schema_initialization"></a>

## 二、结构初始化

部分向量存储在使用前需要初始化后端结构，默认不会自动执行。需要显式启用：通过对应构建参数传入 `boolean`，或在 Spring Boot 的 `application.properties`、`application.yml` 中将该实现的 `initialize-schema` 属性设为 `true`。

属性完整名称取决于具体向量存储，应查对应实现的配置文档。

<a id="_batching_strategy"></a>

## 三、批处理策略（按需深入）

批量写入资料时，往往需要为大量文档生成向量。把所有文档放进一次请求，可能超过嵌入模型的词元（Token）限制，导致请求报错或输入被截断。

Spring AI 用批处理策略把文档集合分成较小批次，使每批估算 Token 数处于配置的限制内，也便于控制吞吐和 API 限流。

`BatchingStrategy` 按文档的 Token 数分组，核心接口如下：

```java
public interface BatchingStrategy {
    List<List<Document>> batch(List<Document> documents);
}
```

`batch` 接收文档列表，返回多个文档批次。**批处理只给文档分组，不会把单篇长文档切成更小的文本块。**

<a id="_default_implementation"></a>

### 默认实现：TokenCountBatchingStrategy

默认实现 `TokenCountBatchingStrategy` 估算各篇文档的 Token 数，控制每批文档的总量不超过计算后的上限。

其默认参数为：

- 原始输入 Token 上限为 `8191`，参考 [OpenAI 嵌入模型的输入限制](https://platform.openai.com/docs/guides/embeddings/embedding-models)。这是策略默认值，不代表所有模型的共同上限。
- 预留 `10%` 的余量，应对估算偏差和额外开销。
- 实际上限的计算方式：`actualMaxInputTokenCount = round(originalMaxInputTokenCount * (1 - RESERVE_PERCENTAGE))`。按 2.0.2 的实现，默认预算为 `7372`。

策略会估算每篇文档的 Token 数，再进行分批；如果单篇文档已超过实际限制，会抛出异常。需要切分长文档时，使用 [TokenTextSplitter](/frameworks/spring-ai/rag/document-ingestion/#tokentextsplitter)。

可以在 Spring Boot 的 `@Configuration` 类中创建自定义 `TokenCountBatchingStrategy` Bean：

```java
@Configuration
public class EmbeddingConfig {
    @Bean
    public BatchingStrategy customTokenCountBatchingStrategy() {
        return new TokenCountBatchingStrategy(
            EncodingType.CL100K_BASE,  // Specify the encoding type
            8000,                      // Set the maximum input token count
            0.1                        // Set the reserve percentage
        );
    }
}
```

这三个参数分别表示：

- `EncodingType.CL100K_BASE`：分词编码类型，`JTokkitTokenCountEstimator` 据此估算 Token 数。若模型使用不同分词器，应检查估算是否适用。
- `8000`：原始输入 Token 上限，应按所用嵌入模型的限制设置。
- `0.1`：预留 `10%` 余量，因此本例实际预算为 `7200`。

这个构造器默认使用 `Document.DEFAULT_CONTENT_FORMATTER` 格式化文档，并以 `MetadataMode.NONE` 处理元数据；需要调整时，可使用包含这些参数的完整构造器。

以 PGvector 为例，自动配置把这个 Bean 注入向量存储；写入时再将策略传给 `EmbeddingModel.embed(...)`。这不表示所有直接的模型调用都会自动使用该策略。

`TokenCountBatchingStrategy` 内部使用 `TokenCountEstimator` 估算 Token 数，默认实现为 `JTokkitTokenCountEstimator`。也可以传入自定义估算器，以适应其他分词方式或模型需求：

```java
TokenCountEstimator customEstimator = new YourCustomTokenCountEstimator();
TokenCountBatchingStrategy strategy = new TokenCountBatchingStrategy(
		customEstimator,
    8000,  // maxInputTokenCount
    0.1,   // reservePercentage
    Document.DEFAULT_CONTENT_FORMATTER,
    MetadataMode.NONE
);
```

<a id="_working_with_auto_truncation"></a>

### 配合自动截断

部分嵌入模型支持 `auto_truncate`，例如 Vertex AI 文本嵌入模型。启用后，模型会截断超长输入并继续处理；禁用时，超限输入会报错。

如果明确接受模型截断长输入，可以把批处理策略的预算设得较高，使这类文档先通过本地 Token 预算检查，再交给模型处理。这是针对提供方行为的特殊配置，不会扩大模型的真实输入上限。

<a id="_configuration_for_auto_truncation"></a>

#### 自动截断配置示例

下面展示如何启用 Vertex AI 自动截断、定义自定义 `BatchingStrategy`，并构建 `PgVectorStore`：

```java
@Configuration
public class AutoTruncationEmbeddingConfig {

    @Bean
    public VertexAiTextEmbeddingModel vertexAiEmbeddingModel(
            VertexAiEmbeddingConnectionDetails connectionDetails) {

        VertexAiTextEmbeddingOptions options = VertexAiTextEmbeddingOptions.builder()
                .model(VertexAiTextEmbeddingOptions.DEFAULT_MODEL_NAME)
                .autoTruncate(true)  // Enable auto-truncation
                .build();

        return new VertexAiTextEmbeddingModel(connectionDetails, options);
    }

    @Bean
    public BatchingStrategy batchingStrategy() {
        // Only use a high token limit if auto-truncation is enabled in your embedding model.
        // Set a much higher token count than the model actually supports
        // (e.g., 132,900 when Vertex AI supports only up to 20,000)
        return new TokenCountBatchingStrategy(
                EncodingType.CL100K_BASE,
                132900,  // Artificially high limit
                0.1      // 10% reserve
        );
    }

    @Bean
    public VectorStore vectorStore(JdbcTemplate jdbcTemplate, EmbeddingModel embeddingModel, BatchingStrategy batchingStrategy) {
        return PgVectorStore.builder(jdbcTemplate, embeddingModel)
            .batchingStrategy(batchingStrategy)
            // other properties omitted here
            .build();
    }
}
```

手动构建时必须显式调用 `.batchingStrategy(batchingStrategy)`；仅声明同类型 Bean 不会改变构建器的默认值。上面的配置表达了：

- 为嵌入模型启用自动截断。
- 批处理策略使用较高的 `132900` Token 预算，让长文档交给模型处理；示例以模型实际限制 `20000` 作为对比。这些数值只用于说明配置思路，实际限制应查所用模型和提供方文档。
- 向量存储使用配置好的嵌入模型和自定义批处理策略。

<a id="_why_this_works"></a>

#### 为什么需要这样配置

这套配置的工作过程是：

- `TokenCountBatchingStrategy` 先检查单篇文档是否超过本地预算，超出就抛出 `IllegalArgumentException`。
- 提高预算后，可以避免预期范围内的长文档在这一步被提前拒绝；它不意味着文档长度可以无限增加。
- 文本超出模型允许的长度时，再由已启用的自动截断功能处理。单条输入、批次总量和请求数量限制仍需分别符合提供方要求，不能把自动截断理解为任意批次都不会报错。

<a id="_best_practices"></a>

#### 使用建议

对明确接受自动截断的场景，可参考以下建议：

- 将批处理预算设为模型实际 Token 上限的 `5–10` 倍，减少本地预算检查提前报错的情况。这是特定截断方案的配置建议，需要按模型的单条输入和批次限制验证，不是通用的批量设置。
- 观察模型是否产生截断警告；并非所有模型都会记录截断日志。
- 评估静默截断对向量质量的影响。
- 使用样本文档测试，确认截断后的向量仍满足检索要求。
- 将这种非常规配置及原因记录下来，方便后续维护。

> 自动截断可能丢弃长文档尾部的重要信息，使向量只表示部分内容。若需要完整覆盖文档，应先把长文档切成较小文本块，再生成向量。

<a id="_spring_boot_auto_configuration"></a>

#### Spring Boot 自动配置

使用 Spring Boot 自动配置时，通过自定义 `BatchingStrategy` Bean 覆盖 Spring AI 默认策略：

```java
@Bean
public BatchingStrategy customBatchingStrategy() {
    // This bean will override the default BatchingStrategy
    return new TokenCountBatchingStrategy(
            EncodingType.CL100K_BASE,
            132900,  // Much higher than model's actual limit
            0.1
    );
}
```

支持该自动配置的向量存储会注入自定义 Bean。手动构造向量存储时，仍需确认构建器是否应用了这个策略。

<a id="_custom_implementation"></a>

### 自定义实现

如果默认的 `TokenCountBatchingStrategy` 不能满足需求，也可以实现自己的批处理逻辑，再通过 Spring Boot 自动配置接入。

在应用中定义 `BatchingStrategy` Bean：

```java
@Configuration
public class EmbeddingConfig {
    @Bean
    public BatchingStrategy customBatchingStrategy() {
        return new CustomBatchingStrategy();
    }
}
```

支持对应自动配置的组件会使用这个自定义策略，替换默认实现。`CustomBatchingStrategy` 和前面的 `YourCustomTokenCountEstimator` 是待自行实现的示意类；这些配置示例应分别选用，避免重复注册多个策略 Bean。

> Spring AI 支持的向量存储通常默认使用 `TokenCountBatchingStrategy`；具体是否可覆盖及如何注入，以对应实现为准。

<a id="_vectorstore_implementations"></a>

## 四、实现与子页阅读顺序

各后端子页主要讲依赖、连接配置、初始化、元数据过滤和原生客户端，按实际使用选择即可。

| 阅读顺序 | 内容                                                                          | 学习目标                                                                                                                                                                                                 |
| -------- | ----------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 先读     | 本篇统一 API                                                                  | 写入、检索、过滤和删除。                                                                                                                                                                                 |
| 1        | [PGvector](/frameworks/spring-ai/rag/vector-stores/pgvector/)                 | PostgreSQL 扩展、索引、维度与 Spring Boot 接入，衔接已有示例。                                                                                                                                           |
| 2        | [Milvus](/frameworks/spring-ai/rag/vector-stores/milvus/)                     | 专用向量库、集合与分区、原生表达式、`nprobe` 调参。                                                                                                                                                      |
| 3        | [Redis](/frameworks/spring-ai/rag/vector-stores/redis/)                       | 元数据索引、向量/文本/范围检索，以及语义缓存。                                                                                                                                                           |
| 4        | [S3 Vector Store](/frameworks/spring-ai/rag/vector-stores/s3-vector-store/)   | AWS 向量桶与索引、客户端凭据、元数据过滤及当前适配边界。                                                                                                                                                 |
| 5        | [Elasticsearch（ES）](/frameworks/spring-ai/rag/vector-stores/elasticsearch/) | dense_vector 映射、距离函数、元数据过滤与 Rest5Client 接入。                                                                                                                                             |
| 按需补充 | 向量原理                                                                      | 基础见 [Embedding 模型](/frameworks/spring-ai/models/embedding-model/)与 [Redis 距离度量](/frameworks/spring-ai/rag/vector-stores/redis/#_distance_metrics)，几何推导见[附录](#_understanding_vectors)。 |

当前后端学习和翻译范围包含 PGvector、Milvus、Redis、S3 Vector Store 和 Elasticsearch（ES）。其余 16 个实现不列入学习任务；下面保留完整参考入口。

下列入口覆盖导航中的 21 个后端实现；另列 `SimpleVectorStore` 作为测试和演示工具。优先选一种后端实践，无需依次学习所有实现。

`VectorStore` 接口的实现与接入入口包括：

- [Azure Vector Search](https://docs.spring.io/spring-ai/reference/api/vectordbs/azure.html)：[Azure](https://learn.microsoft.com/en-us/azure/search/vector-search-overview) 向量存储。
- [Azure Cosmos DB](https://docs.spring.io/spring-ai/reference/api/vectordbs/azure-cosmos-db.html)：外部团队维护的 Azure Cosmos DB 集成，参见下方说明。
- [Amazon Bedrock Knowledge Base](https://docs.spring.io/spring-ai/reference/api/vectordbs/bedrock-knowledge-base.html)：基于 Amazon Bedrock Knowledge Bases 的检索接入。
- [Couchbase](https://docs.spring.io/spring-ai/reference/api/vectordbs/couchbase.html)：Couchbase 集成。
- [Apache Cassandra](https://docs.spring.io/spring-ai/reference/api/vectordbs/apache-cassandra.html)：[Apache Cassandra](https://cassandra.apache.org/doc/latest/cassandra/vector-search/overview.html) 向量存储。
- [Chroma Vector Store](https://docs.spring.io/spring-ai/reference/api/vectordbs/chroma.html)：[Chroma](https://www.trychroma.com/) 向量存储。
- [Elasticsearch Vector Store](/frameworks/spring-ai/rag/vector-stores/elasticsearch/)：[Elasticsearch](https://www.elastic.co/) 向量存储。
- [GemFire Vector Store](https://docs.spring.io/spring-ai/reference/api/vectordbs/gemfire.html)：[GemFire](https://tanzu.vmware.com/content/blog/vmware-gemfire-vector-database-extension) 向量存储。
- [MariaDB Vector Store](https://docs.spring.io/spring-ai/reference/api/vectordbs/mariadb.html)：[MariaDB](https://mariadb.com/) 向量存储。
- [Milvus Vector Store](/frameworks/spring-ai/rag/vector-stores/milvus/)：[Milvus](https://milvus.io/) 向量存储。
- [MongoDB Atlas Vector Store](https://docs.spring.io/spring-ai/reference/api/vectordbs/mongodb.html)：[MongoDB Atlas](https://www.mongodb.com/atlas/database) 向量存储。
- [Neo4j Vector Store](https://docs.spring.io/spring-ai/reference/api/vectordbs/neo4j.html)：[Neo4j](https://neo4j.com/) 向量存储。
- [OpenSearch Vector Store](https://docs.spring.io/spring-ai/reference/api/vectordbs/opensearch.html)：[OpenSearch](https://opensearch.org/platform/search/vector-database.html) 向量存储。
- [Oracle Vector Store](https://docs.spring.io/spring-ai/reference/api/vectordbs/oracle.html)：[Oracle Database](https://docs.oracle.com/en/database/oracle/oracle-database/23/vecse/overview-ai-vector-search.html) 向量存储。
- [PgVector Store](/frameworks/spring-ai/rag/vector-stores/pgvector/)：[PostgreSQL/PGVector](https://github.com/pgvector/pgvector) 向量存储。
- [Pinecone Vector Store](https://docs.spring.io/spring-ai/reference/api/vectordbs/pinecone.html)：[Pinecone](https://www.pinecone.io/) 向量存储。
- [Qdrant Vector Store](https://docs.spring.io/spring-ai/reference/api/vectordbs/qdrant.html)：[Qdrant](https://www.qdrant.tech/) 向量存储。
- [Redis Vector Store](/frameworks/spring-ai/rag/vector-stores/redis/)：[Redis](https://redis.io/) 向量存储。
- [Typesense Vector Store](https://docs.spring.io/spring-ai/reference/api/vectordbs/typesense.html)：[Typesense](https://typesense.org/docs/0.24.0/api/vector-search.html) 向量存储。
- [Weaviate Vector Store](https://docs.spring.io/spring-ai/reference/api/vectordbs/weaviate.html)：[Weaviate](https://weaviate.io/) 向量存储。
- [S3 Vector Store](/frameworks/spring-ai/rag/vector-stores/s3-vector-store/)：[AWS S3](https://aws.amazon.com/s3/features/vectors/) 向量存储。
- [SimpleVectorStore](https://github.com/spring-projects/spring-ai/blob/v2.0.2/spring-ai-vector-store/src/main/java/org/springframework/ai/vectorstore/SimpleVectorStore.java)：简单的向量存储实现，仅适合测试。

> Azure Cosmos DB 的向量存储支持由 Azure Cosmos DB 团队维护的外部模块提供，详见 [azurecosmosdb.github.io/spring-ai/docs/index.html](https://azurecosmosdb.github.io/spring-ai/docs/index.html)。

> `SimpleVectorStore` 不面向生产环境，只用于测试和演示。

后续版本可能增加更多实现。如果需要接入尚未支持的向量数据库，可以在 GitHub 提交 issue，或提交包含实现的 pull request。

各实现的接入细节见对应子章节。

<a id="_example_usage"></a>

## 五、基本读写（重点掌握）

向量入库前，需要配置合适的 Embedding 模型。文档向量与查询向量必须处于兼容的向量空间；Embedding 模型不必与生成回答的模型来自同一提供方。

例如，使用 OpenAI 的 ChatGPT 生成回答时，可以用 `OpenAiEmbeddingModel` 和 `text-embedding-ada-002` 生成向量。这里的模型名沿用原示例，实际接入时应选择提供方当前支持的模型。

OpenAI 的 Spring Boot starter 会自动配置 `EmbeddingModel`，供应用通过依赖注入使用。模型职责与向量空间要求见 [Embedding 模型](/frameworks/spring-ai/models/embedding-model/)。

<a id="_writing_to_a_vector_store"></a>

### 写入向量存储

文档入库通常放在批量导入任务中：先读取资料并生成 Spring AI 的 `Document`，再调用 `VectorStore.add()`。

下面通过 `JsonReader` 从 JSON 文件读取指定字段并生成文档，再交给向量存储实现调用 Embedding 模型，保存文档与向量。`sourceFile` 是源文件路径。若文档过长，还需要显式进行文本切分；读取字段不等于已经按 Token 限制分块。读取与切分见 [ETL 管道](/frameworks/spring-ai/rag/document-ingestion/)。

```java
@Autowired
VectorStore vectorStore;

void load(String sourceFile) {
    JsonReader jsonReader = new JsonReader(new FileSystemResource(sourceFile),
            "price", "name", "shortDescription", "description", "tags");
    List<Document> documents = jsonReader.get();
    this.vectorStore.add(documents);
}
```

<a id="_reading_from_a_vector_store"></a>

### 查询向量存储

用户提问时，先执行相似度检索，找出相关文档，再把文档内容补充到提示词中，作为模型回答问题的上下文。

只需要查询时，可以使用 `VectorStore`，也可以依赖职责更明确的 `VectorStoreRetriever`：

```java
@Autowired
VectorStoreRetriever retriever; // Could also use VectorStore here

String question = "<question from user>";
List<Document> similarDocuments = retriever.similaritySearch(question);

// Or with more specific search parameters
SearchRequest request = SearchRequest.builder()
    .query(question)
    .topK(5)                       // Return top 5 results
    .similarityThreshold(0.7)      // Only return results with similarity score >= 0.7
    .build();

List<Document> filteredDocuments = retriever.similaritySearch(request);
```

通过 `SearchRequest` 为 `similaritySearch()` 指定返回数量和相似度阈值。上例最多返回 5 个结果，并要求相似度达到 `0.7`。

<a id="_separation_of_read_and_write_operations"></a>

### 分离读写职责

分别依赖两个接口，可以明确哪些组件需要写入能力，哪些组件只负责检索：

```java
// Write operations in a service that needs full access
@Service
class DocumentIndexer {
    private final VectorStore vectorStore;

    DocumentIndexer(VectorStore vectorStore) {
        this.vectorStore = vectorStore;
    }

    public void indexDocuments(List<Document> documents) {
        vectorStore.add(documents);
    }
}

// Read-only operations in a service that only needs retrieval
@Service
class DocumentRetriever {
    private final VectorStoreRetriever retriever;

    DocumentRetriever(VectorStoreRetriever retriever) {
        this.retriever = retriever;
    }

    public List<Document> findSimilar(String query) {
        return retriever.similaritySearch(query);
    }
}
```

这种职责划分把修改数据的方法限制在确实需要它的组件中，有助于维护应用。这里限制的是 Java 接口暴露的能力；数据库权限与数据隔离仍需单独配置。

<a id="_retrieval_operations_with_vectorstoreretriever"></a>

## 六、只读检索与 RAG

`VectorStoreRetriever` 提供向量存储的只读视图，只暴露相似度检索功能。RAG 的在线问答链路通常只需要读取资料，可以依赖这一接口，避免耦合写入和删除方法。

<a id="_benefits_of_using_vectorstoreretriever"></a>

### 为什么使用只读接口

- **职责分离**：明确区分读取与写入。

- **接口隔离**：只负责检索的调用方无需接触数据修改方法。

- **函数式接口**：简单场景下可用 Lambda 表达式或方法引用实现。

- **减少依赖**：只做查询的组件无需依赖完整的 `VectorStore`。

<a id="_example_usage_2"></a>

### 只读检索示例

只做相似度检索时，直接注入 `VectorStoreRetriever`：

```java
@Service
public class DocumentRetrievalService {

    private final VectorStoreRetriever retriever;

    public DocumentRetrievalService(VectorStoreRetriever retriever) {
        this.retriever = retriever;
    }

    public List<Document> findSimilarDocuments(String query) {
        return retriever.similaritySearch(query);
    }

    public List<Document> findSimilarDocumentsWithFilters(String query, String country) {
        SearchRequest request = SearchRequest.builder()
            .query(query)
            .topK(5)
            .filterExpression(new FilterExpressionBuilder().eq("country", country).build())
            .build();

        return retriever.similaritySearch(request);
    }
}
```

这个服务只依赖 `VectorStoreRetriever`，因此从接口上就能看出它只检索文档，不修改向量存储。对于变量值，示例使用 `FilterExpressionBuilder`，避免手动拼接引号和表达式。

<a id="_integration_with_rag_applications"></a>

### 集成到 RAG 应用

在 RAG 应用中，用检索器找出相关文档，再将文档文本作为上下文交给聊天模型：

```java
@Service
public class RagService {

    private final VectorStoreRetriever retriever;
    private final ChatModel chatModel;

    public RagService(VectorStoreRetriever retriever, ChatModel chatModel) {
        this.retriever = retriever;
        this.chatModel = chatModel;
    }

    public String generateResponse(String userQuery) {
        // Retrieve relevant documents
        List<Document> relevantDocs = retriever.similaritySearch(userQuery);

        // Extract content from documents to use as context
        String context = relevantDocs.stream()
            .map(Document::getText)
            .filter(org.springframework.util.StringUtils::hasText)
            .collect(Collectors.joining("\n\n"));

        // Generate response using the retrieved context
        String prompt = "Context information:\n" + context + "\n\nUser query: " + userQuery;
        return chatModel.call(prompt);
    }
}
```

这是检索与生成分离的简化示例，没有实现空资料拒答、引用和完整提示词约束。需要接入 Advisor 时，见 [RAG 的检索与生成](/frameworks/spring-ai/rag/retrieval-and-generation/)。

<a id="metadata-filters"></a>

## 七、元数据过滤（重点掌握）

除了向量相似度，还可以按 `Document` 的元数据限定检索范围。以下两种写法最终都生成过滤表达式。

<a id="_filter_string"></a>

### 字符串表达式

通过 `SearchRequest.Builder.filterExpression(String)` 传入类似 SQL 条件的字符串，再交给 `similaritySearch()`。

例如：

- `"country == 'BG'"`

- `"genre == 'drama' && year >= 2020"`

- `"genre in ['comedy', 'documentary', 'drama']"`

<a id="_filter_expression"></a>

### Filter.Expression

`FilterExpressionBuilder` 提供链式 API，用于构建 `Filter.Expression`：

```java
FilterExpressionBuilder b = new FilterExpressionBuilder();
Filter.Expression expression = b.eq("country", "BG").build();
```

比较与数值符号包括（`+`、`-` 用于数值符号，不表示可以在元数据过滤中任意执行算术计算）：

```text
EQUALS: '=='
MINUS : '-'
PLUS: '+'
GT: '>'
GE: '>='
LT: '<'
LE: '<='
NE: '!='
```

使用以下逻辑运算符组合表达式：

```text
AND: 'AND' | 'and' | '&&';
OR: 'OR' | 'or' | '||';
```

例如，选择类型为 `drama` 且年份不早于 2020 的文档：

```java
Filter.Expression exp = b.and(b.eq("genre", "drama"), b.gte("year", 2020)).build();
```

还支持以下运算符：

```text
IN: 'IN' | 'in';
NIN: 'NIN' | 'nin';
NOT: 'NOT' | 'not';
```

例如：

```java
Filter.Expression exp = b.and(b.in("genre", "drama", "documentary"), b.not(b.lt("year", 2020))).build();
```

还支持以下运算符：

```text
IS: 'IS' | 'is';
NULL: 'NULL' | 'null';
NOT NULL: 'NOT NULL' | 'not null';
```

例如：

```java
Filter.Expression missingYear = b.isNull("year").build();
Filter.Expression presentYear = b.isNotNull("year").build();
```

> 并非所有向量存储都支持 `IS NULL` 和 `IS NOT NULL`，使用前应核对对应实现。

<a id="_partitioning_a_shared_index"></a>

### 在共享索引中划分文档组

一个向量索引可能同时存放多个客户、项目或知识库的资料。`VectorStore` 面向整个索引执行操作；需要通过过滤条件限定本次搜索或删除所属的文档组。

写入时，为每个文档添加分组元数据；查询和删除时，使用匹配的过滤条件：

```java
// When writing, record the group the document belongs to.
Document document = new Document(content, Map.of("group", groupId));
vectorStore.add(List.of(document));

// When searching, select documents from that group.
List<Document> results = vectorStore.similaritySearch(SearchRequest.builder()
    .query(query)
    .filterExpression(new FilterExpressionBuilder().eq("group", groupId).build())
    .build());

// When deleting by filter, target the same group.
Filter.Expression scoped = new FilterExpressionBuilder().eq("group", groupId).build();
vectorStore.delete(scoped);
```

保持分组清晰，需要同时做到：

- 每个文档写入时都带上分组标识，确保后续有字段可供过滤。

- 查询和删除都一致地添加分组过滤，避免操作落到其他组。

分组标识应来自应用确认的调用方身份；客户端传来的任意 `groupId` 不能直接作为授权依据。按 ID 删除不会自动继承此前查询的过滤条件，也需要确认 ID 归属。

<a id="_deleting_documents_from_vector_store"></a>

## 八、删除与文档版本管理（参考）

`VectorStore` 提供按文档 ID 和按元数据过滤条件删除的方法。

<a id="_delete_by_document_ids"></a>

### 按文档 ID 删除

已知文档 ID 时，直接传入 ID 列表：

```java
void delete(List<String> idList);
```

该方法删除 ID 与列表匹配的文档。不存在的 ID 通常会被忽略，但具体返回与错误行为以所用后端为准。

使用示例：

```java
// Create and add document
Document document = new Document("The World is Big",
    Map.of("country", "Netherlands"));
vectorStore.add(List.of(document));

// Delete document by ID
vectorStore.delete(List.of(document.getId()));
```

<a id="_delete_by_filter_expression"></a>

### 按 Filter.Expression 删除

需要按多个条件删除时，使用过滤表达式：

```java
void delete(Filter.Expression filterExpression);
```

`Filter.Expression` 定义待删除文档的条件，适合按元数据属性批量删除。

使用示例：

```java
// Create test documents with different metadata
Document bgDocument = new Document("The World is Big",
    Map.of("country", "Bulgaria"));
Document nlDocument = new Document("The World is Big",
    Map.of("country", "Netherlands"));

// Add documents to the store
vectorStore.add(List.of(bgDocument, nlDocument));

// Delete documents from Bulgaria using filter expression
Filter.Expression filterExpression = new Filter.Expression(
    Filter.ExpressionType.EQ,
    new Filter.Key("country"),
    new Filter.Value("Bulgaria")
);
vectorStore.delete(filterExpression);

// Verify deletion with search
SearchRequest request = SearchRequest.builder()
    .query("World")
    .filterExpression("country == 'Bulgaria'")
    .build();
List<Document> results = vectorStore.similaritySearch(request);
// results will be empty as Bulgarian document was deleted
```

<a id="_delete_by_string_filter_expression"></a>

### 按字符串表达式删除

也可以直接传入字符串过滤条件：

```java
void delete(String filterExpression);
```

该方法会在内部将字符串转换为 `Filter.Expression`，适合过滤条件本身就是字符串的场景。下面的查询仅用于独立测试数据中的示意；相似度检索返回空列表，不能单独证明整个索引已完成删除。

使用示例：

```java
// Create and add documents
Document bgDocument = new Document("The World is Big",
    Map.of("country", "Bulgaria"));
Document nlDocument = new Document("The World is Big",
    Map.of("country", "Netherlands"));
vectorStore.add(List.of(bgDocument, nlDocument));

// Delete Bulgarian documents using string filter
vectorStore.delete("country == 'Bulgaria'");

// Verify remaining documents
SearchRequest request = SearchRequest.builder()
    .query("World")
    .topK(5)
    .build();
List<Document> results = vectorStore.similaritySearch(request);
// results will only contain the Netherlands document
```

<a id="_error_handling_when_calling_the_delete_api"></a>

### 处理删除异常

删除方法遇到错误时可能抛出异常。

可使用 `try-catch` 捕获并处理删除失败。解析失败、连接问题或后端执行错误都可能导致异常，不应仅归因为过滤表达式错误：

使用示例：

```java
try {
    vectorStore.delete("country == 'Bulgaria'");
}
catch (Exception  e) {
    logger.error("Failed to delete documents from vector store", e);
}
```

<a id="_document_versioning_use_case"></a>

### 文档版本管理

更新文档时，可以通过业务文档标识与版本元数据定位旧数据，再写入新版本。下面保留先删后写的基础流程；两步不是原子操作，写入失败时可能出现资料缺口。需要可靠更新时，应另行设计版本切换或后端事务流程。

使用示例：

```java
// Create initial document (v1) with version metadata
Document documentV1 = new Document(
    "AI and Machine Learning Best Practices",
    Map.of(
        "docId", "AIML-001",
        "version", "1.0",
        "lastUpdated", "2024-01-01"
    )
);

// Add v1 to the vector store
vectorStore.add(List.of(documentV1));

// Create updated version (v2) of the same document
Document documentV2 = new Document(
    "AI and Machine Learning Best Practices - Updated",
    Map.of(
        "docId", "AIML-001",
        "version", "2.0",
        "lastUpdated", "2024-02-01"
    )
);

// First, delete the old version using filter expression
Filter.Expression deleteOldVersion = new Filter.Expression(
    Filter.ExpressionType.AND,
    new Filter.Expression(
        Filter.ExpressionType.EQ,
        new Filter.Key("docId"),
        new Filter.Value("AIML-001")
    ),
    new Filter.Expression(
        Filter.ExpressionType.EQ,
        new Filter.Key("version"),
        new Filter.Value("1.0")
    )
);
vectorStore.delete(deleteOldVersion);

// Add the new version
vectorStore.add(List.of(documentV2));

// Verify only v2 exists
SearchRequest request = SearchRequest.builder()
    .query("AI and Machine Learning")
    .filterExpression("docId == 'AIML-001'")
    .build();
List<Document> results = vectorStore.similaritySearch(request);
// results will contain only v2 of the document
```

同样的操作也可以用字符串表达式完成：

使用示例：

```java
// Delete old version using string filter
vectorStore.delete("docId == 'AIML-001' AND version == '1.0'");

// Add new version
vectorStore.add(List.of(documentV2));
```

<a id="_performance_considerations_while_deleting_documents"></a>

### 删除操作的性能取舍

- 已知具体文档 ID 时，按 ID 列表删除通常更直接、速度更快。

- 按过滤条件删除可能需要扫描索引以找到匹配文档，具体代价取决于向量存储的实现。

- 大量删除应分批执行，避免一次操作给系统造成过大压力。

- 按文档属性清理数据时，可直接使用过滤表达式，无需先搜集全部 ID。

<a id="_understanding_vectors"></a>

## 九、理解向量

基础概念先看 [AI 核心概念：Embedding](/frameworks/spring-ai/concepts/#embedding内容的向量表示)，模型 API 与维度、向量空间要求见 [Embedding 模型](/frameworks/spring-ai/models/embedding-model/)。度量及分数换算可对照 [Redis 距离度量](/frameworks/spring-ai/rag/vector-stores/redis/#_distance_metrics)；这些工程说明不包含完整数学推导，需要向量几何和距离推导时，再查 [Understanding Vectors](https://docs.spring.io/spring-ai/reference/api/vectordbs/understand-vectordbs.html)。

---

来源：[Vector Databases](https://docs.spring.io/spring-ai/reference/api/vectordbs.html)，按 Spring AI 2.0.2 API 整理。提供方配置、完整参数及向量几何推导保留对应原文入口。
