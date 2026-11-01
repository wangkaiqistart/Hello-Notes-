# RAG 全目录保留链接与原因

本清单保留原有链接，并说明为什么没有改成 Spring AI 模块内链接。局部提及同一技术不等于覆盖完整主题；原文来源和源码证据继续使用原始出处。外部网站本轮未全部重新做可用性验证。

## 算法背景（3 个）

| 链接                                                              | 使用页面     | 保留原因                                                                                 |
| ----------------------------------------------------------------- | ------------ | ---------------------------------------------------------------------------------------- |
| [Word2Vec](https://en.wikipedia.org/wiki/Word2vec)                | 向量存储总览 | Spring AI 模块未分别介绍 Word2Vec、GloVe、BERT 的完整背景，通用 Embedding 说明不能替代。 |
| [GloVe](<https://en.wikipedia.org/wiki/GloVe_(machine_learning)>) | 向量存储总览 | Spring AI 模块未分别介绍 Word2Vec、GloVe、BERT 的完整背景，通用 Embedding 说明不能替代。 |
| [BERT](<https://en.wikipedia.org/wiki/BERT_(language_model)>)     | 向量存储总览 | Spring AI 模块未分别介绍 Word2Vec、GloVe、BERT 的完整背景，通用 Embedding 说明不能替代。 |

## 本地服务示例（2 个）

| 链接                                             | 使用页面 | 保留原因                                                       |
| ------------------------------------------------ | -------- | -------------------------------------------------------------- |
| [http://localhost:19530](http://localhost:19530) | Milvus   | 本地部署后的服务或管理地址，属于运行示例，不是知识库文档引用。 |
| [http://localhost:9001](http://localhost:9001)   | Milvus   | 本地部署后的服务或管理地址，属于运行示例，不是知识库文档引用。 |

## 模块内缺少等价内容（7 个）

| 链接                                                                                                                                    | 使用页面                                     | 保留原因                                                                 |
| --------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------- | ------------------------------------------------------------------------ |
| [Qxotic jinfer](https://docs.spring.io/spring-ai/reference/api/embeddings/jinfer-embeddings.html#reranking)                             | 检索增强生成（RAG）                          | Spring AI 模块没有完整的 jinfer 重排序接入说明；其他 jinfer 主题不等价。 |
| [升级说明](https://docs.spring.io/spring-ai/reference/upgrade-notes.html)                                                               | Elasticsearch（ES）、Milvus、PGvector、Redis | Spring AI 模块没有完整的版本升级迁移说明，不能用当前快速入门替代。       |
| [Understanding Vectors](https://docs.spring.io/spring-ai/reference/api/vectordbs/understand-vectordbs.html)                             | 向量存储总览                                 | Spring AI 模块有向量概念和距离度量说明，但未完整翻译向量几何与数学推导。 |
| [Docker Compose](https://docs.spring.io/spring-ai/reference/api/docker-compose.html)                                                    | PGvector                                     | Spring AI 模块没有等价的开发服务集成与自动连接配置说明。                 |
| [Testcontainers](https://docs.spring.io/spring-ai/reference/api/testcontainers.html)                                                    | PGvector                                     | Spring AI 模块没有等价的开发服务集成与自动连接配置说明。                 |
| [Docker Compose 开发服务](https://docs.spring.io/spring-boot/reference/features/dev-services.html#features.dev-services.docker-compose) | PGvector                                     | Spring AI 模块没有等价的开发服务集成与自动连接配置说明。                 |
| [Testcontainers 开发服务](https://docs.spring.io/spring-boot/reference/features/dev-services.html#features.dev-services.testcontainers) | PGvector                                     | Spring AI 模块没有等价的开发服务集成与自动连接配置说明。                 |

## 原始论文（1 个）

| 链接                                                                                                               | 使用页面            | 保留原因                                               |
| ------------------------------------------------------------------------------------------------------------------ | ------------------- | ------------------------------------------------------ |
| [Modular RAG: Transforming RAG Systems into LEGO-like Reconfigurable Frameworks](https://arxiv.org/abs/2407.21059) | 检索增强生成（RAG） | 论文原始出处；Spring AI 模块未收录全文，保留来源引用。 |

## 未翻译或范围外实现（17 个）

| 链接                                                                                                                  | 使用页面     | 保留原因                                                                 |
| --------------------------------------------------------------------------------------------------------------------- | ------------ | ------------------------------------------------------------------------ |
| [Azure Vector Search](https://docs.spring.io/spring-ai/reference/api/vectordbs/azure.html)                            | 向量存储总览 | 当前未安排翻译的后端接入文档；Spring AI 模块没有同等页面，保留查询入口。 |
| [Azure Cosmos DB](https://docs.spring.io/spring-ai/reference/api/vectordbs/azure-cosmos-db.html)                      | 向量存储总览 | 当前未安排翻译的后端接入文档；Spring AI 模块没有同等页面，保留查询入口。 |
| [Amazon Bedrock Knowledge Base](https://docs.spring.io/spring-ai/reference/api/vectordbs/bedrock-knowledge-base.html) | 向量存储总览 | 当前未安排翻译的后端接入文档；Spring AI 模块没有同等页面，保留查询入口。 |
| [Couchbase](https://docs.spring.io/spring-ai/reference/api/vectordbs/couchbase.html)                                  | 向量存储总览 | 当前未安排翻译的后端接入文档；Spring AI 模块没有同等页面，保留查询入口。 |
| [Apache Cassandra](https://docs.spring.io/spring-ai/reference/api/vectordbs/apache-cassandra.html)                    | 向量存储总览 | 当前未安排翻译的后端接入文档；Spring AI 模块没有同等页面，保留查询入口。 |
| [Chroma Vector Store](https://docs.spring.io/spring-ai/reference/api/vectordbs/chroma.html)                           | 向量存储总览 | 当前未安排翻译的后端接入文档；Spring AI 模块没有同等页面，保留查询入口。 |
| [GemFire Vector Store](https://docs.spring.io/spring-ai/reference/api/vectordbs/gemfire.html)                         | 向量存储总览 | 当前未安排翻译的后端接入文档；Spring AI 模块没有同等页面，保留查询入口。 |
| [MariaDB Vector Store](https://docs.spring.io/spring-ai/reference/api/vectordbs/mariadb.html)                         | 向量存储总览 | 当前未安排翻译的后端接入文档；Spring AI 模块没有同等页面，保留查询入口。 |
| [MongoDB Atlas Vector Store](https://docs.spring.io/spring-ai/reference/api/vectordbs/mongodb.html)                   | 向量存储总览 | 当前未安排翻译的后端接入文档；Spring AI 模块没有同等页面，保留查询入口。 |
| [Neo4j Vector Store](https://docs.spring.io/spring-ai/reference/api/vectordbs/neo4j.html)                             | 向量存储总览 | 当前未安排翻译的后端接入文档；Spring AI 模块没有同等页面，保留查询入口。 |
| [OpenSearch Vector Store](https://docs.spring.io/spring-ai/reference/api/vectordbs/opensearch.html)                   | 向量存储总览 | 当前未安排翻译的后端接入文档；Spring AI 模块没有同等页面，保留查询入口。 |
| [Oracle Vector Store](https://docs.spring.io/spring-ai/reference/api/vectordbs/oracle.html)                           | 向量存储总览 | 当前未安排翻译的后端接入文档；Spring AI 模块没有同等页面，保留查询入口。 |
| [Pinecone Vector Store](https://docs.spring.io/spring-ai/reference/api/vectordbs/pinecone.html)                       | 向量存储总览 | 当前未安排翻译的后端接入文档；Spring AI 模块没有同等页面，保留查询入口。 |
| [Qdrant Vector Store](https://docs.spring.io/spring-ai/reference/api/vectordbs/qdrant.html)                           | 向量存储总览 | 当前未安排翻译的后端接入文档；Spring AI 模块没有同等页面，保留查询入口。 |
| [Typesense Vector Store](https://docs.spring.io/spring-ai/reference/api/vectordbs/typesense.html)                     | 向量存储总览 | 当前未安排翻译的后端接入文档；Spring AI 模块没有同等页面，保留查询入口。 |
| [Weaviate Vector Store](https://docs.spring.io/spring-ai/reference/api/vectordbs/weaviate.html)                       | 向量存储总览 | 当前未安排翻译的后端接入文档；Spring AI 模块没有同等页面，保留查询入口。 |
| [azurecosmosdb.github.io/spring-ai/docs/index.html](https://azurecosmosdb.github.io/spring-ai/docs/index.html)        | 向量存储总览 | 外部团队维护的集成说明；当前 Spring AI 模块没有等价页面。                |

## 原文来源（8 个）

| 链接                                                                                                                           | 使用页面            | 保留原因                               |
| ------------------------------------------------------------------------------------------------------------------------------ | ------------------- | -------------------------------------- |
| [Spring AI ETL Pipeline](https://docs.spring.io/spring-ai/reference/api/etl-pipeline.html)                                     | ETL 管道            | 本篇原文来源，用于溯源，保留官方链接。 |
| [Spring AI Retrieval Augmented Generation](https://docs.spring.io/spring-ai/reference/api/retrieval-augmented-generation.html) | 检索增强生成（RAG） | 本篇原文来源，用于溯源，保留官方链接。 |
| [Elasticsearch](https://docs.spring.io/spring-ai/reference/api/vectordbs/elasticsearch.html)                                   | Elasticsearch（ES） | 本篇原文来源，用于溯源，保留官方链接。 |
| [Vector Databases](https://docs.spring.io/spring-ai/reference/api/vectordbs.html)                                              | 向量存储总览        | 本篇原文来源，用于溯源，保留官方链接。 |
| [Milvus](https://docs.spring.io/spring-ai/reference/api/vectordbs/milvus.html)                                                 | Milvus              | 本篇原文来源，用于溯源，保留官方链接。 |
| [PGvector](https://docs.spring.io/spring-ai/reference/api/vectordbs/pgvector.html)                                             | PGvector            | 本篇原文来源，用于溯源，保留官方链接。 |
| [Redis](https://docs.spring.io/spring-ai/reference/api/vectordbs/redis.html)                                                   | Redis               | 本篇原文来源，用于溯源，保留官方链接。 |
| [S3 Vector Store](https://docs.spring.io/spring-ai/reference/api/vectordbs/s3-vector-store.html)                               | S3 Vector Store     | 本篇原文来源，用于溯源，保留官方链接。 |

## 提供方专有内容（41 个）

| 链接                                                                                                                                                | 使用页面                      | 保留原因                                                                             |
| --------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------- | ------------------------------------------------------------------------------------ |
| [Tika 文档](https://tika.apache.org/3.1.0/formats.html)                                                                                             | ETL 管道                      | TikaDocumentReader 用法不包含 Apache Tika 的完整支持格式表。                         |
| [Elasticsearch](https://www.elastic.co/elasticsearch)                                                                                               | Elasticsearch（ES）           | 产品、部署或客户端／原生查询文档；Spring AI 接入笔记未覆盖这些外部产品的完整用法。   |
| [Docker](https://hub.docker.com/_/elasticsearch/)                                                                                                   | Elasticsearch（ES）           | 产品、部署或客户端／原生查询文档；Spring AI 接入笔记未覆盖这些外部产品的完整用法。   |
| [自行部署 Elasticsearch](https://www.elastic.co/guide/en/elasticsearch/reference/current/install-elasticsearch.html#elasticsearch-install-packages) | Elasticsearch（ES）           | 产品、部署或客户端／原生查询文档；Spring AI 接入笔记未覆盖这些外部产品的完整用法。   |
| [Elastic Cloud](https://www.elastic.co/cloud/elasticsearch-service/signup?page=docs&placement=docs-body)                                            | Elasticsearch（ES）           | 产品、部署或客户端／原生查询文档；Spring AI 接入笔记未覆盖这些外部产品的完整用法。   |
| [Elasticsearch dense_vector 文档](https://www.elastic.co/guide/en/elasticsearch/reference/master/dense-vector.html#dense-vector-params)             | Elasticsearch（ES）           | 产品、部署或客户端／原生查询文档；Spring AI 接入笔记未覆盖这些外部产品的完整用法。   |
| [Query string query](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-query-string-query.html)                             | Elasticsearch（ES）           | 产品、部署或客户端／原生查询文档；Spring AI 接入笔记未覆盖这些外部产品的完整用法。   |
| [Elasticsearch 客户端文档](https://www.elastic.co/guide/en/elasticsearch/client/java-api-client/current/java-rest-low-usage-initialization.html)    | Elasticsearch（ES）           | 产品、部署或客户端／原生查询文档；Spring AI 接入笔记未覆盖这些外部产品的完整用法。   |
| [OpenAI 嵌入模型的输入限制](https://platform.openai.com/docs/guides/embeddings/embedding-models)                                                    | 向量存储总览                  | Embedding 模型笔记只说明通用接口，未完整覆盖 OpenAI 专有配置或模型输入限制。         |
| [Azure](https://learn.microsoft.com/en-us/azure/search/vector-search-overview)                                                                      | 向量存储总览                  | 后端产品与功能入口；当前 Spring AI 模块没有等价的产品手册。                          |
| [Apache Cassandra](https://cassandra.apache.org/doc/latest/cassandra/vector-search/overview.html)                                                   | 向量存储总览                  | 后端产品与功能入口；当前 Spring AI 模块没有等价的产品手册。                          |
| [Chroma](https://www.trychroma.com/)                                                                                                                | 向量存储总览                  | 后端产品与功能入口；当前 Spring AI 模块没有等价的产品手册。                          |
| [Elasticsearch](https://www.elastic.co/)                                                                                                            | 向量存储总览                  | 产品、部署或客户端／原生查询文档；Spring AI 接入笔记未覆盖这些外部产品的完整用法。   |
| [GemFire](https://tanzu.vmware.com/content/blog/vmware-gemfire-vector-database-extension)                                                           | 向量存储总览                  | 后端产品与功能入口；当前 Spring AI 模块没有等价的产品手册。                          |
| [MariaDB](https://mariadb.com/)                                                                                                                     | 向量存储总览                  | 后端产品与功能入口；当前 Spring AI 模块没有等价的产品手册。                          |
| [Milvus](https://milvus.io/)                                                                                                                        | 向量存储总览、Milvus          | Milvus 产品、部署、原生过滤或索引参数说明；站内只有 Spring AI 适配接口和示例。       |
| [MongoDB Atlas](https://www.mongodb.com/atlas/database)                                                                                             | 向量存储总览                  | 后端产品与功能入口；当前 Spring AI 模块没有等价的产品手册。                          |
| [Neo4j](https://neo4j.com/)                                                                                                                         | 向量存储总览                  | 后端产品与功能入口；当前 Spring AI 模块没有等价的产品手册。                          |
| [OpenSearch](https://opensearch.org/platform/search/vector-database.html)                                                                           | 向量存储总览                  | 后端产品与功能入口；当前 Spring AI 模块没有等价的产品手册。                          |
| [Oracle Database](https://docs.oracle.com/en/database/oracle/oracle-database/23/vecse/overview-ai-vector-search.html)                               | 向量存储总览                  | 后端产品与功能入口；当前 Spring AI 模块没有等价的产品手册。                          |
| [PostgreSQL/PGVector](https://github.com/pgvector/pgvector)                                                                                         | 向量存储总览、PGvector        | pgvector 扩展及索引类型限制的原始资料，适配层文档不能替代其完整说明。                |
| [Pinecone](https://www.pinecone.io/)                                                                                                                | 向量存储总览                  | 后端产品与功能入口；当前 Spring AI 模块没有等价的产品手册。                          |
| [Qdrant](https://www.qdrant.tech/)                                                                                                                  | 向量存储总览                  | 后端产品与功能入口；当前 Spring AI 模块没有等价的产品手册。                          |
| [Redis](https://redis.io/)                                                                                                                          | 向量存储总览                  | Redis 产品、云服务或原生查询语法文档；站内 Spring AI 适配说明不是完整替代。          |
| [Typesense](https://typesense.org/docs/0.24.0/api/vector-search.html)                                                                               | 向量存储总览                  | 后端产品与功能入口；当前 Spring AI 模块没有等价的产品手册。                          |
| [Weaviate](https://weaviate.io/)                                                                                                                    | 向量存储总览                  | 后端产品与功能入口；当前 Spring AI 模块没有等价的产品手册。                          |
| [AWS S3](https://aws.amazon.com/s3/features/vectors/)                                                                                               | 向量存储总览、S3 Vector Store | AWS S3 Vectors 产品、资源创建或 SDK 文档；Spring AI 适配说明未覆盖其完整服务和 API。 |
| [Milvus Standalone](https://milvus.io/docs/install_standalone-docker.md)                                                                            | Milvus                        | Milvus 产品、部署、原生过滤或索引参数说明；站内只有 Spring AI 适配接口和示例。       |
| [Milvus Cluster](https://milvus.io/docs/install_cluster-milvusoperator.md)                                                                          | Milvus                        | Milvus 产品、部署、原生过滤或索引参数说明；站内只有 Spring AI 适配接口和示例。       |
| [Milvus Filtering](https://milvus.io/docs/boolean.md)                                                                                               | Milvus                        | Milvus 产品、部署、原生过滤或索引参数说明；站内只有 Spring AI 适配接口和示例。       |
| [Milvus Vector Index](https://milvus.io/docs/index.md?tab=floating)                                                                                 | Milvus                        | Milvus 产品、部署、原生过滤或索引参数说明；站内只有 Spring AI 适配接口和示例。       |
| [pgvector 的索引类型说明](https://github.com/pgvector/pgvector/blob/v0.8.1/README.md#hnsw)                                                          | PGvector                      | pgvector 扩展及索引类型限制的原始资料，适配层文档不能替代其完整说明。                |
| [OpenAI EmbeddingModel](https://docs.spring.io/spring-ai/reference/api/embeddings/openai-embeddings.html)                                           | PGvector                      | Embedding 模型笔记只说明通用接口，未完整覆盖 OpenAI 专有配置或模型输入限制。         |
| [Redis](https://redis.io)                                                                                                                           | Redis                         | Redis 产品、云服务或原生查询语法文档；站内 Spring AI 适配说明不是完整替代。          |
| [Redis Search and Query](https://redis.io/docs/interact/search-and-query/)                                                                          | Redis                         | Redis 产品、云服务或原生查询语法文档；站内 Spring AI 适配说明不是完整替代。          |
| [Redis Cloud](https://app.redislabs.com/#/)                                                                                                         | Redis                         | Redis 产品、云服务或原生查询语法文档；站内 Spring AI 适配说明不是完整替代。          |
| [Docker 镜像](https://hub.docker.com/r/redis/redis-stack)                                                                                           | Redis                         | 产品、部署或客户端／原生查询文档；Spring AI 接入笔记未覆盖这些外部产品的完整用法。   |
| [Redis 查询语法](https://redis.io/docs/interact/search-and-query/query/)                                                                            | Redis                         | Redis 产品、云服务或原生查询语法文档；站内 Spring AI 适配说明不是完整替代。          |
| [S3 Vectors API](https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-vectors.html)                                                             | S3 Vector Store               | AWS S3 Vectors 产品、资源创建或 SDK 文档；Spring AI 适配说明未覆盖其完整服务和 API。 |
| [How to create S3 Vector Bucket](https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-vectors-buckets-create.html)                              | S3 Vector Store               | AWS S3 Vectors 产品、资源创建或 SDK 文档；Spring AI 适配说明未覆盖其完整服务和 API。 |
| [AWS SDK for Java V2 的过滤 Document 对象](https://sdk.amazonaws.com/java/api/latest/software/amazon/awssdk/core/document/Document.html)            | S3 Vector Store               | AWS S3 Vectors 产品、资源创建或 SDK 文档；Spring AI 适配说明未覆盖其完整服务和 API。 |

## 源码与 API 证据（5 个）

| 链接                                                                                                                                                                                                                                                                                   | 使用页面            | 保留原因                                                              |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------- | --------------------------------------------------------------------- |
| [Spring Boot 4.1.2 属性类](https://github.com/spring-projects/spring-boot/blob/v4.1.2/module/spring-boot-elasticsearch/src/main/java/org/springframework/boot/elasticsearch/autoconfigure/ElasticsearchProperties.java)                                                                | Elasticsearch（ES） | 固定版本的源码或 API 证据，用于核对实际实现；站内说明不代替原始证据。 |
| [SimpleVectorStore](https://github.com/spring-projects/spring-ai/blob/v2.0.2/spring-ai-vector-store/src/main/java/org/springframework/ai/vectorstore/SimpleVectorStore.java)                                                                                                           | 向量存储总览        | 固定版本的源码或 API 证据，用于核对实际实现；站内说明不代替原始证据。 |
| [RedisVectorStoreProperties](https://github.com/spring-projects/spring-ai/blob/v2.0.2/auto-configurations/vector-stores/spring-ai-autoconfigure-vector-store-redis/src/main/java/org/springframework/ai/vectorstore/redis/autoconfigure/RedisVectorStoreProperties.java)               | Redis               | 固定版本的源码或 API 证据，用于核对实际实现；站内说明不代替原始证据。 |
| [RedisVectorStoreAutoConfiguration](https://github.com/spring-projects/spring-ai/blob/v2.0.2/auto-configurations/vector-stores/spring-ai-autoconfigure-vector-store-redis/src/main/java/org/springframework/ai/vectorstore/redis/autoconfigure/RedisVectorStoreAutoConfiguration.java) | Redis               | 固定版本的源码或 API 证据，用于核对实际实现；站内说明不代替原始证据。 |
| [v2.0.2 的 S3VectorStore 源码](https://github.com/spring-projects/spring-ai/blob/v2.0.2/vector-stores/spring-ai-s3-vector-store/src/main/java/org/springframework/ai/vectorstore/s3/S3VectorStore.java)                                                                                | S3 Vector Store     | 固定版本的源码或 API 证据，用于核对实际实现；站内说明不代替原始证据。 |

## 后续更新：Docker Compose 已收录

Spring AI 的 Docker Compose 开发服务说明已翻译并补充 PGvector 示例。PGvector 页面原来的 Spring AI Docker Compose 链接和 Boot Docker Compose 服务连接说明，已改为本模块新页及运行流程锚点。Testcontainers 和 Boot 高级规则仍保留官网入口。

本文件前面的链接列表与检查数字记录全目录复核时的快照，这两处引用的当前状态以[后续记录](../spring-ai-docker-compose-zh-CN/coverage-audit.json)为准。
