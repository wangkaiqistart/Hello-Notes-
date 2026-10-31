#### 客户端定制示例

同步客户端可以实现 `McpClientCustomizer<McpClient.SyncSpec>`，异步客户端可以实现 `McpClientCustomizer<McpClient.AsyncSpec>`，按应用需要选择。

同步客户端示例：

```java
@Component
public class CustomMcpSyncClientCustomizer implements McpClientCustomizer<McpClient.SyncSpec> {
    @Override
    public void customize(String serverConfigurationName, McpClient.SyncSpec spec) {

        // 定制请求超时
        spec.requestTimeout(Duration.ofSeconds(30));

        // 设置客户端公开的根 URI
        spec.roots(roots);

        // 处理创建消息的采样请求
        spec.sampling((CreateMessageRequest messageRequest) -> {
            // 处理采样
            CreateMessageResult result = ...
            return result;
        });

        // 处理信息征询请求
        spec.elicitation((ElicitRequest request) -> {
          // 处理信息征询
          return new ElicitResult(ElicitResult.Action.ACCEPT, Map.of("message", request.message()));
        });

        // 接收进度通知
        spec.progressConsumer((ProgressNotification progress) -> {
         // 处理进度通知
        });

        // 工具新增、移除等变化时接收通知
        spec.toolsChangeConsumer((List<McpSchema.Tool> tools) -> {
            // 处理工具变化
        });

        // 可用资源变化时接收通知
        spec.resourcesChangeConsumer((List<McpSchema.Resource> resources) -> {
            // 处理资源变化
        });

        // 可用提示词变化时接收通知
        spec.promptsChangeConsumer((List<McpSchema.Prompt> prompts) -> {
            // 处理提示词变化
        });

        // 接收服务端日志通知
        spec.loggingConsumer((McpSchema.LoggingMessageNotification log) -> {
            // 处理日志消息
        });
    }
}
```

异步客户端示例：

```java
@Component
public class CustomMcpAsyncClientCustomizer implements McpClientCustomizer<McpClient.AsyncSpec> {
    @Override
    public void customize(String serverConfigurationName, McpClient.AsyncSpec spec) {
        // 定制异步客户端
        spec.requestTimeout(Duration.ofSeconds(30));
    }
}
```

`serverConfigurationName` 是当前定制器所作用的服务端连接配置名称，MCP 客户端也基于该配置创建。

客户端自动配置会发现应用上下文中的定制器，并自动应用。

<a id="_transport_support"></a>

### 传输支持

自动配置支持以下传输：

- **标准输入输出（STDIO）**：`spring-ai-starter-mcp-client` 和 `spring-ai-starter-mcp-client-webflux` 均支持。
- **JDK HttpClient 实现的 HTTP/SSE 与 Streamable-HTTP**：由 `spring-ai-starter-mcp-client` 提供。
- **WebFlux 实现的 HTTP/SSE 与 Streamable-HTTP**：由 `spring-ai-starter-mcp-client-webflux` 提供。

<a id="_tool_filtering"></a>

### 工具过滤

`McpToolFilter` 用于过滤发现的工具。可以根据 MCP 连接信息或工具属性，决定是否包含某个工具。

定义一个实现 `McpToolFilter` 的 Bean：

```java
@Component
public class CustomMcpToolFilter implements McpToolFilter {

    @Override
    public boolean test(McpConnectionInfo connectionInfo, McpSchema.Tool tool) {
        // 根据连接信息和工具属性过滤
        // true 表示包含，false 表示排除

        // 排除来自指定客户端的工具
        if (connectionInfo.clientInfo().name().equals("restricted-client")) {
            return false;
        }

        // 包含指定名称前缀的工具
        if (tool.name().startsWith("allowed_")) {
            return true;
        }

        // 排除描述中包含 experimental 的工具
        if (tool.description() != null &&
            tool.description().contains("experimental")) {
            return false;
        }

        return true; // 默认包含其他工具
    }
}
```

