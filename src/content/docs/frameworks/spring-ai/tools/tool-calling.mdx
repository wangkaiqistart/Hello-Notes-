---
title: Spring AI：工具调用
description: 掌握 @Tool、工具注册与执行循环、记忆配合、MCP、参数与上下文、直接返回、异常处理及调用限制。
sidebar:
  label: 工具调用基础
  order: 1
---

工具调用小节分为四篇，先学会接入和排查，再按需要扩展：

| 页面                                                             | 学习重点         | 阅读建议             |
| ---------------------------------------------------------------- | ---------------- | -------------------- |
| 本篇：基础                                                       | 定义、注册与执行 | 先读，跑通调用。     |
| [Advisor](/frameworks/spring-ai/tools/tool-calling-advisor/)     | 循环、历史与事件 | 先读配置，扩展按需。 |
| [工具搜索](/frameworks/spring-ai/tools/tool-search-tool/)        | 按需发现工具     | 工具多时查阅。       |
| [ChatModel](/frameworks/spring-ai/tools/chatmodel-tool-calling/) | 底层手动循环     | 自行编排时查阅。     |

首次阅读本篇，按“[快速入门](#quick-start) → [定义工具](#defining-tools) → [提供工具](#passing-tools) → [执行循环](#the-tool-calling-loop)”建立主线，再看 [JSON Schema](#json-schema)、[工具上下文](#tool-context)、[直接返回](#return-direct)、[异常处理](#exception-handling)和[次数限制](#tool-call-limits)。参数增强、手动循环和自定义 Advisor 留作扩展参考。

阅读层次：[核心用法](#core-usage) → [常用集成与排查](#common-integrations) → [进阶与 API 参考](#advanced-reference)。

本文以 Spring AI **2.0.2** 为准：工具循环由 `ChatClient` 的 `ToolCallingAdvisor` 管理，与 1.x 的 `ChatModel` 内部循环不同。

下文代码是分别展示用法的片段，省略部分 import、依赖注入和业务实现；`...` 为待补充代码，不应整体拼接为可直接运行的类。

**工具调用（Tool Calling）** 让模型请求执行应用定义的函数，并利用执行结果继续处理任务。例如，模型先请求查询订单状态，应用查询后返回结果，模型再组织回答。

工具主要有两类用途：

- **检索信息**：从数据库、Web 服务、文件系统或搜索引擎获取数据，补充模型不知道的信息，例如当前天气、客户资料和最新新闻。
- **执行操作**：在业务系统中执行动作，例如发送邮件、预订航班、更新记录或触发工作流。

虽然称为模型的“工具调用能力”，**工具执行逻辑始终属于应用**。模型只提出调用请求并提供参数；应用负责执行工具、返回结果。模型不会直接获得工具背后 API 的访问权限。

下图展示智能体如何在模型判断与工具执行之间循环，直到得到最终答案。

[![智能体循环：模型根据任务请求工具，应用执行后将结果返回模型，循环直到得到答案](/images/frameworks/spring-ai/tools/spring-ai-agent-loop.png)](/images/frameworks/spring-ai/tools/spring-ai-agent-loop.png)

<a id="core-usage"></a>

## 一、核心用法（重点掌握）

先完成定义、注册和自动执行，再掌握参数、上下文、返回结果与失败处理。

<a id="_architecture_overview"></a>

### 架构概览

Spring AI 2.0 将工具执行循环纳入 `ChatClient` 的 Advisor 链，使其成为可以组合和扩展的组件：

1. [定义工具](/frameworks/spring-ai/tools/tool-calling/#defining-tools)，传给 `ChatClient`。
2. `ChatClient` 自动注册 `ToolCallingAdvisor`，由它驱动[工具调用循环](/frameworks/spring-ai/tools/tool-calling/#the-tool-calling-loop)。
3. 模型选择需要调用的工具，`ToolCallingManager` 执行；循环持续到模型返回不含工具调用的响应。
4. 记忆、可观测性、重试及自定义 Advisor 通过 **Advisor 顺序**与循环配合，详见[记忆与工具循环](/frameworks/spring-ai/tools/tool-calling/#memory-and-the-tool-loop)。

这套架构取代了 Spring AI 1.x 中各个 `ChatModel` 内部的工具执行循环。底层场景仍可直接使用 `ChatModel`，详见 [ChatModel 工具调用](/frameworks/spring-ai/tools/chatmodel-tool-calling/)。

具体型号是否支持工具调用，见[聊天模型能力对比](https://docs.spring.io/spring-ai/reference/api/chat/comparison.html)。

<a id="quick-start"></a>

### 快速入门

在方法上添加 `@Tool`，即可定义工具：

```java
import org.springframework.ai.tool.annotation.Tool;
import org.springframework.context.i18n.LocaleContextHolder;
import java.time.LocalDateTime;
import java.time.ZonedDateTime;
import java.time.format.DateTimeFormatter;

class DateTimeTools {

    @Tool(description = "Get the current date and time in the user's timezone")
    String getCurrentDateTime() {
        return ZonedDateTime.now(LocaleContextHolder.getTimeZone().toZoneId()).toString();
    }

    @Tool(description = "Set a user alarm for the given time, provided in ISO-8601 format")
    void setAlarm(String time) {
        LocalDateTime alarmTime = LocalDateTime.parse(time, DateTimeFormatter.ISO_DATE_TIME);
        System.out.println("Alarm set for " + alarmTime);
    }
}
```

通过 `.tools()` 将工具传给 `ChatClient`，提出一个需要使用工具的问题：

```java
ChatModel chatModel = ...

String response = ChatClient.create(chatModel)
        .prompt("Can you set an alarm 10 minutes from now?")
        .tools(new DateTimeTools())
        .call()
        .content();
```

模型可以先请求 `getCurrentDateTime()`，再根据计算出的时间请求 `setAlarm(...)`，具体选择由模型决定。Spring AI 自动处理请求、执行和结果回传。这里的 `setAlarm` 只解析时间并打印日志，未接入真实闹钟服务。

在 Spring Boot 应用中，优先注入自动配置的 `ChatClient.Builder` 构建客户端，以沿用配置好的工具 Manager 和 Advisor 构建器；这里的 `ChatClient.create(chatModel)` 只展示最简注册方式。

验证时分别观察：模型是否提出了调用请求、工具方法收到什么参数、工具执行结果是否被用于最终回答。只看到一段合理的回答，不能确认工具确实执行过；对缺少时间等必要参数的输入，也应检查模型是否先追问。

<a id="defining-tools"></a>

### 定义工具

Spring AI 提供三种定义方式，从声明式用法到底层控制依次为：

| 方式                   | 适用场景                                                       | 章节                                                                         |
| ---------------------- | -------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| 声明式 `@Tool`         | 可以修改方法源码，希望尽量少写配置。                           | [声明式工具](/frameworks/spring-ai/tools/tool-calling/#declarative-tool)     |
| `MethodToolCallback`   | 需要以编程方式控制基于方法的工具。                             | [方法回调](/frameworks/spring-ai/tools/tool-calling/#method-tool-callback)   |
| `FunctionToolCallback` | 暴露 `Function`、`Supplier`、`Consumer` 等 Lambda 或方法引用。 | [函数回调](/frameworks/spring-ai/tools/tool-calling/#function-tool-callback) |

三种方式最终都生成 `ToolCallback`，进入同一个执行循环，可以混用。

<a id="declarative-tool"></a>

#### 声明式：@Tool

`@Tool` 可用于 public、包级可见或 private 方法，也支持静态方法和实例方法：

```java
class WeatherTools {

    @Tool(description = "Get the current weather for a given city")
    public String getWeather(String city) {
        return weatherService.fetch(city);
    }
}
```

注解支持以下属性：

- `name`：工具名称，默认使用方法名；在提供给模型的工具集合内必须唯一。
- `description`：工具做什么、何时使用。建议明确填写，否则模型缺少选择工具的依据。
- `returnDirect`：将结果直接返回调用方，不再交回模型，见[直接返回](/frameworks/spring-ai/tools/tool-calling/#return-direct)。
- `resultConverter`：使用的 `ToolCallResultConverter`，见[结果转换](/frameworks/spring-ai/tools/tool-calling/#result-conversion)。

AOT 编译（GraalVM 原生镜像）要求包含 `@Tool` 方法的类是 Spring Bean，例如标注 `@Component`；否则需要添加 `@RegisterReflection(memberCategories = MemberCategory.INVOKE_DECLARED_METHODS)`。

通过 `@ToolParam` 描述每个参数：

```java
class WeatherTools {

    @Tool(description = "Get the weather for a city at a specific time")
    public String getWeather(
            @ToolParam(description = "City name") String city,
            @ToolParam(description = "Time in ISO-8601 format", required = false) String at) {
        return weatherService.fetch(city, at);
    }
}
```

参数默认必填。`@ToolParam(required = false)` 或 `@Nullable` 可将参数设为可选，完整规则见 [JSON Schema](/frameworks/spring-ai/tools/tool-calling/#json-schema)。

<a id="passing-tools"></a>

### 向 ChatClient 提供工具

`ChatClient` 有两个工具配置入口：

```java
// 请求级：仅本次请求可用
chatClient.prompt(...)
    .tools(new WeatherTools(), currentWeather)
    .call();

// 默认级：使用该客户端构建的每次请求都可用
ChatClient client = ChatClient.builder(chatModel)
    .defaultTools(new WeatherTools(), currentWeather)
    .build();
```

这两个方法都支持混合参数：带 `@Tool` 方法的 POJO、`ToolCallback`、`ToolCallbackProvider`，以及这些类型的数组或集合，可以在一次调用中混用。

请求级 `.tools(...)` 会**追加**到客户端的默认工具，最终列表由 `.defaultTools(...)` 和请求级工具合并得到。

默认工具会在同一 `ChatClient.Builder` 构建的请求间共享，适合始终可用的能力。高风险或破坏性工具通常应按请求添加，避免默认暴露给所有请求。

底层 `ChatModel` 通过 `ToolCallingChatOptions.toolCallbacks(...)` 配置的默认工具则会被请求级工具列表覆盖，规则见 [ChatModel 工具调用](/frameworks/spring-ai/tools/chatmodel-tool-calling/)。

<a id="the-tool-calling-loop"></a>

### 工具调用循环

调用 `ChatClient` 的 `.call()` 或 `.stream()` 后，请求进入 Advisor 链。`DefaultChatClient` 自动注册的 `ToolCallingAdvisor` 管理整个工具执行过程：

1. 将请求和已注册的工具定义发送给模型。
2. 模型决定是否调用工具，并返回响应。
3. 若响应包含工具调用，Advisor 将其交给 `ToolCallingManager`，由它找到对应的 `ToolCallback` 并执行，将工具结果加入对话历史，再次请求模型。
4. 重复第 2、3 步，直到模型返回不含工具调用的响应，再将该响应交给调用方。

下图展示 Advisor 如何在模型请求和工具执行之间循环。阻塞 `.call()` 和流式 `.stream()` 都支持这一机制。

[![工具调用流程：ToolCallingAdvisor 请求模型、执行工具并回传结果，直到获得最终响应](/images/frameworks/spring-ai/tools/spring-ai-tool-calling-advisor-flow.png)](/images/frameworks/spring-ai/tools/spring-ai-tool-calling-advisor-flow.png)

`ToolCallingAdvisor` 是**递归 Advisor**，每次迭代都会重新进入下游 Advisor 链。同一机制也用于结构化输出的校验重试等循环模式，详见[递归 Advisors](/frameworks/spring-ai/core/advisors/)。

`DefaultChatClient` 限制处理链中至多有一个 `ToolAdvisor`；重复注册会明确报错。默认会自动注册，显式关闭自动注册后也可以没有工具 Advisor。构建器、钩子方法和完整配置见 [ToolCallingAdvisor](/frameworks/spring-ai/tools/tool-calling-advisor/)。

<a id="json-schema"></a>

### JSON Schema

输入 Schema 告诉模型如何传递工具参数。Spring AI 的 `JsonSchemaGenerator` 根据方法或函数的参数列表生成 Schema，并支持多种注解定制。

**参数描述**

可以使用以下注解，其中 Spring AI 注解的优先级最高：

- `@ToolParam(description = "…​")`：Spring AI。
- `@JsonPropertyDescription("...")`：Jackson。
- `@Schema(description = "…​")`：Swagger。

上面按方法参数描述的优先级排列。参数对象的类型还可以用 `@JsonClassDescription("...")` 提供类级描述；它不能直接标在方法参数上。

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
- `@Schema(requiredMode = Schema.RequiredMode.NOT_REQUIRED)`：Swagger。
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

[![工具上下文传递流程：模型只接收工具定义，ToolContext 经独立路径直接传给工具方法](/images/frameworks/spring-ai/tools/tool-context.jpg)](/images/frameworks/spring-ai/tools/tool-context.jpg)

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

默认情况下，工具结果会再次发送给模型，供它继续对话。设置 `returnDirect = true` 后，工具结果直接返回调用方，跳过后续模型请求。适合工具已经生成完整答案、调用方希望直接接收结果的情况。普通 RAG 检索通常只返回参考片段，仍需模型组织回答，不宜仅因它是检索工具就设置直接返回。

下图展示直接返回的路径：工具执行后，结果直接返回应用调用方。

[![工具结果直接返回流程：returnDirect 为 true 时跳过工具结果到模型的后续请求](/images/frameworks/spring-ai/tools/return-direct.jpg)](/images/frameworks/spring-ai/tools/return-direct.jpg)

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

- 通常把运行时工具异常转换成错误消息返回模型；配置在重抛名单中的异常会直接抛出，例如自动配置识别到的 OAuth2 客户端授权异常。
- 原始原因是受检异常或 `Error` 时，继续抛出包装它的 `ToolExecutionException`。

可以通过属性配置：

| 属性                                       | 含义                                                                                                      | 默认值  |
| ------------------------------------------ | --------------------------------------------------------------------------------------------------------- | ------- |
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

Manager 本身不缓存计数；每次执行都从 `prompt.getInstructions()` 重新计算，因此同一个 `ToolCallingManager` 可以供多个并发请求共享。关闭 `ToolCallingAdvisor` 的内部对话历史也不会影响计数，见[循环内的记忆](/frameworks/spring-ai/tools/tool-calling/#inside-the-loop)：即使传给后续处理链的消息经过裁剪，次数限制仍使用当前轮次的完整历史。

<a id="_behavior_when_a_limit_is_exceeded"></a>

#### 达到上限后如何处理

默认情况下，`DefaultToolCallingManager` 抛出 `ToolCallLimitExceededException`，包含工具名、触发的上限，以及当前批次中已经执行的部分 `ToolExecutionResult`。如果触发总调用上限，工具名为 `null`。已经完成的工具结果不会丢失。

`ToolCallingAdvisor` 捕获异常后，通过 `ex.buildGeneration()` 生成一个表示超限的 `Generation`，作为最终响应返回，而不是为每个工具调用各返回一个结果。这样，调用方即使只读取首个结果，也不会被同批次中先前成功的调用遮住超限信息。

该结果的结束原因是 `ToolCallLimitExceededException.FINISH_REASON`；批次中已成功执行的工具结果保存在 `METADATA_PARTIAL_TOOL_RESPONSES` 元数据键下。

如果设置 `onLimitExceeded(ToolCallLimitBehavior.RETURN_ERROR_RESPONSE)`，Manager 会跳过超限调用，生成错误 `ToolResponse`，使用与 `ToolExecutionException` 相同的反馈机制告知模型，并继续对话。如果直接调用 `ToolCallingManager.executeToolCalls(...)`，也可以选择这种方式处理超限。

对应配置如下：

| 属性                                                | 含义                                                      | 默认值  |
| --------------------------------------------------- | --------------------------------------------------------- | ------- |
| `spring.ai.tools.limits.max-calls-per-tool-default` | 每轮单个工具的默认调用上限，`-1` 表示关闭。               | `40`    |
| `spring.ai.tools.limits.max-calls-per-tool.<name>`  | 指定工具的上限覆盖值，`-1` 表示该工具不受单工具上限限制。 | —       |
| `spring.ai.tools.limits.excluded-tools`             | 不受单工具调用上限限制的工具名。                          | —       |
| `spring.ai.tools.limits.max-total-tool-calls`       | 每轮所有工具合计的调用上限，`-1` 表示关闭。               | `150`   |
| `spring.ai.tools.limits.on-limit-exceeded`          | 超限处理方式：`THROW` 或 `RETURN_ERROR_RESPONSE`。        | `THROW` |

<a id="common-integrations"></a>

## 二、常用集成与排查（按场景阅读）

接入 Spring Bean、对话记忆或 MCP 时阅读对应章节；排查工具执行问题时查看可观测性与日志。

<a id="tool-callback-beans"></a>

### ToolCallback Bean

Spring AI 自动发现应用上下文中的 `ToolCallback` Bean，并通过 `ToolCallbackResolver` 支持按名称查找。工具可以定义为 `@Bean`，在需要的位置注入：

```java
@Configuration(proxyBeanMethods = false)
class WeatherToolsConfig {

    @Bean
    ToolCallback currentWeather(WeatherService weatherService) {
        return FunctionToolCallback.builder("currentWeather", weatherService::getWeather)
            .description("Get the weather in location")
            .inputType(WeatherRequest.class)
            .build();
    }
}
```

注入并传给 `ChatClient`：

```java
@Autowired ToolCallback currentWeather;

ChatClient.create(chatModel)
    .prompt("What's the weather in Copenhagen?")
    .tools(currentWeather)
    .call()
    .content();
```

Spring AI 2.0 已移除通过 `SpringBeanToolCallbackResolver`、`toolNames(...)` 按名称解析普通 `Function` Bean 的旧用法；工具现在需要显式注册为 `ToolCallback` Bean。迁移方法见[从 1.x 升级到 2.0](https://docs.spring.io/spring-ai/reference/upgrade-notes.html#tool-calling-1x-to-2x)。

<a id="memory-and-the-tool-loop"></a>

### 记忆与工具循环

`MessageChatMemoryAdvisor` 相对 `ToolCallingAdvisor` 的位置，决定记忆存储能记录多少工具调用上下文。`ToolCallingAdvisor` 的默认顺序为 `HIGHEST_PRECEDENCE + 300`。

<a id="outside-the-loop"></a>

#### 循环外：默认行为

`MessageChatMemoryAdvisor` 的默认顺序为 `HIGHEST_PRECEDENCE + 200`，小于工具 Advisor，因此位于循环外：

- 循环开始前，只加载一次历史。
- 循环结束后，只保存用户消息与最终助手回复。
- 不会看到中间的工具调用请求和工具响应消息。

这与所有 `ChatMemoryRepository` 实现兼容，也延续了 Spring AI 1.x 的行为：旧版工具循环位于 `ChatModel` 内部，记忆 Advisor 无法观察工具消息。

```java
var chatClient = ChatClient.builder(chatModel)
    .defaultAdvisors(MessageChatMemoryAdvisor.builder(chatMemory).build())  // 默认位于循环外
    .build();
```

<a id="inside-the-loop"></a>

#### 循环内：保留工具消息

若希望后续轮次能够利用完整工具记录，了解之前尝试过什么、调用过哪些工具及其结果，就把记忆 Advisor 放到循环内：其 `order` 应大于 `ToolCallingAdvisor.DEFAULT_ORDER`。

```java
var chatMemoryAdvisor = MessageChatMemoryAdvisor.builder(chatMemory)
    .order(BaseAdvisor.HIGHEST_PRECEDENCE + 400)  // 位于 ToolCallingAdvisor 之后，进入循环
    .build();

var chatClient = ChatClient.builder(chatModel)
    .defaultAdvisors(chatMemoryAdvisor)
    .build();
```

为避免重复写入，记忆 Advisor 位于循环内时，必须关闭 `ToolCallingAdvisor` 自己维护的历史。**自动注册时会自动处理**：`DefaultChatClient` 检测到循环内的 `MemoryAdvisor` 后，会关闭内部历史，无需额外配置。若手动构建 `ToolCallingAdvisor`，则需要自行调用构建器的 `.disableInternalConversationHistory()`。

关闭内部历史只改变每轮向下游链传递哪些消息。[工具调用次数限制](/frameworks/spring-ai/tools/tool-calling/#tool-call-limits)仍基于当前完整轮次计算，不受这一开关影响。

下图展示记忆 Advisor 放在工具循环内部时的位置与消息流向。

[![循环内记忆：每次工具迭代都会经过 ChatMemoryAdvisor，保存并恢复工具消息](/images/frameworks/spring-ai/tools/spring-ai-tool-calling-with-inside-memory.png)](/images/frameworks/spring-ai/tools/spring-ai-tool-calling-with-inside-memory.png)

<a id="backend-compatibility"></a>

#### 存储兼容性

并非所有 `ChatMemoryRepository` 都能持久化工具消息。除了普通用户消息和助手回复，存储还必须能够序列化 `ToolResponseMessage` 及带工具调用的助手消息。

2.0 中支持完整消息类型、可以放在循环内使用的内置实现有：

- [InMemoryChatMemoryRepository](https://docs.spring.io/spring-ai/reference/api/chat-memory.html#_in_memory_repository)
- [RedisChatMemoryRepository](https://docs.spring.io/spring-ai/reference/api/chat-memory.html#_redischatmemoryrepository)
- [Neo4jChatMemoryRepository](https://docs.spring.io/spring-ai/reference/api/chat-memory.html#_neo4j_chatmemoryrepository)

需要 JDBC 持久化完整工具消息时，可查看社区项目 [spring-ai-session](https://spring-ai-community.github.io/spring-ai-session/latest/)。它还提供事件溯源历史、按轮次压缩和多智能体分支隔离；来源文档称其计划纳入 Spring AI 2.1。

<a id="mcp-tools"></a>

### MCP 工具

[Model Context Protocol](https://modelcontextprotocol.io/)（MCP）标准化了 AI 应用访问远程服务器工具、资源与提示词的方式。Spring AI 同时支持消费 MCP 服务器的工具，以及向 MCP 客户端暴露应用自己的工具。

<a id="consuming-mcp-server-tools"></a>

#### 使用 MCP 服务器工具

引入 MCP 客户端 Starter，配置一个或多个服务器连接：

```xml
<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>spring-ai-starter-mcp-client</artifactId>
</dependency>
```

```properties
spring.ai.mcp.client.stdio.connections.my-server.command=npx
spring.ai.mcp.client.stdio.connections.my-server.args=-y,@modelcontextprotocol/server-everything
```

自动配置会连接已配置的服务器、发现工具，并提供 `SyncMcpToolCallbackProvider` Bean；异步客户端则提供 `AsyncMcpToolCallbackProvider`。

MCP Provider **不会自动注册到 ChatClient**。虽然它实现了 `ToolCallbackProvider`，但启动时立即列出工具会触发到每个 MCP 服务器的网络请求，因此需要注入并显式接入：

```java
@Autowired SyncMcpToolCallbackProvider mcpTools;

// 配置为默认工具，供每次请求使用
ChatClient chatClient = ChatClient.builder(chatModel)
    .defaultTools(mcpTools)
    .build();

// 或者仅添加到本次请求
chatClient.prompt()
    .user("Search the web for the latest Spring AI release notes")
    .tools(mcpTools)
    .call()
    .content();
```

工具回调自动配置默认开启，可通过 `spring.ai.mcp.client.toolcallback.enabled=false` 关闭。传输、安全、过滤及名称前缀配置见 [MCP 客户端](/frameworks/spring-ai/mcp/client/)。

<a id="exposing-mcp-server-tools"></a>

#### 将 Spring 工具暴露为 MCP 服务器

对外暴露 Spring Bean 时，使用 `@McpTool`，并引入 MCP 服务端 Starter：

```xml
<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>spring-ai-starter-mcp-server-webmvc</artifactId>
</dependency>
```

```java
@Component
public class WeatherTools {

    @McpTool(description = "Get the current weather for a given city")
    public String getWeather(
            @McpToolParam(description = "City name") String city) {
        return weatherService.fetch(city);
    }
}
```

自动配置扫描带 `@McpTool` 的 Bean，为参数生成 JSON Schema，并将工具注册到 MCP 服务器。`@Tool` 用于本地工具声明，`@McpTool` 用于 MCP 服务端注解扫描；已有 `@Tool` 也可通过回调 Provider 暴露。传输与注册方式见 [MCP 服务端](/frameworks/spring-ai/mcp/server/)。

<a id="combining-local-and-mcp-tools"></a>

#### 混用本地工具与 MCP 工具

本地 `@Tool` 方法和远程 MCP 工具都通过 `ToolCallback` 表达，模型与 `ToolCallingAdvisor` 不需要区分其来源。可以在同一次 `.tools(...)` 或 `.defaultTools(...)` 中混用：

```java
chatClient.prompt()
    .tools(new LocalTools(), mcpTools)
    .call()
    .content();
```

混用时需要注意：

- **MCP 的名称冲突处理只覆盖 MCP 工具。** `DefaultMcpToolNamePrefixGenerator` 可以为不同 MCP 服务器的重名工具生成前缀，但不了解本地 `@Tool` 方法。本地与远程工具重名时，应重命名其中一个，或用 `McpToolFilter` 过滤远程工具。
- **明确暴露范围。** MCP 工具来自外部系统，可通过 `McpToolFilter` Bean，按服务器身份、工具名称或描述筛选，避免暴露不需要的工具。

`ChatClient` 会在 `.tools(...)`、`.defaultTools(...)` 合并后的完整列表上检查重名；任意两个回调同名都会抛出 `IllegalStateException`，请求会失败，不会误选工具。

直接调用 `ChatModel.call()` / `.stream()`，或自行构建循环和 `ToolCallingChatOptions` 时，不会自动执行这项合并列表校验。工具按名称匹配，列表中第一个同名回调会被执行，不会报错或记录冲突日志。因此，远程 MCP 工具可能顶替同名本地工具。此时应通过[工具名称前缀](https://docs.spring.io/spring-ai/reference/api/mcp/mcp-client-boot-starter-docs.html#mcp-tool-name-prefix-generation)隔离来源，或在使用前自行调用 `ToolCallingChatOptions.validateToolCallbacks(...)` 校验合并列表。

<a id="observability"></a>

### 可观测性

Spring AI 使用 Micrometer，以 `spring.ai.tool` 为名称记录工具调用观测数据，包括：

- 工具名称与定义元数据。
- 执行耗时。
- 存在 `Tracer` 时的链路追踪上下文。

完整属性见[工具调用可观测性](https://docs.spring.io/spring-ai/reference/observability/index.html#_tool_calling)。

工具参数和结果也可以导出为 Span 属性，但可能包含敏感数据，因此默认关闭。启用方法见[工具参数与结果数据](https://docs.spring.io/spring-ai/reference/observability/index.html#_tool_call_arguments_and_result_data)。

<a id="logging"></a>

#### 日志

主要操作使用 `DEBUG` 级别日志，可以通过以下配置启用：

```properties
logging.level.org.springframework.ai=DEBUG
```

<a id="advanced-reference"></a>

## 三、进阶与 API 参考（按需查阅）

需要包装现有方法、定制结果、接入大量工具或自行管理循环时，在这里查阅完整接口、配置和示例。

<a id="tool-specification-reference"></a>

### 工具规格参考

前面的章节介绍了常见定义与使用方式；本节说明底层接口和定制入口。

<a id="tool-callback"></a>

#### ToolCallback

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

#### ToolDefinition

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

<a id="method-tool-callback"></a>

### 编程式：MethodToolCallback

不能修改源类，或需要在运行时构建工具定义时，可用 `MethodToolCallback` 动态注册：

```java
Method method = ReflectionUtils.findMethod(WeatherTools.class, "getWeather", String.class);

MethodToolCallback callback = MethodToolCallback.builder()
    .toolDefinition(ToolDefinitions.builder(method)
        .description("Get the current weather for a given city")
        .build())
    .toolMethod(method)
    .toolObject(new WeatherTools())
    .build();
```

实例方法必须提供 `toolObject`，静态方法则可省略。更多接口见[工具规范参考](/frameworks/spring-ai/tools/tool-calling/#tool-specification-reference)。

<a id="function-tool-callback"></a>

### 编程式：FunctionToolCallback

`FunctionToolCallback` 用于封装 `Function`、`Supplier`、`Consumer` 或 `BiFunction`，包括 Lambda 与方法引用：

```java
FunctionToolCallback callback = FunctionToolCallback.builder("currentWeather", weatherService::getWeather)
    .description("Get the weather in location")
    .inputType(WeatherRequest.class)
    .build();
```

工厂方法接收工具名称和函数引用，构建器配置描述与输入类型；输入类型用于生成 JSON Schema。

<a id="method-tool-limitations"></a>

### 方法工具的类型限制

使用 `MethodToolCallback` 时，以下类型不支持用作方法参数或返回值：

- `Optional`：改用 `@Nullable` 或 `@ToolParam(required = false)`。
- 异步类型：`CompletableFuture`、`Future`。
- 响应式类型：`Flow`、`Mono`、`Flux`。
- 函数类型：`Function`、`Supplier`、`Consumer`。

这些类型无法直接序列化为模型可用的数据，也没有模型能理解的对应 Schema 表示。

<a id="result-conversion"></a>

### 结果转换

`ToolCallResultConverter` 将工具结果转换为模型接收的 `String`：

```java
@FunctionalInterface
public interface ToolCallResultConverter {
    String convert(Object result, Type returnType);
}
```

默认的 `DefaultToolCallResultConverter` 使用 Jackson 序列化结果。声明式工具通过 `@Tool` 的 `resultConverter` 属性指定转换器；编程式工具通过 `MethodToolCallback` 或 `FunctionToolCallback` 构建器的 `.toolCallResultConverter(...)` 指定。

<a id="scaling-to-hundreds-of-tools"></a>

### 扩展到大量工具

默认 `ToolCallingAdvisor` 会在每次请求中发送全部已注册的工具定义。少量工具时通常没有问题；达到 30 个以上，或多个 MCP 服务器汇总数百个工具时，可能造成上下文膨胀、选择准确率下降和额外 Token 消耗。

`ToolSearchToolCallingAdvisor` 可以替换默认实现，采用**渐进式工具暴露**：按会话为完整工具集建立索引，没有搜索历史时只提供内置的 `toolSearchTool`。模型通过自然语言查询检索相关工具，后续请求再加入已发现的工具定义。

引入[工具搜索 Starter](/frameworks/spring-ai/tools/tool-search-tool/#installation) 后，通过属性启用：

```properties
spring.ai.chat.client.tool-search-advisor.enabled=true
```

完整配置、索引策略、会话 ID 语义和调优方式见[工具搜索](/frameworks/spring-ai/tools/tool-search-tool/)。

<a id="tool-argument-augmentation"></a>

### 工具参数增强

Spring AI 支持动态扩展工具的输入 Schema，添加说明、置信度或元数据等参数，而无需修改原始工具实现。模型看到扩展后的 Schema 并填写额外字段；应用通过消费者读取这些字段，原始工具只接收自己需要的参数。

常见用途包括：

- **调用理由**：在执行前获取模型生成的分步说明。
- **记忆增强**：提取可存入长期记忆的信息。
- **分析与跟踪**：记录元数据、用户意图或使用模式。
- **多智能体协调**：传递智能体标识或协调信号。

调用理由是模型生成的解释文本，不保证反映其真实内部推理过程。

下图展示增强参数如何在到达原始工具前被提取，并交给独立消费者。

[![工具参数增强：模型填写扩展字段，消费者读取额外参数，原始工具接收其原有输入](/images/frameworks/spring-ai/tools/spring-ai-tool-arg-augmenter.png)](/images/frameworks/spring-ai/tools/spring-ai-tool-arg-augmenter.png)

<a id="augmentation-quick-start"></a>

#### 快速使用

先用 Java record 定义增强字段：

```java
public record AgentThinking(
    @ToolParam(description = "Your reasoning for calling this tool", required = true)
    String innerThought,

    @ToolParam(description = "Confidence level (low, medium, high)", required = false)
    String confidence
) {}
```

通过 `AugmentedToolCallbackProvider` 包装工具：

```java
AugmentedToolCallbackProvider<AgentThinking> provider = AugmentedToolCallbackProvider
    .<AgentThinking>builder()
    .toolObject(new WeatherTools())     // 包装原始工具
    .argumentType(AgentThinking.class)  // 增强参数的 Schema 类型
    .argumentConsumer(event -> {        // 可选：消费增强字段
        AgentThinking thinking = event.arguments();
        log.info("Tool: {} | Reasoning: {}", event.toolDefinition().name(), thinking.innerThought());
    })
    .removeExtraArgumentsAfterProcessing(true)
    .build();

ChatClient chatClient = ChatClient.builder(chatModel)
    .defaultTools(provider)
    .build();
```

模型看到包含额外字段的 Schema；消费者获得 `AgentThinking` record，原始工具仍只接收预期参数。

<a id="augmentation-components"></a>

#### 核心组件

- `AugmentedToolCallbackProvider<T>`：包装工具对象或 Provider，使用指定的 record 类型扩充其中所有工具的参数。
- `AugmentedToolCallback<T>`：包装单个 `ToolCallback`。
- `AugmentedArgumentEvent<T>`：向 Consumer 提供 `toolDefinition()`、`rawInput()` 和 `arguments()`。
- `ToolInputSchemaAugmenter`：用于操作 Schema 的底层工具类。

`removeExtraArgumentsAfterProcessing` 默认为 `true`，控制是否把扩充参数传给原始工具。如果原始工具能够忽略额外字段，并且你希望保留这些字段，可以设为 `false`。

<a id="user-controlled-tool-execution"></a>

### 自行控制工具执行

自动注册的循环可以满足大多数需求；以下场景可能需要由应用控制每次迭代：

- 执行工具前等待外部审批。
- 向 SSE 或 WebSocket 接口发送中间进度。
- 在迭代之间执行条件判断。
- 根据旁路信号终止循环。

在单次请求中设置 `AdvisorParams.toolCallingAdvisorAutoRegister(false)`，关闭工具 Advisor 的自动注册。这个开关只阻止框架添加实例，**不会移除显式注册的 `ToolAdvisor`**，包括手动注册的 `ToolSearchToolCallingAdvisor`。下面的 `chatClient` 应未显式注册工具 Advisor；关闭自动注册后，应用检查 `ChatResponse` 并通过 `ToolCallingManager` 执行：

```java
ChatClient chatClient = ...
ToolCallingManager toolCallingManager = ToolCallingManager.builder().build();

ToolCallback[] tools = ToolCallbacks.from(new WeatherTools());
ChatOptions chatOptions = ToolCallingChatOptions.builder().toolCallbacks(tools).build();

String question = "What is the weather in Amsterdam and Paris?";

// 未显式注册 ToolAdvisor 时，关闭自动注册后由应用接管循环
ChatClientResponse response = chatClient.prompt()
    .user(question)
    .options(chatOptions.mutate())
    .advisors(AdvisorParams.toolCallingAdvisorAutoRegister(false))
    .call()
    .chatClientResponse();

Prompt prompt = new Prompt(List.of(new UserMessage(question)), chatOptions);

// 应用自行驱动循环，可以观察或中断每次迭代
while (response.chatResponse() != null && response.chatResponse().hasToolCalls()) {
    ToolExecutionResult result = toolCallingManager.executeToolCalls(prompt, response.chatResponse());
    if (result.returnDirect()) {
        response = response.mutate()
            .chatResponse(ChatResponse.builder()
                .generations(ToolExecutionResult.buildGenerations(result))
                .build())
            .build();
        break;
    }
    prompt = new Prompt(result.conversationHistory(), chatOptions);
    response = chatClient.prompt()
        .messages(result.conversationHistory())
        .options(chatOptions.mutate())
        .advisors(AdvisorParams.toolCallingAdvisorAutoRegister(false))
        .call()
        .chatClientResponse();
}
```

此处通过构建器创建独立的 `ToolCallingManager`，不会自动继承 Spring Boot Bean 的次数限制、异常处理器和观测配置。在 Boot 应用中接管循环时，优先注入已配置的 Manager；还需自行处理[调用超限](#tool-call-limits)等结束条件。

流式 API 也可以采用同样方式：每次迭代产生的 `Flux` 分块流，一边转发给订阅方，一边交给 `ChatClientMessageAggregator` 聚合。完整示例见[自行控制流式工具执行](/frameworks/spring-ai/tools/tool-calling-advisor/#user-controlled-streaming)。

如果要对自动配置的 `ChatClient` 全局关闭自动注册，设置：

```properties
spring.ai.chat.client.tool-calling.enabled=false
```

:::note
自行驱动框架外部的循环，也需要自行处理循环级可观测性、Advisor 组合和单一 `ToolAdvisor` 约束。多数需求，包括向界面发送中间进度，都可以通过在循环内放置自定义 Advisor 完成，比完全接管循环更容易组合，见[扩展工具循环](/frameworks/spring-ai/tools/tool-calling/#extending-the-loop)。
:::

<a id="extending-the-loop"></a>

### 扩展循环：自定义 ToolAdvisor

`ToolCallingAdvisor` 在循环的关键位置提供钩子方法，`DefaultChatClient` 的自动配置也支持替换实现。`ToolSearchToolCallingAdvisor` 就使用这个扩展点实现渐进式工具暴露。

`ToolAdvisor` 是标记接口。自定义工具调用 Advisor 必须实现它，`DefaultChatClient` 才能识别该实现、检查单一 Advisor 约束，并用它替代默认实现。

<a id="hook-methods"></a>

#### 钩子方法

基类提供四对受保护的生命周期钩子，分别对应同步调用与流式调用：

| 钩子                                          | 调用时机               |
| --------------------------------------------- | ---------------------- |
| `doInitializeLoop` / `doInitializeLoopStream` | 第一次迭代前调用一次。 |
| `doBeforeCall` / `doBeforeStream`             | 每次迭代前。           |
| `doAfterCall` / `doAfterStream`               | 每次迭代后。           |
| `doFinalizeLoop` / `doFinalizeLoopStream`     | 循环结束后调用一次。   |

`ToolSearchToolCallingAdvisor` 在 `doInitializeLoop` 中为工具建立索引并补充系统消息，在 `doBeforeCall` 中只注入已经发现的工具。其他自定义子类也可以沿用这个模式。

常见用途包括：

- **审批控制**：执行具有破坏性的工具前暂停，等待人工确认。
- **可观测性**：为每次工具调用向旁路通道发送结构化事件。
- **预算控制**：统计每个会话的 Token 或模型调用次数，超出预算时终止。
- **自定义工具解析**：从启动时尚不可用的动态来源解析工具。

<a id="custom-tool-advisor-autoconfig"></a>

#### 接入自动配置

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

完整 Builder API 与钩子签名见 [ToolCallingAdvisor](/frameworks/spring-ai/tools/tool-calling-advisor/)。

<a id="tool-resolution"></a>

### 工具解析

通常通过 `.tools(...)` 或 `.defaultTools(...)` 显式提供工具。需要在运行时按名称动态查找时，使用 `ToolCallbackResolver`：

```java
public interface ToolCallbackResolver {

    @Nullable
    ToolCallback resolve(String toolName);
}
```

默认自动配置的 `StaticToolCallbackResolver` 包含应用上下文中的所有 `ToolCallback` Bean，以及 `ToolCallbackProvider` Bean 提供的工具。MCP Provider 被排除，以免提前触发远程工具列举，见[使用 MCP Server 工具](/frameworks/spring-ai/tools/tool-calling/#consuming-mcp-server-tools)。

需要从数据库、类路径扫描或远程来源解析工具时，可以替换 Resolver Bean：

```java
@Bean
ToolCallbackResolver toolCallbackResolver(List<ToolCallback> toolCallbacks) {
    return new StaticToolCallbackResolver(toolCallbacks);
}
```

`ToolCallingManager` 在内部使用 Resolver，同时支持 [Advisor 控制的执行](/frameworks/spring-ai/tools/tool-calling/#the-tool-calling-loop)与[应用自行控制的执行](/frameworks/spring-ai/tools/tool-calling/#user-controlled-tool-execution)。

若希望模型请求的工具未附加到当前请求时，也能通过 Resolver 按名称查找并执行，需要启用解析回退：

```properties
spring.ai.tools.resolution.fallback.enabled=true
```

| 属性                                          | 含义                                                                                                                              | 默认值  |
| --------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- | ------- |
| `spring.ai.tools.resolution.fallback.enabled` | 为 `true` 时，当前请求未附加的工具也可能通过 `ToolCallbackResolver` 按名称解析并执行；为 `false` 时，只允许执行请求中附加的工具。 | `false` |

手动构建 `ToolCallingManager` 时，对应设置是 `.resolutionFallbackEnabled(true)`，默认值也是 `false`。

:::caution
启用解析回退后，只要模型给出名称，Resolver 中可解析的工具就可能被执行，包括当前请求未附加的高风险或破坏性工具。仅在能够完整控制 Resolver 暴露范围时启用。
:::

<a id="chatmodel-tool-calling"></a>

### 直接使用 ChatModel 调用工具

如果需要直接控制 `ChatModel`，不使用 `ChatClient` 和 `ToolCallingAdvisor`，可以采用底层工具调用方式。它适用于需要完整控制请求与响应循环、也不需要 Advisor 组合能力的场景。

具体 API、默认工具与运行时工具的优先级，以及完整示例，见 [ChatModel 工具调用](/frameworks/spring-ai/tools/chatmodel-tool-calling/)。

:::note
Spring AI 1.x 中各个 `ChatModel` 自带的内部工具执行循环已经移除。向 `ChatModel` 传入工具，只会发送工具定义并返回模型响应，不会自动执行其中的工具调用。应用需要自行驱动循环，或使用会自动注册 `ToolCallingAdvisor` 的 `ChatClient`。
:::

来源：[工具调用](https://docs.spring.io/spring-ai/reference/api/tools.html)。文档版本：2.0.2；核验日期：2026-11-01。
