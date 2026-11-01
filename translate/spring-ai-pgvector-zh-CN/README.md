# Spring AI：PGvector 向量存储

- 原文：[官方来源](https://docs.spring.io/spring-ai/reference/api/vectordbs/pgvector.html)。
- 版本与日期：Spring AI 2.0.2，2026-11-01。
- 方式：baoyu-translate，沿用项目 zh-CN / refined / technical 配置；独立初译后由主代理审校、修订与润色。
- 站点正文：`src/content/docs/frameworks/spring-ai/rag/vector-stores/pgvector.mdx`。
- 导航：Spring AI → RAG → 向量存储 → PGvector。用户指定阅读范围已扩展为 PGvector → Milvus → Redis → S3 Vector Store → Elasticsearch（ES），其余后端不安排学习和翻译。

## 覆盖与校正

完整保留 7 个源章节锚点、14 个代码块和 9 个来源配置参数。原文没有图片。2 个代码块经过必要校正，其余保持来源内容，差异见 `code-fidelity.json`。

修复 SQL 注释与 YAML 缩进，明确首次初始化、vector 类型索引维度限制、schema 校验顺序、批次文档数与维度回退。

## 引用选择

统一 VectorStore、元数据过滤、Embedding、BOM 和仓库说明使用已确认的站内页面；Redis 的 ChatClient 和 Advisor 也链接已有笔记。具体提供方接入、数据库部署、专有查询/索引文档、升级记录和上游源码没有等价站内页面，保留外链。原文自身的章节链接改为本页锚点，完整映射见 `coverage-audit.json`。

## 文件与验证

`../spring-ai-pgvector.md` 和 `source-article.html` 为来源；`01-analysis.md` 至 `05-revision.md` 为翻译过程，`translation.md` 与站点正文同步。`api/` 保存同版本源码和来源哈希，`api-contract-checks.json` 保存 12 项静态核对，`page-validation.json` 保存桌面与手机验证。

`npm run check`：0 错误、0 警告、0 提示；`npm run build`：成功生成90页。桌面1440px、手机390px均无页面横向溢出；15 个本站链接目标和锚点有效。源章节和代码数量与渲染结果一致。

Java示例只按源码静态核对，未编译或执行；没有连接数据库或调用模型，不把页面检查当作实际接入验收。

## 2026-11-01 RAG 全目录引用复核

本轮按“站内文档只引用 Spring AI 模块”复查整个 RAG 目录。当前页面已调整引用，代码、原始锚点、图片和已有外链保持不变。历史记录中的模块外引用方案已由本次规则替代，完整逐页变更、保留外链原因与验证结果见 [RAG 全目录记录](../spring-ai-rag-reference-audit/README.md)。

当前工作区类型检查 0 错误、0 警告、0 提示；构建通过（92 页）。8 篇桌面与手机共 16 次检查通过，245 个站内页面、锚点与静态资源目标有效，正文的模块外站内文档引用为 0。Java 示例未编译或执行，未连接真实模型、数据库或云服务。

## Docker Compose 引用补齐

Docker Compose 开发服务已收录到 Spring AI 的“工程实践”。本页原 Spring AI Docker Compose 入口和 Boot Docker Compose 连接说明已分别替换为站内新页及运行流程锚点；Testcontainers 接入仍保留外链，因为本模块没有完整等价笔记。

本次只替换两处 URL，代码、原始锚点与其他正文不变。新页与本页的类型检查、构建及桌面／手机端检查通过，详见[本轮记录](../spring-ai-docker-compose-zh-CN/coverage-audit.json)。早先保留这两处外链的原因作为历史记录留存，当前以本节为准。
