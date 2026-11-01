# 审校记录

- 初稿完整保留 2 个依赖片段和 9 条镜像匹配，原文无图片。原文缺少启动过程和 PGvector 场景，应在定稿中增加明确标注的补充说明。
- containers named 指镜像名称匹配，不是自定义 services 键或 container_name。基于 Boot 的自定义镜像说明，PGvector 示例使用 postgres 服务标签。
- PGvector 不在 Spring AI 扩展连接清单里；PostgreSQL JDBC、Redis、Elasticsearch 等连接由 Boot 提供，不能误认为不受支持。AI 模块 POM 非可选地依赖 spring-boot-docker-compose。
- 默认 start-and-stop、映射端口、连接信息优先于连接属性、已启动服务的停止边界，按 Boot 4.1.2 开发服务文档核对后写明。
- 本地示例需先添加 PGvector starter，并提供 EmbeddingModel；1536 是示例维度，initialize-schema 显式开启。服务连接不会完成资料入库或模型配置。
- Maven 和 Gradle 原文依赖保持字节一致；附加 compose.yml 与 application.yml 标为补充示例，不计作原文代码。
- 引用只使用 Spring AI 模块对应内容。Boot 完整生命周期、健康检查、自定义服务和 Testcontainers 缺少等价站内页面，保留原文入口。
