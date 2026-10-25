# 工具调用

**工具调用（Tool Calling）**让 AI 模型请求执行应用定义的函数，并利用执行结果继续处理任务，是构建智能体的基础能力。模型若只能生成文字，主要承担聊天功能；具备信息发现、执行操作和循环处理能力后，才能逐步完成目标。

工具主要有两类用途：

- **检索信息**：从数据库、Web 服务、文件系统或搜索引擎获取数据，补充模型不知道的信息，例如当前天气、客户资料和最新新闻。
- **执行操作**：在业务系统中执行动作，例如发送邮件、预订航班、更新记录或触发工作流。

虽然称为模型的“工具调用能力”，**工具执行逻辑始终属于应用**。模型只提出调用请求并提供参数；应用负责执行工具、返回结果。模型不会直接获得工具背后 API 的访问权限。

下图展示智能体如何在模型判断与工具执行之间循环，直到得到最终答案。

![智能体循环：模型根据任务请求工具，应用执行后将结果返回模型，循环直到得到答案](https://docs.spring.io/spring-ai/reference/_images/tools/spring-ai-agent-loop.png)

<a id="_architecture_overview"></a>

## 架构概览

Spring AI 2.0 将工具执行循环纳入 `ChatClient` 的 Advisor 链，使其成为可以组合和扩展的组件：

1. [定义工具](https://docs.spring.io/spring-ai/reference/api/tools.html#defining-tools)，传给 `ChatClient`。
2. `ChatClient` 自动注册 `ToolCallingAdvisor`，由它驱动[工具调用循环](https://docs.spring.io/spring-ai/reference/api/tools.html#the-tool-calling-loop)。
3. 模型选择需要调用的工具，`ToolCallingManager` 执行；循环持续到模型返回不含工具调用的响应。
4. 记忆、可观测性、重试及自定义 Advisor 通过 **Advisor 顺序**与循环配合，详见[记忆与工具循环](https://docs.spring.io/spring-ai/reference/api/tools.html#memory-and-the-tool-loop)。

这套架构取代了 Spring AI 1.x 中各个 `ChatModel` 内部的工具执行循环。底层场景仍可直接使用 `ChatModel`，详见 [ChatModel 工具调用](https://docs.spring.io/spring-ai/reference/api/tools/chatmodel-tool-calling.html)。

具体型号是否支持工具调用，见[聊天模型能力对比](https://docs.spring.io/spring-ai/reference/api/chat/comparison.html)。

<a id="quick-start"></a>

## 快速入门

在方法上添加 `@Tool`，即可定义工具：

```java
import org.springframework.ai.tool.annotation.Tool;
import org.springframework.context.i18n.LocaleContextHolder;

class DateTimeTools {

    @Tool(description = "Get the current date and time in the user's timezone")
    String getCurrentDateTime() {
        return LocalDateTime.now().atZone(LocaleContextHolder.getTimeZone().toZoneId()).toString();
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

模型会先请求 `getCurrentDateTime()`，再根据计算出的时间请求 `setAlarm(...)`。Spring AI 自动处理请求、执行和结果回传。

<a id="defining-tools"></a>

## 定义工具

Spring AI 提供三种定义方式，从声明式用法到底层控制依次为：

| 方式 | 适用场景 | 章节 |
| --- | --- | --- |
| 声明式 `@Tool` | 可以修改方法源码，希望尽量少写配置。 | [声明式工具](https://docs.spring.io/spring-ai/reference/api/tools.html#declarative-tool) |
| `MethodToolCallback` | 需要以编程方式控制基于方法的工具。 | [方法回调](https://docs.spring.io/spring-ai/reference/api/tools.html#method-tool-callback) |
| `FunctionToolCallback` | 暴露 `Function`、`Supplier`、`Consumer` 等 Lambda 或方法引用。 | [函数回调](https://docs.spring.io/spring-ai/reference/api/tools.html#function-tool-callback) |

三种方式最终都生成 `ToolCallback`，进入同一个执行循环，可以混用。

<a id="declarative-tool"></a>

### 声明式：@Tool

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
- `returnDirect`：将结果直接返回调用方，不再交回模型，见[直接返回](https://docs.spring.io/spring-ai/reference/api/tools.html#return-direct)。
- `resultConverter`：使用的 `ToolCallResultConverter`，见[结果转换](https://docs.spring.io/spring-ai/reference/api/tools.html#result-conversion)。

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

参数默认必填。`@ToolParam(required = false)` 或 `@Nullable` 可将参数设为可选，完整规则见 [JSON Schema](https://docs.spring.io/spring-ai/reference/api/tools.html#json-schema)。

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

实例方法必须提供 `toolObject`，静态方法则可省略。更多接口见[工具规范参考](https://docs.spring.io/spring-ai/reference/api/tools.html#tool-specification-reference)。

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

<a id="passing-tools"></a>

## 向 ChatClient 提供工具

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

底层 `ChatModel` 通过 `ToolCallingChatOptions.toolCallbacks(...)` 配置的默认工具则会被请求级工具列表覆盖，规则见 [ChatModel 工具调用](https://docs.spring.io/spring-ai/reference/api/tools/chatmodel-tool-calling.html)。

<a id="the-tool-calling-loop"></a>

## 工具调用循环

调用 `ChatClient` 的 `.call()` 或 `.stream()` 后，请求进入 Advisor 链。`DefaultChatClient` 自动注册的 `ToolCallingAdvisor` 管理整个工具执行过程：

1. 将请求和已注册的工具定义发送给模型。
2. 模型决定是否调用工具，并返回响应。
3. 若响应包含工具调用，Advisor 将其交给 `ToolCallingManager`，由它找到对应的 `ToolCallback` 并执行，将工具结果加入对话历史，再次请求模型。
4. 重复第 2、3 步，直到模型返回不含工具调用的响应，再将该响应交给调用方。

下图展示 Advisor 如何在模型请求和工具执行之间循环。阻塞 `.call()` 和流式 `.stream()` 都支持这一机制。

![工具调用流程：ToolCallingAdvisor 请求模型、执行工具并回传结果，直到获得最终响应](https://docs.spring.io/spring-ai/reference/_images/tools/spring-ai-tool-calling-advisor-flow.png)

`ToolCallingAdvisor` 是**递归 Advisor**，每次迭代都会重新进入下游 Advisor 链。同一机制也用于结构化输出的校验重试等循环模式，详见[递归 Advisors](https://docs.spring.io/spring-ai/reference/api/advisors-recursive.html)。

`DefaultChatClient` 保证处理链中只有一个 `ToolAdvisor`；重复注册会明确报错。构建器、钩子方法和完整配置见 [ToolCallingAdvisor](https://docs.spring.io/spring-ai/reference/api/tools/tool-calling-advisor.html)。

<a id="memory-and-the-tool-loop"></a>

## 记忆与工具循环

`MessageChatMemoryAdvisor` 相对 `ToolCallingAdvisor` 的位置，决定记忆存储能记录多少工具调用上下文。`ToolCallingAdvisor` 的默认顺序为 `HIGHEST_PRECEDENCE + 300`。

<a id="outside-the-loop"></a>

### 循环外：默认行为

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

### 循环内：保留工具消息

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

关闭内部历史只改变每轮向下游链传递哪些消息。[工具调用次数限制](https://docs.spring.io/spring-ai/reference/api/tools.html#tool-call-limits)仍基于当前完整轮次计算，不受这一开关影响。

下图展示记忆 Advisor 放在工具循环内部时的位置与消息流向。

![循环内记忆：每次工具迭代都会经过 ChatMemoryAdvisor，保存并恢复工具消息](https://docs.spring.io/spring-ai/reference/_images/tools/spring-ai-tool-calling-with-inside-memory.png)

<a id="backend-compatibility"></a>

### 存储兼容性

并非所有 `ChatMemoryRepository` 都能持久化工具消息。除了普通用户消息和助手回复，存储还必须能够序列化 `ToolResponseMessage` 及带工具调用的助手消息。

2.0 中支持完整消息类型、可以放在循环内使用的内置实现有：

- [InMemoryChatMemoryRepository](https://docs.spring.io/spring-ai/reference/api/chat-memory.html#_in_memory_repository)
- [RedisChatMemoryRepository](https://docs.spring.io/spring-ai/reference/api/chat-memory.html#_redischatmemoryrepository)
- [Neo4jChatMemoryRepository](https://docs.spring.io/spring-ai/reference/api/chat-memory.html#_neo4j_chatmemoryrepository)

需要 JDBC 持久化完整工具消息时，可查看社区项目 [spring-ai-session](https://spring-ai-community.github.io/spring-ai-session/latest/)。它还提供事件溯源历史、按轮次压缩和多智能体分支隔离；来源文档称其计划纳入 Spring AI 2.1。

<a id="scaling-to-hundreds-of-tools"></a>

## 扩展到大量工具

默认 `ToolCallingAdvisor` 会在每次请求中发送全部已注册的工具定义。少量工具时通常没有问题；达到 30 个以上，或多个 MCP 服务器汇总数百个工具时，可能造成上下文膨胀、选择准确率下降和额外 Token 消耗。

`ToolSearchToolCallingAdvisor` 可以替换默认实现，采用**渐进式工具暴露**：按会话为完整工具集建立索引，初始只提供内置的 `toolSearchTool`。模型通过自然语言查询检索相关工具，后续请求再加入已发现的工具定义。

通过属性启用：

```properties
spring.ai.chat.client.tool-search-advisor.enabled=true
```

完整配置、索引策略、会话 ID 语义和调优方式见[工具搜索](https://docs.spring.io/spring-ai/reference/api/tools/tool-search-tool.html)。

<a id="mcp-tools"></a>

## MCP 工具

[Model Context Protocol](https://modelcontextprotocol.io/)（MCP）标准化了 AI 应用访问远程服务器工具、资源与提示词的方式。Spring AI 同时支持消费 MCP 服务器的工具，以及向 MCP 客户端暴露应用自己的工具。

<a id="consuming-mcp-server-tools"></a>

### 使用 MCP 服务器工具

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

工具回调自动配置默认开启，可通过 `spring.ai.mcp.client.toolcallback.enabled=false` 关闭。传输、安全、过滤及名称前缀配置见 [MCP Client Boot Starter](https://docs.spring.io/spring-ai/reference/api/mcp/mcp-client-boot-starter-docs.html)。

<a id="exposing-mcp-server-tools"></a>

### 将 Spring 工具暴露为 MCP 服务器

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

自动配置扫描带 `@McpTool` 的 Bean，为参数生成 JSON Schema，并将工具注册到 MCP 服务器。传输、安全与可观测性配置见 [MCP Server Boot Starter](https://docs.spring.io/spring-ai/reference/api/mcp/mcp-server-boot-starter-docs.html)。

<a id="combining-local-and-mcp-tools"></a>

### 混用本地工具与 MCP 工具

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

<a id="tool-argument-augmentation"></a>

## 工具参数增强

Spring AI 支持动态扩展工具的输入 Schema，添加说明、置信度或元数据等参数，而无需修改原始工具实现。模型看到扩展后的 Schema 并填写额外字段；应用通过消费者读取这些字段，原始工具只接收自己需要的参数。

常见用途包括：

- **调用理由**：在执行前获取模型生成的分步说明。
- **记忆增强**：提取可存入长期记忆的信息。
- **分析与跟踪**：记录元数据、用户意图或使用模式。
- **多智能体协调**：传递智能体标识或协调信号。

下图展示增强参数如何在到达原始工具前被提取，并交给独立消费者。

![工具参数增强：模型填写扩展字段，消费者读取额外参数，原始工具接收其原有输入](https://docs.spring.io/spring-ai/reference/_images/tools/spring-ai-tool-arg-augmenter.png)

<a id="augmentation-quick-start"></a>

### 快速使用

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