`McpConnectionInfo` record 提供：

- `clientCapabilities`：客户端能力。
- `clientInfo`：客户端名称和版本。
- `initializeResult`：服务端返回的初始化结果。

自动配置会发现该过滤器，并应用到同步和异步 MCP 工具回调提供方。没有自定义过滤器时，默认包含所有发现的工具。

应用上下文中只应定义一个 `McpToolFilter` Bean。需要多条过滤规则时，将它们组合到一个过滤器中。

<a id="mcp-tool-name-prefix-generation"></a>

### 工具名称前缀

`McpToolNamePrefixGenerator` 用于定制工具名称前缀，避免多个 MCP 服务端提供同名工具时发生冲突。

没有自定义 Bean 时，使用 `DefaultMcpToolNamePrefixGenerator`。默认实现会：

- 跟踪已有连接和工具名称，避免重名。
- 将名称中的非字母数字字符替换为下划线，例如 `my-tool` 变成 `my_tool`。
- 不同连接出现同名工具时，添加计数前缀，例如 `alt_1_toolName`、`alt_2_toolName`。
- 保证线程安全和幂等：相同的客户端、服务端、工具组合始终得到同一个名称。
- 将最终名称限制在 64 个字符以内，必要时从开头截断。

例如：

- 第一次出现 `search` → `search`。
- 另一条连接再次出现 `search` → `alt_1_search`。
- `my-special-tool` → `my_special_tool`。

可以提供自定义实现：

```java
@Component
public class CustomToolNamePrefixGenerator implements McpToolNamePrefixGenerator {

    @Override
    public String prefixedToolName(McpConnectionInfo connectionInfo, Tool tool) {
        // 定制工具名称前缀

        // 使用服务端名称和版本作为前缀
        String serverName = connectionInfo.initializeResult().serverInfo().name();
        String serverVersion = connectionInfo.initializeResult().serverInfo().version();
        return serverName + "_v" + serverVersion.replace(".", "_") + "_" + tool.name();
    }
}
```

`McpConnectionInfo` 中可访问：

- `clientCapabilities`：客户端能力。
- `clientInfo`：客户端名称、标题和版本。
- `initializeResult`：服务端初始化结果，包含服务端信息。

<a id="_built_in_prefix_generators"></a>

#### 内置前缀生成器

- `DefaultMcpToolNamePrefixGenerator`：默认实现，跟踪重名，必要时添加计数前缀。
- `McpToolNamePrefixGenerator.noPrefix()`：原样使用工具名称；多个服务端提供同名工具时可能冲突。

要关闭前缀处理，可以注册以下 Bean。连接多个 MCP 服务端时，不建议这样做：

```java
@Configuration
public class McpConfiguration {

    @Bean
    public McpToolNamePrefixGenerator mcpToolNamePrefixGenerator() {
        return McpToolNamePrefixGenerator.noPrefix();
    }
}
```

同步和异步工具回调提供方通过 Spring 的 `ObjectProvider` 自动获取前缀生成器；未定义自定义 Bean 时，使用 `DefaultMcpToolNamePrefixGenerator`。

:::caution
使用 `McpToolNamePrefixGenerator.noPrefix()` 连接多个 MCP 服务端时，工具重名会导致 `IllegalStateException`。默认生成器会为重名工具添加唯一前缀，避免此类冲突。
:::

