---
title: Spring AI：Docker Compose 开发服务
description: 使用 Docker Compose 启动开发依赖，自动获取模型或向量库连接信息，含完整服务连接清单和 PGvector 配置示例。
sidebar:
  label: Docker Compose 开发服务
  order: 2
---

Spring AI 提供 Spring Boot 自动配置，用于连接通过 Docker Compose 运行的模型服务或向量存储。

开发时，将容器定义写入 `compose.yml`，Spring Boot 可以启动这些容器，并根据镜像生成**服务连接信息（Connection Details）**，供相应的自动配置使用。

:::tip[阅读重点]
先掌握“启动开发依赖 → 识别服务 → 自动配置连接”的流程，再看 [PGvector 示例](#pgvector-example)。完整镜像匹配清单保留在[服务连接](#_service_connections)中，需要其他后端时再查。
:::

## 一、添加依赖

在 Maven 项目的 `pom.xml` 中添加：

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

通过 [Spring AI BOM](/frameworks/spring-ai/getting-started/quickstart/#使用-bom-管理版本)管理版本。还要添加实际使用的模型或向量存储 starter，具体见 [Embedding 模型](/frameworks/spring-ai/models/embedding-model/)与[向量存储实现](/frameworks/spring-ai/rag/vector-stores/#_vectorstore_implementations)。

此模块扩展 Spring Boot 的 Docker Compose 支持，并传递引入 `spring-boot-docker-compose`。只需要 Boot 内置服务连接时，也可以直接按 Boot 文档引入该模块。

<a id="service-connection-lifecycle"></a>

## 二、运行流程与连接信息（补充说明）

本机需要可用的 Docker 环境，并能在命令行调用 `docker` 和 `docker compose`；Spring Boot 文档要求 Docker Compose 至少为 `2.2.0`。

默认流程是：

1. 在应用的工作目录查找 `compose.yml` 等常见 Compose 文件。
2. 应用启动时执行 `docker compose up`。
3. 根据受支持的镜像创建连接信息，使用**容器映射到宿主机的端口**，而不是假定宿主机端口等于容器内部端口。
4. 对应自动配置使用连接信息建立客户端；连接信息优先于相关的连接属性。
5. 应用关闭时执行 `docker compose stop`。如果服务在应用启动前已经运行，Boot 只创建连接信息，不重复启动，也不在应用关闭时停止这些服务。

匹配依据是**镜像名称**，不是 `services:` 下的服务名或 `container_name`。使用自定义镜像时，可通过 `org.springframework.boot.service-connection` 标签声明它兼容的服务类型。

<a id="_service_connections"></a>

## 三、服务连接（完整参考）

`spring-ai-spring-boot-docker-compose` 提供以下服务连接工厂：

| 连接信息类型                           | 匹配的镜像名称                                                          |
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

Spring Boot 的 `spring-boot-docker-compose` 模块还提供 PostgreSQL、Redis、Elasticsearch 等服务连接，完整清单见 [Docker Compose Support](https://docs.spring.io/spring-boot/reference/features/dev-services.html#features.dev-services.docker-compose)。因此，上表不是 Spring AI 可连接后端的完整列表。

这里生成的是连接信息。Milvus 的向量存储配置见 [Milvus](/frameworks/spring-ai/rag/vector-stores/milvus/)，MCP 的传输与客户端能力见 [MCP 客户端](/frameworks/spring-ai/mcp/client/)；`McpSseClientConnectionDetails` 也不表示所有 MCP 传输都由该工厂处理。

<a id="pgvector-example"></a>

## 四、PGvector：启动数据库并自动连接（补充示例）

先按 [PGvector 自动配置](/frameworks/spring-ai/rag/vector-stores/pgvector/#_auto_configuration)添加向量存储 starter，并配置可用的 `EmbeddingModel`。下面只补充 Docker Compose 与连接部分。

在应用工作目录创建 `compose.yml`：

```yaml
services:
  pgvector:
    image: pgvector/pgvector:pg17
    environment:
      POSTGRES_DB: postgres
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - '5432'
    labels:
      org.springframework.boot.service-connection: postgres
    volumes:
      - pgvector-data:/var/lib/postgresql/data

volumes:
  pgvector-data:
```

这是本地开发示例。`pgvector/pgvector` 使用不同于 `postgres` 的镜像名，标签将它声明为 PostgreSQL 服务，让 Boot 的 JDBC 连接工厂识别它。`"5432"` 只指定容器端口，宿主机端口由 Docker 分配，Boot 会发现实际映射。数据库文件保存在命名卷中。

在 `application.yml` 中配置向量存储与容器生命周期：

```yaml
spring:
  docker:
    compose:
      lifecycle-management: start-only
  ai:
    vectorstore:
      pgvector:
        initialize-schema: true
        dimensions: 1536
```

`start-only` 表示随应用启动服务，应用退出时继续保留运行。连接由服务连接信息提供后，无需重复填写 `spring.datasource.url`、用户名和密码。

`1536` 是示例值，必须与实际 Embedding 模型的输出维度一致；详见[维度与向量空间要求](/frameworks/spring-ai/models/embedding-model/#工程上先记住三点)。`initialize-schema` 控制扩展、表和索引初始化，需要相应数据库权限，具体行为见 [PGvector 配置](/frameworks/spring-ai/rag/vector-stores/pgvector/#pgvector-properties)。

数据库可连接后，再通过 [ETL 管道](/frameworks/spring-ai/rag/document-ingestion/)读取、切分并入库，通过 [RAG Advisor](/frameworks/spring-ai/rag/retrieval-and-generation/#_advisors)完成检索和生成。

## 五、配置职责与按需查阅

| 配置或组件       | 负责什么                                         |
| ---------------- | ------------------------------------------------ |
| Docker Compose   | 运行容器、设置环境变量、映射端口和挂载数据卷。   |
| 服务连接信息     | 让自动配置获得客户端所需的地址、端口等连接参数。 |
| 向量存储配置     | 选择索引、维度、距离度量，以及是否初始化结构。   |
| `EmbeddingModel` | 将文档和问题转换为兼容的向量。                   |
| ETL 与 RAG       | 准备资料，并在提问时检索和生成回答。             |

开发服务适合本地开发。生命周期管理、自定义镜像、健康检查、共享服务和打包规则，继续查 [Spring Boot 完整说明](https://docs.spring.io/spring-boot/reference/features/dev-services.html#features.dev-services.docker-compose)。当前笔记未完整覆盖这些高级选项，保留官网入口。

[Testcontainers](https://docs.spring.io/spring-ai/reference/api/testcontainers.html) 是另一种开发服务方案，接入方式另见原文。

---

来源：[Spring AI Docker Compose](https://docs.spring.io/spring-ai/reference/api/docker-compose.html)，文档版本 2.0.2；运行流程与 PGvector 示例参考 Spring Boot 4.1.2 开发服务说明及连接工厂源码，核验日期：2026-11-01。补充示例尚未实际启动容器或调用模型。
