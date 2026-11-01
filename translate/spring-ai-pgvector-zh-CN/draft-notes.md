# 初稿待审问题

代码按来源完整原样保留，待主代理核对并修订：

1. 第 1 个 SQL 块使用 `//` 注释，PostgreSQL 应使用 `--`，否则不能直接执行。
2. application.yml 代码块混用 Tab 和空格，需转为空格，并考虑添加 `initialize-schema: true` 承接首次初始化。
3. HNSW 2000 维限制应限定为 `vector` 类型，并核对 PGvector 当前支持类型；不能泛指所有类型。
4. 手动构造 `.dimensions(1536)` 注释称默认模型维度或1536，建议源码核对默认回退逻辑。
5. 示例中的 TOP_K、SIMILARITY_THRESHOLD、静态枚举常量和 context 均为片段依赖，需标明或给导入提示。
6. `remove-existing-vector-store-table=true` 会删除旧表，正文应直接说明数据后果。
7. Docker 示例为临时容器，`--rm` 且未挂载卷；仅作本地演示，不作为持久化配置。
8. schema-validation 是否要求对象已存在与 initialize-schema 执行先后，应以源码核对表述。

已复用站内向量存储与 Embedding 说明，Docker Compose、Testcontainers、OpenAI 接入和 BOM/仓库原文保留外链供主代理核对是否有等价站内锚点。
