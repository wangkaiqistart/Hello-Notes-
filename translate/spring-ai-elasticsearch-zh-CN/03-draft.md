---
title: Spring AI：Elasticsearch 向量存储
description: Elasticsearch 的准备工作、Spring Boot 自动配置、连接与向量索引参数、元数据过滤、手动创建和原生客户端。
sidebar:
  label: Elasticsearch（ES）
  order: 6
---

`ElasticsearchVectorStore` 将文档的嵌入向量保存在 Elasticsearch 中，并提供相似度检索。

[Elasticsearch](https://www.elastic.co/elasticsearch) 是基于 Apache Lucene 的搜索与分析引擎，原文将其介绍为开源软件。

:::tip[阅读重点]
先准备 Elasticsearch 和 Embedding 模型，再完成 starter 接入、索引初始化、文档写入与检索。重点理解向量维度、相似度函数和元数据过滤；完整连接参数、手动创建与原生客户端保留作参考。统一接口见[向量存储总览](/frameworks/spring-ai/rag/vector-stores/)。
:::

<a id="_prerequisites"></a>

## 一、准备工作

需要一个正在运行的 Elasticsearch 实例，可选择：

- [Docker](https://hub.docker.com/_/elasticsearch/)。
- [自行部署 Elasticsearch](https://www.elastic.co/guide/en/elasticsearch/reference/current/install-elasticsearch.html#elasticsearch-install-packages)。
- [Elastic Cloud](https://www.elastic.co/cloud/elasticsearch-service/signup?page=docs&placement=docs-body)。

<a id="_auto_configuration"></a>

## 二、自动配置（重点掌握）

Spring AI 曾调整自动配置和 starter 的 artifact 名称。迁移旧项目时，参见[升级说明](https://docs.spring.io/spring-ai/reference/upgrade-notes.html)。

Spring AI 提供 Elasticsearch 向量存储的 Spring Boot 自动配置。在 Maven `pom.xml` 中加入：

```xml
<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>spring-ai-starter-vector-store-elasticsearch</artifactId>
</dependency>
```

Gradle 项目在 `build.gradle` 中加入：

```groovy
dependencies {
    implementation 'org.springframework.ai:spring-ai-starter-vector-store-elasticsearch'
}
```

:::note[旧版本兼容说明]
原文为 Spring Boot `3.3.0` 之前的项目保留了 Java 客户端版本提示：较旧客户端与这里使用的查询不兼容，需要显式引入 `elasticsearch-java`。原文文字写“版本大于 `8.13.3`”，但下面示例固定为 `8.13.3`，两者存在不一致。以下仅保留作历史迁移参考，不作为 Spring AI 2.0.2 的配套依赖推荐；当前项目应以选定版本的 BOM 和兼容性说明为准。
:::

历史 Maven 示例：

```xml
<dependency>
    <groupId>co.elastic.clients</groupId>
    <artifactId>elasticsearch-java</artifactId>
    <version>8.13.3</version>
</dependency>
```

历史 Gradle 示例：

```groovy
dependencies {
    implementation 'co.elastic.clients:elasticsearch-java:8.13.3'
}
```

通过[依赖管理](https://docs.spring.io/spring-ai/reference/getting-started.html#dependency-management)引入 Spring AI BOM；Maven Central 与 Snapshot 仓库配置见[制品仓库](https://docs.spring.io/spring-ai/reference/getting-started.html#artifact-repositories)。

向量存储可以初始化所需的索引结构，但必须显式启用：在手动构建时设置 `initializeSchema`，或将 `spring.ai.vectorstore.elasticsearch.initialize-schema` 设为 `true`。

需要高级映射或其他索引设置时，也可以关闭自动初始化，使用 Elasticsearch 客户端手动建索引。

> 早期版本默认初始化结构，当前版本需要主动启用；升级时应注意这一行为变化。

默认值与可选项见[配置属性](#elasticsearchvector-properties)。也可以通过配置 `ElasticsearchVectorStoreOptions` Bean 设置这些向量存储选项。

此外还需要一个已配置的 [`EmbeddingModel`](/frameworks/spring-ai/models/embedding-model/) Bean，负责计算文档的嵌入向量。

随后可以注入 `VectorStore`，写入文档并执行相似度检索：

```java
@Autowired VectorStore vectorStore;

// ...

List <Document> documents = List.of(
    new Document("Spring AI rocks!! Spring AI rocks!! Spring AI rocks!! Spring AI rocks!! Spring AI rocks!!", Map.of("meta1", "meta1")),
    new Document("The World is Big and Salvation Lurks Around the Corner"),
    new Document("You walk forward facing the past and you turn back toward the future.", Map.of("meta2", "meta2")));

// Add the documents to Elasticsearch
vectorStore.add(documents);

// Retrieve documents similar to a query
List<Document> results = this.vectorStore.similaritySearch(SearchRequest.builder().query("Spring").topK(5).build());
```

<a id="elasticsearchvector-properties"></a>

### 配置属性

通过 Spring Boot 的 `application.yml` 配置实例连接信息和向量存储参数：

```yaml
spring:
  elasticsearch:
    uris: <elasticsearch instance URIs>
    username: <elasticsearch username>
    password: <elasticsearch password>
  ai:
    vectorstore:
      elasticsearch:
        initialize-schema: true
        index-name: custom-index
        dimensions: 1536
        similarity: cosine
```

`spring.elasticsearch.*` 用于配置 Elasticsearch 客户端：

| 属性                                                          | 说明                                                | 默认值                  |
| ------------------------------------------------------------- | --------------------------------------------------- | ----------------------- |
| `spring.elasticsearch.connection-timeout`                     | 与 Elasticsearch 建立连接时的超时时间。             | `1s`                    |
| `spring.elasticsearch.password`                               | Elasticsearch 认证密码。                            | -                       |
| `spring.elasticsearch.username`                               | Elasticsearch 认证用户名。                          | -                       |
| `spring.elasticsearch.uris`                                   | Elasticsearch 实例 URI，多个地址以逗号分隔。        | `http://localhost:9200` |
| `spring.elasticsearch.path-prefix`                            | 添加到每个请求路径前的前缀。                        | -                       |
| `spring.elasticsearch.restclient.sniffer.delay-after-failure` | 失败后安排节点探测的等待时间。                      | `1m`                    |
| `spring.elasticsearch.restclient.sniffer.interval`            | 相邻两次常规节点探测的间隔。                        | `5m`                    |
| `spring.elasticsearch.restclient.ssl.bundle`                  | 使用的 SSL bundle 名称。                            | -                       |
| `spring.elasticsearch.socket-keep-alive`                      | 是否启用客户端与 Elasticsearch 之间的 Socket 保活。 | `false`                 |
| `spring.elasticsearch.socket-timeout`                         | 与 Elasticsearch 通信时的 Socket 超时时间。         | `30s`                   |

`spring.ai.vectorstore.elasticsearch.*` 用于配置 `ElasticsearchVectorStore`：

| 属性                                                       | 说明                       | 默认值                     |
| ---------------------------------------------------------- | -------------------------- | -------------------------- |
| `spring.ai.vectorstore.elasticsearch.initialize-schema`    | 是否初始化所需的索引结构。 | `false`                    |
| `spring.ai.vectorstore.elasticsearch.index-name`           | 保存向量的索引名称。       | `spring-ai-document-index` |
| `spring.ai.vectorstore.elasticsearch.dimensions`           | 向量维度。                 | `1536`                     |
| `spring.ai.vectorstore.elasticsearch.similarity`           | 使用的相似度函数。         | `cosine`                   |
| `spring.ai.vectorstore.elasticsearch.embedding-field-name` | 向量检索使用的字段名。     | `embedding`                |

可用的相似度函数包括：

- `cosine`：默认值，计算向量间的余弦相似度，适合多数场景。
- `l2_norm`：欧几里得距离，距离越小越相似。
- `dot_product`：点积，适合已归一化的向量，例如原文列举的 OpenAI 向量；性能应结合实际数据评估。

各函数的详细说明见 [Elasticsearch dense_vector 文档](https://www.elastic.co/guide/en/elasticsearch/reference/master/dense-vector.html#dense-vector-params)。

<a id="_metadata_filtering"></a>

## 三、元数据过滤（重点掌握）

Elasticsearch 支持统一的、可跨后端复用的[元数据过滤表达式](/frameworks/spring-ai/rag/vector-stores/#metadata-filters)。

可以使用字符串表达式：

```java
vectorStore.similaritySearch(SearchRequest.builder()
        .query("The World")
        .topK(TOP_K)
        .similarityThreshold(SIMILARITY_THRESHOLD)
        .filterExpression("author in ['john', 'jill'] && 'article_type' == 'blog'").build());
```

也可以通过 `Filter.Expression` DSL 构建：

```java
FilterExpressionBuilder b = new FilterExpressionBuilder();

vectorStore.similaritySearch(SearchRequest.builder()
        .query("The World")
        .topK(TOP_K)
        .similarityThreshold(SIMILARITY_THRESHOLD)
        .filterExpression(b.and(
                b.in("author", "john", "jill"),
                b.eq("article_type", "blog")).build()).build());
```

这些通用过滤表达式会自动转换为 Elasticsearch 的 [Query string query](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-query-string-query.html)。例如：

```sql
author in ['john', 'jill'] && 'article_type' == 'blog'
```

会转换为 Elasticsearch 原生过滤格式：

```text
(metadata.author:john OR jill) AND metadata.article_type:blog
```

<a id="_manual_configuration"></a>

## 四、手动配置（参考）

也可以自行创建 Elasticsearch 向量存储。Maven 依赖为：

```xml
<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>spring-ai-elasticsearch-store</artifactId>
</dependency>
```

Gradle 依赖为：

```groovy
dependencies {
    implementation 'org.springframework.ai:spring-ai-elasticsearch-store'
}
```

先创建 Elasticsearch `Rest5Client` Bean。自定义客户端的配置说明见 [Elasticsearch 客户端文档](https://www.elastic.co/guide/en/elasticsearch/client/java-api-client/current/java-rest-low-usage-initialization.html)。

```java
@Bean
public Rest5Client restClient() {
    return Rest5Client.builder(new HttpHost("<host>", 9200, "http"))
        .setDefaultHeaders(new Header[]{
            new BasicHeader("Authorization", "Basic <encoded username and password>")
        })
        .build();
}
```

再通过构建器创建 `ElasticsearchVectorStore` Bean：

```java
@Bean
public VectorStore vectorStore(Rest5Client restClient, EmbeddingModel embeddingModel) {
    ElasticsearchVectorStoreOptions options = new ElasticsearchVectorStoreOptions();
    options.setIndexName("custom-index");    // Optional: defaults to "spring-ai-document-index"
    options.setSimilarity(COSINE);           // Optional: defaults to COSINE
    options.setDimensions(1536);             // Optional: defaults to model dimensions or 1536

    return ElasticsearchVectorStore.builder(restClient, embeddingModel)
        .options(options)                     // Optional: use custom options
        .initializeSchema(true)               // Optional: defaults to false
        .batchingStrategy(new TokenCountBatchingStrategy()) // Optional: defaults to TokenCountBatchingStrategy
        .build();
}

// This can be any EmbeddingModel implementation
@Bean
public EmbeddingModel embeddingModel() {
    return new OpenAiEmbeddingModel(OpenAiEmbeddingOptions.builder().apiKey(System.getenv("OPENAI_API_KEY")).build());
}
```

<a id="_accessing_the_native_client"></a>

## 五、访问原生客户端

通过 `getNativeClient()` 可以取得底层 `ElasticsearchClient`：

```java
ElasticsearchVectorStore vectorStore = context.getBean(ElasticsearchVectorStore.class);
Optional<ElasticsearchClient> nativeClient = vectorStore.getNativeClient();

if (nativeClient.isPresent()) {
    ElasticsearchClient client = nativeClient.get();
    // Use the native client for Elasticsearch-specific operations
}
```

原生客户端适合执行统一 `VectorStore` 接口未暴露的 Elasticsearch 专用操作。

---

来源：[Elasticsearch](https://docs.spring.io/spring-ai/reference/api/vectordbs/elasticsearch.html)，按 Spring AI 2.0.2 文档整理。
