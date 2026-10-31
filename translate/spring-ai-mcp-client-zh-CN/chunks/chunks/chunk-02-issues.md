# Client 第 2 块初稿问题

- 原文 `McpCustomizer<...>` 与紧随代码的 `McpClientCustomizer<...>` 不一致。初稿正文按代码使用 McpClientCustomizer，主 agent 应对照 2.0.2 API 确认。
- 抽取结果把两段代码围栏连成了六个反引号，初稿已拆开；两段代码全部保留。
- `CreateMessageResult result = ...` 是未完成片段，无分号；保留代码，正文应明确示例省略业务代码。
- 自定义工具过滤器的 `allowed_` 命中后直接返回 true，非 allowed_ 仍可能默认包含；原注释“Only include tools with specific names”不符合实际分支。初稿注释只写“包含指定名称前缀”，主 agent 可补说明这不是白名单。
- 默认前缀生成器“非字母数字都替换”为简化描述，可能保留下划线、只许 ASCII；需按源码核实。自定义命名示例没有统一字符规范和长度保护，也没有保证各连接唯一。
- `ToolContext` → `_meta` 示例没有向 ChatClient 注册任何工具，仅展示上下文传递；不构成可以完整执行的示例。
- 自定义 Meta Converter 代码只过滤 null，没有默认的 exchange 键过滤；主 agent 应说明完全替换默认逻辑，可能不能直接序列化内部对象。
- 进度示例 `notification.progress() * 100` 假定进度为 0..1；MCP progress 一般表示完成工作量，可能需要 `progress / total * 100`，且 total 可缺省；主 agent 需核对源码并修正。
- 综合 YAML 示例将 `root-change-notification` 放在 `stdio` 下，与前文通用属性表的 `spring.ai.mcp.client.root-change-notification` 不一致，可能配置无效；需核对源码。
- `SyncMcpToolCallbackProvider` 示例把实例字段与可执行语句写在一起，应明确在依赖注入后使用，不可原样拼成字段初始化器。
- `@McpLogging` 与返回 Mono 的 `@McpSampling` 混在一段，ASYNC 扫描可能忽略同步 logging 方法；正文已有同步异步扫描约束，主 agent可简要提醒此段是两种独立方法写法。
- `clients = "server1"` 应指连接配置名而非 McpClient.clientInfo.name；初稿用“哪条连接”避免误解。

本初稿 13 段代码，所有来源代码内容除中文注释外保持。
