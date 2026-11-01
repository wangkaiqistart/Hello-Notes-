# 翻译要求

面向熟悉 Java/Spring Boot 的开发者，用简明技术中文完整翻译 Spring AI 2.0.2 Docker Compose 页。依赖、连接类型和镜像名原样保留。站内引用仅允许 Spring AI 模块，无法等价覆盖的 Boot 高级参考保留官方出处。阅读重点是启动开发服务、识别镜像、获取映射端口与连接信息。

补充真实的 PGvector 开发例子时，标明它由 Spring Boot 的 JDBC 连接工厂处理，以 postgres 服务标签匹配 pgvector 镜像；先配置 PGvector starter 和 EmbeddingModel，再运行容器，初始化显式开启。不把本篇当作 Docker 通用部署手册或 Testcontainers 完整说明。
