# MCP Client Boot Starter

Spring AI 的 MCP（模型上下文协议）Client Boot Starter 为 Spring Boot 应用自动配置 MCP 客户端，支持同步、异步 API 和多种传输方式。

主要能力包括：

- 管理多个客户端实例。
- 按配置自动初始化客户端。
- 配置多条具名连接，支持 STDIO、HTTP/SSE 和 Streamable-HTTP。
- 接入 Spring AI 工具执行框架。
- 按条件包含或排除工具。
- 自定义工具名称前缀，避免名称冲突。
- 管理客户端生命周期，在应用上下文关闭时自动清理资源。
- 通过定制器调整客户端创建过程。

<a id="_starters"></a>

## Starter 选择

<a id="_standard_mcp_client"></a>

### 标准 MCP 客户端

```xml
<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>spring-ai-starter-mcp-client</artifactId>
</dependency>
```

标准 Starter 可同时连接一个或多个 MCP 服务端，支持 `STDIO`、`SSE`、`Streamable-HTTP` 和 `Stateless Streamable-HTTP`。其中 STDIO 通过标准输入输出与服务端进程通信；SSE 和 Streamable-HTTP 使用基于 JDK `HttpClient` 的传输实现。

每条 MCP 服务端连接都会创建一个客户端实例。应用统一选择 `SYNC` 或 `ASYNC`，不能混用。来源建议生产部署使用 `spring-ai-starter-mcp-client-webflux` 提供的 WebFlux SSE 与 Streamable-HTTP 连接。

<a id="_webflux_client"></a>

### WebFlux 客户端

WebFlux Starter 的功能与标准 Starter 类似，HTTP 部分使用 WebFlux 实现，支持 Streamable-HTTP、Stateless Streamable-HTTP 和 SSE。

```xml
<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>spring-ai-starter-mcp-client-webflux</artifactId>
</dependency>
```

<a id="_configuration_properties"></a>

## 配置属性

<a id="_common_properties"></a>

### 通用属性

以下属性统一使用 `spring.ai.mcp.client` 前缀：

| 属性 | 说明 | 默认值 |
| --- | --- | --- |
| `enabled` | 是否启用 MCP 客户端 | `true` |
| `name` | MCP 客户端实例名称 | `spring-ai-mcp-client` |
| `version` | MCP 客户端实例版本 | `1.0.0` |
| `initialized` | 是否在创建时初始化客户端 | `true` |
| `request-timeout` | MCP 客户端请求超时时间 | `20s` |
| `type` | 客户端类型：`SYNC` 或 `ASYNC`；所有客户端必须统一类型 | `SYNC` |
| `root-change-notification` | 是否为所有客户端启用根目录变更通知 | `true` |
| `toolcallback.enabled` | 是否将 MCP 工具回调接入 Spring AI 工具执行框架 | `true` |

<a id="_mcp_annotations_properties"></a>

### MCP 注解属性

MCP 客户端注解用于声明式编写客户端处理器。以下属性使用 `spring.ai.mcp.client.annotation-scanner` 前缀：

| 属性 | 说明 | 默认值 |
| --- | --- | --- |
| `enabled` | 是否自动扫描 MCP 客户端注解 | `true` |

<a id="_stdio_transport_properties"></a>

### STDIO 传输属性

STDIO 通过标准输入输出通信，配置前缀为 `spring.ai.mcp.client.stdio`：

| 属性 | 说明 | 默认值 |
| --- | --- | --- |
| `servers-configuration` | 保存 MCP 服务端配置的 JSON 资源 | — |
| `connections` | 具名 STDIO 连接配置的映射 | — |
| `connections.[name].command` | 启动 MCP 服务端的命令 | — |
| `connections.[name].args` | 命令参数列表 | — |
| `connections.[name].env` | 服务端进程的环境变量映射 | — |

配置示例：

```yaml
spring:
  ai:
    mcp:
      client:
        stdio:
          root-change-notification: true
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

也可以把连接配置放入外部 JSON 文件，格式与 [Claude Desktop 配置](https://modelcontextprotocol.io/quickstart/user)一致：

```yaml
spring:
  ai:
    mcp:
      client:
        stdio:
          servers-configuration: classpath:mcp-servers.json
