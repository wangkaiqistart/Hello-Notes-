#### Client Customization Example

You can implement `McpCustomizer<McpClient.SyncSpec>` for synchronous clients or `McpCustomizer<McpClient.AsyncSpec>` for asynchronous clients, depending on your application’s needs.

* Sync
* Async

```java
@Component
public class CustomMcpSyncClientCustomizer implements McpClientCustomizer<McpClient.SyncSpec> {
    @Override
    public void customize(String serverConfigurationName, McpClient.SyncSpec spec) {

        // Customize the request timeout configuration
        spec.requestTimeout(Duration.ofSeconds(30));

        // Sets the root URIs that this client can access.
        spec.roots(roots);

        // Sets a custom sampling handler for processing message creation requests.
        spec.sampling((CreateMessageRequest messageRequest) -> {
            // Handle sampling
            CreateMessageResult result = ...
            return result;
        });

        // Sets a custom elicitation handler for processing elicitation requests.
        spec.elicitation((ElicitRequest request) -> {
          // handle elicitation
          return new ElicitResult(ElicitResult.Action.ACCEPT, Map.of("message", request.message()));
        });

        // Adds a consumer to be notified when progress notifications are received.
        spec.progressConsumer((ProgressNotification progress) -> {
         // Handle progress notifications
        });

        // Adds a consumer to be notified when the available tools change, such as tools
        // being added or removed.
        spec.toolsChangeConsumer((List<McpSchema.Tool> tools) -> {
            // Handle tools change
        });

        // Adds a consumer to be notified when the available resources change, such as resources
        // being added or removed.
        spec.resourcesChangeConsumer((List<McpSchema.Resource> resources) -> {
            // Handle resources change
        });

        // Adds a consumer to be notified when the available prompts change, such as prompts
        // being added or removed.
        spec.promptsChangeConsumer((List<McpSchema.Prompt> prompts) -> {
            // Handle prompts change
        });

        // Adds a consumer to be notified when logging messages are received from the server.
        spec.loggingConsumer((McpSchema.LoggingMessageNotification log) -> {
            // Handle log messages
        });
    }
}
``````java
@Component
public class CustomMcpAsyncClientCustomizer implements McpClientCustomizer<McpClient.AsyncSpec> {
    @Override
    public void customize(String serverConfigurationName, McpClient.AsyncSpec spec) {
        // Customize the async client configuration
        spec.requestTimeout(Duration.ofSeconds(30));
    }
}
```

The `serverConfigurationName` parameter is the name of the server configuration that the customizer is being applied to and the MCP Client is created for.

The MCP client auto-configuration automatically detects and applies any customizers found in the application context.

<a id="_transport_support"></a>

### Transport Support

The auto-configuration supports multiple transport types:

* Standard I/O (Stdio) (activated by the `spring-ai-starter-mcp-client` and `spring-ai-starter-mcp-client-webflux`)
* (HttpClient) HTTP/SSE and Streamable-HTTP (activated by the `spring-ai-starter-mcp-client`)
* (WebFlux) HTTP/SSE and Streamable-HTTP (activated by the `spring-ai-starter-mcp-client-webflux`)

<a id="_tool_filtering"></a>

### Tool Filtering

The MCP Client Boot Starter supports filtering of discovered tools through the `McpToolFilter` interface. This allows you to selectively include or exclude tools based on custom criteria such as the MCP connection information or tool properties.

To implement tool filtering, create a bean that implements the `McpToolFilter` interface:

```java
@Component
public class CustomMcpToolFilter implements McpToolFilter {

    @Override
    public boolean test(McpConnectionInfo connectionInfo, McpSchema.Tool tool) {
        // Filter logic based on connection information and tool properties
        // Return true to include the tool, false to exclude it

        // Example: Exclude tools from a specific client
        if (connectionInfo.clientInfo().name().equals("restricted-client")) {
            return false;
        }

        // Example: Only include tools with specific names
        if (tool.name().startsWith("allowed_")) {
            return true;
        }

        // Example: Filter based on tool description or other properties
        if (tool.description() != null &&
            tool.description().contains("experimental")) {
            return false;
        }

        return true; // Include all other tools by default
    }
}
```

The `McpConnectionInfo` record provides access to:

* `clientCapabilities` - The capabilities of the MCP client
* `clientInfo` - Information about the MCP client (name and version)
* `initializeResult` - The initialization result from the MCP server

The filter is automatically detected and applied to both synchronous and asynchronous MCP tool callback providers.
If no custom filter is provided, all discovered tools are included by default.

Note: Only one `McpToolFilter` bean should be defined in the application context.
If multiple filters are needed, combine them into a single composite filter implementation.

<a id="mcp-tool-name-prefix-generation"></a>

### Tool Name Prefix Generation

The MCP Client Boot Starter supports customizable tool name prefix generation through the `McpToolNamePrefixGenerator` interface. This feature helps avoid naming conflicts when integrating tools from multiple MCP servers by adding unique prefixes to tool names.

