# Spring AI：Elasticsearch（ES）

- 原文：[文档来源](https://docs.spring.io/spring-ai/reference/api/vectordbs/elasticsearch.html)。
- 版本与日期：Spring AI 2.0.2，2026-11-01。
- 翻译：baoyu-translate，项目配置 zh-CN / refined / technical。
- 站点正文：`src/content/docs/frameworks/spring-ai/rag/vector-stores/elasticsearch.mdx`。
- 导航：Spring AI → RAG → 向量存储 → Elasticsearch（ES）。

## 覆盖与校正

完整覆盖 6 个源章节锚点、15 个代码块和 15 个配置参数，原文没有图片。保留配置、过滤、手动创建与原生客户端内容，增加阅读重点。代码改动逐块记录于 `code-fidelity.json`，详细审校见 `04-critique.md`。

核对 Spring AI v2.0.2 与其配套 Spring Boot v4.1.2 源码。保留旧版客户端依赖作为历史参考，明确原文文字与版本示例不一致。修正 HttpHost 参数顺序、SimilarityFunction.cosine、OpenAI 模型构造及 Lucene 过滤结果。

补充默认维度 1536 不等于模型维度推断、自动配置不消费独立 Options Bean、已有索引不自动迁移映射等边界。按配套 Boot 源码修正 socketKeepAlive 默认值为 true，并说明 sniffer 默认关闭。

## 引用与阅读顺序

统一 VectorStore API、元数据过滤、Embedding、BOM 与仓库配置使用等价的站内笔记。Elasticsearch 部署、Elastic Cloud、dense_vector、查询语法、原生客户端、升级与源码没有等价本地页面，继续保留外链。

当前后端学习范围为 PGvector → Milvus → Redis → S3 Vector Store → Elasticsearch（ES），五篇均已完成；其余 16 个实现只保留查询入口。先选一种跑通 RAG，再比较其他后端。

## 产物与验证

`../spring-ai-elasticsearch.md`、`source-article.html` 与 `source-manifest.json` 保存来源；分析、提示、初稿、审校、修订与最终稿保留在本目录，`translation.md`、`05-revision.md` 与站点正文完全一致。

`coverage-audit.json` 记录完整性；`api/manifest.json` 保存源码出处与哈希，`api-contract-checks.json` 记录 20 项静态核对；`page-validation.json` 记录桌面 1440×1000 和手机 390×844 的渲染与链接检查。

类型检查 0 错误、0 警告、0 提示；生产构建通过，共 92 页。两种视口均无页面横向溢出或运行时错误，12 个站内链接目标与锚点有效。日志见 `check.log`、`build.log` 和 `validation.jsonl`。

Java 示例仅按源码静态核对，未编译或执行；未实际连接 AWS、数据库或模型。

## 2026-11-01 RAG 全目录引用复核

本轮按“站内文档只引用 Spring AI 模块”复查整个 RAG 目录。当前页面已调整引用，代码、原始锚点、图片和已有外链保持不变。历史记录中的模块外引用方案已由本次规则替代，完整逐页变更、保留外链原因与验证结果见 [RAG 全目录记录](../spring-ai-rag-reference-audit/README.md)。

当前工作区类型检查 0 错误、0 警告、0 提示；构建通过（92 页）。8 篇桌面与手机共 16 次检查通过，245 个站内页面、锚点与静态资源目标有效，正文的模块外站内文档引用为 0。Java 示例未编译或执行，未连接真实模型、数据库或云服务。
