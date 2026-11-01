# Spring AI：S3 Vector Store

- 原文：[文档来源](https://docs.spring.io/spring-ai/reference/api/vectordbs/s3-vector-store.html)。
- 版本与日期：Spring AI 2.0.2，2026-11-01。
- 翻译：baoyu-translate，项目配置 zh-CN / refined / technical。
- 站点正文：`src/content/docs/frameworks/spring-ai/rag/vector-stores/s3-vector-store.mdx`。
- 导航：Spring AI → RAG → 向量存储 → S3 Vector Store。

## 覆盖与校正

完整覆盖 7 个源章节锚点、13 个代码块和 2 个配置参数，原文没有图片。保留配置、过滤、手动创建与原生客户端内容，增加阅读重点。代码改动逐块记录于 `code-fidelity.json`，详细审校见 `04-critique.md`。

核对 Spring AI v2.0.2 源码，明确这里使用 AWS S3 Vectors 专用向量桶与索引，需提前创建；两个资源名称没有默认值。补上客户端和区域配置，修正未定义变量及模型构造。JSON 示例只展开排版，解析结果与来源一致。

当前实现不保存或还原原始文档正文，返回文本为向量键，且未应用 similarityThreshold；接入 RAG 需回查正文并自行按距离度量处理阈值。按条件删除会遍历索引，在客户端判断并分批删除，不能当作原子的服务端过滤删除。

## 引用与阅读顺序

统一 VectorStore API、元数据过滤、Embedding、BOM 与仓库配置使用等价的站内笔记。AWS 桶、索引、S3 Vectors API、SDK 与源码没有等价本地页面，继续保留外链。

当前后端学习范围为 PGvector → Milvus → Redis → S3 Vector Store → Elasticsearch（ES），五篇均已完成；其余 16 个实现只保留查询入口。先选一种跑通 RAG，再比较其他后端。

## 产物与验证

`../spring-ai-s3-vector-store.md`、`source-article.html` 与 `source-manifest.json` 保存来源；分析、提示、初稿、审校、修订与最终稿保留在本目录，`translation.md`、`05-revision.md` 与站点正文完全一致。

`coverage-audit.json` 记录完整性；`api/manifest.json` 保存源码出处与哈希，`api-contract-checks.json` 记录 18 项静态核对；`page-validation.json` 记录桌面 1440×1000 和手机 390×844 的渲染与链接检查。

类型检查 0 错误、0 警告、0 提示；生产构建通过，共 92 页。两种视口均无页面横向溢出或运行时错误，14 个站内链接目标与锚点有效。日志见 `check.log`、`build.log` 和 `validation.jsonl`。

Java 示例仅按源码静态核对，未编译或执行；未实际连接 AWS、数据库或模型。

## 2026-11-01 RAG 全目录引用复核

本轮按“站内文档只引用 Spring AI 模块”复查整个 RAG 目录。当前页面已调整引用，代码、原始锚点、图片和已有外链保持不变。历史记录中的模块外引用方案已由本次规则替代，完整逐页变更、保留外链原因与验证结果见 [RAG 全目录记录](../spring-ai-rag-reference-audit/README.md)。

当前工作区类型检查 0 错误、0 警告、0 提示；构建通过（92 页）。8 篇桌面与手机共 16 次检查通过，245 个站内页面、锚点与静态资源目标有效，正文的模块外站内文档引用为 0。Java 示例未编译或执行，未连接真实模型、数据库或云服务。
