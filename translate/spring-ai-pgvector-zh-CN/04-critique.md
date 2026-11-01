# 审校记录

1. SQL 中 // 不是 PostgreSQL 注释；改为 -- 并标注 sql。
2. YAML 混用 Tab/空格；改为两空格缩进，显式开启本地首建 initialize-schema。
3. 2000维上限针对 vector 类型的 HNSW 索引，不泛化到 halfvec 等；核对 pgvector v0.8.1 README。
4. 按 v2.0.2 核对自动配置、初始化默认关闭、schema-validation 先名称后表结构的顺序、维度优先级与1536回退；表中保留全部9项参数。
5. 删除旧表只在初始化路径中执行，会丢失旧数据；max-document-batch-size 是文档数，与 Token 批处理不同。
6. 本地 Docker 示例临时且无持久卷，仅用于学习；配置片段还需已有 EmbeddingModel，静态枚举和TOP_K等是示例上下文。
7. BOM/仓库、统一过滤与Embedding改为等价站内引用；OpenAI专用配置、开发服务与上游扩展说明保留外链。
