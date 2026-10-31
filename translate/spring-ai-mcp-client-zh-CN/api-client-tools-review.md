# Client 工具相关源码审校

日期：2026-10-31。静态读取主 agent 采集到 `../spring-ai-mcp-overview-zh-CN/api/` 的同版本源码。以下行号均对应该目录的文件；未编译运行 Java，未调用 MCP 服务。

## 1. McpClientCustomizer 名称与调用契约

- `McpClientCustomizer.java:17,36,46`：真实类型为 `org.springframework.ai.mcp.customizer.McpClientCustomizer<B>`，方法为 `void customize(String name, B componentBuilder)`。正文使用 `McpCustomizer<...>` 是旧称或笔误，连源码 Javadoc 26-28 行也残留该旧称，不能据注释把接口名改回去。
- `McpClientAutoConfiguration.java:226-228,300-302`：分别收集 `McpClientCustomizer<McpClient.SyncSpec>` 与 `McpClientCustomizer<McpClient.AsyncSpec>`，使用 `orderedStream()`。
- `McpSyncClientConfigurer.java:56-58,70-74`：在原 spec 上按顺序逐个执行定制器；定制器本身返回 void。
- `McpClientAutoConfiguration.java:276-278`：ASYNC 也先按 named transport 名称定制，再 build 客户端。`serverConfigurationName` 指连接配置名称。
- `McpClientAutoConfiguration.java:113-114`：clientInfo.name 实际组装为 `clientName + " - " + serverConnectionName`。过滤器里比较 `connectionInfo.clientInfo().name().equals("restricted-client")` 只是概念示例，未必匹配自动配置实际名称。

建议：正文全部使用 `McpClientCustomizer`；示例保留 `serverConfigurationName`，解释为连接配置名。

## 2. 默认前缀生成器：初始化路径正确，但来源保证过强

### 默认 Bean 与 noPrefix

- `McpToolCallbackAutoConfiguration.java:50-53`：缺少同类型 Bean 时注册 `DefaultMcpToolNamePrefixGenerator`，所以正常 Starter 默认行为确实使用该生成器。
- 同文件 `71-85,90-101`：同步和异步 Provider 均通过 `ObjectProvider.getIfUnique(...)` 获取生成器和 Meta Converter。源码中的 `noPrefix()` 是无法获得唯一生成器时的兜底，不能因此认定正常自动配置默认关闭前缀。
- `McpToolNamePrefixGenerator.java:47-48`：`noPrefix()` 原样返回 `tool.name()`。
- `SyncMcpToolCallbackProvider.java:182-186`：重复名称检查会抛 `IllegalStateException`；异步 Provider 也有对应检查。

### format 不是“所有非字母数字替换成下划线”

- `DefaultMcpToolNamePrefixGenerator.java:64`：首先调用 `McpToolUtils.format(tool.name())`。
- `McpToolUtils.java:117-124`：保留汉字、ASCII 字母数字、下划线与连字符；其他字符直接删除，之后仅将连字符替换为下划线。

建议正文：默认先规范化名称（例如连字符变下划线），发现不同连接工具重名时添加 `alt_` 加计数前缀。不要说所有特殊字符都会变成 `_`。

### 64 字符裁剪不在当前默认生成器路径

- `DefaultMcpToolNamePrefixGenerator.java:62-79`：只 format、集合去重、加计数前缀并返回，没有长度检测。
- `McpToolUtils.java:92-110`：另一方法 `prefixedToolName(prefix, title, toolName)` 中才有长度 >64 时保留最后 64 字符的逻辑（105-108 行）。默认生成器没有调用这个方法。
- `SyncMcpToolCallback.java:69-70` 的旧构造器会调用该工具方法，但 Provider 当前 Builder 路径先通过生成器得到名称（`SyncMcpToolCallbackProvider.java:136-142`），不能用旧构造器的限长实现证明默认生成器限长。

建议删去“默认生成器保证最终名称不超过 64 字符”的强保证；可在自定义生成器说明需要按目标模型限制处理合法字符和长度。

### 幂等保证与源码实现不一致