```

JSON 文件内容示例：

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/username/Desktop",
        "/Users/username/Downloads"
      ]
    }
  }
}
```

<a id="_windows_stdio_configuration"></a>

### Windows STDIO 配置

:::note
Windows 上的 `npx`、`npm` 通常通过 `.cmd` 批处理脚本启动。Java `ProcessBuilder` 不能直接执行这类脚本，需要使用 `cmd.exe /c`。此要求针对批处理入口，不能据此把所有 Node.js 命令都视为 `.cmd`。
:::

<a id="_why_windows_needs_special_handling"></a>

#### 为什么需要特殊处理

`StdioClientTransport` 使用 Java `ProcessBuilder` 启动服务端进程。Windows 原生 `.exe` 程序可以直接启动；批处理脚本和 shell 内置命令则需要交给 `cmd.exe` 执行。

例如，`npx.cmd`、`npm.cmd`，以及某些安装方式提供的 `python.cmd`，都需要经过命令解释器。

<a id="_solution_cmd_exe_wrapper"></a>

#### 使用 cmd.exe 包装命令

调用批处理入口时，把实际命令放在 `cmd.exe /c` 后面。

**Windows：**

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "cmd.exe",
      "args": [
        "/c",
        "npx",
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "C:\\Users\\username\\Desktop"
      ]
    }
  }
}
```

**Linux/macOS：**

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/username/Desktop"
      ]
    }
  }
}
```

<a id="_cross_platform_programmatic_configuration"></a>

#### 跨平台编程式配置

不想维护多套配置文件时，可以在 Spring Boot 应用中识别操作系统，再选择启动方式：

```java
@Bean(destroyMethod = "close")
@ConditionalOnMissingBean(McpSyncClient.class)
public McpSyncClient mcpClient() {
    ServerParameters stdioParams;

    if (isWindows()) {
        // Windows: cmd.exe /c npx approach
        var winArgs = new ArrayList<>(Arrays.asList(
            "/c", "npx", "-y", "@modelcontextprotocol/server-filesystem", "target"));
        stdioParams = ServerParameters.builder("cmd.exe")
                .args(winArgs)
                .build();
    } else {
        // Linux/Mac: direct npx approach
        stdioParams = ServerParameters.builder("npx")
                .args("-y", "@modelcontextprotocol/server-filesystem", "target")
                .build();
    }

    return McpClient.sync(new StdioClientTransport(stdioParams, McpJsonDefaults.getMapper()))
            .requestTimeout(Duration.ofSeconds(10))
            .build()
            .initialize();
}

private static boolean isWindows() {
    return System.getProperty("os.name").toLowerCase().contains("win");
}
```

:::note
来源建议在手动声明 `@Bean` 时添加 `@ConditionalOnMissingBean(McpSyncClient.class)`，以避免与 JSON 配置触发的自动配置重复。实际是否退让仍需核对自动配置的条件和注册顺序。
:::

<a id="_path_considerations"></a>

#### 路径选择

**相对路径**更方便跨环境迁移：

```json
{
  "command": "cmd.exe",
  "args": ["/c", "npx", "-y", "@modelcontextprotocol/server-filesystem", "target"]
}
```

服务端基于进程工作目录解析相对路径。

**绝对路径**需要按 JSON 语法转义反斜杠；以下示例使用 Windows 路径：

```json
{
  "command": "cmd.exe",
  "args": ["/c", "npx", "-y", "@modelcontextprotocol/server-filesystem", "C:\\Users\\username\\project\\target"]
}
```

<a id="_common_windows_batch_files_requiring_cmd_exe"></a>

#### 常见的 Windows 批处理入口

- `npx.cmd`、`npm.cmd`：Node.js 工具与包管理命令。
- `python.cmd`：部分 Python 安装方式提供的入口。
- `pip.cmd`：Python 包管理入口。
- `mvn.cmd`：Maven 命令入口。
- `gradle.cmd`：Gradle 命令入口。
- 自定义 `.cmd` 或 `.bat` 脚本。

