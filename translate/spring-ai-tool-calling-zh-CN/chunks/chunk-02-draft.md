<a id="augmentation-components"></a>

### 核心组件

- `AugmentedToolCallbackProvider<T>`：包装工具对象或 Provider，使用指定的 record 类型扩充其中所有工具的参数。
- `AugmentedToolCallback<T>`：包装单个 `ToolCallback`。
- `AugmentedArgumentEvent<T>`：向 Consumer 提供 `toolDefinition()`、`rawInput()` 和 `arguments()`。
- `ToolInputSchemaAugmenter`：用于操作 Schema 的底层工具类。

`removeExtraArgumentsAfterProcessing` 默认为 `true`，控制是否把扩充参数传给原始工具。如果原始工具能够忽略额外字段，并且你希望保留这些字段，可以设为 `false`。

<a id="user-controlled-tool-execution"></a>

## 自行控制工具执行

自动注册的循环可以满足大多数需求；以下场景可能需要由应用控制每次迭代：

- 执行工具前等待外部审批。
- 向 SSE 或 WebSocket 接口发送中间进度。
- 在迭代之间执行条件判断。
- 根据旁路信号终止循环。

在单次请求中设置 `AdvisorParams.toolCallingAdvisorAutoRegister(false)`，关闭工具 Advisor 的自动注册。之后，应用需要检查 `ChatResponse` 中是否包含工具调用，并通过 `ToolCallingManager` 执行：

```java
ChatClient chatClient = ...
ToolCallingManager toolCallingManager = ToolCallingManager.builder().build();

ToolCallback[] tools = ToolCallbacks.from(new WeatherTools());
ChatOptions chatOptions = ToolCallingChatOptions.builder().toolCallbacks(tools).build();

String question = "What is the weather in Amsterdam and Paris?";

// 关闭 ToolCallingAdvisor，不再自动执行工具循环
ChatClientResponse response = chatClient.prompt()
    .user(question)
    .options(chatOptions)
    .advisors(AdvisorParams.toolCallingAdvisorAutoRegister(false))
    .call()
    .chatClientResponse();

Prompt prompt = new Prompt(List.of(new UserMessage(question)), chatOptions);

// 应用自行驱动循环，可以观察或中断每次迭代
while (response.chatResponse() != null && response.chatResponse().hasToolCalls()) {
    ToolExecutionResult result = toolCallingManager.executeToolCalls(prompt, response.chatResponse());
    prompt = new Prompt(result.conversationHistory(), chatOptions);
    response = chatClient.prompt()
        .messages(result.conversationHistory())
        .options(chatOptions)
        .advisors(AdvisorParams.toolCallingAdvisorAutoRegister(false))
        .call()
        .chatClientResponse();
}
```

