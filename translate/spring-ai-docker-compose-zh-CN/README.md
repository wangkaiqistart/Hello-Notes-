# Spring AI：Docker Compose 开发服务

- 原文：[Docker Compose](https://docs.spring.io/spring-ai/reference/api/docker-compose.html)。
- 来源版本：Spring AI 2.0.2；补充说明核对 Spring Boot 4.1.2，日期 2026-11-01。
- 翻译：baoyu-translate，项目 zh-CN / refined / technical 配置，单篇分析、初译、审校、修订与润色。
- 站点正文：`src/content/docs/frameworks/spring-ai/engineering/docker-compose.mdx`。
- 导航：Spring AI → 工程实践 → Docker Compose 开发服务。

## 内容与优化

完整保留原文服务连接小节、9 类连接、11 个镜像名和 Maven／Gradle 两个依赖片段，原文没有图片。`_service_connections` 原始锚点保留。

补充开发服务启动和停止、宿主机映射端口、镜像名匹配、连接信息优先级，以及服务启动前已经运行时的生命周期边界。PGvector 补充示例使用 `org.springframework.boot.service-connection: postgres` 标签，包含 Compose 定义与向量存储配置两段 YAML。

PGvector 的 PostgreSQL 连接由 Spring Boot JDBC 工厂提供；Spring AI 模块的扩展表不是全部支持清单。模型、维度、结构初始化、资料入库与问答仍由各自组件处理。补充示例明确标注，不与来源代码混淆。

## 引用与关联页面

站内引用仅使用 Spring AI 模块，包括 BOM、Embedding、向量存储总览、PGvector、Milvus、MCP 客户端、ETL 和 RAG。

PGvector 页面两处原 Docker Compose 引用已替换到本篇及运行流程锚点；其余正文、14 个代码块和原始锚点保持不变。正文、定稿、修订与覆盖哈希已同步。

继续保留的外链：Spring Boot 完整开发服务说明（生命周期、健康检查、自定义镜像和打包规则）、Testcontainers 接入，以及本篇原文来源。这些内容没有等价的完整 Spring AI 模块笔记。

## 产物与验证

`../spring-ai-docker-compose.md`、`source-article.html` 和 `source-manifest.json` 保存原文与解析清单。`03-draft.md` 为完整初译，`04-critique.md` 为审校发现，`05-revision.md`、`translation.md` 与站点正文完全一致。

`coverage-audit.json`、`code-fidelity.json` 记录来源完整性、原文两段代码原样保留、补充 YAML 和 PGvector 两处 URL 替换；`api/manifest.json` 保留同版本证据出处与 SHA-256，`api-contract-checks.json` 有 13 项静态核对。补充 YAML 已解析检查字段与结构。

类型检查 0 错误、0 警告、0 提示；构建通过，共 93 页。新页和 PGvector 的桌面 1440×1000／手机 390×844 共 4 次检查通过，33 个站内链接与锚点有效，无页面横向溢出或运行时错误。详情见 `page-validation.json`、`validation.jsonl`、`check.log` 与 `build.log`。

没有实际启动 Docker 容器或 Spring Boot 应用，未连接数据库或调用模型；页面可构建不代表运行示例已经实测。未提交或推送代码。
