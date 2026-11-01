---
title: Spring AI：S3 向量存储
description: 使用 AWS S3 Vectors 保存文档向量，完成相似度检索、元数据过滤和删除，并了解客户端、索引与存储桶配置。
sidebar:
  label: S3 Vector Store
  order: 5
---

`S3VectorStore` 用于存储文档的嵌入向量，并执行相似度检索。

[AWS S3 Vectors](https://aws.amazon.com/s3/features/vectors/) 提供无服务器的向量存储与查询能力，可扩展到大规模数据。这里接入的是 **S3 Vectors 专用服务、向量存储桶与索引**，需要相应的 API 和资源，不是将普通 S3 对象直接当作向量数据库。

[S3 Vectors API](https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-vectors.html) 在 S3 的基础上提供向量数据库能力：

- 通过专用向量记录保存向量及其关联元数据；Spring AI 将元数据转换为 AWS SDK 的 `Document`。
- 读取向量。
- 执行向量检索。

:::tip[阅读重点]
先理解向量存储桶、索引、区域和 AWS 凭据，再配置 `S3VectorsClient` 与 `EmbeddingModel`，完成写入和检索。过滤删除在客户端遍历全索引，数据量大时应重点评估代价。统一接口见[向量存储总览](/frameworks/spring-ai/rag/vector-stores/)。
:::

<a id="_prerequisites"></a>

## 一、准备工作

需要准备：

- 一个 S3 Vectors 向量存储桶，创建方法见 [How to create S3 Vector Bucket](https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-vectors-buckets-create.html)。
- 向量桶中已创建的索引，维度与所用模型输出一致，并选择合适的距离度量。此版本的 `afterPropertiesSet()` 不负责创建桶或索引，也没有通用的 `initialize-schema` 初始化开关。
- 一个计算文档向量的 [`EmbeddingModel`](/frameworks/spring-ai/models/embedding-model/)。如果所选模型提供方要求认证，还需准备对应 API Key。

<a id="_auto_configuration"></a>

## 二、自动配置（重点掌握）

Spring AI 提供 S3 向量存储的 Spring Boot 自动配置。在 Maven `pom.xml` 中添加：

```xml
<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>spring-ai-starter-vector-store-s3</artifactId>
</dependency>
```

使用 Gradle 时，在 `build.gradle` 中添加：

```groovy
dependencies {
    implementation 'org.springframework.ai:spring-ai-starter-vector-store-s3'
}
```

通过[依赖管理](/frameworks/spring-ai/getting-started/quickstart/#使用-bom-管理版本)引入 Spring AI BOM；Maven Central 或 Snapshot 仓库的设置见[制品仓库](/frameworks/spring-ai/getting-started/quickstart/#配置依赖仓库)。

默认值和可配置项见[配置属性](#s3-properties)。还需要配置一个 [`EmbeddingModel`](/frameworks/spring-ai/models/embedding-model/) Bean，负责计算文档向量。

完成配置后，可以注入 `VectorStore` 写入文档并进行相似度检索。文档读取、切分及元数据准备见 [ETL 管道](/frameworks/spring-ai/rag/document-ingestion/)，统一检索参数见 [SearchRequest](/frameworks/spring-ai/rag/vector-stores/#_searchrequest_builder)：

```java
@Autowired VectorStore vectorStore;

// ...

List <Document> documents = List.of(
    new Document("Spring AI rocks!! Spring AI rocks!! Spring AI rocks!! Spring AI rocks!! Spring AI rocks!!", Map.of("meta1", "meta1")),
    new Document("The World is Big and Salvation Lurks Around the Corner"),
    new Document("You walk forward facing the past and you turn back toward the future.", Map.of("meta2", "meta2")));

// Add the documents to S3 Vector Store Bucket
vectorStore.add(documents);

// Retrieve documents similar to a query
List<Document> results = this.vectorStore.similaritySearch(SearchRequest.builder().query("Spring").topK(5).build());
```

<a id="s3-properties"></a>

### 配置属性

连接 AWS S3 Vectors 时，需要自行提供 `S3VectorsClient` Bean，并为客户端配置正确的 AWS 凭据和区域（Region）。客户端示例见[手动配置](#_manual_configuration)；使用 starter 时只需提供该客户端及模型 Bean，不必重复声明 `S3VectorStore`。

`spring.ai.vectorstore.s3.*` 用于配置 `S3VectorStore`：

| 属性                                          | 说明                                                              | 默认值 |
| --------------------------------------------- | ----------------------------------------------------------------- | ------ |
| `spring.ai.vectorstore.s3.index-name`         | 已有向量索引名称，必须配置。原文以 `spring-ai-index` 为例。       | 无     |
| `spring.ai.vectorstore.s3.vector-bucket-name` | 已有向量桶名称，必须配置。原文以 `my-vector-bucket-on-aws` 为例。 | 无     |

两个属性在 v2.0.2 的属性类中都没有默认值，自动配置会校验它们是否非空；上面的示例名称不会自动创建 AWS 资源。

:::note[接入 RAG 前先看当前适配边界]
按 [v2.0.2 的 S3VectorStore 源码](https://github.com/spring-projects/spring-ai/blob/v2.0.2/vector-stores/spring-ai-s3-vector-store/src/main/java/org/springframework/ai/vectorstore/s3/S3VectorStore.java)，写入时保存的是向量键、向量数据和元数据，**不会自动保存原始文档正文**。检索结果的 `Document.text` 是向量键，原始 ID 和 `Document.score` 也未还原；距离放在元数据 `SPRING_AI_S3_DISTANCE` 中。

因此，接入 [RAG Advisor](/frameworks/spring-ai/rag/retrieval-and-generation/#_advisors) 前，应通过向量键或元数据中的业务标识回查正文，再交给生成模型。不能直接把此处的返回文本当作原文片段。该版本也未应用 `SearchRequest.similarityThreshold`；下文保留该通用参数示例，实际阈值筛选需要应用自行处理，并按索引距离度量确定规则。
:::

<a id="_metadata_filtering"></a>

## 三、元数据过滤（重点掌握）

S3 向量存储支持统一的、可跨后端复用的[元数据过滤](/frameworks/spring-ai/rag/vector-stores/#metadata-filters)。

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

这些表达式会自动转换为 [AWS SDK for Java V2 的过滤 Document 对象](https://sdk.amazonaws.com/java/api/latest/software/amazon/awssdk/core/document/Document.html)。例如：

```sql
country in ['UK', 'NL'] && year >= 2020
```

会转换为 S3 Vectors 的过滤格式：

```json
{ "$and": [{ "country": { "$in": ["UK", "NL"] } }, { "year": { "$gte": 2020 } }] }
```

<a id="_filter_based_deletion"></a>

### 按过滤条件删除

统一删除接口及文档版本管理见[向量存储的删除参考](/frameworks/spring-ai/rag/vector-stores/#_deleting_documents_from_vector_store)。可以直接传入字符串过滤条件删除文档：

```java
vectorStore.delete("country in ['UK', 'NL'] && year >= 2020");
```

也可以使用程序化表达式：

```java
FilterExpressionBuilder b = new FilterExpressionBuilder();

vectorStore.delete(b.and(
        b.in("country", "UK", "NL"),
        b.gte("year", 2020)).build());
```

S3 Vectors 没有服务端的“按过滤条件删除”API。Spring AI 会按每页 500 条列出索引中的全部向量，在客户端逐条判断过滤条件，再删除匹配项。因此，大索引的过滤删除成本与向量总量成正比，不能把它当作仅扫描命中文档的后端操作。

<a id="_manual_configuration"></a>

## 四、手动配置（参考）

也可以自行创建 S3 向量存储。先引入 `spring-ai-s3-vector-store`：

```xml
<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>spring-ai-s3-vector-store</artifactId>
</dependency>
```

Gradle 写法：

```groovy
dependencies {
    implementation 'org.springframework.ai:spring-ai-s3-vector-store'
}
```

先创建客户端，再通过构建器创建 `S3VectorStore`。下面的 `S3VectorsClient` 和 `Region` 来自 AWS SDK for Java V2；`AWS_REGION` 指向已有资源所在区域，凭据使用 SDK 默认凭据提供链。两个 `spring.ai.vectorstore.s3.*` 属性填入真实资源名称。

示例同时展示手动创建 OpenAI 模型：需有对应模型依赖和 `OPENAI_API_KEY`；已有自动配置的 `EmbeddingModel` 时直接注入，不必重复声明模型 Bean。过滤转换器默认是 `S3VectorFilterSearchExpressionConverter`，需要定制时实现 `S3VectorFilterExpressionConverter` 并传给构建器：

```java
@Bean(destroyMethod = "close")
public S3VectorsClient s3VectorsClient(@Value("${AWS_REGION}") String region) {
    return S3VectorsClient.builder()
        .region(Region.of(region))
        .build(); // Uses the AWS SDK default credentials provider chain
}

@Bean
public VectorStore s3VectorStore(S3VectorsClient s3VectorsClient, EmbeddingModel embeddingModel,
        @Value("${spring.ai.vectorstore.s3.index-name}") String indexName,
        @Value("${spring.ai.vectorstore.s3.vector-bucket-name}") String vectorBucketName) {
    return new S3VectorStore.Builder(s3VectorsClient, embeddingModel)
        .indexName(indexName)
        .vectorBucketName(vectorBucketName)
        // Optional: replace with your S3VectorFilterExpressionConverter implementation
        .filterExpressionConverter(new S3VectorFilterSearchExpressionConverter())
        .build();
}

@Bean
public EmbeddingModel embeddingModel() {
    // Reads OPENAI_API_KEY through the default OpenAI client setup
    return OpenAiEmbeddingModel.builder().build();
}
```

<a id="_accessing_the_native_client"></a>

## 五、访问原生客户端

通过 `getNativeClient()` 可以取得底层 `S3VectorsClient`：

```java
S3VectorStore vectorStore = context.getBean(S3VectorStore.class);
Optional<S3VectorsClient> nativeClient = vectorStore.getNativeClient();

if (nativeClient.isPresent()) {
    S3VectorsClient s3Client = nativeClient.get();
    // Use the native client for S3-Vector-Store-specific operations
}
```

原生客户端适合执行统一 `VectorStore` 接口未暴露的 S3 Vectors 专用操作。

---

来源：[S3 Vector Store](https://docs.spring.io/spring-ai/reference/api/vectordbs/s3-vector-store.html)，按 Spring AI 2.0.2 文档翻译。示例尚未连接 AWS 或模型运行验证。
