---
title: Spring AI：Redis 向量存储
description: RedisVectorStore 的接入、配置、元数据过滤、距离度量、文本与范围检索，以及语义缓存的使用和隔离。
sidebar:
  label: Redis
  order: 4
---

`RedisVectorStore` 用于在 Redis 中存储文档的嵌入向量，并执行相似度检索。

[Redis](https://redis.io) 是基于内存的数据结构存储，可用作数据库、缓存、消息代理和流处理引擎。原文将其描述为采用 BSD 许可证的开源软件；选用实际发行版时应另行确认版本和许可证。它支持字符串、哈希、列表、集合、有序集合与范围查询、位图、HyperLogLog、地理空间索引和流。

[Redis Search and Query](https://redis.io/docs/interact/search-and-query/) 扩展了 Redis OSS 的核心能力，使 Redis 可以承担向量数据库的职责：

- 在哈希或 JSON 文档中存储向量及其元数据。
- 读取向量。
- 执行 KNN 向量相似度检索。
- 按半径阈值执行范围向量检索。
- 在 `TEXT` 字段上执行全文检索。
- 使用多种距离度量（`COSINE`、`L2`、`IP`）和向量索引算法（`HNSW`、`FLAT`）。

:::tip[阅读重点]
先完成自动配置、文档写入和相似度检索，再理解元数据字段声明与过滤。距离度量、HNSW 调参、文本与范围检索按需深入；语义缓存是独立的应用能力，保留完整配置和隔离参考。
:::

<a id="_prerequisites"></a>

## 一、准备工作

需要具备：

- 一个 Redis Stack 实例。原文提供两种选择：[Redis Cloud](https://app.redislabs.com/#/)（原文推荐），或 [Docker 镜像](https://hub.docker.com/r/redis/redis-stack) `redis/redis-stack:latest`。
- 一个计算文档向量的 `EmbeddingModel`。可用实现见 [Embedding 模型](/frameworks/spring-ai/models/embedding-model/)；如果提供方要求认证，还需准备相应 API Key。

<a id="_auto_configuration"></a>

## 二、自动配置（重点掌握）

> Spring AI 曾调整自动配置与 starter 的 artifact 名称。升级旧项目时，参见[升级说明](https://docs.spring.io/spring-ai/reference/upgrade-notes.html)。

Spring AI 提供 Redis 向量存储的 Spring Boot 自动配置。在 Maven `pom.xml` 中加入：

```xml
<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>spring-ai-starter-vector-store-redis</artifactId>
</dependency>
```

使用 Gradle 时，在 `build.gradle` 中加入：

```groovy
dependencies {
    implementation 'org.springframework.ai:spring-ai-starter-vector-store-redis'
}
```

> 按[依赖管理](https://docs.spring.io/spring-ai/reference/getting-started.html#dependency-management)引入 Spring AI BOM；仓库配置见 [Artifact Repositories](https://docs.spring.io/spring-ai/reference/getting-started.html#artifact-repositories)。

向量存储可以初始化所需结构，但需要显式启用：在对应构造或构建配置中设置 `initializeSchema`，或设置 `spring.ai.vectorstore.redis.initialize-schema=true`。

> 这是与早期版本不同的行为：旧版本默认初始化，目前需要主动启用。

默认值与可配置项见[配置属性](#redisvector-properties)。还需要配置一个 [`EmbeddingModel`](/frameworks/spring-ai/models/embedding-model/) Bean，负责计算文档向量。

随后可以注入 `VectorStore`，写入文档并查询：

```java
@Autowired VectorStore vectorStore;

// ...

List <Document> documents = List.of(
    new Document("Spring AI rocks!! Spring AI rocks!! Spring AI rocks!! Spring AI rocks!! Spring AI rocks!!", Map.of("meta1", "meta1")),
    new Document("The World is Big and Salvation Lurks Around the Corner"),
    new Document("You walk forward facing the past and you turn back toward the future.", Map.of("meta2", "meta2")));

// Add the documents to Redis
vectorStore.add(documents);

// Retrieve documents similar to a query
List<Document> results = this.vectorStore.similaritySearch(SearchRequest.builder().query("Spring").topK(5).build());
```

需要向自动配置的 Redis 结构加入自定义元数据字段时，定义 `List<RedisVectorStore.MetadataField>` Bean：

```java
@Bean
List<RedisVectorStore.MetadataField> redisMetadataFields() {
    return List.of(RedisVectorStore.MetadataField.tag("conversationId"));
}
```

<a id="redisvector-properties"></a>

### 配置属性

连接 Redis 时，需要提供实例地址等连接信息。可使用 Spring Boot 的 `application.yml`：

```yaml
spring:
  data:
    redis:
      url: <redis instance url>
  ai:
    vectorstore:
      redis:
        initialize-schema: true
        index-name: custom-index
        prefix: custom-prefix
```

连接信息也可以写入 `application.properties`：

```properties
spring.data.redis.host=localhost
spring.data.redis.port=6379
spring.data.redis.username=default
spring.data.redis.password=
```

`spring.ai.vectorstore.redis.*` 用于配置 `RedisVectorStore`：

| 属性                                                  | 说明                                                               | 默认值            |
| ----------------------------------------------------- | ------------------------------------------------------------------ | ----------------- |
| `spring.ai.vectorstore.redis.initialize-schema`       | 是否初始化所需结构。                                               | `false`           |
| `spring.ai.vectorstore.redis.index-name`              | 保存向量的索引名称。                                               | `spring-ai-index` |
| `spring.ai.vectorstore.redis.prefix`                  | Redis 键前缀。                                                     | `embedding:`      |
| `spring.ai.vectorstore.redis.distance-metric`         | 向量距离度量：`COSINE`、`L2` 或 `IP`。                             | `COSINE`          |
| `spring.ai.vectorstore.redis.vector-algorithm`        | 向量索引算法：`HNSW` 或 `FLAT`。                                   | `HNSW`            |
| `spring.ai.vectorstore.redis.hnsw-m`                  | HNSW 节点的最大出向连接数。                                        | `16`              |
| `spring.ai.vectorstore.redis.hnsw-ef-construction`    | HNSW 构建索引时考虑的最大连接数。                                  | `200`             |
| `spring.ai.vectorstore.redis.hnsw-ef-runtime`         | HNSW 检索时考虑的连接数。                                          | `10`              |
| `spring.ai.vectorstore.redis.default-range-threshold` | 范围检索的默认半径阈值。                                           | `0.8`             |
| `spring.ai.vectorstore.redis.text-scorer`             | 文本评分算法：`BM25`、`TFIDF`、`BM25STD`、`DISMAX` 或 `DOCSCORE`。 | `BM25`            |

<a id="_metadata_filtering"></a>

## 三、元数据过滤（重点掌握）

Redis 支持统一的、可跨后端复用的[元数据过滤](/frameworks/spring-ai/rag/vector-stores/#metadata-filters)。

可以使用字符串表达式：

```java
vectorStore.similaritySearch(SearchRequest.builder()
        .query("The World")
        .topK(TOP_K)
        .similarityThreshold(SIMILARITY_THRESHOLD)
        .filterExpression("country in ['UK', 'NL'] && year >= 2020").build());
```

也可以通过 `Filter.Expression` DSL 构建：

```java
FilterExpressionBuilder b = new FilterExpressionBuilder();

vectorStore.similaritySearch(SearchRequest.builder()
        .query("The World")
        .topK(TOP_K)
        .similarityThreshold(SIMILARITY_THRESHOLD)
        .filterExpression(b.and(
                b.in("country", "UK", "NL"),
                b.gte("year", 2020)).build()).build());
```

这些过滤表达式会自动转换为 [Redis 查询语法](https://redis.io/docs/interact/search-and-query/query/)。例如：

```sql
country in ['UK', 'NL'] && year >= 2020
```

会转换为 Redis 原生过滤格式：

```text
@country:{UK | NL} @year:[2020 inf]
```

<a id="_manual_configuration"></a>

## 四、手动配置

手动配置时，引入 `spring-ai-redis-store`：

```xml
<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>spring-ai-redis-store</artifactId>
</dependency>
```

Gradle 写法：

```groovy
dependencies {
    implementation 'org.springframework.ai:spring-ai-redis-store'
}
```

先创建 `RedisClient` Bean：

```java
@Bean
public RedisClient jedisClient() {
    return RedisClient.builder().hostAndPort("<host>", 6379).build();
}
```

再通过构建器创建 `RedisVectorStore` Bean：

```java
@Bean
public VectorStore vectorStore(RedisClient jedisClient, EmbeddingModel embeddingModel) {
    return RedisVectorStore.builder(jedisClient, embeddingModel)
        .indexName("custom-index")                // Optional: defaults to "spring-ai-index"
        .prefix("custom-prefix")                  // Optional: defaults to "embedding:"
        .contentFieldName("content")              // Optional: field for document content
        .embeddingFieldName("embedding")          // Optional: field for vector embeddings
        .vectorAlgorithm(Algorithm.HNSW)          // Optional: HNSW or FLAT (defaults to HNSW)
        .distanceMetric(DistanceMetric.COSINE)    // Optional: COSINE, L2, or IP (defaults to COSINE)
        .hnswM(16)                                // Optional: HNSW connections (defaults to 16)
        .hnswEfConstruction(200)                  // Optional: HNSW build parameter (defaults to 200)
        .hnswEfRuntime(10)                        // Optional: HNSW search parameter (defaults to 10)
        .defaultRangeThreshold(0.8)               // Optional: default radius for range searches
        .textScorer(TextScorer.BM25)              // Optional: text scoring algorithm (defaults to BM25)
        .metadataFields(                          // Optional: define metadata fields for filtering
            MetadataField.tag("country"),
            MetadataField.numeric("year"),
            MetadataField.text("description"))
        .initializeSchema(true)                   // Optional: defaults to false
        .batchingStrategy(new TokenCountBatchingStrategy()) // Optional: defaults to TokenCountBatchingStrategy
        .build();
}

// This can be any EmbeddingModel implementation
@Bean
public EmbeddingModel embeddingModel() {
    return new OpenAiEmbeddingModel(OpenAiEmbeddingOptions.builder().apiKey(System.getenv("OPENAI_API_KEY")).build());
}
```

> 过滤表达式用到的元数据字段，必须显式声明字段名及类型（`TAG`、`TEXT` 或 `NUMERIC`）。上例声明了 `country`（`TAG`）、`year`（`NUMERIC`）和 `description`（`TEXT`）。

<a id="_accessing_the_native_client"></a>

## 五、访问原生客户端

`getNativeClient()` 可以取得底层 Redis 客户端 `RedisClient`：

```java
RedisVectorStore vectorStore = context.getBean(RedisVectorStore.class);
Optional<RedisClient> nativeClient = vectorStore.getNativeClient();

if (nativeClient.isPresent()) {
    RedisClient jedisClient = nativeClient.get();
    // Use the native client for Redis-specific operations
}
```

原生客户端用于执行 `VectorStore` 接口未暴露的 Redis 专属操作。

<a id="_distance_metrics"></a>

## 六、距离度量

Redis 向量存储支持三种距离度量：

- **`COSINE`**：余弦相似度，默认选项，衡量向量夹角的余弦值。
- **`L2`**：欧几里得距离，衡量向量间的直线距离。
- **`IP`**：内积，计算向量点积。

原文说明，这些度量会自动转换为 `0–1` 的相似度分数，`1` 表示最相似；实际换算及取值边界需以对应实现为准。

```java
RedisVectorStore vectorStore = RedisVectorStore.builder(jedisClient, embeddingModel)
    .distanceMetric(DistanceMetric.COSINE)  // or L2, IP
    .build();
```

<a id="_hnsw_algorithm_configuration"></a>

## 七、HNSW 算法配置

Redis 向量存储默认使用 HNSW（Hierarchical Navigable Small World，分层可导航小世界）算法执行近似最近邻检索。可以根据数据量、召回率和延迟要求调整参数：

```java
RedisVectorStore vectorStore = RedisVectorStore.builder(jedisClient, embeddingModel)
    .vectorAlgorithm(Algorithm.HNSW)
    .hnswM(32)                    // Maximum outgoing connections per node (default: 16)
    .hnswEfConstruction(100)      // Connections during index building (default: 200)
    .hnswEfRuntime(50)            // Connections during search (default: 10)
    .build();
```

调参时重点关注：

- **`M`**：增大会提高召回率，同时增加内存和索引构建开销。原文给出的常用范围为 `12–48`。
- **`EF_CONSTRUCTION`**：增大会改善索引质量，同时延长构建时间。常用范围为 `100–500`。
- **`EF_RUNTIME`**：增大会提高检索准确性，同时增加查询延迟。常用范围为 `10–100`。

数据集较小或需要精确结果时，可以改用 `FLAT`：

```java
RedisVectorStore vectorStore = RedisVectorStore.builder(jedisClient, embeddingModel)
    .vectorAlgorithm(Algorithm.FLAT)
    .build();
```

<a id="_text_search"></a>

## 八、文本检索

`RedisVectorStore` 也可以使用 Redis Query Engine 的全文检索能力，在 `TEXT` 字段中按关键词和短语查找文档：

```java
// Search for documents containing specific text
List<Document> textResults = vectorStore.searchByText(
    "machine learning",   // search query
    "content",            // field to search (must be TEXT type)
    10,                   // limit
    "category == 'AI'"    // optional filter expression
);
```

文本检索支持：

- 单词检索。
- `inOrder=true` 时按顺序进行短语匹配。
- `inOrder=false` 时使用 OR 语义匹配词项。
- 通过停用词过滤常见词。
- 多种文本评分算法。

在构建存储时配置文本检索行为：

```java
RedisVectorStore vectorStore = RedisVectorStore.builder(jedisClient, embeddingModel)
    .textScorer(TextScorer.TFIDF)                    // Text scoring algorithm
    .inOrder(true)                                   // Match terms in order
    .stopwords(Set.of("is", "a", "the", "and"))      // Ignore common words
    .metadataFields(MetadataField.text("description")) // Define TEXT fields
    .build();
```

<a id="_text_scoring_algorithms"></a>

### 文本评分算法

可用算法包括：

- **`BM25`**：在 TF-IDF 基础上引入词频饱和处理，默认使用。
- **`TFIDF`**：经典的词频—逆文档频率算法。
- **`BM25STD`**：标准化 BM25。
- **`DISMAX`**：Disjunction Max。
- **`DOCSCORE`**：文档评分。

原文说明，文本分数也会归一化到 `0–1`，以便与向量相似度分数保持一致；具体换算以实现为准。

<a id="_range_search"></a>

## 九、范围检索

范围检索按指定半径阈值筛选文档，而不是固定返回若干最近邻：

```java
// Search with explicit radius
List<Document> rangeResults = vectorStore.searchByRange(
    "AI and machine learning",  // query
    0.8,                        // radius (similarity threshold)
    "category == 'AI'"          // optional filter expression
);
```

也可以在构建时设置默认范围阈值：

```java
RedisVectorStore vectorStore = RedisVectorStore.builder(jedisClient, embeddingModel)
    .defaultRangeThreshold(0.8)  // Set default threshold
    .build();

// Use default threshold
List<Document> results = vectorStore.searchByRange("query");
```

当需求是返回达到相似度阈值的相关文档，而不是限制为固定数量时，可以考虑范围检索。

<a id="_semantic_caching"></a>

## 十、语义缓存（进阶参考）

语义缓存使用 Redis 向量检索，按用户问题的**语义相似度**复用聊天回答。即使问题的字面表达不同，只要语义接近，也可能命中已有缓存。

<a id="_why_semantic_caching"></a>

### 为什么使用语义缓存

传统缓存要求键完全相同。以下三个问题语义相近，但原始字符串不同：

- “法国的首都是哪里？”
- “告诉我法国的首都。”
- “哪座城市是法国首都？”

如果直接以原始问题作键，传统缓存会分别处理这些请求，从而重复调用大语言模型。语义缓存先将问题转换为向量，再比较其**含义**。

主要收益：

- **降低 API 成本**：减少重复的大语言模型调用。
- **降低延迟**：命中时直接返回缓存，无需等待模型推理。
- **提高吞吐能力**：更多查询可以复用结果，API 成本不必同比增加。
- **保持回答一致**：语义相近的问题可复用相同回答。

<a id="_auto_configuration_2"></a>

### 自动配置

Spring AI 提供 Redis 语义缓存的 Spring Boot 自动配置。Maven 依赖为：

```xml
<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>spring-ai-starter-vector-store-redis-semantic-cache</artifactId>
</dependency>
```

Gradle 依赖为：

```groovy
dependencies {
    implementation 'org.springframework.ai:spring-ai-starter-vector-store-redis-semantic-cache'
}
```

> 自动配置提供面向语义缓存优化的默认嵌入模型 `redis/langcache-embed-v1`。定义自己的 `EmbeddingModel` Bean 可以覆盖它。

<a id="semantic-cache-properties"></a>

### 配置属性

`spring.ai.vectorstore.redis.semantic-cache.*` 用于配置语义缓存：

| 属性                                                              | 说明                                                         | 默认值                 |
| ----------------------------------------------------------------- | ------------------------------------------------------------ | ---------------------- |
| `spring.ai.vectorstore.redis.semantic-cache.enabled`              | 是否启用语义缓存。                                           | `true`                 |
| `spring.ai.vectorstore.redis.semantic-cache.host`                 | Redis 主机。                                                 | `localhost`            |
| `spring.ai.vectorstore.redis.semantic-cache.port`                 | Redis 端口。                                                 | `6379`                 |
| `spring.ai.vectorstore.redis.semantic-cache.similarity-threshold` | 缓存命中的相似度阈值，范围为 `0.0–1.0`；越高要求语义越接近。 | `0.95`                 |
| `spring.ai.vectorstore.redis.semantic-cache.index-name`           | 缓存条目的 Redis 搜索索引名。                                | `semantic-cache-index` |
| `spring.ai.vectorstore.redis.semantic-cache.prefix`               | 缓存条目的 Redis 键前缀。                                    | `semantic-cache:`      |

`application.yml` 示例：

```yaml
spring:
  ai:
    vectorstore:
      redis:
        semantic-cache:
          enabled: true
          host: localhost
          port: 6379
          similarity-threshold: 0.85
          index-name: my-app-cache
          prefix: 'my-app:semantic-cache:'
```

<a id="_using_the_semanticcacheadvisor"></a>

### 使用 SemanticCacheAdvisor

`SemanticCacheAdvisor` 与 Spring AI 的 `ChatClient` Advisor 机制集成，负责缓存回答，并为语义相近的问题返回缓存结果：

```java
@Autowired
private SemanticCache semanticCache;

@Autowired
private ChatModel chatModel;

public void example() {
    // Create the cache advisor
    SemanticCacheAdvisor cacheAdvisor = SemanticCacheAdvisor.builder()
        .cache(semanticCache)
        .build();

    // First query - calls the LLM and caches the response
    ChatResponse response1 = ChatClient.builder(chatModel)
        .build()
        .prompt("What is the capital of France?")
        .advisors(cacheAdvisor)
        .call()
        .chatResponse();

    // Similar query - returns cached response (no LLM call)
    ChatResponse response2 = ChatClient.builder(chatModel)
        .build()
        .prompt("Tell me the capital city of France")
        .advisors(cacheAdvisor)
        .call()
        .chatResponse();

    // response1 and response2 contain the same cached answer
}
```

它会自动执行：

- 调用大语言模型前，检查是否存在语义相近的缓存问题。
- 匹配结果达到相似度阈值时，直接返回缓存回答。
- 模型成功返回后，缓存新的回答。
- 支持同步和流式聊天调用。

<a id="_direct_cache_usage"></a>

### 直接使用缓存

需要更细的控制时，可以直接操作 `SemanticCache`：

```java
@Autowired
private SemanticCache semanticCache;

// Store a response with a query
semanticCache.set("What is the capital of France?", chatResponse);

// Store with TTL (time-to-live) for automatic expiration
semanticCache.set("What's the weather today?", weatherResponse, Duration.ofHours(1));

// Retrieve a semantically similar response
Optional<ChatResponse> cached = semanticCache.get("Tell me France's capital");

if (cached.isPresent()) {
    // Use the cached response
    String answer = cached.get().getResult().getOutput().getText();
}

// Clear all cached entries
semanticCache.clear();
```

<a id="_manual_configuration_2"></a>

### 手动配置

也可以手动创建语义缓存组件：

```java
@Configuration
public class SemanticCacheConfig {

    @Bean
    public RedisClient jedisClient() {
        return RedisClient.builder().hostAndPort("localhost", 6379).build();
    }

    @Bean
    public SemanticCache semanticCache(RedisClient jedisClient, EmbeddingModel embeddingModel) {
        return DefaultSemanticCache.builder()
            .jedisClient(jedisClient)
            .embeddingModel(embeddingModel)
            .distanceThreshold(0.3)           // Lower = stricter matching
            .indexName("my-semantic-cache")
            .prefix("cache:")
            .build();
    }

    @Bean
    public SemanticCacheAdvisor semanticCacheAdvisor(SemanticCache cache) {
        return SemanticCacheAdvisor.builder()
            .cache(cache)
            .build();
    }
}
```

<a id="_cache_isolation_with_namespaces"></a>

### 使用命名空间隔离缓存

多租户应用或需要独立缓存空间时，可以使用不同索引名区分缓存条目：

```java
// Create isolated caches for different users or contexts
SemanticCache user1Cache = DefaultSemanticCache.builder()
    .jedisClient(jedisClient)
    .embeddingModel(embeddingModel)
    .indexName("user-1-cache")
    .build();

SemanticCache user2Cache = DefaultSemanticCache.builder()
    .jedisClient(jedisClient)
    .embeddingModel(embeddingModel)
    .indexName("user-2-cache")
    .build();

// Each user gets their own isolated cache space
SemanticCacheAdvisor user1Advisor = SemanticCacheAdvisor.builder()
    .cache(user1Cache)
    .build();
```

<a id="_system_prompt_isolation"></a>

### 按系统提示词隔离

`SemanticCacheAdvisor` 会根据系统提示词区分缓存。相同用户问题配合不同系统提示词时，使用不同缓存上下文，适用于多角色或依赖上下文的应用：

```java
SemanticCacheAdvisor cacheAdvisor = SemanticCacheAdvisor.builder()
    .cache(semanticCache)
    .build();

// Query with technical support persona
ChatResponse technicalResponse = ChatClient.builder(chatModel)
    .build()
    .prompt()
    .system("You are a technical support specialist. Provide detailed technical answers.")
    .user("How do I reset my password?")
    .advisors(cacheAdvisor)
    .call()
    .chatResponse();

// Same query with customer service persona - cache MISS (different context)
ChatResponse serviceResponse = ChatClient.builder(chatModel)
    .build()
    .prompt()
    .system("You are a friendly customer service agent. Keep responses brief and helpful.")
    .user("How do I reset my password?")
    .advisors(cacheAdvisor)
    .call()
    .chatResponse();

// Same query with technical support persona again - cache HIT
ChatResponse technicalAgain = ChatClient.builder(chatModel)
    .build()
    .prompt()
    .system("You are a technical support specialist. Provide detailed technical answers.")
    .user("How do I reset my password?")
    .advisors(cacheAdvisor)
    .call()
    .chatResponse();
// Returns the cached technical response
```

其处理方式是计算系统提示词的确定性哈希，并在写入和读取缓存时将哈希作为元数据过滤条件：

- 相同问题 + 相同系统提示词：可命中相同缓存。
- 相同问题 + 不同系统提示词：不命中另一上下文的缓存，分别保存。
- 不带系统提示词的问题：共享一个公共缓存上下文。

<a id="_context_aware_cache_api"></a>

### 带上下文的缓存 API

高级场景可以直接使用接收上下文标识的方法：

```java
// Store with explicit context hash
String contextHash = "technical-support-context";
semanticCache.set("How do I reset my password?", response, contextHash);

// Retrieve with context filtering
Optional<ChatResponse> cached = semanticCache.get("How do I reset my password?", contextHash);

// Different context hash returns empty (no match)
Optional<ChatResponse> otherContext = semanticCache.get("How do I reset my password?", "billing-context");
```

<a id="_tuning_the_similarity_threshold"></a>

### 调整相似度阈值

相似度阈值表示问题需要与缓存条目多接近才能命中，范围为 `0.0–1.0`：

- **较高阈值，例如 `0.95`**：要求语义非常接近，减少误命中，但可能漏掉可复用的缓存。
- **较低阈值，例如 `0.70`**：接受更宽泛的语义匹配，提高命中率，但可能返回相关性不足的回答。

手动构建示例使用的是**距离阈值**，方向相反，值越小越严格：

```java
// Strict matching - only very similar queries hit the cache
SemanticCache strictCache = DefaultSemanticCache.builder()
    .jedisClient(jedisClient)
    .embeddingModel(embeddingModel)
    .distanceThreshold(0.2)  // Strict (distance-based, lower = stricter)
    .build();

// Lenient matching - broader semantic similarity accepted
SemanticCache lenientCache = DefaultSemanticCache.builder()
    .jedisClient(jedisClient)
    .embeddingModel(embeddingModel)
    .distanceThreshold(0.5)  // Lenient
    .build();
```

> 可先从严格匹配开始，再按应用对语义差异的容忍度逐步放宽。相似度阈值与距离阈值的数值不能直接混用。

<a id="_ttl_and_cache_expiration"></a>

### TTL 与缓存过期

缓存回答可以设置生存时间（TTL），到期自动删除，适合天气等时效性数据：

```java
// Cache weather data for 1 hour
semanticCache.set("What's the weather in New York?", weatherResponse, Duration.ofHours(1));

// Cache general knowledge indefinitely (no TTL)
semanticCache.set("What is photosynthesis?", scienceResponse);

// Redis automatically removes expired entries
```

<a id="_how_it_works"></a>

### 工作流程

语义缓存的执行过程为：

1. **问题向量化**：使用配置的 `EmbeddingModel` 将问题转换为嵌入向量。
2. **向量检索**：Redis 通过范围向量查询 `VECTOR_RANGE` 查找满足阈值的缓存条目。
3. **缓存命中**：找到语义相近的问题时，直接返回已缓存的 `ChatResponse`。
4. **缓存未命中**：继续调用大语言模型，并保存新回答供后续请求复用。

实现使用 HNSW 向量索引加速相似度检索，以支持较大规模的缓存。

---

来源：[Redis](https://docs.spring.io/spring-ai/reference/api/vectordbs/redis.html)，按 Spring AI 2.0.2 文档翻译。示例尚未连接 Redis 或模型运行验证。
