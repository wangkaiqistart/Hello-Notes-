# 向量数据库

向量数据库用于保存向量并进行相似度检索，是 AI 应用中常见的数据组件。

与关系型数据库常见的精确匹配查询不同，向量检索查找的是与查询向量相似的向量。相似度的计算方式见[向量相似度](https://docs.spring.io/spring-ai/reference/api/vectordbs/understand-vectordbs.html#vectordbs-similarity)。

向量数据库可以把自有资料接入 AI 应用：先将资料写入向量库；用户提问时，先检索相关文档，再把文档作为上下文，与问题一起交给模型。这就是[检索增强生成（RAG）](https://docs.spring.io/spring-ai/reference/concepts.html#concept-rag)。

下面介绍 Spring AI 统一的向量存储接口、不同后端的实现和基本用法。末尾的向量原理入口进一步解释相似度检索。

<a id="api-overview"></a>

## API 概览

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

因此，`VectorStore` 同时支持添加、删除和相似度检索。

<a id="_searchrequest_builder"></a>

### SearchRequest：构建检索请求

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

写入向量库时，嵌入模型把文本转换为 `float[]`，也就是嵌入向量。常见的向量表示技术包括 [Word2Vec](https://en.wikipedia.org/wiki/Word2vec)、[GloVe](https://en.wikipedia.org/wiki/GloVe_(machine_learning))、[BERT](https://en.wikipedia.org/wiki/BERT_(language_model))，也可以使用 OpenAI 的 `text-embedding-ada-002` 等文本嵌入模型，将词、句子或段落转换成向量。

**生成向量是 `EmbeddingModel` 的职责，向量数据库负责存储和检索。** Spring AI 的具体 `VectorStore` 实现会在写入和查询过程中协调这些步骤。

`similaritySearch` 根据查询文本检索相似文档，可通过以下参数控制结果：

- `k`：最多返回多少个相似文档，通常称为 Top-K 或 K 近邻（KNN）检索。
- `threshold`：范围为 `0` 到 `1` 的相似度阈值，越接近 `1` 要求越相似。例如设为 `0.75`，只保留满足该阈值要求的结果；具体分数与底层后端的计算方式有关。
- `Filter.Expression`：通过链式 DSL（领域专用语言）构建过滤条件，类似 SQL 的 `WHERE`，但过滤对象是 `Document` 的元数据键值。
- `filterExpression`：基于 ANTLR4 的字符串 DSL。例如有 `country`、`year`、`isActive` 元数据时，可使用 `country == 'UK' && year >= 2020 && isActive == true`。

过滤语法详见[元数据过滤](https://docs.spring.io/spring-ai/reference/api/vectordbs.html#metadata-filters)。

<a id="_schema_initialization"></a>

## 结构初始化

部分向量存储在使用前需要初始化后端结构，默认不会自动执行。需要显式启用：通过对应构造参数传入 `boolean`，或在 Spring Boot 的 `application.properties`、`application.yml` 中将该实现的 `initialize-schema` 属性设为 `true`。

属性完整名称取决于具体向量存储，应查对应实现的配置文档。

<a id="_batching_strategy"></a>

## 批处理策略

批量写入资料时，往往需要为大量文档生成向量。把所有文档放进一次请求，可能超过嵌入模型的 Token 限制，导致请求报错或输入被截断。

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
- 实际上限的计算方式：`actualMaxInputTokenCount = originalMaxInputTokenCount * (1 - RESERVE_PERCENTAGE)`。

策略会估算每篇文档的 Token 数，再进行分批；如果单篇文档已超过实际限制，会抛出异常。

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

支持对应自动配置的组件会注入这个 Bean，替换默认批处理策略。

`TokenCountBatchingStrategy` 内部使用 `TokenCountEstimator` 估算 Token 数，默认实现为 `JTokkitTokenCountEstimator`。也可以传入自定义估算器，以适应其他分词方式或模型需求：

```java
TokenCountEstimator customEstimator = new YourCustomTokenCountEstimator();
TokenCountBatchingStrategy strategy = new TokenCountBatchingStrategy(
		this.customEstimator,
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
            // other properties omitted here
            .build();
    }
}
```

这段配置意在表达：

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

原文对接受自动截断的场景给出以下建议：

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

支持对应配置的组件会使用这个自定义策略，替换默认实现。

> Spring AI 支持的向量存储通常默认使用 `TokenCountBatchingStrategy`；具体是否可覆盖及如何注入，以对应实现为准。

<a id="_vectorstore_implementations"></a>

## VectorStore 实现

`VectorStore` 接口的实现包括：

- [Azure Vector Search](https://docs.spring.io/spring-ai/reference/api/vectordbs/azure.html)：[Azure](https://learn.microsoft.com/en-us/azure/search/vector-search-overview) 向量存储。
- [Apache Cassandra](https://docs.spring.io/spring-ai/reference/api/vectordbs/apache-cassandra.html)：[Apache Cassandra](https://cassandra.apache.org/doc/latest/cassandra/vector-search/overview.html) 向量存储。
- [Chroma Vector Store](https://docs.spring.io/spring-ai/reference/api/vectordbs/chroma.html)：[Chroma](https://www.trychroma.com/) 向量存储。
- [Elasticsearch Vector Store](https://docs.spring.io/spring-ai/reference/api/vectordbs/elasticsearch.html)：[Elasticsearch](https://www.elastic.co/) 向量存储。
- [GemFire Vector Store](https://docs.spring.io/spring-ai/reference/api/vectordbs/gemfire.html)：[GemFire](https://tanzu.vmware.com/content/blog/vmware-gemfire-vector-database-extension) 向量存储。
- [MariaDB Vector Store](https://docs.spring.io/spring-ai/reference/api/vectordbs/mariadb.html)：[MariaDB](https://mariadb.com/) 向量存储。
- [Milvus Vector Store](https://docs.spring.io/spring-ai/reference/api/vectordbs/milvus.html)：[Milvus](https://milvus.io/) 向量存储。
- [MongoDB Atlas Vector Store](https://docs.spring.io/spring-ai/reference/api/vectordbs/mongodb.html)：[MongoDB Atlas](https://www.mongodb.com/atlas/database) 向量存储。
- [Neo4j Vector Store](https://docs.spring.io/spring-ai/reference/api/vectordbs/neo4j.html)：[Neo4j](https://neo4j.com/) 向量存储。
- [OpenSearch Vector Store](https://docs.spring.io/spring-ai/reference/api/vectordbs/opensearch.html)：[OpenSearch](https://opensearch.org/platform/search/vector-database.html) 向量存储。
- [Oracle Vector Store](https://docs.spring.io/spring-ai/reference/api/vectordbs/oracle.html)：[Oracle Database](https://docs.oracle.com/en/database/oracle/oracle-database/23/vecse/overview-ai-vector-search.html) 向量存储。
- [PgVector Store](https://docs.spring.io/spring-ai/reference/api/vectordbs/pgvector.html)：[PostgreSQL/PGVector](https://github.com/pgvector/pgvector) 向量存储。
- [Pinecone Vector Store](https://docs.spring.io/spring-ai/reference/api/vectordbs/pinecone.html)：[Pinecone](https://www.pinecone.io/) 向量存储。
- [Qdrant Vector Store](https://docs.spring.io/spring-ai/reference/api/vectordbs/qdrant.html)：[Qdrant](https://www.qdrant.tech/) 向量存储。
- [Redis Vector Store](https://docs.spring.io/spring-ai/reference/api/vectordbs/redis.html)：[Redis](https://redis.io/) 向量存储。
- [Typesense Vector Store](https://docs.spring.io/spring-ai/reference/api/vectordbs/typesense.html)：[Typesense](https://typesense.org/docs/0.24.0/api/vector-search.html) 向量存储。
- [Weaviate Vector Store](https://docs.spring.io/spring-ai/reference/api/vectordbs/weaviate.html)：[Weaviate](https://weaviate.io/) 向量存储。
- [S3 Vector Store](https://docs.spring.io/spring-ai/reference/api/vectordbs/s3-vector-store.html)：[AWS S3](https://aws.amazon.com/s3/features/vectors/) 向量存储。
- [SimpleVectorStore](https://github.com/spring-projects/spring-ai/blob/main/spring-ai-vector-store/src/main/java/org/springframework/ai/vectorstore/SimpleVectorStore.java)：简单的向量存储实现，仅适合测试。

> Azure Cosmos DB 的向量存储支持由 Azure Cosmos DB 团队维护的外部模块提供，详见 [azurecosmosdb.github.io/spring-ai/docs/index.html](https://azurecosmosdb.github.io/spring-ai/docs/index.html)。

> `SimpleVectorStore` 不面向生产环境，只用于测试和演示。

后续版本可能增加更多实现。如果需要接入尚未支持的向量数据库，可以在 GitHub 提交 issue，或提交包含实现的 pull request。

各实现的接入细节见对应子章节。

<a id="_example_usage"></a>
