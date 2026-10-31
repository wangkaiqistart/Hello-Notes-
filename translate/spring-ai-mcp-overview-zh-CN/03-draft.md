# 模型上下文协议（MCP）

:::tip
初次接触 MCP，可以结合[入门指南](https://docs.spring.io/spring-ai/reference/guides/getting-started-mcp.html)中的动手示例阅读。
:::

**模型上下文协议（Model Context Protocol，MCP）** 为 AI 应用访问外部工具和资源提供统一接口。应用可以通过它连接数据库、API、文件系统及其他服务，并根据运行环境选择合适的传输方式。

[MCP Java SDK](https://modelcontextprotocol.io/sdk/java/mcp-overview) 提供协议的 Java 实现，支持同步与异步通信。Spring AI 在其基础上提供 Boot Starter 和 Java 注解，既能连接已有 MCP 服务，也能把 Spring 业务能力发布为 MCP 服务。可以从 [Spring Initializr](https://start.spring.io) 创建带 MCP 支持的项目。

<a id="_mcp_java_sdk_architecture"></a>

## MCP Java SDK 架构

本节介绍 SDK 的底层架构；使用 Spring Boot 时，可以重点阅读后面的 [Spring AI 集成](#_spring_ai_mcp_integration)。SDK 分为三层，各自负责协议操作、会话和消息传输。

<a id="_clientserver_layer_top"></a>

### 客户端与服务端层

最上层处理应用逻辑和协议操作：

- `McpClient`：管理客户端操作和服务端连接。
- `McpServer`：处理服务端协议操作和客户端请求。
- 两者都通过下层的会话组件管理通信。

<a id="_session_layer_middle"></a>

### 会话层

中间层维护通信模式和连接状态：

- `McpSession`：会话管理核心接口。
- `McpClientSession`：客户端会话实现。
- `McpServerSession`：服务端会话实现。

<a id="_transport_layer_bottom"></a>

### 传输层

底层负责实际消息传输：

- `McpTransport`：处理 JSON-RPC 消息的序列化与反序列化。
- 支持 STDIO、HTTP/SSE、Streamable-HTTP 等传输实现。
- 为上层会话和协议操作提供通信基础。

下图将三层放在一起，重点看客户端、服务端如何通过会话层复用不同的传输实现。

[![MCP Java SDK 三层架构：客户端和服务端层、会话层与传输层的对应关系](/images/frameworks/spring-ai/mcp/mcp-stack.svg)](/images/frameworks/spring-ai/mcp/mcp-stack.svg)

### MCP 客户端

[MCP Client](https://modelcontextprotocol.io/sdk/java/mcp-client) 负责建立和管理与服务端的连接，包括：

- 协议版本协商与能力协商。
- JSON-RPC 通信和消息传输。
- 工具发现与调用、资源访问和管理、提示词交互。
- 可选的根目录（Roots）管理与采样（Sampling）支持。
- 同步与异步操作。
- STDIO 进程通信、基于 Java HttpClient 的 SSE，以及基于 WebFlux 的响应式 SSE 等传输实现。

下图展示客户端 API、会话与传输组件的关系。

[![Java MCP 客户端架构：同步与异步 API 通过会话连接多种传输实现](/images/frameworks/spring-ai/mcp/java-mcp-client-architecture.jpg)](/images/frameworks/spring-ai/mcp/java-mcp-client-architecture.jpg)

### MCP 服务端

[MCP Server](https://modelcontextprotocol.io/sdk/java/mcp-server) 向客户端提供特定领域的能力，包括：

- 工具发布与发现、通过 URI 访问资源、提示词模板。
- 与客户端协商能力、发送结构化日志和通知。
- 并发客户端连接管理，以及同步与异步 API。
- STDIO、Streamable-HTTP、无状态 Streamable-HTTP 和 SSE 传输。

下图展示服务端如何把能力注册、会话管理与传输分开。

[![Java MCP 服务端架构：工具、资源与提示词通过同步或异步服务端及传输层提供给客户端](/images/frameworks/spring-ai/mcp/java-mcp-server-architecture.jpg)](/images/frameworks/spring-ai/mcp/java-mcp-server-architecture.jpg)

直接使用底层 API 时，查阅 [MCP Java SDK 文档](https://modelcontextprotocol.io/sdk/java/mcp-overview)；使用 Spring Boot 时，优先使用下面的 Starter。

<a id="_spring_ai_mcp_integration"></a>

## Spring AI MCP 集成

Spring AI 提供客户端与服务端两组 Boot Starter。

<a id="_client_starters"></a>

### 客户端 Starter

详细配置见 [MCP Client Boot Starter](https://docs.spring.io/spring-ai/reference/api/mcp/mcp-client-boot-starter-docs.html)。

| 依赖 | 传输支持 |
| --- | --- |
| `spring-ai-starter-mcp-client` | STDIO，以及基于 JDK HttpClient 的 Streamable-HTTP、无状态 Streamable-HTTP 和 SSE |
| `spring-ai-starter-mcp-client-webflux` | 基于 WebFlux 的 Streamable-HTTP、无状态 Streamable-HTTP 和 SSE，也支持 STDIO |

<a id="_server_starters"></a>

### 服务端 Starter

详细配置见 [MCP Server Boot Starter](https://docs.spring.io/spring-ai/reference/api/mcp/mcp-server-boot-starter-docs.html)。根据传输方式和 Web 技术栈选择依赖。

<a id="_stdio"></a>

#### STDIO

| 传输 | 依赖 | 配置 |
| --- | --- | --- |
| [标准输入输出](https://docs.spring.io/spring-ai/reference/api/mcp/mcp-stdio-sse-server-boot-starter-docs.html) | `spring-ai-starter-mcp-server` | `spring.ai.mcp.server.stdio=true` |

<a id="_webmvc"></a>

#### WebMVC

| 传输 | 依赖 | 配置 |
| --- | --- | --- |
| [SSE](https://docs.spring.io/spring-ai/reference/api/mcp/mcp-stdio-sse-server-boot-starter-docs.html#_sse_webmvc_server) | `spring-ai-starter-mcp-server-webmvc` | `spring.ai.mcp.server.protocol=SSE` |
| [Streamable-HTTP](https://docs.spring.io/spring-ai/reference/api/mcp/mcp-streamable-http-server-boot-starter-docs.html#_streamable_http_webmvc_server) | `spring-ai-starter-mcp-server-webmvc` | `spring.ai.mcp.server.protocol=STREAMABLE` |
| [无状态 Streamable-HTTP](https://docs.spring.io/spring-ai/reference/api/mcp/mcp-stateless-server-boot-starter-docs.html#_stateless_webmvc_server) | `spring-ai-starter-mcp-server-webmvc` | `spring.ai.mcp.server.protocol=STATELESS` |

<a id="_webflux_reactive"></a>

#### WebFlux

| 传输 | 依赖 | 配置 |
| --- | --- | --- |
| [SSE](https://docs.spring.io/spring-ai/reference/api/mcp/mcp-stdio-sse-server-boot-starter-docs.html#_sse_webflux_server) | `spring-ai-starter-mcp-server-webflux` | `spring.ai.mcp.server.protocol=SSE` |
| [Streamable-HTTP](https://docs.spring.io/spring-ai/reference/api/mcp/mcp-streamable-http-server-boot-starter-docs.html#_streamable_http_webflux_server) | `spring-ai-starter-mcp-server-webflux` | `spring.ai.mcp.server.protocol=STREAMABLE` |
| [无状态 Streamable-HTTP](https://docs.spring.io/spring-ai/reference/api/mcp/mcp-stateless-server-boot-starter-docs.html#_stateless_webflux_server) | `spring-ai-starter-mcp-server-webflux` | `spring.ai.mcp.server.protocol=STATELESS` |

新建 HTTP 服务优先考虑 Streamable-HTTP；旧的 HTTP+SSE 传输自 Spring AI 2.0.0 起弃用。2.0.2 的 `protocol` 默认值为 `STREAMABLE`，建议示例中显式配置，避免与旧版默认值混淆。

<a id="_spring_ai_mcp_annotations"></a>

## MCP 注解

除编程式配置外，Spring AI 的 [MCP 注解模块](https://docs.spring.io/spring-ai/reference/api/mcp/mcp-annotations-overview.html)还可以用 Java 方法声明服务端操作、处理客户端请求与通知。

注解可用于创建工具、资源和提示词，自动生成工具参数的 JSON Schema，访问请求元数据与上下文，并通过自动扫描减少注册代码。

| 类别 | 注解或类型 |
| --- | --- |
| [服务端注解](https://docs.spring.io/spring-ai/reference/api/mcp/mcp-annotations-server.html) | `@McpTool`、`@McpResource`、`@McpPrompt`、`@McpComplete` |
| [客户端注解](https://docs.spring.io/spring-ai/reference/api/mcp/mcp-annotations-client.html) | `@McpLogging`、`@McpSampling`、`@McpElicitation`、`@McpProgress` |
| [特殊参数](https://docs.spring.io/spring-ai/reference/api/mcp/mcp-annotations-special-params.html) | `McpSyncServerExchange`、`McpAsyncServerExchange`、`McpTransportContext`、`McpMeta` |

注解模块支持自动发现、扫描范围配置，并与 MCP Boot Starter 集成。

<a id="_upgrading_to_spring_ai_2_0"></a>

## 升级到 Spring AI 2.0

Spring AI 2.0 将 Spring 专用 MCP 传输实现 `mcp-spring-webflux` 和 `mcp-spring-webmvc` 从 MCP Java SDK 移入 Spring AI 项目。直接引用这些依赖或类的应用，需要更新依赖坐标和 Java import。

<a id="_maven_dependency_group_id_change"></a>

### Maven 依赖坐标变化

两个传输模块的 groupId 从 `io.modelcontextprotocol.sdk` 改为 `org.springframework.ai`。

迁移前：

```xml
<dependency>
    <groupId>io.modelcontextprotocol.sdk</groupId>
    <artifactId>mcp-spring-webflux</artifactId>
</dependency>
<dependency>
    <groupId>io.modelcontextprotocol.sdk</groupId>
    <artifactId>mcp-spring-webmvc</artifactId>
</dependency>
```

迁移后：

```xml
<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>mcp-spring-webflux</artifactId>
</dependency>
<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>mcp-spring-webmvc</artifactId>
</dependency>
```

使用 `spring-ai-bom` 管理依赖版本时，不必为这些依赖单独指定版本；使用 Starter 时通常会间接引入对应模块。

<a id="_java_package_relocation"></a>

### Java 包名迁移

服务端传输类迁入以下包：

| 类 | 旧包 | 新包 |
| --- | --- | --- |
| `WebFluxSseServerTransportProvider` | `io.modelcontextprotocol.server.transport` | `org.springframework.ai.mcp.server.webflux.transport` |
| `WebFluxStreamableServerTransportProvider` | `io.modelcontextprotocol.server.transport` | `org.springframework.ai.mcp.server.webflux.transport` |
| `WebFluxStatelessServerTransport` | `io.modelcontextprotocol.server.transport` | `org.springframework.ai.mcp.server.webflux.transport` |
| `WebMvcSseServerTransportProvider` | `io.modelcontextprotocol.server.transport` | `org.springframework.ai.mcp.server.webmvc.transport` |
| `WebMvcStreamableServerTransportProvider` | `io.modelcontextprotocol.server.transport` | `org.springframework.ai.mcp.server.webmvc.transport` |
| `WebMvcStatelessServerTransport` | `io.modelcontextprotocol.server.transport` | `org.springframework.ai.mcp.server.webmvc.transport` |

客户端传输类迁入以下包：

| 类 | 旧包 | 新包 |
| --- | --- | --- |
| `WebFluxSseClientTransport` | `io.modelcontextprotocol.client.transport` | `org.springframework.ai.mcp.client.webflux.transport` |
| `WebClientStreamableHttpTransport` | `io.modelcontextprotocol.client.transport` | `org.springframework.ai.mcp.client.webflux.transport` |

import 更新示例：

```java
// Before
import io.modelcontextprotocol.server.transport.WebFluxSseServerTransportProvider;
import io.modelcontextprotocol.server.transport.WebMvcSseServerTransportProvider;
import io.modelcontextprotocol.client.transport.WebFluxSseClientTransport;
import io.modelcontextprotocol.client.transport.WebClientStreamableHttpTransport;

// After
import org.springframework.ai.mcp.server.webflux.transport.WebFluxSseServerTransportProvider;
import org.springframework.ai.mcp.server.webmvc.transport.WebMvcSseServerTransportProvider;
import org.springframework.ai.mcp.client.webflux.transport.WebFluxSseClientTransport;
import org.springframework.ai.mcp.client.webflux.transport.WebClientStreamableHttpTransport;
```

<a id="_mcp_sdk_version_requirement"></a>

### MCP SDK 版本

升级到 Spring AI 2.0 时，MCP Java SDK 也离开了旧的 `0.18.x` 版本线。来源的迁移说明使用 `1.0.0 RC1` 及以后版本作为当时的升级基线；这不是当前应用应手动固定的 SDK 版本。Spring AI 2.0.2 的父 POM 已使用 MCP SDK `2.1.0`，实际项目应遵循对应 Spring AI BOM 的版本管理。

<a id="_spring_boot_auto_configuration_users"></a>

### 使用 Boot 自动配置的项目

如果项目完全依赖 Starter 自动配置，通常无需修改 Java 代码：自动配置已经适配新包名。直接声明过旧传输模块的项目，仍需按上面的规则更新 `pom.xml` 或 `build.gradle`。

<a id="_additional_resources"></a>

## 延伸阅读

- [MCP 注解](https://docs.spring.io/spring-ai/reference/api/mcp/mcp-annotations-overview.html)
- [MCP Client Boot Starter](https://docs.spring.io/spring-ai/reference/api/mcp/mcp-client-boot-starter-docs.html)
- [MCP Server Boot Starter](https://docs.spring.io/spring-ai/reference/api/mcp/mcp-server-boot-starter-docs.html)
- [MCP 工具类](https://docs.spring.io/spring-ai/reference/api/mcp/mcp-helpers.html)
- [MCP 协议规范](https://modelcontextprotocol.github.io/specification/)
