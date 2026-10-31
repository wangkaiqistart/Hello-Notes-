# MCP Client Boot Starter

The Spring AI MCP (Model Context Protocol) Client Boot Starter provides auto-configuration for MCP client functionality in Spring Boot applications.
It supports both synchronous and asynchronous client implementations with various transport options.

The MCP Client Boot Starter provides:

* Management of multiple client instances
* Automatic client initialization (if enabled)
* Support for multiple named transports (STDIO, Http/SSE and Streamable HTTP)
* Integration with Spring AI’s tool execution framework
* Tool filtering capabilities for selective tool inclusion/exclusion
* Customizable tool name prefix generation for avoiding naming conflicts
* Proper lifecycle management with automatic cleanup of resources when the application context is closed
* Customizable client creation through customizers

<a id="_starters"></a>

## Starters

<a id="_standard_mcp_client"></a>

### Standard MCP Client

```xml
<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>spring-ai-starter-mcp-client</artifactId>
</dependency>
```

The standard starter connects simultaneously to one or more MCP servers over `STDIO` (in-process), `SSE`, `Streamable-HTTP` and `Stateless Streamable-HTTP` transports.
The SSE and Streamable-Http transports use the JDK HttpClient-based transport implementation.
Each connection to an MCP server creates a new MCP client instance.
You can choose either `SYNC` or `ASYNC` MCP clients (note: you cannot mix sync and async clients).
For production deployment, we recommend using the WebFlux-based SSE & StreamableHttp connection with the `spring-ai-starter-mcp-client-webflux`.

<a id="_webflux_client"></a>

### WebFlux Client

The WebFlux starter provides similar functionality to the standard starter but uses a WebFlux-based Streamable-Http, Stateless Streamable-Http and SSE transport implementation.

```xml
<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>spring-ai-starter-mcp-client-webflux</artifactId>
</dependency>
```

<a id="_configuration_properties"></a>

## Configuration Properties

<a id="_common_properties"></a>

### Common Properties

The common properties are prefixed with `spring.ai.mcp.client`:

| Property | Description | Default Value |
| --- | --- | --- |
| `enabled` | Enable/disable the MCP client | `true` |
| `name` | Name of the MCP client instance | `spring-ai-mcp-client` |
| `version` | Version of the MCP client instance | `1.0.0` |
| `initialized` | Whether to initialize clients on creation | `true` |
| `request-timeout` | Timeout duration for MCP client requests | `20s` |
| `type` | Client type (SYNC or ASYNC). All clients must be either sync or async; mixing is not supported | `SYNC` |
| `root-change-notification` | Enable/disable root change notifications for all clients | `true` |
| `toolcallback.enabled` | Enable/disable the MCP tool callback integration with Spring AI’s tool execution framework | `true` |

<a id="_mcp_annotations_properties"></a>

### MCP Annotations Properties

MCP Client Annotations provide a declarative way to implement MCP client handlers using Java annotations.
The client mcp-annotations properties are prefixed with `spring.ai.mcp.client.annotation-scanner`:

| Property | Description | Default Value |
| --- | --- | --- |
| `enabled` | Enable/disable the MCP client annotations auto-scanning | `true` |

<a id="_stdio_transport_properties"></a>

### Stdio Transport Properties

Properties for Standard I/O transport are prefixed with `spring.ai.mcp.client.stdio`:

| Property | Description | Default Value |
| --- | --- | --- |
| `servers-configuration` | Resource containing the MCP servers configuration in JSON format | - |
| `connections` | Map of named stdio connection configurations | - |
| `connections.[name].command` | The command to execute for the MCP server | - |
| `connections.[name].args` | List of command arguments | - |
| `connections.[name].env` | Map of environment variables for the server process | - |

Example configuration:

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

