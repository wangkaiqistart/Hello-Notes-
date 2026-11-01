# 共享翻译上下文

目标：把 Spring AI 2.0.2 Vector Databases 文档完整精翻为简体中文技术笔记。受众熟悉 Java/Spring Boot，风格简明准确、自然中文，保持完整内容供后续查阅。遵循项目 zh-CN/refined/technical 配置。

术语：VectorStore=向量存储；Vector Database=向量数据库；Retriever=检索器；BatchingStrategy=批处理策略；metadata filter=元数据过滤；auto-truncation=自动截断；Embedding=嵌入（Embedding）；Token=词元（Token）。代码、API 标识符、模型名、占位符不翻译。32 个原代码块必须全部保留，允许翻译注释但不擅自改变 API，主代理会对同版本源码做必要校正。保留每个源章节的显式锚点和链接。

内容分为总览/API、批处理/自动截断、后端列表、读写与只读检索、元数据过滤、删除及版本管理。不要删减参数、代码、列举项或参考实现。英文长句用自然中文重写，避免逐句翻译腔。

准确性边界：只读接口不是后端权限控制；Embedding 模型与生成模型不必相同提供方，文档与查询向量空间须兼容。TokenCountBatchingStrategy 不切分文档，8191 是策略默认，不能当作全部模型通用上限。自动截断高限额的源文数值属于示例，不代表当前所有模型真实上限；保留原文提议但提示按提供方核验，不能承诺不报错。正文之外的校正事项交回主代理审校。

站内链接可使用：/frameworks/spring-ai/models/embedding-model/、/frameworks/spring-ai/rag/document-ingestion/、/frameworks/spring-ai/rag/retrieval-and-generation/、/frameworks/spring-ai/engineering/evaluation/、/basics/embedding/embedding-basics/、/rag/vector-db/chroma-vector-store/#相似度怎么理解。Chroma 页是 Python 示例，仅作为原理参考；不得替换 Spring AI Chroma 提供方配置链接。提供方链接先保留外部绝对 URL。

只处理各自源块正文，不添加 frontmatter、总阅读路线或最终来源页脚。这些由主代理合并时添加。
