# Vector Databases

A vector database is a specialized type of database that plays an essential role in AI applications.

In vector databases, queries differ from traditional relational databases. Instead of exact matches, they perform similarity searches. When given a vector as a query, a vector database returns vectors that are “similar” to the query vector. Further details on how this similarity is calculated at a high-level is provided in a [Vector Similarity](https://docs.spring.io/spring-ai/reference/api/vectordbs/understand-vectordbs.html#vectordbs-similarity).

Vector databases are used to integrate your data with AI models. The first step in their usage is to load your data into a vector database. Then, when a user query is to be sent to the AI model, a set of similar documents is first retrieved. These documents then serve as the context for the user’s question and are sent to the AI model, along with the user’s query. This technique is known as [Retrieval Augmented Generation (RAG)](https://docs.spring.io/spring-ai/reference/concepts.html#concept-rag).

The following sections describe the Spring AI interface for using multiple vector database implementations and some high-level sample usage.

The last section is intended to demystify the underlying approach of similarity searching in vector databases.

<a id="api-overview"></a>

## API Overview

This section serves as a guide to the `VectorStore` interface and its associated classes within the Spring AI framework.

Spring AI offers an abstracted API for interacting with vector databases through the `VectorStore` interface and its read-only counterpart, the `VectorStoreRetriever` interface.

<a id="_vectorstoreretriever_interface"></a>

### VectorStoreRetriever Interface

Spring AI provides a read-only interface called `VectorStoreRetriever` that exposes only the document retrieval functionality:

```java
@FunctionalInterface
public interface VectorStoreRetriever {

    List<Document> similaritySearch(SearchRequest request);

    default List<Document> similaritySearch(String query) {
        return this.similaritySearch(SearchRequest.builder().query(query).build());
    }
}
```

This functional interface is designed for use cases where you only need to retrieve documents from a vector store without performing any mutation operations. It follows the principle of least privilege by exposing only the necessary functionality for document retrieval.

<a id="_vectorstore_interface"></a>

### VectorStore Interface

The `VectorStore` interface extends `VectorStoreRetriever` and adds mutation capabilities:

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

The `VectorStore` interface combines both read and write operations, allowing you to add, delete, and search for documents in a vector database.

<a id="_searchrequest_builder"></a>

### SearchRequest Builder

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

To insert data into the vector database, encapsulate it within a `Document` object. The `Document` class encapsulates content from a data source, such as a PDF or Word document, and includes text represented as a string. It also contains metadata in the form of key-value pairs, including details such as the filename.

Upon insertion into the vector database, the text content is transformed into a numerical array, or a `float[]`, known as vector embeddings, using an embedding model. Embedding models, such as [Word2Vec](https://en.wikipedia.org/wiki/Word2vec), [GLoVE](https://en.wikipedia.org/wiki/GloVe_(machine_learning)), and [BERT](https://en.wikipedia.org/wiki/BERT_(language_model)), or OpenAI’s `text-embedding-ada-002`, are used to convert words, sentences, or paragraphs into these vector embeddings.

The vector database’s role is to store and facilitate similarity searches for these embeddings. It does not generate the embeddings itself. For creating vector embeddings, the `EmbeddingModel` should be utilized.

The `similaritySearch` methods in the interface allow for retrieving documents similar to a given query string. These methods can be fine-tuned by using the following parameters:

- `k`: An integer that specifies the maximum number of similar documents to return. This is often referred to as a 'top K' search, or 'K nearest neighbors' (KNN).
 
- `threshold`: A double value ranging from 0 to 1, where values closer to 1 indicate higher similarity. By default, if you set a threshold of 0.75, for instance, only documents with a similarity above this value are returned.
 
- `Filter.Expression`: A class used for passing a fluent DSL (Domain-Specific Language) expression that functions similarly to a 'where' clause in SQL, but it applies exclusively to the metadata key-value pairs of a `Document`.
 
- `filterExpression`: An external DSL based on ANTLR4 that accepts filter expressions as strings. For example, with metadata keys like country, year, and `isActive`, you could use an expression such as: `country == 'UK' && year >= 2020 && isActive == true.`
    

Find more information on the `Filter.Expression` in the [Metadata Filters](https://docs.spring.io/spring-ai/reference/api/vectordbs.html#metadata-filters) section.

<a id="_schema_initialization"></a>

## Schema Initialization

Some vector stores require their backend schema to be initialized before usage. It will not be initialized for you by default. You must opt-in, by passing a `boolean` for the appropriate constructor argument or, if using Spring Boot, setting the appropriate `initialize-schema` property to `true` in `application.properties` or `application.yml`. Check the documentation for the vector store you are using for the specific property name.

<a id="_batching_strategy"></a>

## Batching Strategy

When working with vector stores, it’s often necessary to embed large numbers of documents. While it might seem straightforward to make a single call to embed all documents at once, this approach can lead to issues. Embedding models process text as tokens and have a maximum token limit, often referred to as the context window size. This limit restricts the amount of text that can be processed in a single embedding request. Attempting to embed too many tokens in one call can result in errors or truncated embeddings.

To address this token limit, Spring AI implements a batching strategy. This approach breaks down large sets of documents into smaller batches that fit within the embedding model’s maximum context window. Batching not only solves the token limit issue but can also lead to improved performance and more efficient use of API rate limits.

Spring AI provides this functionality through the `BatchingStrategy` interface, which allows for processing documents in sub-batches based on their token counts.

The core `BatchingStrategy` interface is defined as follows:

```java
public interface BatchingStrategy {
    List<List<Document>> batch(List<Document> documents);
}
```

This interface defines a single method, `batch`, which takes a list of documents and returns a list of document batches.

<a id="_default_implementation"></a>

### Default Implementation

Spring AI provides a default implementation called `TokenCountBatchingStrategy`. This strategy batches documents based on their token counts, ensuring that each batch does not exceed a calculated maximum input token count.

Key features of `TokenCountBatchingStrategy`:

- Uses [OpenAI’s max input token count](https://platform.openai.com/docs/guides/embeddings/embedding-models) (8191) as the default upper limit.
 
- Incorporates a reserve percentage (default 10%) to provide a buffer for potential overhead.
 
- Calculates the actual max input token count as: `actualMaxInputTokenCount = originalMaxInputTokenCount * (1 - RESERVE_PERCENTAGE)`
    

The strategy estimates the token count for each document, groups them into batches without exceeding the max input token count, and throws an exception if a single document exceeds this limit.

You can also customize the `TokenCountBatchingStrategy` to better suit your specific requirements. This can be done by creating a new instance with custom parameters in a Spring Boot `@Configuration` class.

Here’s an example of how to create a custom `TokenCountBatchingStrategy` bean:

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

In this configuration:

- `EncodingType.CL100K_BASE`: Specifies the encoding type used for tokenization. This encoding type is used by the `JTokkitTokenCountEstimator` to accurately estimate token counts.
 
- `8000`: Sets the maximum input token count. This value should be less than or equal to the maximum context window size of your embedding model.
 
- `0.1`: Sets the reserve percentage. The percentage of tokens to reserve from the max input token count. This creates a buffer for potential token count increases during processing.
    

By default, this constructor uses `Document.DEFAULT_CONTENT_FORMATTER` for content formatting and `MetadataMode.NONE` for metadata handling. If you need to customize these parameters, you can use the full constructor with additional parameters.

Once defined, this custom `TokenCountBatchingStrategy` bean will be automatically used by the `EmbeddingModel` implementations in your application, replacing the default strategy.

The `TokenCountBatchingStrategy` internally uses a `TokenCountEstimator` (specifically, `JTokkitTokenCountEstimator`) to calculate token counts for efficient batching. This ensures accurate token estimation based on the specified encoding type.

Additionally, `TokenCountBatchingStrategy` provides flexibility by allowing you to pass in your own implementation of the `TokenCountEstimator` interface. This feature enables you to use custom token counting strategies tailored to your specific needs. For example:

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

### Working with Auto-Truncation

Some embedding models, such as Vertex AI text embedding, support an `auto_truncate` feature. When enabled, the model silently truncates text inputs that exceed the maximum size and continues processing; when disabled, it throws an explicit error for inputs that are too large.

When using auto-truncation with the batching strategy, you must configure your batching strategy with a much higher input token count than the model’s actual maximum. This prevents the batching strategy from raising exceptions for large documents, allowing the embedding model to handle truncation internally.

<a id="_configuration_for_auto_truncation"></a>

#### Configuration for Auto-Truncation

When enabling auto-truncation, set your batching strategy’s maximum input token count much higher than the model’s actual limit. This prevents the batching strategy from raising exceptions for large documents, allowing the embedding model to handle truncation internally.

Here’s an example configuration for using Vertex AI with auto-truncation and custom `BatchingStrategy` and then using them in the PgVectorStore:

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

In this configuration:

- The embedding model has auto-truncation enabled, allowing it to handle oversized inputs gracefully.
 
- The batching strategy uses an artificially high token limit (132,900) that’s much larger than the actual model limit (20,000).
 
- The vector store uses the configured embedding model and the custom `BatchingStrategy` bean.
     

<a id="_why_this_works"></a>

#### Why This Works

This approach works because:

- The `TokenCountBatchingStrategy` checks if any single document exceeds the configured maximum and throws an `IllegalArgumentException` if it does.
 
- By setting a very high limit in the batching strategy, we ensure that this check never fails.
 
- Documents or batches exceeding the model’s limit are silently truncated and processed by the embedding model’s auto-truncation feature.
     

<a id="_best_practices"></a>

#### Best Practices

When using auto-truncation:

- Set the batching strategy’s max input token count to be at least 5-10x larger than the model’s actual limit to avoid premature exceptions from the batching strategy.
 
- Monitor your logs for truncation warnings from the embedding model (note: not all models log truncation events).
 
- Consider the implications of silent truncation on your embedding quality.
 
- Test with sample documents to ensure truncated embeddings still meet your requirements.
 
- Document this configuration for future maintainers, as it is non-standard.
    

> While auto-truncation prevents errors, it can result in incomplete embeddings. Important information at the end of long documents may be lost. If your application requires all content to be embedded, split documents into smaller chunks before embedding.

<a id="_spring_boot_auto_configuration"></a>

#### Spring Boot Auto-Configuration

If you’re using Spring Boot auto-configuration, you must provide a custom `BatchingStrategy` bean to override the default one that comes with Spring AI:

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

The presence of this bean in your application context will automatically replace the default batching strategy used by all vector stores.

<a id="_custom_implementation"></a>

### Custom Implementation

While `TokenCountBatchingStrategy` provides a robust default implementation, you can customize the batching strategy to fit your specific needs. This can be done through Spring Boot’s auto-configuration.

To customize the batching strategy, define a `BatchingStrategy` bean in your Spring Boot application:

```java
@Configuration
public class EmbeddingConfig {
    @Bean
    public BatchingStrategy customBatchingStrategy() {
        return new CustomBatchingStrategy();
    }
}
```

This custom `BatchingStrategy` will then be automatically used by the `EmbeddingModel` implementations in your application.

> Vector stores supported by Spring AI are configured to use the default `TokenCountBatchingStrategy`.

<a id="_vectorstore_implementations"></a>

## VectorStore Implementations

These are the available implementations of the `VectorStore` interface:

- [Azure Vector Search](https://docs.spring.io/spring-ai/reference/api/vectordbs/azure.html) - The [Azure](https://learn.microsoft.com/en-us/azure/search/vector-search-overview) vector store.
 
- [Apache Cassandra](https://docs.spring.io/spring-ai/reference/api/vectordbs/apache-cassandra.html) - The [Apache Cassandra](https://cassandra.apache.org/doc/latest/cassandra/vector-search/overview.html) vector store.
 
- [Chroma Vector Store](https://docs.spring.io/spring-ai/reference/api/vectordbs/chroma.html) - The [Chroma](https://www.trychroma.com/) vector store.
 
- [Elasticsearch Vector Store](https://docs.spring.io/spring-ai/reference/api/vectordbs/elasticsearch.html) - The [Elasticsearch](https://www.elastic.co/) vector store.
 
- [GemFire Vector Store](https://docs.spring.io/spring-ai/reference/api/vectordbs/gemfire.html) - The [GemFire](https://tanzu.vmware.com/content/blog/vmware-gemfire-vector-database-extension) vector store.
 
- [MariaDB Vector Store](https://docs.spring.io/spring-ai/reference/api/vectordbs/mariadb.html) - The [MariaDB](https://mariadb.com/) vector store.
 
- [Milvus Vector Store](https://docs.spring.io/spring-ai/reference/api/vectordbs/milvus.html) - The [Milvus](https://milvus.io/) vector store.
 
- [MongoDB Atlas Vector Store](https://docs.spring.io/spring-ai/reference/api/vectordbs/mongodb.html) - The [MongoDB Atlas](https://www.mongodb.com/atlas/database) vector store.
 
- [Neo4j Vector Store](https://docs.spring.io/spring-ai/reference/api/vectordbs/neo4j.html) - The [Neo4j](https://neo4j.com/) vector store.
 
- [OpenSearch Vector Store](https://docs.spring.io/spring-ai/reference/api/vectordbs/opensearch.html) - The [OpenSearch](https://opensearch.org/platform/search/vector-database.html) vector store.
 
- [Oracle Vector Store](https://docs.spring.io/spring-ai/reference/api/vectordbs/oracle.html) - The [Oracle Database](https://docs.oracle.com/en/database/oracle/oracle-database/23/vecse/overview-ai-vector-search.html) vector store.
 
- [PgVector Store](https://docs.spring.io/spring-ai/reference/api/vectordbs/pgvector.html) - The [PostgreSQL/PGVector](https://github.com/pgvector/pgvector) vector store.
 
- [Pinecone Vector Store](https://docs.spring.io/spring-ai/reference/api/vectordbs/pinecone.html) - [Pinecone](https://www.pinecone.io/) vector store.
 
- [Qdrant Vector Store](https://docs.spring.io/spring-ai/reference/api/vectordbs/qdrant.html) - [Qdrant](https://www.qdrant.tech/) vector store.
 
- [Redis Vector Store](https://docs.spring.io/spring-ai/reference/api/vectordbs/redis.html) - The [Redis](https://redis.io/) vector store.
 
- [Typesense Vector Store](https://docs.spring.io/spring-ai/reference/api/vectordbs/typesense.html) - The [Typesense](https://typesense.org/docs/0.24.0/api/vector-search.html) vector store.
 
- [Weaviate Vector Store](https://docs.spring.io/spring-ai/reference/api/vectordbs/weaviate.html) - The [Weaviate](https://weaviate.io/) vector store.
 
- [S3 Vector Store](https://docs.spring.io/spring-ai/reference/api/vectordbs/s3-vector-store.html) - The [AWS S3](https://aws.amazon.com/s3/features/vectors/) vector store.
 
- [SimpleVectorStore](https://github.com/spring-projects/spring-ai/blob/main/spring-ai-vector-store/src/main/java/org/springframework/ai/vectorstore/SimpleVectorStore.java) - A simple implementation of a vector storage, good only for testing purposes.
    

> Azure Cosmos DB vector store support is available as an external module maintained by the Azure Cosmos DB team. See [azurecosmosdb.github.io/spring-ai/docs/index.html](https://azurecosmosdb.github.io/spring-ai/docs/index.html) for more information.

> The `SimpleVectorStore` implementation is not designed for production use and should only be used for testing or demonstration purposes.

More implementations may be supported in future releases.

If you have a vector database that needs to be supported by Spring AI, open an issue on GitHub or, even better, submit a pull request with an implementation.

Information on each of the `VectorStore` implementations can be found in the subsections of this chapter.

<a id="_example_usage"></a>