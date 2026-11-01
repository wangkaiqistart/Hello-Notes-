# 内容分析

来源：https://docs.spring.io/spring-ai/reference/api/vectordbs/s3-vector-store.html，2.0.2。面向熟悉 Java / Spring Boot 的开发者。完整翻译依赖、准备工作、配置表、过滤、手动创建和原生客户端，不删参考内容。

术语：VectorStore=向量存储；Embedding=嵌入（Embedding）；index=索引；schema=数据库模式/结构（按上下文）；collection=集合；dimension=维度；metadata filter=元数据过滤；batching strategy=批处理策略。

风格：简明技术笔记，中文自然表达，保留全部代码、表格参数、默认值、锚点和外链。重点标注最短接入链路，完整配置供查阅。核对版本、默认初始化、索引/维度、距离度量与依赖名称，Java 示例仅能声称静态核对。

翻译要求：逐节完整覆盖来源，保留每个原始锚点，保留所有代码块原文（先不擅自改代码，错误单列说明供主代理审核）。表格逐行翻译说明而不改配置名和默认值。文档新增中文 frontmatter，顺序为 S3 Vector Store 5、Elasticsearch 6。正文只保留一个页面主标题（frontmatter title），原 h1 不重复。站内确认等价的引用可替换：向量存储总览 /frameworks/spring-ai/rag/vector-stores/；Embedding /frameworks/spring-ai/models/embedding-model/；元数据过滤 /frameworks/spring-ai/rag/vector-stores/#metadata-filters；RAG /frameworks/spring-ai/rag/retrieval-and-generation/；ETL /frameworks/spring-ai/rag/document-ingestion/。其余不确定引用保留。来源链接列于文末。不得声称实际运行数据库/模型。初稿写到03-draft.md，交主代理审校。