By default, if no custom `McpToolNamePrefixGenerator` bean is provided, the starter uses `DefaultMcpToolNamePrefixGenerator` which ensures unique tool names across all MCP client connections. The default generator:

* Tracks all existing connections and tool names to ensure uniqueness
* Formats tool names by replacing non-alphanumeric characters with underscores (e.g., `my-tool` becomes `my_tool`)
* When duplicate tool names are detected across different connections, adds a counter prefix (e.g., `alt_1_toolName`, `alt_2_toolName`)
* Is thread-safe and maintains idempotency - the same combination of (client, server, tool) always gets the same unique name
* Ensures the final name doesn’t exceed 64 characters (truncating from the beginning if necessary)

For example:

* First occurrence of tool `search` → `search`
* Second occurrence of tool `search` from a different connection → `alt_1_search`
* Tool with special characters `my-special-tool` → `my_special_tool`

You can customize this behavior by providing your own implementation:

```java
@Component
public class CustomToolNamePrefixGenerator implements McpToolNamePrefixGenerator {

    @Override
    public String prefixedToolName(McpConnectionInfo connectionInfo, Tool tool) {
        // Custom logic to generate prefixed tool names

        // Example: Use server name and version as prefix
        String serverName = connectionInfo.initializeResult().serverInfo().name();
        String serverVersion = connectionInfo.initializeResult().serverInfo().version();
        return serverName + "_v" + serverVersion.replace(".", "_") + "_" + tool.name();
    }
}
```

The `McpConnectionInfo` record provides comprehensive information about the MCP connection:

* `clientCapabilities` - The capabilities of the MCP client
* `clientInfo` - Information about the MCP client (name, title, and version)
* `initializeResult` - The initialization result from the MCP server, including server information

<a id="_built_in_prefix_generators"></a>

#### Built-in Prefix Generators

The framework provides several built-in prefix generators:

* `DefaultMcpToolNamePrefixGenerator` - Ensures unique tool names by tracking duplicates and adding counter prefixes when needed (used by default if no custom bean is provided)
* `McpToolNamePrefixGenerator.noPrefix()` - Returns tool names without any prefix (may cause conflicts if multiple servers provide tools with the same name)

To disable prefixing entirely and use raw tool names (not recommended if using multiple MCP servers), register the no-prefix generator as a bean:

```java
@Configuration
public class McpConfiguration {

    @Bean
    public McpToolNamePrefixGenerator mcpToolNamePrefixGenerator() {
        return McpToolNamePrefixGenerator.noPrefix();
    }
}
```

The prefix generator is automatically detected and applied to both synchronous and asynchronous MCP tool callback providers through Spring’s `ObjectProvider` mechanism.
If no custom generator bean is provided, the `DefaultMcpToolNamePrefixGenerator` is used automatically.

