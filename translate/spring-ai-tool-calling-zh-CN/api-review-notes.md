# 工具调用 2.0.2 API 复核

日期：2026-10-26。本次仅静态读取源码，不运行 Java，不执行工具。Spring AI 源码来自主审已下载的 2.0.2 sources.jar；路径均相对于本目录的 `api/`。补充解包了 `JsonSchemaGenerator.java`、`AbstractSpringAiSchemaModule.java`、`SpringAiSchemaModule.java` 与 `ToolCallLimits.java`。另从 Maven Central `com.fasterxml.jackson.core:jackson-annotations:2.22:sources` 保存两个 Jackson 注解定义，用来验证不变的注解契约；该补充版本不代表已确认 Spring AI BOM 恰好管理 2.22。

## 需要修正的来源表述

### 1. Jackson 描述注解使用 value，不是 description

- `JsonSchemaGenerator.java:27-28` 明确导入 `com.fasterxml.jackson.annotation.JsonProperty`、`com.fasterxml.jackson.annotation.JsonPropertyDescription`。即使树模型使用 `tools.jackson.databind`（41-42 行），Jackson 注解仍位于 `com.fasterxml.jackson.annotation`。
- `JsonSchemaGenerator.java:270-286`：方法参数描述依次读取非空的 `ToolParam.description()`、`JsonPropertyDescription.value()`、`Schema.description()`。
- `JsonPropertyDescription.java:17` 允许 FIELD / METHOD / PARAMETER 等目标；28 行定义 `String value() default ""`，没有 `description` 元素。
- `JsonClassDescription.java:17` 仅允许 ANNOTATION_TYPE / TYPE；26 行也是 `value()`，不能直接用在方法参数上。

建议正文将参数描述列表改为：

- `@ToolParam(description = "...")`。
- `@JsonPropertyDescription("...")`，等价于 `value = "..."`。
- `@Schema(description = "...")`。

`@JsonClassDescription("...")` 单独说明为参数对象类型的类级描述，不能与直接描述方法参数的注解混为一谈。来源的 `@JsonClassDescription(description = ...)` 和 `@JsonPropertyDescription(description = ...)` 都不能作为有效 Java 写法。

### 2. 仅 @Schema(required = false) 不能在当前实现中声明可选

- `JsonSchemaGenerator.java:232-256` 给出方法参数必填判定优先级：`ToolParam` → `JsonProperty` → `Schema` → Spring `Nullness` → 默认 `true`。
- 245-248 行的 Schema 判定是 `requiredMode == REQUIRED || requiredMode == AUTO || required()`。
- `AbstractSpringAiSchemaModule.java:97-133` 对对象字段采用相同策略。

建议把来源可选参数列表的 `@Schema(required = false)` 改为 `@Schema(requiredMode = Schema.RequiredMode.NOT_REQUIRED)`。否则 `requiredMode` 默认 AUTO 时仍被视为必填，`required=false` 单独不起作用。优先推荐 `@ToolParam(required = false)`，可直接与注解描述组合。

### 3. 结果转换器不通过 ToolMetadata 配置

- `ToolMetadata.java:30-56` 只提供 `returnDirect()`、静态 `builder()` 和 `from(Method)`，没有结果转换器配置。
- `MethodToolCallback.java:250-252`：真实构建方法为 `.toolCallResultConverter(ToolCallResultConverter)`。
- `FunctionToolCallback.java:223-225`：同样支持 `.toolCallResultConverter(...)`。
- `DefaultToolCallResultConverter.java:46-69`：一般结果通过 JsonHelper 序列化；void 有 Done 约定；RenderedImage 还有 PNG / Base64 特殊分支。

建议改成：声明式工具使用 `@Tool(resultConverter = ...)`；编程式工具在 `MethodToolCallback` 或 `FunctionToolCallback` 构建器中配置 `.toolCallResultConverter(...)`。无需增加代码块，仅纠正正文入口。

### 4. 异常处理中的“原样抛出”和“所有 RuntimeException”需限定

- `DefaultToolExecutionExceptionProcessor.java:60-84`：若原始 cause 属于 RuntimeException，先检查显式的 rethrow allowlist；命中则抛出原始运行时异常。否则若 `alwaysThrow=true`，抛出包装后的 `ToolExecutionException`；默认返回包装异常的消息，缺失时生成包含工具名和异常类名的消息。
- 原始 cause 是受检异常或 Error 时，66-69 行抛出的是包装后的 `ToolExecutionException`，并非原始受检异常 / Error 本身。
- `ToolCallingAutoConfiguration.java:117-132` 在 Spring Security OAuth2 的 `ClientAuthorizationException` 存在时，将它加入 rethrow allowlist，因此自动配置下不宜说“任何 RuntimeException 都会返回给模型”。

