# 对话记忆官网覆盖审计

日期：2026-11-01。来源：[Chat Memory](https://docs.spring.io/spring-ai/reference/api/chat-memory.html)。

## 结论

核心内容与示例无遗漏；本次发现并补齐两处小细节：自定义 `ChatMemoryRepository` 的扩展入口，以及 JDBC 嵌入式初始化的 H2、HSQL、Derby 示例。补齐后，官网 33 个子章节均有对应内容，34 段代码、29 个配置项完整覆盖，原文无图片。

核对实时抓取的官网单页正文，去除导航和面包屑后，与此前保存的来源正文一致。因此这两处属于此前译文的轻微省略，并非官网新增内容。此次重排也没有删减既有正文。

## 章节对照

按语义逐节核对正文、提示、表格和示例；标题可合并或调整顺序，不以标题数量相等作为完整依据。

| 官网章节                                                                                                                                                    | 中文位置                                                                   | 结果   |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- | ------ |
| [Quick Start](https://docs.spring.io/spring-ai/reference/api/chat-memory.html#_quick_start)                                                                 | [对应内容](/frameworks/spring-ai/core/chat-memory/#default-configuration)  | 已覆盖 |
| [Working with Conversation IDs](https://docs.spring.io/spring-ai/reference/api/chat-memory.html#_working_with_conversation_ids)                             | [对应内容](/frameworks/spring-ai/core/chat-memory/#conversation-id)        | 已覆盖 |
| [Memory Types](https://docs.spring.io/spring-ai/reference/api/chat-memory.html#_memory_types)                                                               | [对应内容](/frameworks/spring-ai/core/chat-memory/#memory-vs-history)      | 已覆盖 |
| [Message Window Chat Memory](https://docs.spring.io/spring-ai/reference/api/chat-memory.html#_message_window_chat_memory)                                   | [对应内容](/frameworks/spring-ai/core/chat-memory/#message-window)         | 已覆盖 |
| [Turn-boundary eviction](https://docs.spring.io/spring-ai/reference/api/chat-memory.html#_turn_boundary_eviction)                                           | [对应内容](/frameworks/spring-ai/core/chat-memory/#turn-eviction)          | 已覆盖 |
| [Memory Storage](https://docs.spring.io/spring-ai/reference/api/chat-memory.html#_memory_storage)                                                           | [对应内容](/frameworks/spring-ai/core/chat-memory/#repositories)           | 已覆盖 |
| [In-Memory Repository](https://docs.spring.io/spring-ai/reference/api/chat-memory.html#_in_memory_repository)                                               | [对应内容](/frameworks/spring-ai/core/chat-memory/#in-memory)              | 已覆盖 |
| [JdbcChatMemoryRepository](https://docs.spring.io/spring-ai/reference/api/chat-memory.html#_jdbcchatmemoryrepository)                                       | [对应内容](/frameworks/spring-ai/core/chat-memory/#jdbc)                   | 已覆盖 |
| [Reading Message Timestamps](https://docs.spring.io/spring-ai/reference/api/chat-memory.html#_reading_message_timestamps)                                   | [对应内容](/frameworks/spring-ai/core/chat-memory/#jdbc-timestamps)        | 已覆盖 |
| [Supported Databases and Dialect Abstraction](https://docs.spring.io/spring-ai/reference/api/chat-memory.html#_supported_databases_and_dialect_abstraction) | [对应内容](/frameworks/spring-ai/core/chat-memory/#jdbc-dialects)          | 已覆盖 |
| [Configuration Properties](https://docs.spring.io/spring-ai/reference/api/chat-memory.html#_configuration_properties)                                       | [对应内容](/frameworks/spring-ai/core/chat-memory/#jdbc-dialects)          | 已覆盖 |
| [Schema Initialization](https://docs.spring.io/spring-ai/reference/api/chat-memory.html#_schema_initialization)                                             | [对应内容](/frameworks/spring-ai/core/chat-memory/#jdbc-dialects)          | 已覆盖 |
| [Extending Dialects](https://docs.spring.io/spring-ai/reference/api/chat-memory.html#_extending_dialects)                                                   | [对应内容](/frameworks/spring-ai/core/chat-memory/#jdbc-dialects)          | 已覆盖 |
| [CassandraChatMemoryRepository](https://docs.spring.io/spring-ai/reference/api/chat-memory.html#_cassandrachatmemoryrepository)                             | [对应内容](/frameworks/spring-ai/core/chat-memory/#cassandra)              | 已覆盖 |
| [Configuration Properties](https://docs.spring.io/spring-ai/reference/api/chat-memory.html#_configuration_properties_2)                                     | [对应内容](/frameworks/spring-ai/core/chat-memory/#cassandra-config)       | 已覆盖 |
| [Schema Initialization](https://docs.spring.io/spring-ai/reference/api/chat-memory.html#_schema_initialization_2)                                           | [对应内容](/frameworks/spring-ai/core/chat-memory/#cassandra-config)       | 已覆盖 |
| [Neo4j ChatMemoryRepository](https://docs.spring.io/spring-ai/reference/api/chat-memory.html#_neo4j_chatmemoryrepository)                                   | [对应内容](/frameworks/spring-ai/core/chat-memory/#neo4j)                  | 已覆盖 |
| [Configuration Properties](https://docs.spring.io/spring-ai/reference/api/chat-memory.html#_configuration_properties_3)                                     | [对应内容](/frameworks/spring-ai/core/chat-memory/#neo4j-indexes)          | 已覆盖 |
| [Index Initialization](https://docs.spring.io/spring-ai/reference/api/chat-memory.html#_index_initialization)                                               | [对应内容](/frameworks/spring-ai/core/chat-memory/#neo4j-indexes)          | 已覆盖 |
| [CosmosDBChatMemoryRepository](https://docs.spring.io/spring-ai/reference/api/chat-memory.html#_cosmosdbchatmemoryrepository)                               | [对应内容](/frameworks/spring-ai/core/chat-memory/#cosmos-db)              | 已覆盖 |
| [MongoChatMemoryRepository](https://docs.spring.io/spring-ai/reference/api/chat-memory.html#_mongochatmemoryrepository)                                     | [对应内容](/frameworks/spring-ai/core/chat-memory/#mongodb)                | 已覆盖 |
| [Configuration Properties](https://docs.spring.io/spring-ai/reference/api/chat-memory.html#_configuration_properties_4)                                     | [对应内容](/frameworks/spring-ai/core/chat-memory/#mongodb-config)         | 已覆盖 |
| [Collection Initialization](https://docs.spring.io/spring-ai/reference/api/chat-memory.html#_collection_initialization)                                     | [对应内容](/frameworks/spring-ai/core/chat-memory/#mongodb-config)         | 已覆盖 |
| [RedisChatMemoryRepository](https://docs.spring.io/spring-ai/reference/api/chat-memory.html#_redischatmemoryrepository)                                     | [对应内容](/frameworks/spring-ai/core/chat-memory/#redis)                  | 已覆盖 |
| [Configuration Properties](https://docs.spring.io/spring-ai/reference/api/chat-memory.html#_configuration_properties_5)                                     | [对应内容](/frameworks/spring-ai/core/chat-memory/#redis-config)           | 已覆盖 |
| [Advanced Querying](https://docs.spring.io/spring-ai/reference/api/chat-memory.html#_advanced_querying)                                                     | [对应内容](/frameworks/spring-ai/core/chat-memory/#redis-query)            | 已覆盖 |
| [Metadata Field Indexing](https://docs.spring.io/spring-ai/reference/api/chat-memory.html#_metadata_field_indexing)                                         | [对应内容](/frameworks/spring-ai/core/chat-memory/#redis-metadata)         | 已覆盖 |
| [Schema Initialization](https://docs.spring.io/spring-ai/reference/api/chat-memory.html#_schema_initialization_3)                                           | [对应内容](/frameworks/spring-ai/core/chat-memory/#redis-config)           | 已覆盖 |
| [Requirements](https://docs.spring.io/spring-ai/reference/api/chat-memory.html#_requirements)                                                               | [对应内容](/frameworks/spring-ai/core/chat-memory/#redis)                  | 已覆盖 |
| [Memory in Chat Client](https://docs.spring.io/spring-ai/reference/api/chat-memory.html#_memory_in_chat_client)                                             | [对应内容](/frameworks/spring-ai/core/chat-memory/#chatclient-memory)      | 已覆盖 |
| [VectorStoreChatMemoryAdvisor](https://docs.spring.io/spring-ai/reference/api/chat-memory.html#_vectorstorechatmemoryadvisor)                               | [对应内容](/frameworks/spring-ai/core/chat-memory/#vector-memory-template) | 已覆盖 |
| [Custom Template](https://docs.spring.io/spring-ai/reference/api/chat-memory.html#_custom_template)                                                         | [对应内容](/frameworks/spring-ai/core/chat-memory/#vector-memory-template) | 已覆盖 |
| [Memory in Chat Model](https://docs.spring.io/spring-ai/reference/api/chat-memory.html#_memory_in_chat_model)                                               | [对应内容](/frameworks/spring-ai/core/chat-memory/#chatmodel-memory)       | 已覆盖 |

## 代码与配置

- 34 段代码按 `code-fidelity.json` 的来源与目标位置逐段核对：32 段除注释及空白外相同；另外 2 段保留既有 JDBC properties 与 Cassandra `.build()` 校正。
- 29 个表格配置项全部对应；此前的 Cassandra 属性前缀与消息列默认值校正继续保留。Redis 的元数据索引定义另含在对应代码块中。
- 七类存储、完整轮次淘汰、会话 ID 必传、工具消息过滤、JDBC 迁移、Neo4j 标签约束、MongoDB TTL 索引重建、Redis 模块要求均已核对。

## 有意保留的校正

现有译文与官网在少数位置写法不同，原因是官网文字与该版本 API 不一致，而非漏译。证据来自此前保存的 [2.0.2 API 与源码核验](api-contract-checks.json)，本次未重新下载全部 API 制品。

- 向量记忆使用 `.systemPromptTemplate()`，保留两个占位符及与 ChatClient 模板配置的区别。官网 `.promptTemplate()` 未直接照抄。
- 官网提到的 `StPromptTemplate` 名称未机械照译；已保留默认 StringTemplate 引擎说明，既有源码实际创建 `PromptTemplate`。
- 工具中间消息说明区分 Advisor 执行位置与 Repository 支持类型，保留手动执行入口。
- Cassandra 的配置前缀、消息列默认值及 Builder 创建方式，JDBC 初始化选项与注释语法，沿用已有校正。

## 验证范围

补充后再次执行 `npm run check`（0 错误、0 警告、0 提示）与 `npm run build`（139 页），均通过。桌面 1440px、手机 390px 检查通过，新增内容正常显示，34 段代码与原有 30 个标题锚点保留，48 个站内链接及锚点可访问；定稿、修订与站点正文逐字节一致。

33 个章节的语义与配置描述由人工核对；代码映射、配置键存在性与数量由脚本辅助核验。完整机器记录见 [覆盖审计 JSON](2026-11-01-coverage-audit.json)。此次审计不包含外链页面全文，不编译执行 Java、不连接数据库或调用模型。

[结构调整记录](2026-11-01-structure.md)保留本次补充之前的历史页面哈希；本审计记录对应补充后的当前页面。
