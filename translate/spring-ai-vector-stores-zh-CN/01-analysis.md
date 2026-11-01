# 内容分析

源文 Vector Databases，当前版本 2.0.2。正文约 4503 个空白分隔词，34 个章节锚点、32 个代码块、0 张图片。按项目精翻配置处理，分块初译后统一审校。

## 子目录策略

官方导航有 21 个实现子页；它们是同一 VectorStore 抽象的后端实现，不是需要逐一学习的连续章节。本次翻译总览；下一篇优先 PGvector，承接已译 RAG/评估测试中的 pgVectorStore 示例，补齐数据库扩展、维度、索引与配置。Chroma 作为备选；已有本地 Python/LangChain 笔记只覆盖原理和 Python 接入，不等价于 Spring AI 配置。其他后端按项目需要查阅。

Understanding Vectors 是总览正文链接的原理附录，不在这 21 个后端子页之中。已有 Embedding 基础与 Chroma 相似度笔记可复用，几何推导保留原文入口，不重复翻译。

## 术语

Vector Store：向量存储；Vector Database：向量数据库；Retriever：检索器；batching：批处理；chunking：文本切分；schema initialization：结构初始化；auto-truncation：自动截断；metadata filter：元数据过滤；embedding：嵌入（Embedding）；token：词元（Token）。API 标识符与代码保留英文。

## 重点与难点

- 完整保留参考内容，给学习路线和重点层次；不因篇幅长删代码或删除/过滤参考。
- VectorStoreRetriever 是接口层面只读，不能代替数据库权限和租户隔离。
- 生成模型与 Embedding 模型不必来自同一提供方；真正需要兼容的是文档和查询的向量空间及存储维度。源文“must match higher-level AI model”需校正。
- BatchingStrategy 分组不切分文档；默认 8191 与 10% 余量是策略默认，不是所有 Embedding 模型的共同限制。
- 自动截断高限额案例是特定提供方的非常规配置，不能理解为放宽真实模型限制或保证永不失败；保留示例与 5–10 倍建议的上下文，明确需按实际单条/批次限制验证。
- 核对手动 PgVectorStore 构建代码是否真正应用传入 batchingStrategy，原文可能漏调用。
- 核对文档格式化默认值、TokenCountEstimator、Vertex AI 构造 API、过滤操作符、删除实现行为。
- 统一 API 不表示所有后端支持所有过滤符；元数据过滤必须由可信应用逻辑补齐且适用于搜索/删除。
- 删除/版本替换示例是步骤示意，不把先删后写称为原子更新，说明删除非幂等重试和缺口问题仅在相关示例需要时简述。
- 完整保留后端查询入口；主题相当的概念链接优先本站。提供方专属配置与数学推导无同等覆盖时保留外链。
