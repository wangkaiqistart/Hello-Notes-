# 工具搜索

AI 智能体连接 Slack、GitHub、Jira 或多个 MCP Server 后，可用工具会迅速增加。来源举例：多服务部署可能聚合 50 多个工具，仅工具定义就在对话开始前消耗 55,000 多个词元（Token）；当模型面对 30 多个名称相似的工具时，选择准确率也可能下降。

`ToolSearchToolCallingAdvisor` 通过替换默认 `ToolCallingAdvisor` 实现**渐进式工具暴露**：不一次发送所有工具定义，而是根据需要逐步提供。来源在 OpenAI、Anthropic 和 Gemini 上的测试中观察到 34–64% 的 Token 降幅，同时保留对大型工具库的访问能力。测试条件与方法见[工具智能选择博客](https://spring.io/blog/2025/12/11/spring-ai-tool-search-tools-tzolov)，这些数值不是对所有应用的效果保证。

本篇介绍该 Advisor、`ToolIndex` 检索策略、配置与 Spring Boot 自动配置。它在整体架构中的位置见[扩展到数百个工具](https://docs.spring.io/spring-ai/reference/api/tools.html#scaling-to-hundreds-of-tools)。

<a id="how-it-works"></a>

## 工作流程

`ToolSearchToolCallingAdvisor` 继承 `ToolCallingAdvisor`，覆盖初始化与每次迭代前的钩子。运行过程如下：

1. **建立索引**：会话开始时，把全部已注册工具写入配置的 `ToolIndex`，此时不向模型发送这些工具定义。
2. **初始请求**：第一次模型请求只包含内置的 `toolSearchTool` 定义。
3. **发现能力**：模型需要某项能力时，用自然语言查询调用 `toolSearchTool`。
4. **搜索并扩展**：`ToolIndex` 找到匹配工具，将其定义加入下一次迭代的上下文。
5. **请求工具调用**：模型获得定义后，发出普通工具调用请求。
6. **执行工具**：`ToolCallingManager` 执行已发现的工具，并返回结果。
7. **生成回答**：模型根据工具结果输出最终答案。

下图重点看“先搜索工具，再执行工具”的两阶段过程，而非把整个工具目录一开始就放入请求：

![工具搜索调用流程：先调用 toolSearchTool 找到相关工具，再向模型提供定义并执行业务工具](https://docs.spring.io/spring-ai/reference/_images/tools/spring-ai-tool-search-tool-calling-flow.png)

索引按会话划分，并发对话使用各自的工具索引，详见[会话隔离](https://docs.spring.io/spring-ai/reference/api/tools/tool-search-tool.html#session-scoping)。

<a id="when-to-use"></a>

## 何时使用

适合以下情况：

- `ChatClient` 注册了 10 个以上工具。
- 每次请求的工具定义占用超过 10K Token。
- 连接多个 MCP Server，聚合后的工具目录很大。
- 工具数量增多后，已经出现选择不准确的问题。

以下情况继续使用默认 `ToolCallingAdvisor` 即可：

- 工具少于 10 个。
- 每个会话都会频繁用到全部工具。
- 工具定义很短，额外的搜索往返成本高于节省的 Token。

<a id="installation"></a>

## 安装

最简单的方式是使用包含 Lucene 和自动配置的 Spring Boot Starter。

Maven：

```xml
<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>spring-ai-starter-tool-search-advisor</artifactId>
</dependency>
```

Gradle：

```gradle
dependencies {
    implementation 'org.springframework.ai:spring-ai-starter-tool-search-advisor'
}
```

需要手动配置时，也可以直接使用库模块。

Maven：

```xml
<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>spring-ai-tool-search-advisor</artifactId>
</dependency>
```

Gradle：

```gradle
dependencies {
    implementation 'org.springframework.ai:spring-ai-tool-search-advisor'
}
```

<a id="quick-start"></a>

## 快速开始

最简接入见后面的 [Spring Boot 自动配置](https://docs.spring.io/spring-ai/reference/api/tools/tool-search-tool.html#spring-boot-auto-configuration)。手动装配示例：

```java
// 1. 配置 ToolIndex（语义、关键词或正则检索）
@Bean
ToolIndex toolIndex(VectorStore vectorStore) {
    return new VectorToolIndex(vectorStore);
}

// 2. 构建 Advisor
var toolSearchAdvisor = ToolSearchToolCallingAdvisor.builder()
    .toolIndex(toolIndex)
    .maxResults(5)
    .build();

// 3. 注册到 ChatClient：工具先建立索引，不会一开始就全部发送给模型
ChatClient chatClient = ChatClient.builder(chatModel)
    .defaultTools(new MyTools())
    .defaultAdvisors(toolSearchAdvisor)
    .build();

// 4. 发起请求，通过 Advisor 上下文提供会话 ID
String answer = chatClient.prompt("Help me plan what to wear today in Amsterdam")
    .advisors(a -> a.param(ChatMemory.CONVERSATION_ID, "user-42-session"))
    .call()
    .content();
```

<a id="session-scoping"></a>

## 会话隔离

`ToolSearchToolCallingAdvisor` 为每个会话分别建立索引。会话 ID 决定当前请求使用哪组工具索引，从而划分不同租户或不同对话的工具集合。

每次请求都必须提供会话 ID。默认从 Advisor 上下文的 `ChatMemory.CONVERSATION_ID` 键中读取：

```java
chatClient.prompt()
    .advisors(a -> a.param(ChatMemory.CONVERSATION_ID, "user-42-session"))
    .user("...")
    .call()
    .content();
```

如果应用已用 `tenantId`、`userId` 等其他键传递会话标识，可以通过 `sessionIdKeyName(...)` 或对应配置修改读取位置：

```java
var advisor = ToolSearchToolCallingAdvisor.builder()
    .toolIndex(toolIndex)
    .sessionIdKeyName("tenantId")
    .build();
```

如果已经为 `MessageChatMemoryAdvisor` 传入会话 ID，同一个上下文键也能用于工具搜索，不需要重复提供。

<a id="search-strategies"></a>

## 检索策略

`ToolIndex` 抽象检索实现，内置三种策略：

| 策略 | 实现 | 适用场景 |
| --- | --- | --- |
| 语义检索 | `VectorToolIndex` | 自然语言、模糊匹配和不同措辞；调用方描述需要什么，而非直接给出工具名。 |
| 关键词检索 | `LuceneToolIndex` | 词汇明确，需要快速、精确的关键词匹配。 |
| 正则匹配 | `RegexToolIndex` | 工具名有固定模式，例如 `get_*_data`；默认实现，无额外依赖。 |

<a id="vector-tool-index"></a>

### VectorToolIndex：语义检索

使用基于嵌入（Embedding）的相似度检索，适合根据自然语言描述查找工具：

```java
@Bean
ToolIndex vectorToolIndex(VectorStore vectorStore) {
    return new VectorToolIndex(vectorStore);
}
```

需要一个 `VectorStore` Bean，例如通过 `spring-ai-starter-vector-store-pgvector` 提供。建立索引时，对工具名和描述生成向量；查询时，对 `toolSearchTool` 的查询生成向量，返回 Top-K 匹配项。

<a id="lucene-tool-index"></a>

### LuceneToolIndex：关键词检索

使用 Apache Lucene 进行关键词检索，速度快，不依赖 Embedding 模型：

```java
@Bean
ToolIndex luceneToolIndex() {
    return new LuceneToolIndex();          // 默认最低分数为 0.25
    // return new LuceneToolIndex(0.4f);   // 自定义最低分数阈值
}
```

低于最低分数阈值的命中会被过滤。提高阈值会收紧匹配，降低阈值则放宽匹配。

<a id="regex-tool-index"></a>

### RegexToolIndex：模式匹配

按正则表达式匹配工具名称，适合工具名遵循固定规范（如 `get_*`、`database`）的情况，无额外依赖：

```java
@Bean
ToolIndex regexToolIndex() {
    return new RegexToolIndex();
}
```

未显式设置 `tool-index-type` 时，默认使用它。

<a id="configuration"></a>

## 配置

`ToolSearchToolCallingAdvisor.Builder` 继承 `ToolCallingAdvisor.Builder`，增加以下检索选项。继承的选项见 [ToolCallingAdvisor 构建器](https://docs.spring.io/spring-ai/reference/api/tools/tool-calling-advisor.html#builder-options)。

| 选项 | 作用 | 默认值 |
| --- | --- | --- |
| `toolIndex(ToolIndex)` | 使用的工具检索实现。 | 必填 |
| `maxResults(Integer)` | 每次 `toolSearchTool` 调用最多返回多少个工具引用。为 `null` 时由模型决定，内置工具描述提示值为 5。 | `null` |
| `systemMessageSuffix(String)` | 附加到系统消息的提示词，说明如何使用 `toolSearchTool`。 | 内置模板，见 `DEFAULT_SYSTEM_PROMPT_SUFFIX.md` |
| `referenceToolNameAccumulation(boolean)` | 为 `true` 时累积之前所有搜索调用发现的工具名；为 `false` 时仅保留最近一次搜索轮次的结果，包括该轮并行搜索的全部结果。 | `true` |
| `sessionIdKeyName(String)` | 从 Advisor 上下文读取会话 ID 时使用的键。 | `ChatMemory.CONVERSATION_ID` |
| `evictionStrategy(ToolIndexEvictionStrategy)` | 决定何时释放会话工具索引，见[索引淘汰](https://docs.spring.io/spring-ai/reference/api/tools/tool-search-tool.html#index-eviction)。 | `LruEvictionStrategy(1000)` |

<a id="tool-index-api"></a>

## ToolIndex API

`ToolIndex` 及配套类型 `ToolSearchRequest`、`ToolSearchResponse`、`ToolReference` 位于 `spring-ai-tool-search-tool` 模块的 `org.springframework.ai.tool.toolsearch` 包。`LuceneToolIndex`、`VectorToolIndex` 和 `RegexToolIndex` 也在这个模块中。

```xml
<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>spring-ai-tool-search-tool</artifactId>
</dependency>
```

```java
public interface ToolIndex {

    void indexTool(String sessionId, ToolReference toolReference);

    /** 默认实现循环调用 indexTool。 */
    void indexTools(String sessionId, List<ToolReference> toolReferences);

    ToolSearchResponse search(ToolSearchRequest request);

    void clearIndex(String sessionId);
}
```

每项操作都通过 `sessionId` 划分范围。需要自定义策略时，可以直接实现 `ToolIndex`，例如带角色过滤的数据库工具目录，或带缓存的远程工具注册表。

<a id="index-eviction"></a>

## 索引淘汰

每个会话的工具索引都会占用内存。`ToolIndexEvictionStrategy` 决定何时释放它们。

默认策略为 `LruEvictionStrategy(1000)`，最多保留 1,000 个活跃会话，超出时淘汰最久未使用的会话。也可以调用 `advisor.evictSession(sessionId)` 主动释放，例如用户退出登录时。

淘汰检查在每次请求时惰性执行，不需要后台线程。内置策略如下：

| 策略 | 行为 |
| --- | --- |
| `LruEvictionStrategy(maxSessions)`（默认） | 活跃会话超过上限时，淘汰最久未使用的会话。 |
| `NeverEvictStrategy.INSTANCE` | 不自动淘汰，直到显式调用 `evictSession()`。 |
| `AlwaysEvictStrategy.INSTANCE` | 每次请求前清空当前会话索引，每轮重新建立索引，适合测试或工具集合每次都变化的场景。 |
| `TtlEvictionStrategy(duration)` | 淘汰空闲时间超过 TTL 的会话。 |
| `CompositeEvictionStrategy(strategies...)` | 组合多个策略；任一策略要求淘汰就执行。 |

```java
// 默认：LRU 最多保留 1000 个会话，无需额外配置
var advisor = ToolSearchToolCallingAdvisor.builder()
    .toolIndex(toolIndex)
    .build();

// 不自动淘汰，自行管理会话生命周期
var advisor = ToolSearchToolCallingAdvisor.builder()
    .toolIndex(toolIndex)
    .evictionStrategy(NeverEvictStrategy.INSTANCE)
    .build();

// 每次请求都淘汰并重新建立索引，适合测试
var advisor = ToolSearchToolCallingAdvisor.builder()
    .toolIndex(toolIndex)
    .evictionStrategy(AlwaysEvictStrategy.INSTANCE)
    .build();

// 自定义 LRU 会话上限
var advisor = ToolSearchToolCallingAdvisor.builder()
    .toolIndex(toolIndex)
    .evictionStrategy(new LruEvictionStrategy(200))
    .build();

// 淘汰空闲超过 30 分钟的会话
var advisor = ToolSearchToolCallingAdvisor.builder()
    .toolIndex(toolIndex)
    .evictionStrategy(new TtlEvictionStrategy(Duration.ofMinutes(30)))
    .build();

// 组合 TTL 和 LRU 上限
var advisor = ToolSearchToolCallingAdvisor.builder()
    .toolIndex(toolIndex)
    .evictionStrategy(new CompositeEvictionStrategy(
        new TtlEvictionStrategy(Duration.ofMinutes(30)),
        new LruEvictionStrategy(200)))
    .build();
```

<a id="spring-boot-auto-configuration"></a>

## Spring Boot 自动配置

引入 `spring-ai-starter-tool-search-advisor` 后，用一个属性启用：

```properties
spring.ai.chat.client.tool-search-advisor.enabled=true
```

启用后，自动配置会：

- 注册声明类型为 `ToolCallingAdvisor.Builder<?>` 的 `ToolSearchToolCallingAdvisor.Builder` Bean。默认构建器有 `@ConditionalOnMissingBean` 条件，因此搜索构建器可以替换默认 `ToolCallingAdvisor`，无需修改现有 `ChatClient` 代码。底层机制见[自定义 ToolAdvisor 的自动配置集成](https://docs.spring.io/spring-ai/reference/api/tools.html#custom-tool-advisor-autoconfig)。
- 应用没有显式声明 `ToolIndex` 时，自动注册一个。

<a id="tool-index-auto-selection"></a>

### 自动选择 ToolIndex

通过 `spring.ai.chat.client.tool-search-advisor.tool-index-type` 选择实现：

| 值 | 实现 | 依赖条件 |
| --- | --- | --- |
| `regex`（默认） | `RegexToolIndex` | 无额外依赖。 |
| `lucene` | `LuceneToolIndex` | 类路径中有 `org.apache.lucene:lucene-core`，Starter 已包含。 |
| `vector` | `VectorToolIndex` | 应用上下文中存在 `VectorStore` Bean。 |

应用自定义的 `ToolIndex` Bean 始终优先，`@ConditionalOnMissingBean` 会跳过内置配置。

<a id="properties-reference"></a>

### 配置属性参考

| 属性 | 作用 | 默认值 |
| --- | --- | --- |
| `spring.ai.chat.client.tool-search-advisor.enabled` | 启用工具搜索；为 `true` 时替换默认 `ToolCallingAdvisor`。 | `false` |
| `spring.ai.chat.client.tool-search-advisor.tool-index-type` | 工具索引实现：`regex`、`lucene` 或 `vector`。 | `regex` |
| `spring.ai.chat.client.tool-search-advisor.max-results` | 每次搜索返回工具引用的数量上限；`null` 使用内置默认行为。 | `null` |
| `spring.ai.chat.client.tool-search-advisor.system-message-suffix` | 附加到系统消息的自定义提示词；`null` 使用内置模板。 | `null` |
| `spring.ai.chat.client.tool-search-advisor.reference-tool-name-accumulation` | 是否累积全部搜索轮次发现的工具名；为 `false` 时仅保留最近一轮，包括该轮并行调用的结果。 | `true` |
| `spring.ai.chat.client.tool-search-advisor.session-id-key-name` | Advisor 上下文中传递会话 ID 的键。 | `chat_memory_conversation_id` |
| `spring.ai.chat.client.tool-search-advisor.advisor-order` | 在处理链中的执行顺序。 | `HIGHEST_PRECEDENCE + 300` |
| `spring.ai.chat.client.tool-search-advisor.eviction.lru-max-sessions` | LRU 策略保留的最大活跃会话数。 | `1000` |
| `spring.ai.chat.client.tool-search-advisor.eviction.ttl` | 空闲会话的 TTL；设置后使用 LRU 与 TTL 的组合策略，接受 `30m`、`1h` 等 `java.time.Duration` 格式。 | `null` |
| `spring.ai.chat.client.tool-search-advisor.lucene.min-score-threshold` | Lucene 命中的最低分数阈值，仅对 `tool-index-type=lucene` 生效。 | `0.25` |

<a id="example-configurations"></a>

### 配置示例

Lucene：自定义分数阈值，并启用 TTL 淘汰：

```properties
spring.ai.chat.client.tool-search-advisor.enabled=true
spring.ai.chat.client.tool-search-advisor.tool-index-type=lucene
spring.ai.chat.client.tool-search-advisor.lucene.min-score-threshold=0.4
spring.ai.chat.client.tool-search-advisor.eviction.ttl=30m
```

向量检索，需要应用已有 `VectorStore` Bean：

```properties
spring.ai.chat.client.tool-search-advisor.enabled=true
spring.ai.chat.client.tool-search-advisor.tool-index-type=vector
```

多租户部署中，自定义会话 ID 的上下文键：

```properties
spring.ai.chat.client.tool-search-advisor.enabled=true
spring.ai.chat.client.tool-search-advisor.tool-index-type=vector
spring.ai.chat.client.tool-search-advisor.session-id-key-name=tenantId
```

<a id="see-also"></a>

## 相关阅读

- [扩展到数百个工具](https://docs.spring.io/spring-ai/reference/api/tools.html#scaling-to-hundreds-of-tools)：概念说明。
- [ToolCallingAdvisor](https://docs.spring.io/spring-ai/reference/api/tools/tool-calling-advisor.html)：基类与继承的构建器选项。
- [智能工具选择：节省 34–64% Token](https://spring.io/blog/2025/12/11/spring-ai-tool-search-tools-tzolov)：2025 年 12 月的测试结果与方法。
- [动态工具发现指南](https://docs.spring.io/spring-ai/reference/guides/dynamic-tool-search.html)：完整示例。