- `DefaultMcpToolNamePrefixGenerator.java:55-59`：只有已见连接集合、所有已用名称集合和计数器，没有 ConnectionId→生成名称映射。
- `62-79`：每次调用都以 format 后原名称初始化；只有 `existingConnections.add(...)` 为 true 时才进入重名处理。若某连接第一次因冲突返回 `alt_1_search`，第二次同一 ConnectionId 的 add 为 false，就直接返回 `search`，不再返回原先分配的前缀名。
- `ConnectionId` 使用 clientInfo、serverInfo、完整 Tool record（82 行），不等同稳定的独立物理连接标识。
- Provider 平常缓存回调（同步 `125-154`），可减少重复生成；工具列表事件清缓存后（`160-166`）会重新发现并生成，不足以证明所有路径均幂等。

建议正文避免承诺“相同连接始终得到同一个唯一名称”；将它写为默认实现用于缓解 MCP 工具重名。这里是静态控制流推导，不声称已经运行复现。

## 3. ToolContextToMcpMetaConverter 契约

- `ToolContextToMcpMetaConverter.java:44`：方法 `Map<String,Object> convert(ToolContext toolContext)`。
- `46-58`：`defaultConverter()` 对 null 上下文、空 Map 返回空 Map；过滤键 `McpToolUtils.TOOL_CONTEXT_MCP_EXCHANGE_KEY` 及 null 值；其余条目原样收集。
- `McpToolUtils.java:80`：exchange 键的实际字符串是 `"exchange"`。
- `ToolContextToMcpMetaConverter.java:66-67`：`noOp()` 返回空 Map。
- `SyncMcpToolCallback.java:127-130` 与 `AsyncMcpToolCallback.java:126-129`：把转换结果传给 `CallToolRequest.builder(...).meta(mcpMeta)`。这正是 MCP `_meta`，与模型生成的 `arguments` 分开。
- 回调使用原始远程工具名请求服务端，不将模型侧加过前缀的工具名发送过去（同步 129-134、异步 128-129）。

来源自定义 Converter 示例只过滤 null 并给键加 `app_` 前缀，完全替换了默认转换，并没有继承 exchange 键排除规则。若上下文中真的存在内部 exchange 对象，可能把它也加入元数据。建议保留示例并明确自定义实现负责过滤，或改用 `defaultConverter().convert(toolContext)` 的结果再处理，以保留默认排除规则。

`progressToken` 的示例仅展示传递上下文，没有给 ChatClient 注册 MCP 工具，不构成独立可运行的完整调用示例。

## 4. ProgressNotification 不保证 0..1

- `McpSchema.java:5222-5226`：`progress` 是当前进度值；`total` 是可选的总工作量，已知时才提供；`message` 可选。
- record 字段为 `Double progress`、`Double total`（5235-5240）；构造器要求 progress 和 progressToken 非 null（5242-5244）。
- 反序列化兼容旧数据时可能把缺失 progress 替换为 0.0（5247-5264）；这不改变 total 可缺失的契约。
- Builder 仅保存传入 progress，不会转换为百分数，total 独立可选（5272-5296）。

来源 `double percentage = notification.progress() * 100` 不成立。可用写法：

```java
Double total = notification.total();
if (total != null && total > 0) {
    double percentage = notification.progress() / total * 100;
    System.out.printf("Progress: %.2f%% - %s%n", percentage, notification.message());
} else {
    System.out.printf("Progress: %s - %s%n", notification.progress(), notification.message());
}
```

该示例只按已知 total 计算百分比；未知 total 时显示原始进度。不要额外断言 progress 一定小于 total，也无需声称 API 强制归一化。

## 5. 补充：ElicitResult 示例构造器仍有效

- `McpSchema.java:4751-4757`：`ElicitRequest` 提供 `message()`、`meta()`、`mode()`。
- `McpSchema.java:5055-5058`：`ElicitResult` 主 record 有 action/content/meta 三字段。
- `5085-5087`：保留双参数兼容构造器 `ElicitResult(Action, Map<String,Object>)`，会把 meta 设为 null；来源示例 `new ElicitResult(ElicitResult.Action.ACCEPT, Map.of(...))` 可以保留。

但原示例只是定制器片段，`roots`、采样实现、完整业务逻辑等仍需应用补齐，不能宣称整类可直接运行。
