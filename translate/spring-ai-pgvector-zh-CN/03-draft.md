---
title: Spring AI：PGvector 向量存储
description: 使用 PostgreSQL 与 PGvector 完成向量写入、相似度检索和元数据过滤，保留完整配置、手动构建与本地运行参考。
sidebar:
  label: PGvector
  order: 2
---

`PgVectorStore` 将文档的嵌入向量保存在 PostgreSQL 中，并提供相似度检索。

[PGvector](https://github.com/pgvector/pgvector) 是 PostgreSQL 的开源扩展，支持存储和检索机器学习模型生成的向量，提供精确近邻与近似近邻检索，并可结合 PostgreSQL 的索引、查询等功能使用。

:::tip[阅读重点]
先准备数据库和 Embedding 模型，再通过 starter 接入并完成一次写入、检索与过滤。索引、距离度量、维度和初始化配置是重点；手动构建与原生客户端作为后续参考。统一接口见[向量存储总览](/frameworks/spring-ai/rag/vector-stores/)。
:::

<a id="_prerequisites"></a>

## 一、准备工作

准备可访问的 PostgreSQL 实例，并启用 `vector`、`hstore` 和 `uuid-ossp` 扩展。

可以通过 [Docker Compose](https://docs.spring.io/spring-ai/reference/api/docker-compose.html) 或 [Testcontainers](https://docs.spring.io/spring-ai/reference/api/testcontainers.html)，将 PGvector 作为 Spring Boot 开发服务运行。也可以参考[本地运行](#_run_postgres_pgvector_db_locally)，直接启动 Docker 容器。

显式启用结构初始化后，`PgVectorStore` 会在启动时尝试安装所需扩展；若表与索引不存在，则创建 `vector_store` 表及索引。也可以手动准备：

```text
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS hstore;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS vector_store (
	id uuid DEFAULT uuid_generate_v4() PRIMARY KEY,
	content text,
	metadata json,
	embedding vector(1536) // 1536 is the default embedding dimension
);

CREATE INDEX ON vector_store USING HNSW (embedding vector_cosine_ops);
```

将 `1536` 替换为实际 Embedding 模型的输出维度。原文说明 PGvector 的 HNSW 索引最多支持 2000 维。

还需要一个[Embedding 模型](/frameworks/spring-ai/models/embedding-model/)，用于生成写入 `PgVectorStore` 的向量；模型提供方要求认证时，需准备相应 API Key。

<a id="_auto_configuration"></a>

## 二、自动配置（重点）

Spring AI 曾调整自动配置和 starter 的模块名称，迁移旧项目时应检查[升级说明](https://docs.spring.io/spring-ai/reference/upgrade-notes.html)。

在 Maven 项目中添加 PGvector starter：

```xml
<dependency>
	<groupId>org.springframework.ai</groupId>
	<artifactId>spring-ai-starter-vector-store-pgvector</artifactId>
</dependency>
```

Gradle 项目在 `build.gradle` 中添加：

```groovy
dependencies {
    implementation 'org.springframework.ai:spring-ai-starter-vector-store-pgvector'
}
```

向量存储可以初始化所需数据库结构，但需要主动启用 `initializeSchema`，或在 `application.properties` 中设置 `spring.ai.vectorstore.pgvector.initialize-schema=true`。

:::note[初始化默认关闭]
早期版本会默认初始化结构；当前版本需要显式启用，这是与旧版不同的行为。
:::

还需要一个 `EmbeddingModel` Bean 来计算文档向量，可在[Embedding 模型](/frameworks/spring-ai/models/embedding-model/)中了解接口与选型。以 [OpenAI EmbeddingModel](https://docs.spring.io/spring-ai/reference/api/embeddings/openai-embeddings.html) 为例，添加以下依赖：

```xml
<dependency>
	<groupId>org.springframework.ai</groupId>
	<artifactId>spring-ai-starter-model-openai</artifactId>
</dependency>
```

对应的 Gradle 配置：

```groovy
dependencies {
    implementation 'org.springframework.ai:spring-ai-starter-model-openai'
}
```

通过[依赖管理](https://docs.spring.io/spring-ai/reference/getting-started.html#dependency-management)引入 Spring AI BOM；Maven Central 与 Snapshot 仓库的配置见[构件仓库](https://docs.spring.io/spring-ai/reference/getting-started.html#artifact-repositories)。

在 Spring Boot 的 `application.yml` 中设置数据库连接与 PGvector 参数：

```text
spring:
  datasource:
    url: jdbc:postgresql://localhost:5432/postgres
    username: postgres
    password: postgres
  ai:
	vectorstore:
	  pgvector:
		index-type: HNSW
		distance-type: COSINE_DISTANCE
		dimensions: 1536
		max-document-batch-size: 10000 # Optional: Maximum number of documents per batch
```

通过 Spring Boot 的 [Docker Compose 开发服务](https://docs.spring.io/spring-boot/reference/features/dev-services.html#features.dev-services.docker-compose)或 [Testcontainers 开发服务](https://docs.spring.io/spring-boot/reference/features/dev-services.html#features.dev-services.testcontainers)运行 PGvector 时，URL、用户名和密码由 Spring Boot 自动配置，无需重复填写。

各项默认值与可选配置见下方[配置属性](#pgvector-properties)。

完成配置后，即可注入 `VectorStore`，写入文档并执行相似度检索：

```java
@Autowired VectorStore vectorStore;

// ...

List<Document> documents = List.of(
    new Document("Spring AI rocks!! Spring AI rocks!! Spring AI rocks!! Spring AI rocks!! Spring AI rocks!!", Map.of("meta1", "meta1")),
    new Document("The World is Big and Salvation Lurks Around the Corner"),
    new Document("You walk forward facing the past and you turn back toward the future.", Map.of("meta2", "meta2")));

// Add the documents to PGVector
vectorStore.add(documents);

// Retrieve documents similar to a query
List<Document> results = this.vectorStore.similaritySearch(SearchRequest.builder().query("Spring").topK(5).build());
```

<a id="pgvector-properties"></a>

### 配置属性

以下属性用于定制 PGvector 向量存储。

| 属性                                                                | 说明                                                                                                                                                                                                                                                                                       | 默认值          |
| ------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------- |
| `spring.ai.vectorstore.pgvector.index-type`                         | 近邻索引类型。`NONE`：精确近邻检索；`IVFFlat`：将向量分成多个列表，只搜索最接近查询向量的部分列表，构建更快、内存占用更低，但速度与召回率的取舍通常不如 HNSW；`HNSW`：构建多层图，构建较慢、占用内存较多，但查询表现通常更好。HNSW 不需要 IVFFlat 那样的训练步骤，因此可在空表上创建索引。 | HNSW            |
| `spring.ai.vectorstore.pgvector.distance-type`                      | 检索距离度量，默认 `COSINE_DISTANCE`。若向量已归一化为单位长度，也可考虑 `EUCLIDEAN_DISTANCE` 或 `NEGATIVE_INNER_PRODUCT`，结合实际数据评估性能。                                                                                                                                          | COSINE_DISTANCE |
| `spring.ai.vectorstore.pgvector.dimensions`                         | 向量维度。未显式设置时，从 `EmbeddingModel` 获取；建表时确定向量列维度。修改维度后，也需要重新创建 `vector_store` 表。                                                                                                                                                                     | -               |
| `spring.ai.vectorstore.pgvector.remove-existing-vector-store-table` | 启动时是否删除已有的 `vector_store` 表。                                                                                                                                                                                                                                                   | false           |
| `spring.ai.vectorstore.pgvector.initialize-schema`                  | 是否初始化所需数据库结构。                                                                                                                                                                                                                                                                 | false           |
| `spring.ai.vectorstore.pgvector.schema-name`                        | 向量存储使用的数据库模式（schema）。                                                                                                                                                                                                                                                       | `public`        |
| `spring.ai.vectorstore.pgvector.table-name`                         | 向量存储表名。                                                                                                                                                                                                                                                                             | `vector_store`  |
| `spring.ai.vectorstore.pgvector.schema-validation`                  | 是否校验数据库模式与表名，确认名称有效且对应对象存在。                                                                                                                                                                                                                                     | false           |
| `spring.ai.vectorstore.pgvector.max-document-batch-size`            | 每个批次最多处理的文档数。                                                                                                                                                                                                                                                                 | 10000           |

自定义 schema 或表名时，可设置 `spring.ai.vectorstore.pgvector.schema-validation=true`，检查名称及对象，降低 SQL 注入风险。

<a id="_metadata_filtering"></a>

## 三、元数据过滤（重点）

PGvector 支持统一的、可跨后端复用的[元数据过滤语法](/frameworks/spring-ai/rag/vector-stores/#metadata-filters)。

可以直接传入字符串表达式：

```java
vectorStore.similaritySearch(
    SearchRequest.builder()
    .query("The World")
    .topK(TOP_K)
    .similarityThreshold(SIMILARITY_THRESHOLD)
    .filterExpression("author in ['john', 'jill'] && article_type == 'blog'").build());
```

也可以通过 `Filter.Expression` DSL 构建相同条件：

```java
FilterExpressionBuilder b = new FilterExpressionBuilder();

vectorStore.similaritySearch(SearchRequest.builder()
    .query("The World")
    .topK(TOP_K)
    .similarityThreshold(SIMILARITY_THRESHOLD)
    .filterExpression(b.and(
        b.in("author","john", "jill"),
        b.eq("article_type", "blog")).build()).build());
```

这些表达式会被转换为 PostgreSQL JSON path 表达式，用于过滤文档元数据。

<a id="_manual_configuration"></a>

## 四、手动配置（参考）

也可以手动创建 `PgVectorStore`。先添加 PostgreSQL 连接、`JdbcTemplate` 自动配置及 PGvector 存储依赖：

```xml
<dependency>
	<groupId>org.springframework.boot</groupId>
	<artifactId>spring-boot-starter-jdbc</artifactId>
</dependency>

<dependency>
	<groupId>org.postgresql</groupId>
	<artifactId>postgresql</artifactId>
	<scope>runtime</scope>
</dependency>

<dependency>
	<groupId>org.springframework.ai</groupId>
	<artifactId>spring-ai-pgvector-store</artifactId>
</dependency>
```

仍需通过[依赖管理](https://docs.spring.io/spring-ai/reference/getting-started.html#dependency-management)引入 Spring AI BOM。

将 `JdbcTemplate` 和 `EmbeddingModel` 传给构建器：

```java
@Bean
public VectorStore vectorStore(JdbcTemplate jdbcTemplate, EmbeddingModel embeddingModel) {
    return PgVectorStore.builder(jdbcTemplate, embeddingModel)
        .dimensions(1536)                    // Optional: defaults to model dimensions or 1536
        .distanceType(COSINE_DISTANCE)       // Optional: defaults to COSINE_DISTANCE
        .indexType(HNSW)                     // Optional: defaults to HNSW
        .initializeSchema(true)              // Optional: defaults to false
        .schemaName("public")                // Optional: defaults to "public"
        .vectorTableName("vector_store")     // Optional: defaults to "vector_store"
        .maxDocumentBatchSize(10000)         // Optional: defaults to 10000
        .build();
}
```

<a id="_run_postgres_pgvector_db_locally"></a>

## 五、本地运行 PostgreSQL 与 PGvector

使用 Docker 启动：

```text
docker run -it --rm --name postgres -p 5432:5432 -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres pgvector/pgvector
```

使用 `psql` 连接该实例：

```text
psql -U postgres -h localhost -p 5432
```

<a id="_accessing_the_native_client"></a>

## 六、访问原生客户端（参考）

`PgVectorStore.getNativeClient()` 可返回底层 JDBC 客户端 `JdbcTemplate`：

```java
PgVectorStore vectorStore = context.getBean(PgVectorStore.class);
Optional<JdbcTemplate> nativeClient = vectorStore.getNativeClient();

if (nativeClient.isPresent()) {
    JdbcTemplate jdbc = nativeClient.get();
    // Use the native client for PostgreSQL-specific operations
}
```

需要使用统一 `VectorStore` 接口未暴露的 PostgreSQL 功能时，可以通过该客户端执行原生操作。

---

来源：[PGvector](https://docs.spring.io/spring-ai/reference/api/vectordbs/pgvector.html)，按 Spring AI 2.0.2 文档整理。
