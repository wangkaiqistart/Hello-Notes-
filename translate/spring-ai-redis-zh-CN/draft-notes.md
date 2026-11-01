# Redis 初稿待审校点

初稿完整保留 24 个源章节锚点、33 个源代码块（逐块原样保留）、16 行配置表和全部源链接目标（允许的站内替换除外），没有源图片。

1. 手动配置示例末尾 OpenAiEmbeddingModel 构造器与 OpenAiEmbeddingOptions.apiKey 写法疑似不符合 2.0.2 API。按要求初稿代码未改，请核对后修订或改为注入已配置 EmbeddingModel；代码主题不要丢失。
2. 原文说 Redis 开源且 BSD licensed，不能概括目前所有版本。初稿保留历史描述但补了发行版/许可证边界，可进一步压缩为中性介绍并把历史原句留审校记录。
3. 0–1 归一化和所有度量都保证范围的说法需检查源码，尤其 COSINE/IP、文本分数转换。初稿已标为原文说明并提示以实现为准，建议用实际公式替换。
4. 原文称范围检索返回所有阈值内文档，需核对是否内部存在 LIMIT/默认数量限制。
5. RedisVectorStore 的 searchByText、searchByRange 是具体实现扩展方法，不属于 VectorStore 接口，调用变量需要是 RedisVectorStore。
6. 文本/范围示例使用 category 过滤，前面的 metadataFields 只声明 country/year/description，执行前应补声明 category TAG 字段。
7. 文本搜索 inOrder=true 是否等价严格短语匹配需检查源码；初稿只写“按顺序进行短语匹配”，未声称全部实现细节。
8. 仅使用不同 indexName 的缓存隔离示例没有不同 prefix；若索引按同一默认前缀建索引，是否实际隔离必须核对，不能把索引名直接当租户授权。
9. 系统提示词哈希只区分系统提示词，不代表隔离完整历史、权限、工具结果和个人上下文。建议明确不适合直接共享个性化回答；不扩展为完整安全清单。
10. 语义缓存 similarity-threshold 与 builder distanceThreshold 数值方向不同，初稿明确提示不可直接混用，需核对自动配置换算公式与实际默认值。
11. 默认 redis/langcache-embed-v1 的自动配置是否需要模型下载/额外依赖和维度约束，需核对同版本源码。
12. TTL 的 set/get/clear 边界与 namespace 清空范围可据源码再补必要说明；当前代码只保留原文。

以上为初稿诊断，不代表已执行模型或 Redis。