流式 API 也可以采用同样方式：每次迭代产生的 `Flux` 分块流，一边转发给订阅方，一边交给 `ChatClientMessageAggregator` 聚合。完整示例见[自行控制流式工具执行](https://docs.spring.io/spring-ai/reference/api/tools/tool-calling-advisor.html#user-controlled-streaming)。

如果要对自动配置的 `ChatClient` 全局关闭自动注册，设置：

```properties
spring.ai.chat.client.tool-calling.enabled=false
```

:::note
自行驱动框架外部的循环，也需要自行处理循环级可观测性、Advisor 组合和单一 `ToolAdvisor` 约束。多数需求，包括向界面发送中间进度，都可以通过在循环内放置自定义 Advisor 完成，比完全接管循环更容易组合，见[扩展工具循环](https://docs.spring.io/spring-ai/reference/api/tools.html#extending-the-loop)。
:::

<a id="extending-the-loop"></a>

## 扩展循环：自定义 ToolAdvisor

`ToolCallingAdvisor` 在循环的关键位置提供钩子方法，`DefaultChatClient` 的自动配置也支持替换实现。`ToolSearchToolCallingAdvisor` 就使用这个扩展点实现渐进式工具暴露。

`ToolAdvisor` 是标记接口。自定义工具调用 Advisor 必须实现它，`DefaultChatClient` 才能识别该实现、检查单一 Advisor 约束，并用它替代默认实现。

<a id="hook-methods"></a>

### 钩子方法

基类提供四对受保护的生命周期钩子，分别对应同步调用与流式调用：

| 钩子 | 调用时机 |
| --- | --- |
| `doInitializeLoop` / `doInitializeLoopStream` | 第一次迭代前调用一次。 |
| `doBeforeCall` / `doBeforeStream` | 每次迭代前。 |
| `doAfterCall` / `doAfterStream` | 每次迭代后。 |
| `doFinalizeLoop` / `doFinalizeLoopStream` | 循环结束后调用一次。 |

`ToolSearchToolCallingAdvisor` 在 `doInitializeLoop` 中为工具建立索引并补充系统消息，在 `doBeforeCall` 中只注入已经发现的工具。其他自定义子类也可以沿用这个模式。

常见用途包括：

- **审批控制**：执行具有破坏性的工具前暂停，等待人工确认。
- **可观测性**：为每次工具调用向旁路通道发送结构化事件。
- **预算控制**：统计每个会话的 Token 或模型调用次数，超出预算时终止。
- **自定义工具解析**：从启动时尚不可用的动态来源解析工具。

<a id="custom-tool-advisor-autoconfig"></a>

### 接入自动配置

自定义 `ToolAdvisor` 可以接入自动配置，无需手动组装 `ChatClient`。扩展入口是 `ToolCallingAdvisor.Builder<?>` Bean。

`ChatClientAutoConfiguration` 使用 `@ConditionalOnMissingBean` 声明默认 Builder。要替换它，在一个早于 `ChatClientAutoConfiguration` 执行的自动配置中，注册返回类型为基类 `ToolCallingAdvisor.Builder<?>` 的 Bean：

```java
@AutoConfiguration(beforeName = "org.springframework.ai.model.chat.client.autoconfigure.ChatClientAutoConfiguration")
@ConditionalOnProperty(prefix = "my.advisor", name = "enabled", havingValue = "true")
public class MyToolAdvisorAutoConfiguration {

    @Bean
    @ConditionalOnMissingBean
    ToolCallingAdvisor.Builder<?> toolCallingAdvisorBuilder(ToolCallingManager toolCallingManager) {
        return MyCustomToolCallingAdvisor.builder()
            .toolCallingManager(toolCallingManager);
    }
}
```

随后，`ChatClient.Builder` 会使用自定义 Builder 自动注册你的 Advisor。`ToolSearchToolCallingAdvisor` 的自动配置使用的也是这一机制。

完整 Builder API 与钩子签名见 [ToolCallingAdvisor](https://docs.spring.io/spring-ai/reference/api/tools/tool-calling-advisor.html)。

<a id="tool-specification-reference"></a>

## 工具规格参考

前面的章节介绍了常见定义与使用方式；本节说明底层接口和定制入口。

<a id="tool-callback"></a>

### ToolCallback

`ToolCallback` 同时封装模型看到的工具定义，以及工具被调用时执行的逻辑：

```java
public interface ToolCallback {

    /** 模型据此判断何时以及如何调用工具。 */
    ToolDefinition getToolDefinition();

    /** 控制工具处理方式的元数据，例如直接返回结果。 */
    ToolMetadata getToolMetadata();

    /** 使用给定 JSON 输入执行工具并返回结果。 */
    String call(String toolInput);

    /** 使用给定输入和工具上下文执行工具。 */
    String call(String toolInput, ToolContext toolContext);
}
```

内置实现包括 `MethodToolCallback` 和 `FunctionToolCallback`。需要完全控制执行逻辑时，可以直接实现 `ToolCallback`，例如像 MCP 集成一样代理远程工具。

<a id="tool-definition"></a>

### ToolDefinition

`ToolDefinition` 是模型看到的工具契约，包含名称、描述和输入 Schema：

```java
public interface ToolDefinition {

    /** 在提供给模型的工具集合中唯一的名称。 */
    String name();

    /** 模型据此判断何时调用工具。 */
    String description();

    /** 工具输入参数的 JSON Schema。 */
    String inputSchema();
}
```

可以通过 `ToolDefinition.builder()` 构建：

```java
ToolDefinition toolDefinition = ToolDefinition.builder()
    .name("currentWeather")
    .description("Get the weather in location")
    .inputSchema("""
        {
            "type": "object",
            "properties": {
                "location": { "type": "string" },
                "unit": { "type": "string", "enum": ["C", "F"] }
            },
            "required": ["location", "unit"]
        }
    """)
    .build();
```

对于基于方法的工具，`ToolDefinitions.from(method)` 可以自动生成定义。如果方法上有 `@Tool`，注解中的名称与描述会覆盖基于方法名生成的默认值。

<a id="json-schema"></a>

### JSON Schema

输入 Schema 告诉模型如何传递工具参数。Spring AI 的 `JsonSchemaGenerator` 根据方法或函数的参数列表生成 Schema，并支持多种注解定制。

**参数描述**

可以使用以下注解，其中 Spring AI 注解的优先级最高：

- `@ToolParam(description = "…​")`：Spring AI。
- `@JsonClassDescription(description = "…​")`：Jackson。
- `@JsonPropertyDescription(description = "…​")`：Jackson。
- `@Schema(description = "…​")`：Swagger。

```java
class CustomerTools {

    @Tool(description = "Update customer information")
    void updateCustomerInfo(
            Long id,
            String name,
            @ToolParam(description = "Email address, RFC 5322 format", required = false) String email) {
        // ...
    }
}
```

**必填与可选参数**

默认所有参数都必填。可以通过以下注解声明可选，优先级从高到低排列：

- `@ToolParam(required = false)`：Spring AI。
- `@JsonProperty(required = false)`：Jackson。
- `@Schema(required = false)`：Swagger。
- `@Nullable`：Spring Framework / JSpecify。

:::note
正确设置必填状态有助于减少幻觉。必填字段要求模型提供值，可选字段则允许省略；如果一个字段被标为必填，而模型又无法获取它的值，就可能编造参数。
:::

<a id="tool-context"></a>

### 工具上下文

`ToolContext` 用于向工具方法传递租户 ID、用户 ID、请求范围等应用侧数据。这些数据不会发送给模型，只供工具内部使用。

其传递过程如下：

1. 聊天请求携带工具定义与工具上下文；Spring AI 只将工具定义发送给模型（1）。
2. 模型决定调用工具，将调用请求返回给 Spring AI（2），后者分派给匹配的工具（3）。
3. 调用工具时，工具上下文直接传给工具（3″），不经过模型。
4. 工具把结果返回给 Spring AI（4），Spring AI 再将结果交给模型（5），最终回答作为聊天响应返回（6）。

下图重点看（3″）的独立路径：工具上下文直接到达工具，不经过模型。

![工具上下文传递流程：模型只接收工具定义，ToolContext 经独立路径直接传给工具方法](https://docs.spring.io/spring-ai/reference/_images/tools/tool-context.jpg)

下面示例中，`.toolContext()` 设置的 `Map.of("tenantId", "acme")` 对应步骤（1）；`getCustomerInfo` 通过 `ToolContext` 参数在步骤（3″）读取它。租户 ID 到达工具时不会暴露给模型。

```java
class CustomerTools {

    @Tool(description = "Retrieve customer information")
    Customer getCustomerInfo(Long id, ToolContext toolContext) {
        return customerRepository.findById(id, toolContext.getContext().get("tenantId"));
    }
}

String response = ChatClient.create(chatModel)
        .prompt("Tell me more about the customer with ID 42")
        .tools(new CustomerTools())
        .toolContext(Map.of("tenantId", "acme"))
        .call()
        .content();
```

同时设置默认和请求级 `toolContext` 时，两者会合并，同名键以请求级值为准。

<a id="return-direct"></a>

### 直接返回结果

默认情况下，工具结果会再次发送给模型，供它继续对话。设置 `returnDirect = true` 后，工具结果直接返回调用方，跳过后续模型请求。适合工具输出本身已是最终答案的情况，例如 RAG 检索结果，可省去没有必要的额外延迟。

下图展示直接返回的路径：工具执行后，结果直接返回应用调用方。

![工具结果直接返回流程：returnDirect 为 true 时跳过工具结果到模型的后续请求](https://docs.spring.io/spring-ai/reference/_images/tools/return-direct.jpg)

声明式工具可以在注解中设置：

```java
@Tool(description = "Retrieve customer information", returnDirect = true)
Customer getCustomerInfo(Long id) { ... }
```

编程式工具通过 `ToolMetadata` 设置：

```java
ToolMetadata toolMetadata = ToolMetadata.builder()
    .returnDirect(true)
    .build();
```

:::note
如果模型在同一轮请求调用多个工具，只有这些工具全部设置了 `returnDirect = true`，才会直接返回；否则结果仍会发送给模型。
:::

<a id="result-conversion"></a>

### 结果转换

`ToolCallResultConverter` 将工具结果转换为模型接收的 `String`：

```java
@FunctionalInterface
public interface ToolCallResultConverter {
    String convert(Object result, Type returnType);
}
```

默认的 `DefaultToolCallResultConverter` 使用 Jackson 序列化结果。可以通过 `@Tool` 的 `resultConverter` 属性或 `ToolMetadata` 设置自定义转换器。

<a id="method-tool-limitations"></a>

### 方法工具的类型限制

使用 `MethodToolCallback` 时，以下类型不支持用作方法参数或返回值：

- `Optional`：改用 `@Nullable` 或 `@ToolParam(required = false)`。
- 异步类型：`CompletableFuture`、`Future`。
- 响应式类型：`Flow`、`Mono`、`Flux`。
- 函数类型：`Function`、`Supplier`、`Consumer`。

这些类型无法直接序列化为模型可用的数据，也没有模型能理解的对应 Schema 表示。

<a id="exception-handling"></a>

### 异常处理

工具执行抛出的异常会包装为 `ToolExecutionException`，交给 `ToolExecutionExceptionProcessor`：

```java
@FunctionalInterface
public interface ToolExecutionExceptionProcessor {
    String process(ToolExecutionException exception);
}
```

处理器可以返回错误消息，让框架将错误反馈给模型，由模型恢复对话或解释失败；也可以重新抛出异常，交给应用调用方处理。

默认的 `DefaultToolExecutionExceptionProcessor`：

- 将 `RuntimeException` 的消息返回给模型。
- 始终重新抛出受检异常和 `Error`。

可以通过属性配置：

| 属性 | 含义 | 默认值 |
| --- | --- | --- |
| `spring.ai.tools.throw-exception-on-error` | 为 `true` 时抛出所有工具错误，交给调用方处理；为 `false` 时按默认异常策略将可处理的错误作为消息返回模型。 | `false` |

也可以替换处理器 Bean：

```java
@Bean
ToolExecutionExceptionProcessor toolExecutionExceptionProcessor() {
    return new DefaultToolExecutionExceptionProcessor(true);
}
```

:::note
自行实现 `ToolCallback` 时，执行失败应从 `call()` 抛出 `ToolExecutionException`，异常处理器按这一类型处理工具失败。
:::

<a id="tool-call-limits"></a>

### 工具调用次数限制

`DefaultToolCallingManager` 限制单轮内的工具调用次数，避免工具循环失控：

```java
ToolCallingManager toolCallingManager = ToolCallingManager.builder()
    .maxCallsPerTool(40)                           // 单个工具的默认上限
    .maxCallsPerTool("search", 10)                  // 覆盖指定工具的上限
    .excludeToolFromLimit("getCurrentWeather")      // 该工具不受单工具上限限制
    .maxTotalToolCalls(150)                         // 所有工具合计的调用上限
    .onLimitExceeded(ToolCallLimitBehavior.THROW)   // 也可使用 RETURN_ERROR_RESPONSE
    .build();
```

即使不调用这些配置方法，`DefaultToolCallingManager.DEFAULT_MAX_CALLS_PER_TOOL` 和 `DEFAULT_MAX_TOTAL_TOOL_CALLS` 定义的默认上限也会生效。使用 `unlimitedCallsPerTool()` 或 `unlimitedTotalToolCalls()` 可分别关闭上限。

<a id="_counting"></a>

#### 如何计数

计数只针对当前轮次：从最后一条 `UserMessage` 开始，统计后续 `ToolResponseMessage` 中的调用。因此，循环外的 `ChatMemory` Advisor 回放旧消息，不会增加新一轮的计数。

Manager 本身不缓存计数；每次执行都从 `prompt.getInstructions()` 重新计算，因此同一个 `ToolCallingManager` 可以供多个并发请求共享。关闭 `ToolCallingAdvisor` 的内部对话历史也不会影响计数，见[循环内的记忆](https://docs.spring.io/spring-ai/reference/api/tools.html#inside-the-loop)：即使传给后续处理链的消息经过裁剪，次数限制仍使用当前轮次的完整历史。

<a id="_behavior_when_a_limit_is_exceeded"></a>

#### 达到上限后如何处理

默认情况下，`DefaultToolCallingManager` 抛出 `ToolCallLimitExceededException`，包含工具名、触发的上限，以及当前批次中已经执行的部分 `ToolExecutionResult`。如果触发总调用上限，工具名为 `null`。已经完成的工具结果不会丢失。

`ToolCallingAdvisor` 捕获异常后，通过 `ex.buildGeneration()` 生成一个表示超限的 `Generation`，作为最终响应返回，而不是为每个工具调用各返回一个结果。这样，调用方即使只读取首个结果，也不会被同批次中先前成功的调用遮住超限信息。

该结果的结束原因是 `ToolCallLimitExceededException.FINISH_REASON`；批次中已成功执行的工具结果保存在 `METADATA_PARTIAL_TOOL_RESPONSES` 元数据键下。

如果设置 `onLimitExceeded(ToolCallLimitBehavior.RETURN_ERROR_RESPONSE)`，Manager 会跳过超限调用，生成错误 `ToolResponse`，使用与 `ToolExecutionException` 相同的反馈机制告知模型，并继续对话。如果直接调用 `ToolCallingManager.executeToolCalls(...)`，也可以选择这种方式处理超限。

对应配置如下：

| 属性 | 含义 | 默认值 |
| --- | --- | --- |
| `spring.ai.tools.limits.max-calls-per-tool-default` | 每轮单个工具的默认调用上限，`-1` 表示关闭。 | `40` |
| `spring.ai.tools.limits.max-calls-per-tool.<name>` | 指定工具的上限覆盖值，`-1` 表示该工具不受单工具上限限制。 | — |
| `spring.ai.tools.limits.excluded-tools` | 不受单工具调用上限限制的工具名。 | — |
| `spring.ai.tools.limits.max-total-tool-calls` | 每轮所有工具合计的调用上限，`-1` 表示关闭。 | `150` |
| `spring.ai.tools.limits.on-limit-exceeded` | 超限处理方式：`THROW` 或 `RETURN_ERROR_RESPONSE`。 | `THROW` |

<a id="tool-resolution"></a>

## 工具解析

通常通过 `.tools(...)` 或 `.defaultTools(...)` 显式提供工具。需要在运行时按名称动态查找时，使用 `ToolCallbackResolver`：

```java
public interface ToolCallbackResolver {

    @Nullable
    ToolCallback resolve(String toolName);
}
```

默认自动配置的 `StaticToolCallbackResolver` 包含应用上下文中的所有 `ToolCallback` Bean，以及 `ToolCallbackProvider` Bean 提供的工具。MCP Provider 被排除，以免提前触发远程工具列举，见[使用 MCP Server 工具](https://docs.spring.io/spring-ai/reference/api/tools.html#consuming-mcp-server-tools)。

需要从数据库、类路径扫描或远程来源解析工具时，可以替换 Resolver Bean：

```java
@Bean
ToolCallbackResolver toolCallbackResolver(List<ToolCallback> toolCallbacks) {
    return new StaticToolCallbackResolver(toolCallbacks);
}
```

`ToolCallingManager` 在内部使用 Resolver，同时支持 [Advisor 控制的执行](https://docs.spring.io/spring-ai/reference/api/tools.html#the-tool-calling-loop)与[应用自行控制的执行](https://docs.spring.io/spring-ai/reference/api/tools.html#user-controlled-tool-execution)。

若希望模型请求的工具未附加到当前请求时，也能通过 Resolver 按名称查找并执行，需要启用解析回退：

```properties
spring.ai.tools.resolution.fallback.enabled=true
```

| 属性 | 含义 | 默认值 |
| --- | --- | --- |
| `spring.ai.tools.resolution.fallback.enabled` | 为 `true` 时，当前请求未附加的工具也可能通过 `ToolCallbackResolver` 按名称解析并执行；为 `false` 时，只允许执行请求中附加的工具。 | `false` |

手动构建 `ToolCallingManager` 时，对应设置是 `.resolutionFallbackEnabled(true)`，默认值也是 `false`。

:::caution
启用解析回退后，只要模型给出名称，Resolver 中可解析的工具就可能被执行，包括当前请求未附加的高风险或破坏性工具。仅在能够完整控制 Resolver 暴露范围时启用。
:::

<a id="observability"></a>

## 可观测性

Spring AI 使用 Micrometer，以 `spring.ai.tool` 为名称记录工具调用观测数据，包括：

- 工具名称与定义元数据。
- 执行耗时。
- 存在 `Tracer` 时的链路追踪上下文。

完整属性见[工具调用可观测性](https://docs.spring.io/spring-ai/reference/observability/index.html#_tool_calling)。

工具参数和结果也可以导出为 Span 属性，但可能包含敏感数据，因此默认关闭。启用方法见[工具参数与结果数据](https://docs.spring.io/spring-ai/reference/observability/index.html#_tool_call_arguments_and_result_data)。

<a id="logging"></a>

### 日志

主要操作使用 `DEBUG` 级别日志，可以通过以下配置启用：

```properties
logging.level.org.springframework.ai=DEBUG
```

<a id="chatmodel-tool-calling"></a>

## 直接使用 ChatModel 调用工具

如果需要直接控制 `ChatModel`，不使用 `ChatClient` 和 `ToolCallingAdvisor`，可以采用底层工具调用方式。它适用于需要完整控制请求与响应循环、也不需要 Advisor 组合能力的场景。

具体 API、默认工具与运行时工具的优先级，以及完整示例，见 [ChatModel 工具调用](https://docs.spring.io/spring-ai/reference/api/tools/chatmodel-tool-calling.html)。

:::note
Spring AI 1.x 中各个 `ChatModel` 自带的内部工具执行循环已经移除。向 `ChatModel` 传入工具，只会发送工具定义并返回模型响应，不会自动执行其中的工具调用。应用需要自行驱动循环，或使用会自动注册 `ToolCallingAdvisor` 的 `ChatClient`。
:::