:::note
该生成器只处理 MCP 连接之间的重名，无法感知本地 `@Tool` 方法。关于本地工具与远程工具的名称冲突，以及哪些调用路径会检测冲突，见[混用本地工具与 MCP 工具](https://docs.spring.io/spring-ai/reference/api/tools.html#combining-local-and-mcp-tools)。
:::

<a id="_tool_context_to_mcp_meta_converter"></a>

### 将 ToolContext 转为 MCP 元数据

`ToolContextToMcpMetaConverter` 用于把 Spring AI 的[工具上下文（ToolContext）](https://docs.spring.io/spring-ai/reference/api/tools.html#tool-context)转换为 MCP 工具调用元数据。这样可以在模型生成的调用参数之外，另行传递用户 ID、访问令牌等上下文。

例如，将 `progressToken` 放入工具上下文，参与 [MCP 进度通知流程](https://modelcontextprotocol.io/specification/2025-06-18/basic/utilities/progress#progress-flow)，跟踪耗时操作：

```java
ChatModel chatModel = ...

String response = ChatClient.create(chatModel)
        .prompt("Tell me more about the customer with ID 42")
        .toolContext(Map.of("progressToken", "my-progress-token"))
        .call()
        .content();
```

没有自定义转换器 Bean 时，默认使用 `ToolContextToMcpMetaConverter.defaultConverter()`：

- 过滤 MCP exchange 键 `McpToolUtils.TOOL_CONTEXT_MCP_EXCHANGE_KEY`。
- 过滤值为 `null` 的条目。
- 其余条目作为元数据传递。

自定义实现示例：

```java
@Component
public class CustomToolContextToMcpMetaConverter implements ToolContextToMcpMetaConverter {

    @Override
    public Map<String, Object> convert(ToolContext toolContext) {
        if (toolContext == null || toolContext.getContext() == null) {
            return Map.of();
        }

        // 定制 ToolContext 到 MCP 元数据的转换
        Map<String, Object> metadata = new HashMap<>();

        // 为所有键添加应用前缀
        for (Map.Entry<String, Object> entry : toolContext.getContext().entrySet()) {
            if (entry.getValue() != null) {
                metadata.put("app_" + entry.getKey(), entry.getValue());
            }
        }

        // 添加其他元数据
        metadata.put("timestamp", System.currentTimeMillis());
        metadata.put("source", "spring-ai");

        return metadata;
    }
}
```

<a id="_built_in_converters"></a>

#### 内置转换器

- `ToolContextToMcpMetaConverter.defaultConverter()`：过滤 MCP exchange 键及 `null` 值，默认使用。
- `ToolContextToMcpMetaConverter.noOp()`：返回空 Map，关闭上下文到元数据的转换。

关闭转换的配置如下：

```java
@Configuration
public class McpConfiguration {

    @Bean
    public ToolContextToMcpMetaConverter toolContextToMcpMetaConverter() {
        return ToolContextToMcpMetaConverter.noOp();
    }
}
```

同步和异步 MCP 工具回调通过 Spring 的 `ObjectProvider` 自动获取转换器；没有自定义 Bean 时使用默认转换器。

<a id="_disable_the_mcp_toolcallback_auto_configuration"></a>

### 关闭 MCP ToolCallback 自动配置

MCP ToolCallback 自动配置默认开启，可通过 `spring.ai.mcp.client.toolcallback.enabled=false` 关闭。

关闭后，不会根据可用的 MCP 工具创建 `ToolCallbackProvider` Bean。

<a id="_mcp_client_annotations"></a>

## MCP 客户端注解

Client Starter 自动发现并注册以下注解方法：

- `@McpLogging`：处理服务端日志通知。
- `@McpSampling`：处理服务端发起的模型采样请求。
- `@McpElicitation`：处理服务端发起的信息征询请求，向用户收集补充信息。
- `@McpProgress`：处理耗时操作的进度通知。
- `@McpToolListChanged`：处理服务端工具列表变化通知。
- `@McpResourceListChanged`：处理服务端资源列表变化通知。
- `@McpPromptListChanged`：处理服务端提示词列表变化通知。

用法示例：

```java
@Component
public class McpClientHandlers {

    @McpLogging(clients = "server1")
    public void handleLoggingMessage(LoggingMessageNotification notification) {
        System.out.println("Received log: " + notification.level() +
                          " - " + notification.data());
    }

    @McpSampling(clients = "server1")
    public CreateMessageResult handleSamplingRequest(CreateMessageRequest request) {
        // 处理请求并生成响应
        String response = generateLLMResponse(request);

        return CreateMessageResult.builder(Role.ASSISTANT, response, "gpt-4")
            .build();
    }

    @McpProgress(clients = "server1")
    public void handleProgressNotification(ProgressNotification notification) {
        double percentage = notification.progress() * 100;
        System.out.println(String.format("Progress: %.2f%% - %s",
            percentage, notification.message()));
    }

    @McpToolListChanged(clients = "server1")
    public void handleToolListChanged(List<McpSchema.Tool> updatedTools) {
        System.out.println("Tool list updated: " + updatedTools.size() + " tools available");
        // 更新本地工具注册表
        toolRegistry.updateTools(updatedTools);
    }
}
```

注解同时支持同步和异步实现，`clients` 参数可以指定要处理哪条连接的事件：

```java
@McpLogging(clients = "server1")
public void handleServer1Logs(LoggingMessageNotification notification) {
    // 处理指定服务端的日志
    logToFile("server1.log", notification);
}

@McpSampling(clients = "server1")
public Mono<CreateMessageResult> handleAsyncSampling(CreateMessageRequest request) {
    return Mono.fromCallable(() -> {
        String response = generateLLMResponse(request);
        return CreateMessageResult.builder(Role.ASSISTANT, response, "gpt-4")
            .build();
    }).subscribeOn(Schedulers.boundedElastic());
}
```

各注解的完整用法见 [MCP 客户端注解](https://docs.spring.io/spring-ai/reference/api/mcp/mcp-annotations-client.html)。

<a id="_usage_example"></a>

## 使用示例

添加合适的 Starter 依赖后，在 `application.properties` 或 `application.yml` 配置客户端：

```yaml
spring:
  ai:
    mcp:
      client:
        enabled: true
        name: my-mcp-client
        version: 1.0.0
        request-timeout: 30s
        type: SYNC  # 响应式应用也可选 ASYNC
        sse:
          connections:
            server1:
              url: http://localhost:8080
            server2:
              url: http://otherserver:8081
        streamable-http:
          connections:
            server3:
              url: http://localhost:8083
              endpoint: /mcp
        stdio:
          root-change-notification: false
          connections:
            server1:
              command: /path/to/server
              args:
                - --port=8080
                - --mode=production
              env:
                API_KEY: your-api-key
                DEBUG: "true"
```

自动配置创建的客户端可以直接注入：

```java
@Autowired
private List<McpSyncClient> mcpSyncClients;  // 同步客户端

// 或

@Autowired
private List<McpAsyncClient> mcpAsyncClients;  // 异步客户端
```

工具回调默认开启。此时，所有客户端发现的 MCP 工具会通过 `ToolCallbackProvider` 提供：

```java
@Autowired
private SyncMcpToolCallbackProvider toolCallbackProvider;
ToolCallback[] toolCallbacks = toolCallbackProvider.getToolCallbacks();
```

<a id="_example_applications"></a>

## 示例应用

- [Brave 搜索聊天机器人](https://github.com/spring-projects/spring-ai-examples/tree/main/model-context-protocol/web-search/brave-chatbot)：通过 MCP 调用网络搜索服务。
- [默认 MCP Client Starter](https://github.com/spring-projects/spring-ai-examples/tree/main/model-context-protocol/client-starter/starter-default-client)：演示 `spring-ai-starter-mcp-client`。
- [WebFlux MCP Client Starter](https://github.com/spring-projects/spring-ai-examples/tree/main/model-context-protocol/client-starter/starter-webflux-client)：演示 `spring-ai-starter-mcp-client-webflux`。

<a id="_additional_resources"></a>

## 更多资料

- [Spring AI 文档](https://docs.spring.io/spring-ai/reference/)
- [MCP 规范](https://modelcontextprotocol.github.io/specification/)
- [Spring Boot 自动配置](https://docs.spring.io/spring-boot/docs/current/reference/html/features.html#features.developing-auto-configuration)