::: warning
When using `McpToolNamePrefixGenerator.noPrefix()` with multiple MCP servers, duplicate tool names will cause an `IllegalStateException`. The default `DefaultMcpToolNamePrefixGenerator` prevents this by automatically adding unique prefixes to duplicate tool names.
:::
::: note
This generator only de-duplicates names across MCP connections; it has no visibility into local `@Tool` methods.
See [Combining Local and MCP Tools](https://docs.spring.io/spring-ai/reference/api/tools.html#combining-local-and-mcp-tools) for the local/remote collision case and which call paths actually guard against it.
:::

<a id="_tool_context_to_mcp_meta_converter"></a>

### Tool Context to MCP Meta Converter

The MCP Client Boot Starter supports customizable conversion of Spring AI’s [ToolContext](https://docs.spring.io/spring-ai/reference/api/tools.html#tool-context) to MCP tool-call metadata through the `ToolContextToMcpMetaConverter` interface.
This feature allows you to pass additional contextual information (e.g. user id, secrets token) as metadata along with the LLM’s generated call arguments.

For example you can pass the MCP `progressToken` to your [MCP Progress Flow](https://modelcontextprotocol.io/specification/2025-06-18/basic/utilities/progress#progress-flow) in the tool context to track the progress of long-running operations:

```java
ChatModel chatModel = ...

String response = ChatClient.create(chatModel)
        .prompt("Tell me more about the customer with ID 42")
        .toolContext(Map.of("progressToken", "my-progress-token"))
        .call()
        .content();
```

By default, if no custom converter bean is provided, the starter uses `ToolContextToMcpMetaConverter.defaultConverter()` which:

* Filters out the MCP exchange key (`McpToolUtils.TOOL_CONTEXT_MCP_EXCHANGE_KEY`)
* Filters out entries with null values
* Passes through all other context entries as metadata

You can customize this behavior by providing your own implementation:

```java
@Component
public class CustomToolContextToMcpMetaConverter implements ToolContextToMcpMetaConverter {

    @Override
    public Map<String, Object> convert(ToolContext toolContext) {
        if (toolContext == null || toolContext.getContext() == null) {
            return Map.of();
        }

        // Custom logic to convert tool context to MCP metadata
        Map<String, Object> metadata = new HashMap<>();

        // Example: Add custom prefix to all keys
        for (Map.Entry<String, Object> entry : toolContext.getContext().entrySet()) {
            if (entry.getValue() != null) {
                metadata.put("app_" + entry.getKey(), entry.getValue());
            }
        }

        // Example: Add additional metadata
        metadata.put("timestamp", System.currentTimeMillis());
        metadata.put("source", "spring-ai");

        return metadata;
    }
}
```

<a id="_built_in_converters"></a>

#### Built-in Converters

The framework provides built-in converters:

* `ToolContextToMcpMetaConverter.defaultConverter()` - Filters out MCP exchange key and null values (used by default if no custom bean is provided)
* `ToolContextToMcpMetaConverter.noOp()` - Returns an empty map, effectively disabling context-to-metadata conversion

To disable context-to-metadata conversion entirely:

```java
@Configuration
public class McpConfiguration {

    @Bean
    public ToolContextToMcpMetaConverter toolContextToMcpMetaConverter() {
        return ToolContextToMcpMetaConverter.noOp();
    }
}
```

The converter is automatically detected and applied to both synchronous and asynchronous MCP tool callbacks through Spring’s `ObjectProvider` mechanism.
If no custom converter bean is provided, the default converter is used automatically.

<a id="_disable_the_mcp_toolcallback_auto_configuration"></a>

### Disable the MCP ToolCallback Auto-Configuration

The MCP ToolCallback auto-configuration is enabled by default, but can be disabled with the `spring.ai.mcp.client.toolcallback.enabled=false` property.

When disabled, no `ToolCallbackProvider` bean is created from the available MCP tools.

<a id="_mcp_client_annotations"></a>

## MCP Client Annotations

The MCP Client Boot Starter automatically detects and registers annotated methods for handling various MCP client operations:

* **@McpLogging** - Handles logging message notifications from MCP servers
* **@McpSampling** - Handles sampling requests from MCP servers for LLM completions
* **@McpElicitation** - Handles elicitation requests to gather additional information from users
* **@McpProgress** - Handles progress notifications for long-running operations
* **@McpToolListChanged** - Handles notifications when the server’s tool list changes
* **@McpResourceListChanged** - Handles notifications when the server’s resource list changes
* **@McpPromptListChanged** - Handles notifications when the server’s prompt list changes

Example usage:

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
        // Process the request and generate a response
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
        // Update local tool registry
        toolRegistry.updateTools(updatedTools);
    }
}
```

The annotations support both synchronous and asynchronous implementations, and can be configured for specific clients using the `clients` parameter:

```java
@McpLogging(clients = "server1")
public void handleServer1Logs(LoggingMessageNotification notification) {
    // Handle logs from specific server
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

For detailed information about all available annotations and their usage patterns, see the [MCP Client Annotations](https://docs.spring.io/spring-ai/reference/api/mcp/mcp-annotations-client.html) documentation.

<a id="_usage_example"></a>

## Usage Example

Add the appropriate starter dependency to your project and configure the client in `application.properties` or `application.yml`:

```yaml
spring:
  ai:
    mcp:
      client:
        enabled: true
        name: my-mcp-client
        version: 1.0.0
        request-timeout: 30s
        type: SYNC  # or ASYNC for reactive applications
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

The MCP client beans will be automatically configured and available for injection:

```java
@Autowired
private List<McpSyncClient> mcpSyncClients;  // For sync client

// OR

@Autowired
private List<McpAsyncClient> mcpAsyncClients;  // For async client
```

When tool callbacks are enabled (the default behavior), the registered MCP Tools with all MCP clients are provided as a `ToolCallbackProvider` instance:

```java
@Autowired
private SyncMcpToolCallbackProvider toolCallbackProvider;
ToolCallback[] toolCallbacks = toolCallbackProvider.getToolCallbacks();
```

<a id="_example_applications"></a>

## Example Applications

* [Brave Web Search Chatbot](https://github.com/spring-projects/spring-ai-examples/tree/main/model-context-protocol/web-search/brave-chatbot) - A chatbot that uses the Model Context Protocol to interact with a web search server.
* [Default MCP Client Starter](https://github.com/spring-projects/spring-ai-examples/tree/main/model-context-protocol/client-starter/starter-default-client) - A simple example of using the default `spring-ai-starter-mcp-client` MCP Client Boot Starter.
* [WebFlux MCP Client Starter](https://github.com/spring-projects/spring-ai-examples/tree/main/model-context-protocol/client-starter/starter-webflux-client) - A simple example of using the `spring-ai-starter-mcp-client-webflux` MCP Client Boot Starter.

<a id="_additional_resources"></a>

## Additional Resources

* [Spring AI Documentation](https://docs.spring.io/spring-ai/reference/)
* [Model Context Protocol Specification](https://modelcontextprotocol.github.io/specification/)
* [Spring Boot Auto-configuration](https://docs.spring.io/spring-boot/docs/current/reference/html/features.html#features.developing-auto-configuration)