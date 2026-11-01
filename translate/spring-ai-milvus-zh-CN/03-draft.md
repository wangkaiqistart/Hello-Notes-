---
title: Spring AI：Milvus 向量存储
description: Milvus 的准备工作、Spring Boot 自动配置、手动创建、元数据过滤、专用检索参数、配置参考与原生客户端。
sidebar:
  label: Milvus
  order: 3
---

[Milvus](https://milvus.io/) 是开源向量数据库，提供向量索引和相似度检索能力，通过索引算法加速大规模数据集中的相似向量查询。

:::tip[阅读重点]
先完成“启动 Milvus → 配置 EmbeddingModel → 添加 starter 与连接参数 → 写入和检索”。再掌握元数据过滤，以及 `MilvusSearchRequest` 中的原生表达式和 `nprobe`；完整配置表保留作参考。统一的读写与检索接口见[向量存储总览](/frameworks/spring-ai/rag/vector-stores/)。
:::

<a id="_prerequisites"></a>

## 一、准备工作

需要一个正在运行的 Milvus 实例，可选择：

- [Milvus Standalone](https://milvus.io/docs/install_standalone-docker.md)：支持 Docker、Operator、Helm、DEB/RPM 和 Docker Compose 等部署方式。
- [Milvus Cluster](https://milvus.io/docs/install_cluster-milvusoperator.md)：支持 Operator 和 Helm。

还需要配置 [`EmbeddingModel`](/frameworks/spring-ai/models/embedding-model/)，为 `MilvusVectorStore` 中的文档生成嵌入向量；所选提供方要求认证时，应准备对应的 API Key。

<a id="_dependencies"></a>

## 二、依赖与自动配置（重点掌握）

Spring AI 的自动配置模块和 starter 的 artifact 名称经历过调整，旧项目迁移时先查看[升级说明](https://docs.spring.io/spring-ai/reference/upgrade-notes.html)。

在 Maven 项目中添加 Milvus VectorStore starter：

```xml
<dependency>
	<groupId>org.springframework.ai</groupId>
	<artifactId>spring-ai-starter-vector-store-milvus</artifactId>
</dependency>
```

Gradle 项目在 `build.gradle` 中添加：

```groovy
dependencies {
    implementation 'org.springframework.ai:spring-ai-starter-vector-store-milvus'
}
```

按[依赖管理](https://docs.spring.io/spring-ai/reference/getting-started.html#dependency-management)说明引入 Spring AI BOM；Maven Central 或 Snapshot 仓库的配置见[制品仓库](https://docs.spring.io/spring-ai/reference/getting-started.html#artifact-repositories)。

向量存储可以初始化所需的后端结构，但必须显式启用：在手动构建时设置 `initializeSchema`，或在 `application.properties` 中将 `spring.ai.vectorstore.milvus.initialize-schema` 设为 `true`。早期版本默认执行初始化，升级时需要注意这一行为变化。

`MilvusVectorStore` 还需要一个 `EmbeddingModel` 实例来计算文档向量，具体模型接入见 [Embedding 模型](/frameworks/spring-ai/models/embedding-model/)。

通过 Spring Boot 的 `application.yml` 配置实例连接信息和向量存储参数：

```text
spring:
	ai:
		vectorstore:
			milvus:
				client:
					host: "localhost"
					port: 19530
					username: "root"
					password: "milvus"
				databaseName: "default"
				collectionName: "vector_store"
				embeddingDimension: 1536
				indexType: IVF_FLAT
				metricType: COSINE
```

各参数的默认值和可选项见[配置参考](#milvus-properties)。

完成配置后，可注入 `VectorStore` 写入文档并进行相似度检索：

```java
@Autowired VectorStore vectorStore;

// ...

List <Document> documents = List.of(
    new Document("Spring AI rocks!! Spring AI rocks!! Spring AI rocks!! Spring AI rocks!! Spring AI rocks!!", Map.of("meta1", "meta1")),
    new Document("The World is Big and Salvation Lurks Around the Corner"),
    new Document("You walk forward facing the past and you turn back toward the future.", Map.of("meta2", "meta2")));

// Add the documents to Milvus Vector Store
vectorStore.add(documents);

// Retrieve documents similar to a query
List<Document> results = this.vectorStore.similaritySearch(SearchRequest.builder().query("Spring").topK(5).build());
```

<a id="_manual_configuration"></a>

### 手动创建

也可以自行配置 `MilvusVectorStore`。添加底层实现依赖：

```xml
<dependency>
	<groupId>org.springframework.ai</groupId>
	<artifactId>spring-ai-milvus-store</artifactId>
</dependency>
```

依赖版本仍通过 [Spring AI BOM](https://docs.spring.io/spring-ai/reference/getting-started.html#dependency-management) 统一管理。

下面展示向量存储和 `MilvusServiceClient` 的创建方式：

```java
	@Bean
	public VectorStore vectorStore(MilvusServiceClient milvusClient, EmbeddingModel embeddingModel) {
		return MilvusVectorStore.builder(milvusClient, embeddingModel)
				.collectionName("test_vector_store")
				.databaseName("default")
				.indexType(IndexType.IVF_FLAT)
				.metricType(MetricType.COSINE)
				.batchingStrategy(new TokenCountBatchingStrategy())
				.initializeSchema(true)
				.build();
	}

	@Bean
	public MilvusServiceClient milvusClient() {
		return new MilvusServiceClient(ConnectParam.newBuilder()
			.withAuthorization("minioadmin", "minioadmin")
			.withUri(milvusContainer.getEndpoint())
			.build());
	}
```

<a id="_metadata_filtering"></a>

## 三、元数据过滤（重点掌握）

Milvus 支持 Spring AI 通用的[元数据过滤表达式](/frameworks/spring-ai/rag/vector-stores/#metadata-filters)，可以使用字符串 DSL：

```java
vectorStore.similaritySearch(
    SearchRequest.builder()
    .query("The World")
    .topK(TOP_K)
    .similarityThreshold(SIMILARITY_THRESHOLD)
    .filterExpression("author in ['john', 'jill'] && article_type == 'blog'").build());
```

也可以通过 `Filter.Expression` DSL 构建：

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

这些表达式会转换为等价的 Milvus 过滤条件。

检索结果中的数值元数据通过 Gson 反序列化：整数返回 `Long`，小数返回 `Double`。原有代码若把整数元数据直接强制转换为 `Double`，应改用 `Long` 或通用的 `Number` 类型。

<a id="_using_milvussearchrequest"></a>

## 四、使用 MilvusSearchRequest

`MilvusSearchRequest` 扩展 `SearchRequest`，增加 Milvus 专用的原生过滤表达式和 JSON 检索参数：

```java
MilvusSearchRequest request = MilvusSearchRequest.milvusBuilder()
    .query("sample query")
    .topK(5)
    .similarityThreshold(0.7)
    .nativeExpression("metadata[\"age\"] > 30") // Overrides filterExpression if both are set
    .filterExpression("age <= 30") // Ignored if nativeExpression is set
    .searchParamsJson("{\"nprobe\":128}")
    .build();
List results = vectorStore.similaritySearch(request);
```

当 `nativeExpression` 和通用的 `filterExpression` 同时设置时，**优先使用 `nativeExpression`**。该接口适合需要利用 Milvus 专用检索能力的场景。

<a id="_importance_of_nativeexpression_and_searchparamsjson_in_milvussearchrequest"></a>

## 五、nativeExpression 与 searchParamsJson（重点掌握）

这两个参数分别控制原生过滤与索引检索行为。

**`nativeExpression`** 使用 Milvus 原生语法表达过滤条件，可覆盖通用 DSL 尚未暴露的能力。语法见 [Milvus Filtering](https://milvus.io/docs/boolean.md)。

```java
MilvusSearchRequest request = MilvusSearchRequest.milvusBuilder()
    .query("sample query")
    .topK(5)
    .nativeExpression("metadata['category'] == 'science'")
    .build();
```

**`searchParamsJson`** 用于传入索引相关的检索参数，尤其需要关注默认 `IVF_FLAT` 索引的 `nprobe`，索引说明见 [Milvus Vector Index](https://milvus.io/docs/index.md?tab=floating)。

原文指出，未指定时 `nprobe` 默认值为 `1`，可能造成召回率较低，甚至没有检索结果。应根据索引与数据规模调整，不要只关注 `topK`。

```java
MilvusSearchRequest request = MilvusSearchRequest.milvusBuilder()
    .query("sample query")
    .topK(5)
    .searchParamsJson("{\"nprobe\":128}")
    .build();
```

`nativeExpression` 负责更具体的条件过滤；`searchParamsJson` 用于调整检索行为，避免过低的 `nprobe` 影响召回效果。

<a id="milvus-properties"></a>

## 六、配置参考

在 Spring Boot 配置中使用以下属性定制 Milvus 向量存储。

| 属性                                                        | 说明                                                                                                          | 默认值           |
| ----------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- | ---------------- |
| `spring.ai.vectorstore.milvus.database-name`                | 使用的 Milvus 数据库名称。                                                                                    | `default`        |
| `spring.ai.vectorstore.milvus.collection-name`              | 保存向量的集合名称。                                                                                          | `vector_store`   |
| `spring.ai.vectorstore.milvus.partition-name`               | 已存在的 Milvus 分区名称，限定写入、删除和查询的操作范围。未设置或为空时使用 Milvus 默认行为。                | -                |
| `spring.ai.vectorstore.milvus.initialize-schema`            | 是否初始化 Milvus 后端结构。                                                                                  | `false`          |
| `spring.ai.vectorstore.milvus.embedding-dimension`          | 集合中存储的向量维度。                                                                                        | `1536`           |
| `spring.ai.vectorstore.milvus.index-type`                   | 集合的索引类型。                                                                                              | `IVF_FLAT`       |
| `spring.ai.vectorstore.milvus.metric-type`                  | 集合使用的距离或相似度度量。                                                                                  | `COSINE`         |
| `spring.ai.vectorstore.milvus.index-parameters`             | 创建集合索引时使用的参数。                                                                                    | `{"nlist":1024}` |
| `spring.ai.vectorstore.milvus.id-field-name`                | 集合中的 ID 字段名称。                                                                                        | `doc_id`         |
| `spring.ai.vectorstore.milvus.auto-id`                      | ID 字段是否使用自动生成的 ID。                                                                                | `false`          |
| `spring.ai.vectorstore.milvus.content-field-name`           | 正文字段名称。                                                                                                | `content`        |
| `spring.ai.vectorstore.milvus.metadata-field-name`          | 元数据字段名称。                                                                                              | `metadata`       |
| `spring.ai.vectorstore.milvus.embedding-field-name`         | 向量字段名称。                                                                                                | `embedding`      |
| `spring.ai.vectorstore.milvus.client.host`                  | Milvus 主机名称或地址。                                                                                       | `localhost`      |
| `spring.ai.vectorstore.milvus.client.port`                  | 连接端口。                                                                                                    | `19530`          |
| `spring.ai.vectorstore.milvus.client.uri`                   | Milvus 实例的 URI。                                                                                           | -                |
| `spring.ai.vectorstore.milvus.client.token`                 | 用于身份识别和认证的 Token。                                                                                  | -                |
| `spring.ai.vectorstore.milvus.client.connect-timeout-ms`    | 客户端通道的连接超时时间，必须大于 `0`，单位毫秒。                                                            | `10000`          |
| `spring.ai.vectorstore.milvus.client.keep-alive-time-ms`    | 客户端通道的保活间隔，必须大于 `0`，单位毫秒。                                                                | `55000`          |
| `spring.ai.vectorstore.milvus.client.keep-alive-timeout-ms` | 客户端通道的保活超时时间，必须大于 `0`，单位毫秒。                                                            | `20000`          |
| `spring.ai.vectorstore.milvus.client.rpc-deadline-ms`       | 等待服务端响应的截止时间，必须大于或等于 `0`。设置后，网络波动引起 RPC 快速失败时，客户端会在截止期限内等待。 | `0`              |
| `spring.ai.vectorstore.milvus.client.client-key-path`       | TLS 双向认证使用的 `client.key` 路径，仅在 `secure=true` 时生效。                                             | -                |
| `spring.ai.vectorstore.milvus.client.client-pem-path`       | TLS 双向认证使用的 `client.pem` 路径，仅在 `secure=true` 时生效。                                             | -                |
| `spring.ai.vectorstore.milvus.client.ca-pem-path`           | TLS 双向认证使用的 `ca.pem` 路径，仅在 `secure=true` 时生效。                                                 | -                |
| `spring.ai.vectorstore.milvus.client.server-pem-path`       | TLS 单向认证使用的 `server.pem` 路径，仅在 `secure=true` 时生效。                                             | -                |
| `spring.ai.vectorstore.milvus.client.server-name`           | 覆盖 SSL 主机名校验使用的目标名称，仅在 `secure=true` 时生效；该值会传给 `grpc.ssl_target_name_override`。    | -                |
| `spring.ai.vectorstore.milvus.client.secure`                | 是否为连接启用 TLS。                                                                                          | `false`          |
| `spring.ai.vectorstore.milvus.client.idle-timeout-ms`       | 客户端通道空闲超时时间，必须大于 `0`。                                                                        | `24h`            |
| `spring.ai.vectorstore.milvus.client.username`              | 连接用户名。                                                                                                  | `root`           |
| `spring.ai.vectorstore.milvus.client.password`              | 连接密码。                                                                                                    | `milvus`         |

<a id="_starting_milvus_store"></a>

## 七、启动 Milvus

原文以其项目的 `src/test/resources/` 目录为起点，在包含 Compose 配置的目录运行：

```bash
docker-compose up
```

清理环境使用：

```bash
docker-compose down; rm -Rf ./volumes
```

随后可连接 Milvus 服务端点 [http://localhost:19530](http://localhost:19530)。[http://localhost:9001](http://localhost:9001) 是配套存储服务的管理入口，示例用户名和密码均为 `minioadmin`。

<a id="_troubleshooting"></a>

## 八、排查资源问题

原文在 Docker 提示资源问题时列出了以下清理命令：

```bash
docker system prune --all --force --volumes
```

<a id="_accessing_the_native_client"></a>

## 九、访问原生客户端

通过 `getNativeClient()` 可以取得底层 `MilvusServiceClient`：

```java
MilvusVectorStore vectorStore = context.getBean(MilvusVectorStore.class);
Optional<MilvusServiceClient> nativeClient = vectorStore.getNativeClient();

if (nativeClient.isPresent()) {
    MilvusServiceClient client = nativeClient.get();
    // Use the native client for Milvus-specific operations
}
```

原生客户端适合执行统一 `VectorStore` 接口未暴露的 Milvus 专用操作。

---

来源：[Milvus](https://docs.spring.io/spring-ai/reference/api/vectordbs/milvus.html)，按 Spring AI 2.0.2 文档整理。
