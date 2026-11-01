# 向量存储子目录学习范围

用户已确定翻译和学习五种后端，均已完成：

1. [PGvector](/frameworks/spring-ai/rag/vector-stores/pgvector/)：PostgreSQL 扩展、索引、维度、初始化与 Spring Boot 配置。
2. [Milvus](/frameworks/spring-ai/rag/vector-stores/milvus/)：专用向量库、集合与分区、原生表达式、nprobe 与连接配置。
3. [Redis](/frameworks/spring-ai/rag/vector-stores/redis/)：元数据索引、距离度量、文本/范围检索和语义缓存。

4. [S3 Vector Store](/frameworks/spring-ai/rag/vector-stores/s3-vector-store/)：AWS 向量桶、索引、客户端配置、过滤删除与当前适配边界。
5. [Elasticsearch（ES）](/frameworks/spring-ai/rag/vector-stores/elasticsearch/)：dense_vector 映射、距离函数、元数据过滤和 Rest5Client 接入。

先读统一API总览，再按以上顺序阅读。实践时先选一种后端完成入库、检索、过滤与删除，再对照其他实现，不要求同时维护五套运行环境。

官方导航共21个实现；其余16个不列入当前学习任务，也不安排翻译，完整来源入口保留在总览及directory-plan.json中。既有Chroma原理笔记仍可引用，不安排其Spring AI接入翻译。

Understanding Vectors 为原理附录：Embedding 基础仅复用 Spring AI 模块内的核心概念与 Embedding 模型笔记；距离度量参考本模块 Redis 章节，几何推导保留原文链接。
