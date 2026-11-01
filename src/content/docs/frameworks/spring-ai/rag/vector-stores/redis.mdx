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
先完成自动配置、文档写入和相似度检索，再理解元数据字段声明与过滤。距离度量、HNSW 调参、文本与范围检索按需深入；语义缓存是独立的应用能力，保留完整配置和隔离参考。统一读写与检索接口见[向量存储总览](/frameworks/spring-ai/rag/vector-stores/)。
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

> 按[依赖管理](/frameworks/spring-ai/getting-started/quickstart/#使用-bom-管理版本)引入 Spring AI BOM；仓库配置见 [Artifact Repositories](/frameworks/spring-ai/getting-started/quickstart/#配置依赖仓库)。

向量存储可以初始化所需结构，但需要显式启用：在对应构造或构建配置中设置 `initializeSchema`，或设置 `spring.ai.vectorstore.redis.initialize-schema=true`。

> 这是与早期版本不同的行为：旧版本默认初始化，目前需要主动启用。

默认值与可配置项见[配置属性](#redisvector-properties)。还需要配置一个 [`EmbeddingModel`](/frameworks/spring-ai/models/embedding-model/) Bean，负责计算文档向量。

随后可以注入 `VectorStore`，写入文档并查询。文档读取和切分见 [ETL 管道](/frameworks/spring-ai/rag/document-ingestion/)，统一检索参数见 [SearchRequest](/frameworks/spring-ai/rag/vector-stores/#_searchrequest_builder)：

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

需要向自动配置的 Redis 结构加入自定义元数据字段时，定义 `List<RedisVectorStore.MetadataField>` Bean。过滤示例中的 `country`、`year`，以及后文的 `category`，也应按实际用途加入该列表；下面先以 `conversationId` 为例：

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

下面保留原文列出的全部参数，并按 v2.0.2 的属性类与自动配置标出实际入口。**部分原文键名没有绑定到自动配置，仅同名构建器方法可用。**

| 原文属性                                              | 实际入口与说明                                                                               | 默认值                                             |
| ----------------------------------------------------- | -------------------------------------------------------------------------------------------- | -------------------------------------------------- |
| `spring.ai.vectorstore.redis.initialize-schema`       | 是否初始化所需结构。                                                                         | `false`                                            |
| `spring.ai.vectorstore.redis.index-name`              | 自动配置的索引名；手动构建用 `.indexName(...)`。                                             | 自动配置 `default-index`；构建器 `spring-ai-index` |
| `spring.ai.vectorstore.redis.prefix`                  | 自动配置的键前缀；手动构建用 `.prefix(...)`。                                                | 自动配置 `default:`；构建器 `embedding:`           |
| `spring.ai.vectorstore.redis.distance-metric`         | 此键未绑定；手动构建用 `.distanceMetric(...)`，可选 `COSINE`、`L2`、`IP`。                   | 构建器 `COSINE`                                    |
| `spring.ai.vectorstore.redis.vector-algorithm`        | 此键未绑定；手动构建用 `.vectorAlgorithm(...)`，可选 `HNSW`、`FLAT`。                        | 构建器 `HNSW`                                      |
| `spring.ai.vectorstore.redis.hnsw-m`                  | 实际配置为 `spring.ai.vectorstore.redis.hnsw.m`：节点最大出向连接数。                        | `16`                                               |
| `spring.ai.vectorstore.redis.hnsw-ef-construction`    | 实际配置为 `spring.ai.vectorstore.redis.hnsw.ef-construction`：构建时的候选列表大小。        | `200`                                              |
| `spring.ai.vectorstore.redis.hnsw-ef-runtime`         | 实际配置为 `spring.ai.vectorstore.redis.hnsw.ef-runtime`：查询时的候选列表大小。             | `10`                                               |
| `spring.ai.vectorstore.redis.default-range-threshold` | 此键未绑定；使用 `.defaultRangeThreshold(...)`。原文表列 `0.8`，实际构建器默认未设置。       | 未设置；无参范围检索需要先显式配置                 |
| `spring.ai.vectorstore.redis.text-scorer`             | 此键未绑定；使用 `.textScorer(...)`，可选 `BM25`、`TFIDF`、`BM25STD`、`DISMAX`、`DOCSCORE`。 | 构建器 `BM25`                                      |

上述差异依据 [RedisVectorStoreProperties](https://github.com/spring-projects/spring-ai/blob/v2.0.2/auto-configurations/vector-stores/spring-ai-autoconfigure-vector-store-redis/src/main/java/org/springframework/ai/vectorstore/redis/autoconfigure/RedisVectorStoreProperties.java) 与 [RedisVectorStoreAutoConfiguration](https://github.com/spring-projects/spring-ai/blob/v2.0.2/auto-configurations/vector-stores/spring-ai-autoconfigure-vector-store-redis/src/main/java/org/springframework/ai/vectorstore/redis/autoconfigure/RedisVectorStoreAutoConfiguration.java) 核对。使用其他版本时，应重新确认有效属性。

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

通过 Advisor 按请求传入条件时，见 [RAG 动态过滤](/frameworks/spring-ai/rag/retrieval-and-generation/#_dynamic_filter_expressions)。这些过滤表达式会自动转换为 [Redis 查询语法](https://redis.io/docs/interact/search-and-query/query/)。例如：

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

再通过构建器创建 `RedisVectorStore` Bean。示例同时展示手动创建 OpenAI Embedding 模型：需有相应模型依赖并设置 `OPENAI_API_KEY`；已有自动配置的 `EmbeddingModel` 时直接注入，不必重复声明模型 Bean。`RedisClient` 来自 `redis.clients.jedis`，`Algorithm`、`DistanceMetric`、`TextScorer`、`MetadataField` 是 `RedisVectorStore` 的嵌套类型。

```java
@Bean
public RedisVectorStore vectorStore(RedisClient jedisClient, EmbeddingModel embeddingModel) {
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
            MetadataField.tag("category"),
            MetadataField.text("description"))
        .initializeSchema(true)                   // Optional: defaults to false
        .batchingStrategy(new TokenCountBatchingStrategy()) // Optional: defaults to TokenCountBatchingStrategy
        .build();
}

// This can be any EmbeddingModel implementation
@Bean
public EmbeddingModel embeddingModel() {
    // Reads OPENAI_API_KEY through the default OpenAI client setup.
    return OpenAiEmbeddingModel.builder().build();
}
```

> 过滤表达式用到的元数据字段，必须显式声明字段名及类型（`TAG`、`TEXT` 或 `NUMERIC`）。上例声明了 `country`、`category`（`TAG`）、`year`（`NUMERIC`）和 `description`（`TEXT`）。已有索引的字段结构还需单独核对，声明 Bean 不等于自动迁移旧索引。

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

Spring AI 将后端分数转换为越高越相似的 `Document.score`，阈值参数的统一入口见 [SearchRequest](/frameworks/spring-ai/rag/vector-stores/#_searchrequest_builder)。v2.0.2 使用的主要换算为：`COSINE`：`max((2 - rawScore) / 2, 0)`；`L2`：`1 / (1 + rawScore)`；`IP`：将 `(rawScore + 1) / 2` 限制到 `0–1`。这些是适配层的换算规则，不能将不同度量、后端或模型的同一分数直接当作同等相关性。

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

`RedisVectorStore` 也可以使用 Redis Query Engine 的全文检索能力，在 `TEXT` 字段中按关键词和短语查找文档。`searchByText`、`searchByRange` 是具体实现的扩展方法，变量应声明为 `RedisVectorStore`；它们不属于通用 `VectorStore` 接口。过滤使用的 `category` 需先声明为 `TAG` 字段：

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

`searchByText` 在此版本只对简单的 `field == 'value'` 做特殊转换，其他过滤通常按 Redis 原生条件拼接；不要把它当作完整的通用过滤 DSL。

在构建存储时配置文本检索行为；独立运行下面的示例还需准备索引，过滤时仍要加入相应元数据字段：

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

适配层检测到 `$score` 时，会将其除以 `10` 并限制上限为 `1`；缺少可用分数时可能回退为 `0.9`。因此文本结果的 `Document.score` 不一定是检索引擎实际评分，不能据此把文本检索与向量检索当作已校准的统一排序。

<a id="_range_search"></a>

## 九、范围检索

范围检索按阈值筛选文档。虽然参数名是 `radius`，此版本接收的是 `0–1` 的归一化相似度阈值，越高越严格，内部再转换为 Redis 距离。第三参数直接使用 Redis 原生过滤条件：

```java
// Search with explicit radius
List<Document> rangeResults = vectorStore.searchByRange(
    "AI and machine learning",  // query
    0.8,                        // radius (similarity threshold)
    "@category:{AI}"          // optional filter expression
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

范围检索适合按相似度阈值筛选的场景，但不能将本接口的返回值当作全部匹配文档。v2.0.2 的原生范围查询没有显式遍历分页，数量还受 Redis 查询默认值限制；`IP` 且阈值很小时另有 `topK(1000)` 回退。需要全量结果时应使用原生客户端明确分页。

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

> 类路径中有 `TransformersEmbeddingModel` 且尚无其他 `EmbeddingModel` Bean 时，自动配置会准备 `redis/langcache-embed-v1`（768 维）；首次准备需能获取对应 tokenizer 与 ONNX 模型资源。已有模型 Bean 时复用它，并非无条件加载默认模型。

<a id="semantic-cache-properties"></a>

### 配置属性

`spring.ai.vectorstore.redis.semantic-cache.*` 用于配置语义缓存：

| 属性                                                              | 说明                                                          | 默认值                           |
| ----------------------------------------------------------------- | ------------------------------------------------------------- | -------------------------------- |
| `spring.ai.vectorstore.redis.semantic-cache.enabled`              | 是否启用语义缓存。                                            | `true`                           |
| `spring.ai.vectorstore.redis.semantic-cache.host`                 | 原文键在此版本未绑定；实际连接使用 `spring.data.redis.host`。 | Spring Boot 常用默认 `localhost` |
| `spring.ai.vectorstore.redis.semantic-cache.port`                 | 原文键在此版本未绑定；实际连接使用 `spring.data.redis.port`。 | Spring Boot 常用默认 `6379`      |
| `spring.ai.vectorstore.redis.semantic-cache.similarity-threshold` | 缓存命中的相似度阈值，范围为 `0.0–1.0`；越高要求语义越接近。  | `0.95`                           |
| `spring.ai.vectorstore.redis.semantic-cache.index-name`           | 缓存条目的 Redis 搜索索引名。                                 | `semantic-cache-index`           |
| `spring.ai.vectorstore.redis.semantic-cache.prefix`               | 缓存条目的 Redis 键前缀。                                     | `semantic-cache:`                |

连接由 Spring Boot 的 `JedisConnectionFactory` 提供；语义缓存属性类没有独立的 `host`、`port` 字段。按实际入口配置的 `application.yml` 示例：

```yaml
spring:
  data:
    redis:
      host: localhost
      port: 6379
  ai:
    vectorstore:
      redis:
        semantic-cache:
          enabled: true
          similarity-threshold: 0.85
          index-name: my-app-cache
          prefix: 'my-app:semantic-cache:'
```

<a id="_using_the_semanticcacheadvisor"></a>

### 使用 SemanticCacheAdvisor

`SemanticCacheAdvisor` 与 Spring AI 的 [`ChatClient`](/frameworks/spring-ai/core/chat-client/) 的 [Advisor 机制](/frameworks/spring-ai/core/advisors/#核心组件与执行流程)集成，负责缓存回答，并为语义相近的问题返回缓存结果：

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

需要更细的控制时，可以直接操作 `SemanticCache`。`clear()` 会清理当前缓存索引可见的全部条目，不能当作只清理当前用户的操作：

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

不同缓存空间应同时使用独立的**索引名与键前缀**。只有索引名不同、前缀相同，仍可能索引到同一批 Redis 数据；下面对原文示例补上独立前缀。具体选择哪个空间应由应用确认的身份决定，命名空间本身不代替访问授权：

```java
// Create isolated caches for different users or contexts
SemanticCache user1Cache = DefaultSemanticCache.builder()
    .jedisClient(jedisClient)
    .embeddingModel(embeddingModel)
    .indexName("user-1-cache")
    .prefix("user-1:semantic-cache:")
    .build();

SemanticCache user2Cache = DefaultSemanticCache.builder()
    .jedisClient(jedisClient)
    .embeddingModel(embeddingModel)
    .indexName("user-2-cache")
    .prefix("user-2:semantic-cache:")
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
- 不带系统提示词时：上下文哈希为 `null`，该版本不会添加上下文过滤，不能保证只匹配“无系统提示词”的条目。

这里的哈希只包含系统提示词，不覆盖完整会话历史、用户权限、模型参数或工具结果。需要这些维度隔离时，使用独立缓存空间或自行构造明确的上下文标识。

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

手动构建示例使用的是**距离阈值**，方向相反，值越小越严格。v2.0.2 在读取时按 `similarity = 1 - distance / 2` 转换：`0.2` 对应 `0.9`，`0.5` 对应 `0.75`。日常接入建议统一用 `.similarityThreshold(...)`；距离模式的部分 `set` 重载查重时直接使用内部存储值，未完全沿用读取时的换算，下面代码保留作 API 对照：

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

> 可先从严格匹配开始，再按应用对语义差异的容忍度逐步放宽。相似度阈值与距离阈值的数值不能直接混用；相同系统提示词也只有达到阈值时才命中。

<a id="_ttl_and_cache_expiration"></a>

### TTL 与缓存过期

显式调用带 `Duration` 的 `set` 重载时，Redis 实现会给写入键设置过期时间，适合天气等时效性数据。`SemanticCacheAdvisor` 默认使用带上下文的 `set`，不会自动给全部回答加 TTL；采用自定义 `VectorStore` 时，也不能假定该重载一定能设置 Redis 过期时间：

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
2. **向量检索**：无上下文过滤时可走范围查询 `VECTOR_RANGE`；需要上下文过滤时，此版本使用带过滤的相似度检索（`topK(5)`）。
3. **缓存命中**：找到语义相近的问题时，直接返回已缓存的 `ChatResponse`。
4. **缓存未命中**：继续调用大语言模型，并保存新回答供后续请求复用。

实现使用 HNSW 向量索引加速相似度检索，以支持较大规模的缓存。

---

来源：[Redis](https://docs.spring.io/spring-ai/reference/api/vectordbs/redis.html)，按 Spring AI 2.0.2 文档翻译。示例尚未连接 Redis 或模型运行验证。
