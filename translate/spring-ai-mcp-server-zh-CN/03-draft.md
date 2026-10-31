# MCP Server Boot Starter

[MCP 服务端](https://modelcontextprotocol.io/docs/learn/server-concepts)通过标准协议接口向 AI 应用提供特定能力。每个服务端通常围绕一个业务领域提供功能。

Spring AI MCP Server Boot Starter 将这些能力接入 Spring Boot 自动配置体系，支持：

- 自动配置工具、资源和提示词等服务端组件。
- STDIO、SSE、Streamable-HTTP 与无状态服务端等传输和运行方式。
- 同步与异步 API。
- 多种传输实现，以及灵活的工具、资源和提示词定义。
- 能力变更通知。
- [基于注解开发服务端](https://docs.spring.io/spring-ai/reference/api/mcp/mcp-annotations-server.html)，自动扫描并注册 Bean。

::: warning

HTTP 传输（SSE、Streamable-HTTP 和 Stateless）默认暴露未经身份验证的 JSON-RPC 端点。Starter 本身不提供认证与授权，能访问端点的客户端就可能列出并调用已注册的工具、资源和提示词。

向本机以外开放 MCP 服务前，应先配置安全边界，详见[保护 MCP 服务端](https://docs.spring.io/spring-ai/reference/api/mcp/mcp-server-boot-starter-docs.html#securing-the-mcp-server)。STDIO 通过进程的标准输入输出通信，不直接暴露网络端点，因此不属于这里的 HTTP 端点风险。

:::

<a id="_mcp_server_boot_starters"></a>

## MCP Server Boot Starter

根据传输方式选择 Starter，并设置对应的 `spring.ai.mcp.server.protocol`；STDIO 使用独立的 `stdio` 开关。

<a id="_stdio"></a>

### STDIO

| 服务端类型 | 依赖 | 配置 |
| --- | --- | --- |
| [标准输入输出（STDIO）](https://docs.spring.io/spring-ai/reference/api/mcp/mcp-stdio-sse-server-boot-starter-docs.html) | `spring-ai-starter-mcp-server` | `spring.ai.mcp.server.stdio=true` |

<a id="_webmvc"></a>

### WebMVC

| 服务端类型 | 依赖 | 配置 |
| --- | --- | --- |
| [SSE WebMVC](https://docs.spring.io/spring-ai/reference/api/mcp/mcp-stdio-sse-server-boot-starter-docs.html#_sse_webmvc_server)（自 2.0.0 起弃用，改用 STREAMABLE） | `spring-ai-starter-mcp-server-webmvc` | `spring.ai.mcp.server.protocol=SSE` |
| [Streamable-HTTP WebMVC](https://docs.spring.io/spring-ai/reference/api/mcp/mcp-streamable-http-server-boot-starter-docs.html#_streamable_http_webmvc_server) | `spring-ai-starter-mcp-server-webmvc` | `spring.ai.mcp.server.protocol=STREAMABLE` |
| [无状态 WebMVC](https://docs.spring.io/spring-ai/reference/api/mcp/mcp-stateless-server-boot-starter-docs.html#_stateless_webmvc_server) | `spring-ai-starter-mcp-server-webmvc` | `spring.ai.mcp.server.protocol=STATELESS` |

<a id="_webflux_reactive"></a>

### WebFlux（响应式）

| 服务端类型 | 依赖 | 配置 |
| --- | --- | --- |
| [SSE WebFlux](https://docs.spring.io/spring-ai/reference/api/mcp/mcp-stdio-sse-server-boot-starter-docs.html#_sse_webflux_server)（自 2.0.0 起弃用，改用 STREAMABLE） | `spring-ai-starter-mcp-server-webflux` | `spring.ai.mcp.server.protocol=SSE` |
| [Streamable-HTTP WebFlux](https://docs.spring.io/spring-ai/reference/api/mcp/mcp-streamable-http-server-boot-starter-docs.html#_streamable_http_webflux_server) | `spring-ai-starter-mcp-server-webflux` | `spring.ai.mcp.server.protocol=STREAMABLE` |
| [无状态 WebFlux](https://docs.spring.io/spring-ai/reference/api/mcp/mcp-stateless-server-boot-starter-docs.html#_stateless_webflux_server) | `spring-ai-starter-mcp-server-webflux` | `spring.ai.mcp.server.protocol=STATELESS` |

<a id="_server_capabilities"></a>

## 服务端能力

具体能力取决于服务端与传输类型：

- **Tools（工具）**：向客户端提供模型可以请求调用的工具。
- **Resources（资源）**：以统一方式提供可访问的资源。
- **Prompts（提示词）**：提供可复用的提示词模板。
- **Completions（补全）**：为提示词参数和资源 URI 提供自动补全建议。
- **Logging（日志）**：向客户端发送结构化日志。
- **Progress（进度）**：通过通知消息报告长时间任务的进度，为可选能力。
- **Ping**：用于检查服务端状态的可选机制。

这些能力默认启用；关闭某项能力后，服务端不再注册或向客户端暴露对应功能。

<a id="_server_protocols"></a>

## 服务端协议与传输

- [**STDIO**](https://docs.spring.io/spring-ai/reference/api/mcp/mcp-stdio-sse-server-boot-starter-docs.html)：通过标准输入与标准输出通信，通常由客户端启动本地服务端子进程。设置 `spring.ai.mcp.server.stdio=true` 启用。
- [**SSE**](https://docs.spring.io/spring-ai/reference/api/mcp/mcp-stdio-sse-server-boot-starter-docs.html#_sse_webmvc_server)：基于服务器发送事件的旧式传输。服务端作为独立进程运行，可处理多个客户端连接。
- [**Streamable-HTTP**](https://docs.spring.io/spring-ai/reference/api/mcp/mcp-streamable-http-server-boot-starter-docs.html)：[Streamable HTTP 传输](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports#streamable-http)使用 HTTP POST 和 GET 请求，可选用 SSE 流返回多条服务端消息，替代旧式 SSE 传输。服务端可独立运行并处理多个客户端连接；设置 `spring.ai.mcp.server.protocol=STREAMABLE` 启用。
- [**Stateless（无状态）**](https://docs.spring.io/spring-ai/reference/api/mcp/mcp-stateless-server-boot-starter-docs.html)：请求之间不保留协议会话状态，简化微服务和云部署。设置 `spring.ai.mcp.server.protocol=STATELESS` 启用。

<a id="securing-the-mcp-server"></a>

## 保护 MCP 服务端

MCP 传输实现不绑定具体认证方案。自动配置负责建立端点，不负责执行认证与授权。与其他 Spring Web 端点一样，HTTP MCP 服务的安全边界应由额外的安全层提供，例如 Spring Security 或 [MCP Security](https://github.com/spring-ai-community/mcp-security)。

::: caution

默认情况下，MCP 端点（Streamable-HTTP 默认使用 `POST /mcp`）接受请求，不要求客户端提供凭据。能够访问网络端点的客户端可以列出并调用已注册的工具、资源和提示词。注册能力即意味着暴露能力；对外部署前，应先保护该端点。

:::

<a id="_syncasync_server_api_options"></a>

## 同步与异步服务端 API

MCP Server API 支持命令式同步模型和响应式异步模型：

- **同步服务端**：默认类型，使用 `McpSyncServer`，适合直接的请求—响应处理。配置 `spring.ai.mcp.server.type=SYNC` 后，自动配置同步工具规格。**只注册同步 MCP 注解方法，异步方法会被忽略。**
- **异步服务端**：使用 `McpAsyncServer`，面向非阻塞处理。配置 `spring.ai.mcp.server.type=ASYNC` 后，自动配置异步工具规格，并集成 Project Reactor。**只注册异步 MCP 注解方法，同步方法会被忽略。**

<a id="_mcp_server_annotations"></a>

## MCP 服务端注解

Server Starter 支持用 Java 注解声明 MCP 能力，减少手动创建和注册规格的代码。

<a id="_key_annotations"></a>

### 主要注解

- [**`@McpTool`**](https://docs.spring.io/spring-ai/reference/api/mcp/mcp-annotations-server.html#_mcptool)：将方法声明为 MCP 工具，自动生成参数 JSON Schema。
- [**`@McpResource`**](https://docs.spring.io/spring-ai/reference/api/mcp/mcp-annotations-server.html#_mcpresource)：通过 URI 模板提供资源访问。
- [**`@McpPrompt`**](https://docs.spring.io/spring-ai/reference/api/mcp/mcp-annotations-server.html#_mcpprompt)：生成用于 AI 交互的提示词消息。
- [**`@McpComplete`**](https://docs.spring.io/spring-ai/reference/api/mcp/mcp-annotations-server.html#_mcpcomplete)：为提示词提供自动补全。

<a id="_special_parameters"></a>

### 特殊参数

注解方法支持注入[特殊参数](https://docs.spring.io/spring-ai/reference/api/mcp/mcp-annotations-special-params.html)，获取请求上下文：

- **`McpMeta`**：读取 MCP 请求元数据。
- **`@McpProgressToken`**：接收长时间任务使用的进度令牌。
- **`McpSyncServerExchange` / `McpAsyncServerExchange`**：访问完整服务端交互上下文，执行高级操作。
- **`McpTransportContext`**：轻量的传输上下文，可用于无状态操作。
- **`CallToolRequest`**：访问工具调用请求，支持动态 Schema 等场景。

<a id="_simple_example"></a>

### 简单示例

下面的 Bean 定义一个加法工具和一个配置资源：

```java
@Component
public class CalculatorTools {

    @McpTool(name = "add", description = "Add two numbers together")
    public int add(
            @McpToolParam(description = "First number", required = true) int a,
            @McpToolParam(description = "Second number", required = true) int b) {
        return a + b;
    }

    @McpResource(uri = "config://{key}", name = "Configuration")
    public String getConfig(String key) {
        return configData.get(key);
    }
}
```

<a id="_adding_data_to_mcptransportcontext"></a>

### 向 McpTransportContext 添加数据

`McpTransportContext` 默认是空上下文 `McpTransportContext.EMPTY`，使 MCP 服务端不依赖具体传输方式。

工具需要读取 HTTP 请求头、远程主机等传输信息时，可在传输 Provider 上配置 `TransportContextExtractor`。

WebMVC 示例：

```java
@Bean
public WebMvcStreamableServerTransportProvider transport() {
    return WebMvcStreamableServerTransportProvider.builder()
        .contextExtractor(serverRequest -> {
            String authorization = serverRequest.headers().firstHeader("Authorization");
            return McpTransportContext.create(Map.of("authorization", authorization));
        })
        .build();
}
```

WebFlux 示例：

```java
@Bean
public WebFluxStreamableServerTransportProvider transport() {
    return WebFluxStreamableServerTransportProvider.builder()
        .contextExtractor(serverRequest -> {
            String authorization = serverRequest.headers().firstHeader("Authorization");
            return McpTransportContext.create(Map.of("authorization", authorization));
        })
        .build();
}
```

随后在工具中通过 `McpSyncRequestContext` 或 `McpAsyncRequestContext` 读取传输上下文：

```java
@McpTool
public String accessProtectedResource(McpSyncRequestContext requestContext) {
    McpTransportContext context = requestContext.transportContext();
    String authorization = (String) context.get("authorization");

    return "Successfully accessed protected resource.";
}
```

<a id="_auto_configuration"></a>

### 自动配置

Spring Boot 会自动发现并注册包含 MCP 注解方法的 Bean：

```java
@SpringBootApplication
public class McpServerApplication {
    public static void main(String[] args) {
        SpringApplication.run(McpServerApplication.class, args);
    }
}
```

自动配置依次完成：

1. 扫描带 MCP 注解的 Bean。
2. 创建对应的规格对象。
3. 将其注册到 MCP 服务端。
4. 根据配置选择同步或异步实现。

<a id="_configuration_properties"></a>

### 配置属性

服务端注解扫描器配置如下：

```yaml
spring:
  ai:
    mcp:
      server:
        type: SYNC  # or ASYNC
        annotation-scanner:
          enabled: true
```

<a id="_additional_resources"></a>

### 延伸阅读

- [服务端注解参考](https://docs.spring.io/spring-ai/reference/api/mcp/mcp-annotations-server.html)：完整注解用法。
- [特殊参数](https://docs.spring.io/spring-ai/reference/api/mcp/mcp-annotations-special-params.html)：高级参数注入。
- [注解示例](https://docs.spring.io/spring-ai/reference/api/mcp/mcp-annotations-examples.html)：完整示例与使用场景。

<a id="_example_applications"></a>

## 示例应用

- [天气服务端：SSE WebFlux](https://github.com/spring-projects/spring-ai-examples/tree/main/model-context-protocol/weather/starter-webflux-server)：使用 WebFlux 传输与 Server Starter。
- [天气服务端：STDIO](https://github.com/spring-projects/spring-ai-examples/tree/main/model-context-protocol/weather/starter-stdio-server)：使用 STDIO 传输与 Server Starter。
- [手动配置天气服务端](https://github.com/spring-projects/spring-ai-examples/tree/main/model-context-protocol/weather/manual-webflux-server)：直接使用 Java SDK 配置服务端，便于对照自动配置。
- Streamable-HTTP WebFlux / WebMVC 示例：来源标注为待补充。
- Stateless WebFlux / WebMVC 示例：来源标注为待补充。

<a id="_additional_resources_2"></a>

## 更多资料

- [MCP 服务端注解](https://docs.spring.io/spring-ai/reference/api/mcp/mcp-annotations-server.html)：用注解声明服务端能力。
- [特殊参数](https://docs.spring.io/spring-ai/reference/api/mcp/mcp-annotations-special-params.html)：参数注入与上下文访问。
- [MCP 注解示例](https://docs.spring.io/spring-ai/reference/api/mcp/mcp-annotations-examples.html)：完整示例与使用场景。
- [Spring AI 文档](https://docs.spring.io/spring-ai/reference/)。
- [MCP 协议规范](https://modelcontextprotocol.io/specification)。
- [Spring Boot 自动配置](https://docs.spring.io/spring-boot/docs/current/reference/html/features.html#features.developing-auto-configuration)。
