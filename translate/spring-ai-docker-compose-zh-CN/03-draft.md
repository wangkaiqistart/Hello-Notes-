# Docker Compose

Spring AI 提供 Spring Boot 自动配置，用于连接通过 Docker Compose 运行的模型服务或向量存储。在 Maven 项目的 `pom.xml` 中添加：

```xml
<dependency>
   <groupId>org.springframework.ai</groupId>
   <artifactId>spring-ai-spring-boot-docker-compose</artifactId>
</dependency>
```

Gradle 项目在 `build.gradle` 中添加：

```groovy
dependencies {
    implementation 'org.springframework.ai:spring-ai-spring-boot-docker-compose'
}
```

通过 [依赖管理](/frameworks/spring-ai/getting-started/quickstart/#使用-bom-管理版本)引入 Spring AI BOM。

<a id="_service_connections"></a>

## 服务连接

`spring-ai-spring-boot-docker-compose` 模块提供以下服务连接工厂：

| 连接信息类型                           | 匹配的镜像                                                              |
| -------------------------------------- | ----------------------------------------------------------------------- |
| `AwsOpenSearchConnectionDetails`       | `localstack/localstack`                                                 |
| `ChromaConnectionDetails`              | `chromadb/chroma`、`ghcr.io/chroma-core/chroma`                         |
| `MilvusServiceClientConnectionDetails` | `milvusdb/milvus`                                                       |
| `OllamaConnectionDetails`              | `ollama/ollama`                                                         |
| `OpenSearchConnectionDetails`          | `opensearchproject/opensearch`                                          |
| `QdrantConnectionDetails`              | `qdrant/qdrant`                                                         |
| `TypesenseConnectionDetails`           | `typesense/typesense`                                                   |
| `WeaviateConnectionDetails`            | `semitechnologies/weaviate`、`cr.weaviate.io/semitechnologies/weaviate` |
| `McpSseClientConnectionDetails`        | `docker/mcp-gateway`                                                    |

Spring Boot 的 `spring-boot-docker-compose` 模块还提供更多服务连接。完整清单见 [Docker Compose Support](https://docs.spring.io/spring-boot/reference/features/dev-services.html#features.dev-services.docker-compose)。