<a id="_reference_implementation"></a>

#### 参考实现

[Spring AI Filesystem 示例](https://github.com/spring-projects/spring-ai-examples/tree/main/model-context-protocol/filesystem)展示了自动识别操作系统并创建 MCP 客户端的完整实现。

<a id="_streamable_http_transport_properties"></a>

### Streamable-HTTP 传输属性

用于连接 Streamable-HTTP 和 Stateless Streamable-HTTP 服务端。配置前缀为 `spring.ai.mcp.client.streamable-http`：

| 属性 | 说明 | 默认值 |
| --- | --- | --- |
| `connections` | 具名 Streamable-HTTP 连接配置的映射 | — |
| `connections.[name].url` | MCP 服务端的基础 URL | — |
| `connections.[name].endpoint` | 追加到基础 URL 的端点路径 | `/mcp` |

配置示例：

```yaml
spring:
  ai:
    mcp:
      client:
        streamable-http:
          connections:
            server1:
              url: http://localhost:8080
            server2:
              url: http://otherserver:8081
              endpoint: /custom-sse
```

<a id="_sse_transport_properties"></a>

### SSE 传输属性

SSE（服务器发送事件）配置前缀为 `spring.ai.mcp.client.sse`：

| 属性 | 说明 | 默认值 |
| --- | --- | --- |
| `connections` | 具名 SSE 连接配置的映射 | — |
| `connections.[name].url` | SSE 通信的基础 URL | — |
| `connections.[name].sse-endpoint` | 追加到基础 URL 的 SSE 端点路径 | `/sse` |

配置示例：

```yaml
spring:
  ai:
    mcp:
      client:
        sse:
          connections:
            # Simple configuration using default /sse endpoint
            server1:
              url: http://localhost:8080
            # Custom SSE endpoint
            server2:
              url: http://otherserver:8081
              sse-endpoint: /custom-sse
            # Complex URL with path and token (like MCP Hub)
            mcp-hub:
              url: http://localhost:3000
              sse-endpoint: /mcp-hub/sse/cf9ec4527e3c4a2cbb149a85ea45ab01
            # SSE endpoint with query parameters
            api-server:
              url: https://api.example.com
              sse-endpoint: /v1/mcp/events?token=abc123&format=json
```

<a id="_url_splitting_guidelines"></a>

#### 拆分 URL

完整 SSE URL 应拆成基础 URL 和端点路径：

| 完整 URL | 配置 |
| --- | --- |
| `http://localhost:3000/mcp-hub/sse/token123` | `url: localhost:3000`；`sse-endpoint: /mcp-hub/sse/token123` |
| `https://api.service.com/v2/events?key=secret` | `url: api.service.com`；`sse-endpoint: /v2/events?key=secret` |
| `http://localhost:8080/sse` | `url: localhost:8080`；`sse-endpoint: /sse`，也可省略默认路径 |

<a id="_troubleshooting_sse_connections"></a>

#### 排查 SSE 连接问题

遇到 **404 Not Found** 时：

- 检查 URL 拆分：基础 `url` 应只包含协议、主机和端口。
- 确认 `sse-endpoint` 以 `/` 开头，并保留完整路径与查询参数。
- 用浏览器或 `curl` 请求完整 URL，确认端点可访问。

<a id="_streamable_http_transport_properties_2"></a>

### Streamable-HTTP 配置补充

以下为来源再次列出的 Streamable-HTTP 配置，前缀同样是 `spring.ai.mcp.client.streamable-http`：

| 属性 | 说明 | 默认值 |
| --- | --- | --- |
| `connections` | 具名 Streamable-HTTP 连接配置的映射 | — |
| `connections.[name].url` | MCP 服务端的基础 URL | — |
| `connections.[name].endpoint` | 追加到基础 URL 的端点路径 | `/mcp` |

配置示例：

```yaml
spring:
  ai:
    mcp:
      client:
        streamable-http:
          connections:
            server1:
              url: http://localhost:8080
            server2:
              url: http://otherserver:8081
              endpoint: /custom-sse
```

<a id="_features"></a>

## 客户端能力

<a id="_syncasync_client_types"></a>

### 同步与异步客户端

Starter 支持两种客户端类型：

- **同步客户端**：默认类型，配置为 `spring.ai.mcp.client.type=SYNC`，适合传统阻塞式请求响应。仅注册同步 MCP 注解方法，忽略异步方法。
- **异步客户端**：配置为 `spring.ai.mcp.client.type=ASYNC`，适合响应式、非阻塞调用。仅注册异步 MCP 注解方法，忽略同步方法。

<a id="client-scope-and-session-boundaries"></a>

### 客户端作用域与会话边界

自动配置的 `McpSyncClient` 和 `McpAsyncClient` 是应用级单例。每条已配置的服务端连接对应一个客户端 Bean，应用的所有请求共享该实例。

每个客户端代表一个 MCP 协议会话，会话随客户端存活；服务端终止会话并返回 HTTP 404，或客户端关闭时，原会话才结束或重建。

:::caution
**MCP 协议会话不等于用户隔离边界。**

通过 `transportContextProvider(…)`、`McpSyncHttpClientRequestCustomizer` 或 WebClient 的 `ExchangeFilterFunction` 传递的凭据会按请求发送，服务端能收到当前调用者的身份；但底层协议会话仍由使用该客户端 Bean 的所有调用者共享。

多用户应用需要考虑：

- `initialize` 与 `tools/list` 发生在连接初始化时，使用当时可用的身份，而非后来调用工具的用户身份。
- 服务端如果只按 MCP 会话保存状态，该状态会由客户端 Bean 的所有用户共享。
- 服务端发起的采样和信息征询通过共享通道到达客户端，不自动携带用户归属。

客户端和服务端都不能直接把 MCP 会话当作用户或租户边界。
:::

是否需要独立会话，取决于连接的 MCP 服务端。无状态服务端通常可以共享客户端；有状态服务端如果逐请求按 Token 鉴权，且不在会话中保存用户相关状态，也可以共享。

以下情况应考虑按用户或租户分别建立会话：

- 服务端按身份过滤 `tools/list`、资源或提示词。由于发现过程只执行一次，共享用户可能都看到初次发现时的结果。
- 服务端在会话中保存工作目录、订阅、分页游标、缓存上下文等用户相关状态。
- 使用采样或信息征询，且需要把服务端请求对应到具体用户。
- 服务端按会话审计或限流，或部署要求租户不能共享协议会话。
- 无法确认第三方服务端如何处理会话。

需要独立协议会话的应用，应自行管理生命周期：为每个用户或租户创建独立的传输和客户端，在其工作结束时关闭。自动配置的共享 Bean 不适合这一用途，Spring AI 也未提供按用户管理的客户端池。编程式创建方式见[绕过 Spring AI 自动配置](https://docs.spring.io/spring-ai/reference/api/mcp/mcp-security.html#_working_around_spring_ai_autoconfiguration)。

<a id="_client_customization"></a>

### 客户端定制

自动配置通过回调接口开放客户端规格的定制入口，可以调整请求超时、事件处理与消息处理行为。

<a id="_customization_types"></a>

#### 可定制内容

- **请求配置**：设置请求超时。
- [**采样处理器**](https://modelcontextprotocol.io/specification/2025-06-18/client/sampling)：服务端通过客户端请求模型补全或生成。客户端保留模型访问、选择和权限控制，服务端无需持有模型 API Key。
- [**文件系统根目录（Roots）**](https://modelcontextprotocol.io/specification/2025-06-18/client/roots)：客户端向服务端声明可操作目录的范围。服务端可向支持该能力的客户端查询根目录列表，并接收列表变更通知。
- [**信息征询处理器**](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation)：服务端在交互过程中通过客户端向用户补充询问信息。
- **事件处理器**：接收服务端通知，包括工具列表、资源列表、提示词列表的变更，以及[日志](https://modelcontextprotocol.io/specification/2025-06-18/server/utilities/logging)和[进度](https://modelcontextprotocol.io/specification/2025-06-18/basic/utilities/progress)通知。

客户端可以通过设置最低日志级别控制日志详细程度。

<a id="_client_customization_example"></a>
