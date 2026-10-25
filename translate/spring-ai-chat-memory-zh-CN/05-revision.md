---
title: Spring AI：对话记忆
description: ChatMemory 的会话隔离、消息窗口与完整轮次淘汰，各类存储实现，以及 ChatClient 和 ChatModel 的多轮对话用法。
sidebar:
  label: 对话记忆
  order: 10
---

大语言模型（LLM）本身不会保留上一次请求的状态。应用要支持多轮对话，就需要保存相关消息，并在后续请求中重新提供上下文。Spring AI 用 `ChatMemory` 管理这部分对话记忆。

初次学习可先读“记忆与历史的区别”“会话 ID”“消息窗口”和“在 ChatClient 中使用记忆”，再按项目使用的数据库查看存储配置。

## 记忆与完整聊天历史

`ChatMemory` 和 `ChatMemoryRepository` 分工如下：

| 抽象 | 职责 |
| --- | --- |
| `ChatMemory` | 决定保留哪些上下文消息、何时淘汰。可以实现最近 N 条、按时间或按 Token 预算等策略。 |
| `ChatMemoryRepository` | 保存、读取和删除消息，负责底层存储。 |

对话记忆只需包含本次回答相关的上下文；完整聊天历史则记录用户与模型交换过的全部消息。**窗口记忆不能替代完整聊天历史。** 需要长期查询、审计或完整回放时，应单独持久化原始记录，例如使用 Spring Data。

## 默认配置与快速接入

Spring AI 自动配置 `ChatMemory` Bean，默认组合是 `MessageWindowChatMemory` 与 `InMemoryChatMemoryRepository`。如果已配置 JDBC、Cassandra、Neo4j 等其他存储实现，自动配置会使用该实现。

```java
@Autowired
ChatMemory chatMemory;
```

只有内存存储时，消息保存在当前应用进程中，重启后不会保留。需要持久化时，再替换 `ChatMemoryRepository`，消息窗口策略可以继续复用。

下文都是分别演示用法的代码片段，省略 import 与应用配置。注入对象可用后再构建 `ChatMemory`，例如在 `@Bean` 工厂方法中完成；不要把依赖字段注入的构建语句直接作为字段初始化器。

## 会话 ID：上下文属于谁

每次记忆操作都必须显式提供会话 ID。`ChatMemory` 和 `ChatMemoryRepository` 按这个值读取、追加或删除消息；相同 ID 会指向相同会话。

多用户应用应为每个用户分配独立的会话 ID。同一用户有多个对话时，每个对话也要独立标识。常见做法是在服务端根据当前用户或会话生成 ID：

```java
// 根据当前用户与会话生成 ID，隔离各用户的对话。
String conversationId = currentUser.getId() + ":" + httpSession.getId();

chatClient.prompt()
    .user(userInput)
    .advisors(a -> a.param(ChatMemory.CONVERSATION_ID, conversationId))
    .call()
    .content();
```

这里的 `currentUser`、`httpSession` 和 `userInput` 由应用提供；示例按用户与 HTTP Session 分组。如果同一 Session 允许开启多个聊天窗口，还需加入独立的聊天会话标识。

- 不同用户不要共用固定 ID。
- 服务端生成或校验会话 ID，读取和删除时检查会话归属。
- 列出或删除会话时，只操作当前用户有权访问的 ID。

会话 ID 是存储分组依据，用户身份校验和访问控制仍由应用负责。

## 消息窗口：保留最近的上下文

`MessageWindowChatMemory` 是内置的默认策略。它维护一个消息滑动窗口，默认最多 **20 条消息**，超出后淘汰较早的消息，并保留 `SystemMessage`。

例如，将窗口上限改为 10 条：

```java
MessageWindowChatMemory memory = MessageWindowChatMemory.builder()
    .maxMessages(10)
    .build();
```

这里计算的是消息条数，**不是对话轮数**。一次用户提问可能包含多个模型回复、工具调用和工具结果。

### 按完整轮次淘汰

一轮从 `UserMessage` 开始，包含后续助手回复、工具调用与工具结果，直到下一条 `UserMessage` 之前。

窗口需要裁剪时，会按完整轮次淘汰。如果按数量计算的切点落在助手回复或工具结果上，就继续向后移动到下一条 `UserMessage`，避免留下缺少原始提问的半轮上下文。

因此，`maxMessages` 是窗口上限，实际保留的消息可能更少。若一轮工具调用就超过窗口大小，全部非系统消息都可能被淘汰，直到加入新的 `UserMessage`。应为典型的完整轮次预留足够空间。