Alternatively, you can configure stdio connections using an external JSON file using the [Claude Desktop format](https://modelcontextprotocol.io/quickstart/user):

```yaml
spring:
  ai:
    mcp:
      client:
        stdio:
          servers-configuration: classpath:mcp-servers.json
```

The Claude Desktop format looks like this:

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

### Windows STDIO Configuration

::: important
On Windows, commands like `npx`, `npm`, and `node` are implemented as **batch files** (`.cmd`), not native executables. Java’s `ProcessBuilder` cannot execute batch files directly and requires the `cmd.exe /c` wrapper.
:::

<a id="_why_windows_needs_special_handling"></a>

#### Why Windows Needs Special Handling

When Java’s `ProcessBuilder` (used internally by `StdioClientTransport`) attempts to spawn a process on Windows, it can only execute:

* Native executables (`.exe` files)
* System commands available to `cmd.exe`

Windows batch files like `npx.cmd`, `npm.cmd`, and even `python.cmd` (from the Microsoft Store) require the `cmd.exe` shell to execute them.

<a id="_solution_cmd_exe_wrapper"></a>

#### Solution: cmd.exe Wrapper

Wrap batch file commands with `cmd.exe /c`:

**Windows Configuration:**

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

**Linux/macOS Configuration:**

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

#### Cross-Platform Programmatic Configuration

For applications that need to work across platforms without separate configuration files, use OS detection in your Spring Boot application:

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
```::: note
When using programmatic configuration with `@Bean`, add `@ConditionalOnMissingBean(McpSyncClient.class)` to avoid conflicts with auto-configuration from JSON files.
:::

<a id="_path_considerations"></a>

#### Path Considerations

**Relative paths** (recommended for portability):

```json
{
  "command": "cmd.exe",
  "args": ["/c", "npx", "-y", "@modelcontextprotocol/server-filesystem", "target"]
}
```

The MCP server resolves relative paths based on the application’s working directory.

**Absolute paths** (Windows requires backslashes or escaped forward slashes):

```json
{
  "command": "cmd.exe",
  "args": ["/c", "npx", "-y", "@modelcontextprotocol/server-filesystem", "C:\\Users\\username\\project\\target"]
}
```

<a id="_common_windows_batch_files_requiring_cmd_exe"></a>

#### Common Windows Batch Files Requiring cmd.exe

* `npx.cmd`, `npm.cmd` - Node package managers
* `python.cmd` - Python (Microsoft Store installation)
* `pip.cmd` - Python package manager
* `mvn.cmd` - Maven wrapper
* `gradle.cmd` - Gradle wrapper
* Custom `.cmd` or `.bat` scripts

<a id="_reference_implementation"></a>

#### Reference Implementation

See [Spring AI Examples - Filesystem](https://github.com/spring-projects/spring-ai-examples/tree/main/model-context-protocol/filesystem) for a complete cross-platform MCP client implementation that automatically detects the OS and configures the client appropriately.

<a id="_streamable_http_transport_properties"></a>

### Streamable-HTTP Transport Properties

Used for connecting to Streamable-HTTP and Stateless Streamable-HTTP MCP servers.

Properties for Streamable-HTTP transport are prefixed with `spring.ai.mcp.client.streamable-http`:

| Property | Description | Default Value |
| --- | --- | --- |
| `connections` | Map of named Streamable-HTTP connection configurations | - |
| `connections.[name].url` | Base URL endpoint for Streamable-Http communication with the MCP server | - |
| `connections.[name].endpoint` | the streamable-http endpoint (as url suffix) to use for the connection | `/mcp` |

Example configuration:

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

### SSE Transport Properties

Properties for Server-Sent Events (SSE) transport are prefixed with `spring.ai.mcp.client.sse`:

| Property | Description | Default Value |
| --- | --- | --- |
| `connections` | Map of named SSE connection configurations | - |
| `connections.[name].url` | Base URL endpoint for SSE communication with the MCP server | - |
| `connections.[name].sse-endpoint` | the sse endpoint (as url suffix) to use for the connection | `/sse` |

Example configurations:

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

#### URL Splitting Guidelines

When you have a full SSE URL, split it into base URL and endpoint path:

| Full URL | Configuration |
| --- | --- |
| `http://localhost:3000/mcp-hub/sse/token123` | `url: localhost:3000`  `sse-endpoint: /mcp-hub/sse/token123` |
| `https://api.service.com/v2/events?key=secret` | `url: api.service.com`  `sse-endpoint: /v2/events?key=secret` |
| `http://localhost:8080/sse` | `url: localhost:8080`  `sse-endpoint: /sse` (or omit for default) |

<a id="_troubleshooting_sse_connections"></a>

#### Troubleshooting SSE Connections

**404 Not Found Errors:**

* Verify URL splitting: ensure the base `url` contains only the scheme, host, and port
* Check the `sse-endpoint` starts with `/` and includes the full path and query parameters
* Test the full URL directly in a browser or curl to confirm it’s accessible

<a id="_streamable_http_transport_properties_2"></a>

### Streamable Http Transport Properties

Properties for Streamable Http transport are prefixed with `spring.ai.mcp.client.streamable-http`:

| Property | Description | Default Value |
| --- | --- | --- |
| `connections` | Map of named Streamable Http connection configurations | - |
| `connections.[name].url` | Base URL endpoint for Streamable-Http communication with the MCP server | - |
| `connections.[name].endpoint` | the streamable-http endpoint (as url suffix) to use for the connection | `/mcp` |

Example configuration:

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

## Features

<a id="_syncasync_client_types"></a>

### Sync/Async Client Types

The starter supports two types of clients:

* Synchronous - default client type (`spring.ai.mcp.client.type=SYNC`), suitable for traditional request-response patterns with blocking operations

**NOTE:** The SYNC client will register only synchronous MCP annotated methods. Asynchronous methods will be ignored.

* Asynchronous - suitable for reactive applications with non-blocking operations, configured using `spring.ai.mcp.client.type=ASYNC`

**NOTE:** The ASYNC client will register only asynchronous MCP annotated methods. Synchronous methods will be ignored.

<a id="client-scope-and-session-boundaries"></a>

### Client Scope and Session Boundaries

The auto-configured `McpSyncClient` and `McpAsyncClient` beans are application-scoped singletons.
One client bean is created per configured MCP server connection, and that bean is shared by every request the application serves.

Each client represents a single MCP protocol session.
The session stays attached to the client bean for its whole lifetime and is replaced only when the server terminates it (HTTP 404) or the client is closed.

::: warning
**The MCP session is not a per-user boundary.**
Per-request credentials propagated through `transportContextProvider(…​)`, a `McpSyncHttpClientRequestCustomizer`, or a `WebClient` `ExchangeFilterFunction` are applied per request and do reach the server with the calling user’s identity.
The MCP protocol session underneath them is still shared by every caller of that client bean.
Multi-user applications should account for the following:

* The `initialize` and `tools/list` exchanges happen once, under whatever identity is available when the client connects, not under the identity of the user who later invokes a tool.
* Any server-side state keyed on the MCP session alone is shared by all users of the client bean.
* Server-initiated interactions such as sampling and elicitation arrive on a shared stream and carry no per-user attribution.
Do not treat the MCP session as a user or tenant boundary on either side of the connection.
:::

Whether this matters depends on the MCP server you connect to.
A shared client is fine against a stateless server, and against a stateful one that authorizes every request from the supplied token and keeps no user-meaningful state on the session.
Consider a separate session per user or per tenant when:

* The server filters `tools/list`, resources, or prompts by identity, since discovery runs once and every user then sees the first caller’s view.
* The server keeps user-meaningful state on the session, such as a working directory, subscriptions, pagination cursors, or cached context.
* You use sampling or elicitation and need those server-initiated requests attributed to a specific user.
* The server audits or rate-limits by session, or your deployment requires that tenants not share a protocol session.
* You cannot verify how a third-party server treats its sessions.

Applications that need a separate MCP protocol session per user or per tenant must manage that lifecycle themselves, creating one transport and client per principal and closing it when that principal’s work completes.
The auto-configured beans are not suitable for this, and Spring AI does not provide per-user client pooling.
See [Working Around Spring AI Autoconfiguration](https://docs.spring.io/spring-ai/reference/api/mcp/mcp-security.html#_working_around_spring_ai_autoconfiguration) for programmatic client construction.

<a id="_client_customization"></a>

### Client Customization

The auto-configuration provides extensive client spec customization capabilities through callback interfaces. These customizers allow you to configure various aspects of the MCP client behavior, from request timeouts to event handling and message processing.

<a id="_customization_types"></a>

#### Customization Types

The following customization options are available:

* **Request Configuration** - Set custom request timeouts
* [**Custom Sampling Handlers**](https://modelcontextprotocol.io/specification/2025-06-18/client/sampling) - standardized way for servers to request LLM sampling (`completions` or `generations`) from LLMs via clients. This flow allows clients to maintain control over model access, selection, and permissions while enabling servers to leverage AI capabilities — with no server API keys necessary.
* [**File system (Roots) Access**](https://modelcontextprotocol.io/specification/2025-06-18/client/roots) - standardized way for clients to expose filesystem `roots` to servers.
  Roots define the boundaries of where servers can operate within the filesystem, allowing them to understand which directories and files they have access to.
  Servers can request the list of roots from supporting clients and receive notifications when that list changes.
* [**Elicitation Handlers**](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation) - standardized way for servers to request additional information from users through the client during interactions.
* **Event Handlers** - client’s handler to be notified when a certain server event occurs:

  + Tools change notifications - when the list of available server tools changes
  + Resources change notifications - when the list of available server resources changes.
  + Prompts change notifications - when the list of available server prompts changes.
  + [**Logging Handlers**](https://modelcontextprotocol.io/specification/2025-06-18/server/utilities/logging) - standardized way for servers to send structured log messages to clients.
  + [**Progress Handlers**](https://modelcontextprotocol.io/specification/2025-06-18/basic/utilities/progress) - standardized way for servers to send structured progress messages to clients.

Clients can control logging verbosity by setting minimum log levels

<a id="_client_customization_example"></a>