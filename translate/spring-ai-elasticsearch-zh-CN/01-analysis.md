# 内容分析

来源：https://docs.spring.io/spring-ai/reference/api/vectordbs/elasticsearch.html，2.0.2。面向熟悉 Java / Spring Boot 的开发者。完整翻译依赖、准备工作、配置表、过滤、手动创建和原生客户端，不删参考内容。

术语：VectorStore=向量存储；Embedding=嵌入（Embedding）；index=索引；schema=数据库模式/结构（按上下文）；collection=集合；dimension=维度；metadata filter=元数据过滤；batching strategy=批处理策略。

风格：简明技术笔记，中文自然表达，保留全部代码、表格参数、默认值、锚点和外链。重点标注最短接入链路，完整配置供查阅。核对版本、默认初始化、索引/维度、距离度量与依赖名称，Java 示例仅能声称静态核对。