## 存储实现

所有实现都应按从旧到新的顺序返回消息。选择存储前，除了持久化和部署方式，还要确认它是否支持业务需要的消息类型。

### 内存：InMemoryChatMemoryRepository

`InMemoryChatMemoryRepository` 使用 `ConcurrentHashMap` 保存消息。未配置其他 Repository 时，Spring AI 默认自动配置它：

```java
@Autowired
ChatMemoryRepository chatMemoryRepository;
```

也可以手动创建：

```java
ChatMemoryRepository repository = new InMemoryChatMemoryRepository();
```

适合本地学习或无需跨进程保留上下文的场景。多个应用实例各自持有内存，不能据此共享会话。

### JDBC：关系数据库

`JdbcChatMemoryRepository` 通过 JDBC 持久化消息，使用 `sequence_id` 记录消息在会话内的位置，并按该字段升序读取。

**JDBC 实现不支持工具调用消息。** 保存时会过滤带工具调用的 `AssistantMessage`，以及 `ToolResponseMessage`，读取时不会恢复这些消息。若需要完整保存工具调用过程，可评估 [Spring AI Session](https://spring-ai-community.github.io/spring-ai-session/latest/) 及其 [JDBC session store](https://spring-ai-community.github.io/spring-ai-session/latest/session-jdbc/)。

#### 依赖与创建

Maven：

```xml
<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>spring-ai-starter-model-chat-memory-repository-jdbc</artifactId>
</dependency>
```

Gradle：

```groovy
dependencies {
    implementation 'org.springframework.ai:spring-ai-starter-model-chat-memory-repository-jdbc'
}
```

使用自动配置的 Repository 构建记忆窗口：

```java
@Autowired
JdbcChatMemoryRepository chatMemoryRepository;

ChatMemory chatMemory = MessageWindowChatMemory.builder()
    .chatMemoryRepository(chatMemoryRepository)
    .maxMessages(10)
    .build();
```

手动创建时，提供 `JdbcTemplate` 和数据库方言：

```java
ChatMemoryRepository chatMemoryRepository = JdbcChatMemoryRepository.builder()
    .jdbcTemplate(jdbcTemplate)
    .dialect(new PostgresChatMemoryRepositoryDialect())
    .build();

ChatMemory chatMemory = MessageWindowChatMemory.builder()
    .chatMemoryRepository(chatMemoryRepository)
    .maxMessages(10)
    .build();
```

#### 读取消息时间

每条消息保存创建时间，类型为 `java.time.Instant`，元数据键为 `JdbcChatMemoryRepository.CONVERSATION_TS`：

```java
List<Message> messages = chatMemory.get(conversationId);
for (Message message : messages) {
    Instant createdAt = (Instant) message.getMetadata().get(JdbcChatMemoryRepository.CONVERSATION_TS);
}
```

重复保存会话时，已有消息保留原来的创建时间，适合用于界面展示。

#### 数据库与方言

内置支持 PostgreSQL、MySQL / MariaDB、SQL Server、HSQLDB 和 Oracle Database。`JdbcChatMemoryRepositoryDialect.from(DataSource)` 可以从 JDBC URL 自动识别方言。

以下配置统一使用前缀 `spring.ai.chat.memory.repository.jdbc.`：

| 属性后缀 | 含义 | 默认值 |
| --- | --- | --- |
| `initialize-schema` | 初始化策略：`embedded`、`always` 或 `never`。 | `embedded` |
| `schema` | 初始化脚本位置，支持 `classpath:` 与平台占位符。 | `classpath:org/springframework/ai/chat/memory/repository/jdbc/schema-@@platform@@.sql` |
| `platform` | 替换脚本路径中的 `@@platform@@`。 | 自动识别 |

自动配置使用对应数据库的 SQL 脚本创建 `SPRING_AI_CHAT_MEMORY` 表，默认只对嵌入式数据库执行初始化。

从 2.0.0 起，表中新增控制消息顺序的 `sequence_id` 列，原有 `timestamp` 列也会通过消息元数据暴露。已有数据库需要按[升级说明](https://docs.spring.io/spring-ai/reference/upgrade-notes.html)迁移。

初始化策略三选一；下面启用默认选项，另外两项作为注释供选择：

```properties
# 仅对嵌入式数据库初始化（默认）
spring.ai.chat.memory.repository.jdbc.initialize-schema=embedded
# 始终初始化：需要时取消下一行注释，并注释掉上面的配置
# spring.ai.chat.memory.repository.jdbc.initialize-schema=always
# 不初始化：交给 Flyway / Liquibase 等工具管理时使用
# spring.ai.chat.memory.repository.jdbc.initialize-schema=never
```

自定义脚本位置：

```properties
spring.ai.chat.memory.repository.jdbc.schema=classpath:/custom/path/schema-mysql.sql
```

支持其他数据库时，实现 `JdbcChatMemoryRepositoryDialect`，提供读取、写入和删除 SQL，再传入构建器：

```java
ChatMemoryRepository chatMemoryRepository = JdbcChatMemoryRepository.builder()
    .jdbcTemplate(jdbcTemplate)
    .dialect(new MyCustomDbDialect())
    .build();
```

`MyCustomDbDialect` 是应用自行实现的方言类。

### Cassandra：按时间保存窗口快照

`CassandraChatMemoryRepository` 使用 Apache Cassandra，适合需要高可用、持久化、扩展能力和生存时间（TTL）的场景。

它采用时间序列结构，保存历次聊天窗口的快照，可用于治理与审计；消息按时间戳升序返回。应按保留要求配置 TTL，来源以三年为例，这并非默认保留时长。窗口快照也不等于完整消息日志，尤其要注意下述工具消息限制。

**Cassandra 实现不支持工具调用消息。** 带工具调用的 `AssistantMessage` 和 `ToolResponseMessage` 在保存时会被过滤；需要完整过程时可评估前述 Spring AI Session。

#### 依赖与创建

Maven：

```xml
<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>spring-ai-starter-model-chat-memory-repository-cassandra</artifactId>
</dependency>
```

Gradle：

```groovy
dependencies {
    implementation 'org.springframework.ai:spring-ai-starter-model-chat-memory-repository-cassandra'
}
```

使用自动配置：

```java
@Autowired
CassandraChatMemoryRepository chatMemoryRepository;

ChatMemory chatMemory = MessageWindowChatMemory.builder()
    .chatMemoryRepository(chatMemoryRepository)
    .maxMessages(10)
    .build();
```

手动创建时，先构建 `CassandraChatMemoryRepositoryConfig`，再调用 `create(...)`：

```java
ChatMemoryRepository chatMemoryRepository = CassandraChatMemoryRepository
    .create(CassandraChatMemoryRepositoryConfig.builder().withCqlSession(cqlSession).build());

ChatMemory chatMemory = MessageWindowChatMemory.builder()
    .chatMemoryRepository(chatMemoryRepository)
    .maxMessages(10)
    .build();
```

#### 配置与初始化

连接设置来自 Spring Boot 的 `spring.cassandra.*` 配置。下面列出本地连接示例值，使用时填写实际集群地址、端口和数据中心：

| 属性 | 含义 | 本地连接示例值 |
| --- | --- | --- |
| `spring.cassandra.contact-points` | 用于发现集群的初始节点。 | `127.0.0.1` |
| `spring.cassandra.port` | 原生协议端口。 | `9042` |
| `spring.cassandra.local-datacenter` | 连接的数据中心。 | `datacenter1` |

Repository 设置统一使用前缀 `spring.ai.chat.memory.repository.cassandra.`：

| 属性后缀 | 含义 | 默认值 |
| --- | --- | --- |
| `time-to-live` | 写入消息的 TTL。 | 未设置 |
| `keyspace` | Keyspace 名称。 | `springframework` |
| `messages-column` | 保存消息的列名。 | `messages` |
| `table` | 表名。 | `ai_chat_memory` |
| `initialize-schema` | 是否在启动时初始化结构。 | `true` |

启动时会自动创建默认的 `ai_chat_memory` 表。设置 `spring.ai.chat.memory.repository.cassandra.initialize-schema=false` 可关闭初始化。

### Neo4j：图数据库

`Neo4jChatMemoryRepository` 把会话消息保存为属性图中的节点与关系，适合需要结合 Neo4j 图能力持久化上下文的应用。消息按会话内的消息索引升序返回。

#### 依赖与创建

Maven：

```xml
<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>spring-ai-starter-model-chat-memory-repository-neo4j</artifactId>
</dependency>
```

Gradle：

```groovy
dependencies {
    implementation 'org.springframework.ai:spring-ai-starter-model-chat-memory-repository-neo4j'
}
```

使用自动配置：

```java
@Autowired
Neo4jChatMemoryRepository chatMemoryRepository;

ChatMemory chatMemory = MessageWindowChatMemory.builder()
    .chatMemoryRepository(chatMemoryRepository)
    .maxMessages(10)
    .build();
```

手动创建时提供 Neo4j `Driver`：

```java
ChatMemoryRepository chatMemoryRepository = Neo4jChatMemoryRepository.builder()
    .driver(driver)
    .build();

ChatMemory chatMemory = MessageWindowChatMemory.builder()
    .chatMemoryRepository(chatMemoryRepository)
    .maxMessages(10)
    .build();
```

#### 标签与索引

以下配置统一使用前缀 `spring.ai.chat.memory.repository.neo4j.`：

| 属性后缀 | 对应节点 | 默认标签 |
| --- | --- | --- |
| `session-label` | 会话 | `Session` |
| `message-label` | 消息 | `Message` |
| `tool-call-label` | 工具调用 | `ToolCall` |
| `metadata-label` | 消息元数据 | `Metadata` |
| `tool-response-label` | 工具响应 | `ToolResponse` |
| `media-label` | 消息关联的媒体 | `Media` |

标签必须以字母或下划线开头，其余字符只允许字母、数字和下划线；无效标签会在启动时触发 `IllegalArgumentException`。

Repository 会自动确保会话 ID 和消息索引上的索引存在，自定义标签也会创建相应索引。不需要单独初始化表结构，但应用必须能够连接 Neo4j。

### Cosmos DB：外部模块

`CosmosDBChatMemoryRepository` 由 Azure Cosmos DB 团队维护，作为外部模块提供。接入方法见 [Cosmos DB 对话记忆文档](https://azurecosmosdb.github.io/spring-ai/docs/chat-memory.html)。

### MongoDB：文档数据库

`MongoChatMemoryRepository` 使用 MongoDB 保存消息，适合需要灵活文档结构的持久化场景。消息按时间戳升序读取。

**MongoDB 实现不支持工具调用消息。** 保存时会过滤带工具调用的 `AssistantMessage` 和 `ToolResponseMessage`。需要完整保存工具调用过程时，可评估前述 Spring AI Session。

#### 依赖与创建

Maven：

```xml
<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>spring-ai-starter-model-chat-memory-repository-mongodb</artifactId>
</dependency>
```

Gradle：

```groovy
dependencies {
    implementation 'org.springframework.ai:spring-ai-starter-model-chat-memory-repository-mongodb'
}
```

使用自动配置：

```java
@Autowired
MongoChatMemoryRepository chatMemoryRepository;

ChatMemory chatMemory = MessageWindowChatMemory.builder()
    .chatMemoryRepository(chatMemoryRepository)
    .maxMessages(10)
    .build();
```

手动创建时提供 `MongoTemplate`：

```java
ChatMemoryRepository chatMemoryRepository = MongoChatMemoryRepository.builder()
    .mongoTemplate(mongoTemplate)
    .build();

ChatMemory chatMemory = MessageWindowChatMemory.builder()
    .chatMemoryRepository(chatMemoryRepository)
    .maxMessages(10)
    .build();
```

#### 配置与集合初始化

以下配置统一使用前缀 `spring.ai.chat.memory.repository.mongo.`，注意与 Starter 名称中的 `mongodb` 区分：

| 属性后缀 | 含义 | 默认值 |
| --- | --- | --- |
| `create-indices` | 启动时是否自动创建或重建索引。修改 TTL 会删除并重建 TTL 索引。 | `false` |
| `ttl` | 消息 TTL，单位为秒；未设置时不过期。 | `0` |

启动时，如果 `ai_chat_memory` 集合不存在，自动配置会创建它。

### Redis：JSON 存储与检索

`RedisChatMemoryRepository` 使用 Redis Stack 的 RedisJSON 与 Redis Query Engine，将消息保存为 JSON 文档，并建立搜索索引。它支持可选 TTL，以及按内容、消息类型、时间范围和元数据查询。消息按时间戳升序读取。

需要 Redis Stack 7.0 或更高版本，并包含 Redis Query Engine 与 RedisJSON 模块；普通的 Redis 键值实例不能直接替代。Jedis 客户端库随依赖引入。

#### 依赖与创建

Maven：

```xml
<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>spring-ai-starter-model-chat-memory-repository-redis</artifactId>
</dependency>
```

Gradle：

```groovy
dependencies {
    implementation 'org.springframework.ai:spring-ai-starter-model-chat-memory-repository-redis'
}
```

使用自动配置：

```java
@Autowired
RedisChatMemoryRepository chatMemoryRepository;

ChatMemory chatMemory = MessageWindowChatMemory.builder()
    .chatMemoryRepository(chatMemoryRepository)
    .maxMessages(10)
    .build();
```

手动创建时提供 Jedis 的 `RedisClient`，可设置索引名、键前缀和 TTL：

```java
RedisClient jedisClient = RedisClient.builder().hostAndPort("localhost", 6379).build();

ChatMemoryRepository chatMemoryRepository = RedisChatMemoryRepository.builder()
    .jedisClient(jedisClient)
    .indexName("my-chat-index")
    .keyPrefix("my-chat:")
    .timeToLive(Duration.ofHours(24))
    .build();

ChatMemory chatMemory = MessageWindowChatMemory.builder()
    .chatMemoryRepository(chatMemoryRepository)
    .maxMessages(10)
    .build();
```

#### 配置与索引初始化

以下配置统一使用前缀 `spring.ai.chat.memory.repository.redis.`：

| 属性后缀 | 含义 | 默认值 |
| --- | --- | --- |
| `host` | Redis 主机。 | `localhost` |
| `port` | Redis 端口。 | `6379` |
| `username` | Redis ACL 用户名。 | 无 |
| `password` | Redis 密码。 | 无 |
| `index-name` | 搜索索引名。 | `chat-memory-idx` |
| `key-prefix` | 记忆条目的键前缀。 | `chat-memory:` |
| `time-to-live` | 条目 TTL，如 `24h`、`30d`。 | 不过期 |
| `initialize-schema` | 启动时是否初始化搜索索引。 | `true` |
| `max-conversation-ids` | 返回会话 ID 的数量上限。 | `1000` |
| `max-messages-per-conversation` | 每个会话返回消息的数量上限。 | `1000` |

搜索索引不存在时，自动配置会在启动时创建；设置 `spring.ai.chat.memory.repository.redis.initialize-schema=false` 可关闭。这两个查询数量上限与 `MessageWindowChatMemory.maxMessages` 的窗口策略不同。

#### 高级查询

Redis 实现还实现了 `AdvancedRedisChatMemoryRepository`。下面分别展示按类型、内容、时间、元数据和自定义表达式查询：

```java
// 转换为高级查询接口
AdvancedRedisChatMemoryRepository advancedRepo = (AdvancedRedisChatMemoryRepository) chatMemoryRepository;

// 跨会话按消息类型查询
List<MessageWithConversation> userMessages = advancedRepo.findByType(MessageType.USER, 100);

// 按内容查询
List<MessageWithConversation> results = advancedRepo.findByContent("Spring AI", 50);

// 在指定会话内按时间范围查询
List<MessageWithConversation> recentMessages = advancedRepo.findByTimeRange(
    conversationId,
    Instant.now().minus(Duration.ofHours(1)),
    Instant.now(),
    100
);

// 按元数据查询
List<MessageWithConversation> priorityMessages = advancedRepo.findByMetadata("priority", "high", 50);

// 执行自定义 Redis 查询
List<MessageWithConversation> customResults = advancedRepo.executeQuery("@type:USER @content:Redis", 100);
```

其中 `findByType`、`findByContent`、`findByMetadata` 和示例中的自定义表达式可能跨会话查询，不能直接作为普通用户的会话列表接口。应用必须把查询范围限制在当前用户有权访问的会话；`findByTimeRange` 示例则显式传入了 `conversationId`。

#### 元数据字段索引

通过 `metadata-fields` 定义需要检索的元数据字段：

```properties
spring.ai.chat.memory.repository.redis.metadata-fields[0].name=priority
spring.ai.chat.memory.repository.redis.metadata-fields[0].type=tag
spring.ai.chat.memory.repository.redis.metadata-fields[1].name=score
spring.ai.chat.memory.repository.redis.metadata-fields[1].type=numeric
spring.ai.chat.memory.repository.redis.metadata-fields[2].name=category
spring.ai.chat.memory.repository.redis.metadata-fields[2].type=tag
```

字段类型支持 `tag`（精确匹配）、`text`（全文搜索）和 `numeric`（数值范围查询）。

## 在 ChatClient 中使用记忆

使用 [ChatClient API](/frameworks/spring-ai/core/chat-client/) 时，通过记忆 Advisor 自动补充上下文：

| Advisor | 上下文来源与注入方式 |
| --- | --- |
| `MessageChatMemoryAdvisor` | 从 `ChatMemory` 读取当前会话消息，以消息列表形式加入提示词。 |
| `VectorStoreChatMemoryAdvisor` | 从 `VectorStore` 检索对话记忆，将结果作为纯文本附加到系统消息；只支持文本交互。 |

例如，把消息窗口与 `MessageChatMemoryAdvisor` 组合：

```java
ChatMemory chatMemory = MessageWindowChatMemory.builder().build();

ChatClient chatClient = ChatClient.builder(chatModel)
    .defaultAdvisors(MessageChatMemoryAdvisor.builder(chatMemory).build())
    .build();
```

每次调用时，Advisor 根据会话 ID 读取并维护记忆：

```java
String conversationId = "007";

chatClient.prompt()
    .user("Do I have license to code?")
    .advisors(a -> a.param(ChatMemory.CONVERSATION_ID, conversationId))
    .call()
    .content();
```

`"007"` 只是单会话示例，实际应用应使用前文的服务端会话分配方式。

**所有记忆 Advisor 都要求显式传入 `ChatMemory.CONVERSATION_ID`。** 没有默认会话 ID，缺失时会抛出 `IllegalArgumentException`。

### 工具调用消息的边界

默认情况下，记忆 Advisor 位于工具调用循环外，不会逐次保存循环中的中间消息。需要保存这些消息时，可按[用户控制的工具执行](https://docs.spring.io/spring-ai/reference/api/tools.html#user-controlled-tool-execution)自行管理，或结合 [Advisors API](/frameworks/spring-ai/core/advisors/) 调整处理链。

在 2.0.2 中，`ToolCallingAdvisor` 允许后续 Advisor 参与每次工具调用迭代；是否采集中间消息取决于 Advisor 的位置与执行方式。即使已经采集，Repository 仍须支持对应消息类型：JDBC、Cassandra、MongoDB 会过滤工具调用消息，不能据此承诺完整回放。

### VectorStoreChatMemoryAdvisor 自定义模板

`VectorStoreChatMemoryAdvisor` 默认通过模板把检索到的记忆合入系统消息。可用构建器的 `.systemPromptTemplate()` 传入自定义 `PromptTemplate`，方法签名见 [2.0.2 API](https://docs.spring.io/spring-ai/docs/2.0.2/api/org/springframework/ai/chat/client/advisor/vectorstore/VectorStoreChatMemoryAdvisor.Builder.html)。

模板必须包含两个占位符：

- `instructions`：原始系统消息。
- `long_term_memory`：检索到的对话记忆。

可使用不同的 `TemplateRenderer`；默认基于 [StringTemplate](https://www.stringtemplate.org/) 引擎。

这里配置的是 **Advisor 合并记忆时使用的模板**。`ChatClient.templateRenderer()` 则用于 Advisor 执行前的初始用户与系统提示词渲染，两者不是同一个配置入口，详见[提示词模板](/frameworks/spring-ai/core/chat-client/#提示词模板)。

## 直接使用 ChatModel 管理记忆

直接调用 [ChatModel](/frameworks/spring-ai/models/chat-model/) 时，需要显式管理消息：先加入用户消息，再读取上下文调用模型，最后把模型回复加入记忆。

```java
// 创建记忆实例
ChatMemory chatMemory = MessageWindowChatMemory.builder().build();
String conversationId = "007";

// 第一次交互
UserMessage userMessage1 = new UserMessage("My name is James Bond");
chatMemory.add(conversationId, userMessage1);
ChatResponse response1 = chatModel.call(new Prompt(chatMemory.get(conversationId)));
chatMemory.add(conversationId, response1.getResult().getOutput());

// 第二次交互
UserMessage userMessage2 = new UserMessage("What is my name?");
chatMemory.add(conversationId, userMessage2);
ChatResponse response2 = chatModel.call(new Prompt(chatMemory.get(conversationId)));
chatMemory.add(conversationId, response2.getResult().getOutput());

// 模型可根据上下文回答 "James Bond"
```

第二次请求会带上第一次对话的上下文，模型因而能够根据历史回答姓名；实际响应仍由所选模型决定。这里的 `"007"` 同样只是演示 ID。

来源：[Chat Memory](https://docs.spring.io/spring-ai/reference/api/chat-memory.html)。文档版本：2.0.2；核验日期：2026-10-25。
