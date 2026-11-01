# Spring AI：向量存储

- 原文：[Vector Databases](https://docs.spring.io/spring-ai/reference/api/vectordbs.html)。
- 版本与日期：Spring AI 2.0.2，2026-11-01。
- 翻译：baoyu-translate，项目配置 zh-CN / refined / technical；两块初译后统一审校。
- 站点正文：`src/content/docs/frameworks/spring-ai/rag/vector-stores/index.mdx`。
- 导航：Spring AI → RAG → 向量存储 → 向量存储总览。

## 覆盖与校正

总览完整覆盖 34 个源章节锚点和 32 个代码块，原文没有图片。22 个代码块原样保留，10 个按 v2.0.2 源码校正。修订包括旧 Document/ChatModel 方法、过滤构建器、局部变量和手动注入批处理策略，详见 `code-fidelity.json` 与 `04-critique.md`。

补充只读接口与数据库权限的区别、模型向量空间兼容、自动截断的提供方边界、批处理不等于文本切分，以及删除/版本更新的验证和原子性边界。23 项 API 静态核对记录在 `api-contract-checks.json`，源码快照与出处在 `api/`。

## 子目录计划

官方导航包含 21 个后端实现页；总览正文原列 18 个后端，已补齐导航中的另外三个入口，并保留 SimpleVectorStore 测试入口。

按用户最新要求，PGvector、Milvus、Redis、S3 Vector Store、Elasticsearch 五篇均已完成，阅读顺序相同。其余 16 个后端不列入学习任务，也不安排翻译，只保留入口。完整安排见 `directory-plan.md` 与 `directory-plan.json`。

Understanding Vectors 为原理附录；基础内容复用 Spring AI 模块内的核心概念、Embedding 模型和 Redis 距离度量，几何推导保留原文。

## 引用选择

RAG、ETL、Embedding、评估测试与距离度量说明使用 Spring AI 模块内的笔记。Chroma 接入未纳入当前翻译范围，保留对应原文入口。

尚无等价本地内容的后端配置、向量几何推导、Word2Vec/GloVe/BERT 背景、模型输入限制、SimpleVectorStore 实现源码和 Azure Cosmos DB 外部模块继续保留外链。源码链接固定到 v2.0.2。

## 产物与验证

`../spring-ai-vector-stores.md` 和 `source-article.html` 为来源；分析、提示、初稿、审校、修订与最终稿依次保存，最终稿与站点正文一致。`coverage-audit.json` 记录完整性，源面包屑和上一篇导航不作为正文引用；`page-validation.json` 记录桌面和移动端的渲染、锚点与站内链接检查。

运行 `npm run check`、`npm run build`，结果见 `validation.jsonl`。Java 示例只按源码静态核对，未编译或执行，未连接数据库或模型。

验证结果：类型检查 0 错误、0 警告、0 提示；生产构建通过（92 页，含五篇后端接入文档）；总览桌面与手机检查通过，51 个站内链接目标与锚点有效，页面无横向溢出。

## 2026-11-01 RAG 全目录引用复核

本轮按“站内文档只引用 Spring AI 模块”复查整个 RAG 目录。当前页面已调整引用，代码、原始锚点、图片和已有外链保持不变。历史记录中的模块外引用方案已由本次规则替代，完整逐页变更、保留外链原因与验证结果见 [RAG 全目录记录](../spring-ai-rag-reference-audit/README.md)。

当前工作区类型检查 0 错误、0 警告、0 提示；构建通过（92 页）。8 篇桌面与手机共 16 次检查通过，245 个站内页面、锚点与静态资源目标有效，正文的模块外站内文档引用为 0。Java 示例未编译或执行，未连接真实模型、数据库或云服务。