建议正文：默认将普通运行时工具错误转成反馈消息；受检异常 / Error 对应的包装异常继续抛出；配置了重抛名单的运行时异常按名单抛出。`throw-exception-on-error=false` 不意味着一切异常都转成模型消息。

## 调用次数与 returnDirect：来源关键值正确

- `DefaultToolCallingManager.java:100`：每工具默认 40 次；107 行：每轮合计 150 次；372-380 行 Builder 使用相同默认值，默认超限策略 THROW。
- `ToolCallLimits.java:81-104`：只扫描最后一个 UserMessage 起的 ToolResponseMessage，每个 ToolResponse 按名称累计；没有 UserMessage 时扫描全部消息。
- `DefaultToolCallingManager.java:234-246` 每次执行从输入历史重建计数，并在本批次逐个增加，不持有会话计数缓存。
- `ToolCallLimits.java:113-127`：排除指定工具仅免除该工具的单工具上限，仍计入总上限。
- `ToolCallingAutoConfiguration.java:149-175`：properties 的 `-1` 被转换为 Builder 的 unlimited / exclude 方法；不能把 -1 直接传给要求大于零的 `maxCallsPerTool(int)` 或 `maxTotalToolCalls(int)`。
- `DefaultToolCallingManager.java:299-304` 对本批次所有工具的 `returnDirect` 做 AND，来源“全部 true 才直接返回”正确。

## 工具搜索配置：默认值与细节

### 已确认的默认值

`ToolSearchAdvisorProperties.java`：

| 属性后缀 | 默认值 | 行号 |
| --- | --- | --- |
| `enabled` | `false` | 46 |
| `tool-index-type` | `regex` | 62 |
| `max-results` | `null` | 68 |
| `session-id-key-name` | `ChatMemory.CONVERSATION_ID` | 75 |
| `reference-tool-name-accumulation` | `true` | 82 |
| `system-message-suffix` | `null`，使用内置资源 | 89 |
| `advisor-order` | `ToolCallingAdvisor.DEFAULT_ORDER` | 96 |
| `eviction.lru-max-sessions` | `1000` | 176 |
| `eviction.ttl` | `null` | 183 |
| `lucene.min-score-threshold` | `0.25f` | 214 |

`ToolCallingAdvisor.java:75` 确认 order 为 `Ordered.HIGHEST_PRECEDENCE + 300`。`ToolSearchAdvisorAutoConfiguration.java:152-157` 确认 TTL 设置后使用 LRU + TTL 组合；218-230 行确认 regex 是 matchIfMissing=true 的默认索引；显式自定义 ToolIndex Bean 使自动配置退让。

### maxResults 配置是回退值，不是不可突破的硬上限

- `ToolSearchTool.java:48-62`：模型传入 `maxResults` 时优先使用模型值；模型未提供时才回退到 Advisor 的 maxResults。
- 模型与 Advisor 都没有指定时，ToolSearchRequest.maxResults 为 null，由索引实现取默认值。
- `RegexToolIndex.java:60,132`、`LuceneToolIndex.java:81,163`、`VectorToolIndex.java:65,138` 的索引默认返回数量都是 10。
- `ToolSearchTool.java:50` 中模型可见的描述提示“1–10，默认 5”，这只是模型提示，不等于 Java 强制设置为 5，也不是显式范围校验。

建议 Builder / 属性表写“模型未传值时使用的搜索结果数量；未设置时由索引默认值处理”，不要把 `.maxResults(5)` 描述为服务端硬限制或一概称默认 5。

### referenceToolNameAccumulation 的源码比属性注释更准确

- `ToolSearchToolCallingAdvisor.java:291-320` 以每条包含搜索结果的 ToolResponseMessage 为一个搜索轮次分组。
- true 累积当前可见历史中的所有分组；false 只选最近一组，但保留该组中的全部并行搜索结果。
- 因而来源正文关于“保留最近轮次内所有并行调用”正确；属性类 78-80 行“only last response”的旧注释较粗略，不应据此把并行结果丢掉。

### Regex 实现范围比“仅按工具名匹配”更广

- `RegexToolIndex.java:45-51` 说明工具名称与描述都参与匹配，名称权重为描述两倍；自然语言查询也会被转换成组合正则。
- 95-98 行同时索引 `toolName()` 和 `summary()`。

建议保留“轻量模式/正则匹配”作为定位，但不要断言只搜索工具名；这会把当前实现能力缩窄。

## 未在本轮改动

没有修改分块初稿、站点页面、导航或其他译稿。上述修正由主审统一处理并记入来源差异记录。
