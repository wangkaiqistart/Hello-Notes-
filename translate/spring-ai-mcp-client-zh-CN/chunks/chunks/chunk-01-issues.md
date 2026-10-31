# Client 第 1 块审校线索

本块包含 13 段代码，初稿逐字保留来源代码（仅修复抽取时围栏与 `:::note` 黏连）；保留所有章节锚点、属性与链接。

## 需要源码核验

1. **STDIO 配置位置**：第 3 段 YAML 把 `root-change-notification` 放在 `client.stdio` 下，但通用属性表明确该属性位于 `spring.ai.mcp.client`。综合示例也有此问题，建议统一移到 `client` 层。
2. **跨平台 `mcpClient()` 返回值**：第 8 段方法返回 `McpSyncClient`，却链式 `.build().initialize()`。SDK 的 `initialize()` 很可能返回 `InitializeResult` 而非客户端；建议构建后单独初始化并返回客户端，需结合 1.0.x SDK 源码核验。
3. **`@ConditionalOnMissingBean(McpSyncClient.class)`**：注解只能约束本 Bean 是否创建，未必能阻止 JSON/Stdio 自动配置创建额外客户端；尤其自动配置可能声明集合 Bean。初稿保留为“来源建议”，并明确需核对注册条件，定稿应按源码确认。
4. **请求超时默认值**：属性表写 `20s`，建议对照 2.0.2 McpClientCommonProperties 确认。
5. **共享 MCP 会话**：当前页面新增长段落，初稿完整保留。每用户凭据传输与协议会话独立是两个问题；不要把 ToolContext、ChatMemory.CONVERSATION_ID 或 HTTP Token 等同 MCP 会话隔离。

## 明确的来源文字问题

- Windows 段把 `node` 与 `npx`/`npm` 一概列为 `.cmd`，不准确；Node.js 通常为 `node.exe`。初稿正文已按“批处理入口才需 cmd.exe /c”解释，未改代码。
- ProcessBuilder 不能直接执行 shell 内置命令，应交给 cmd.exe。初稿已纠正来源的含混列表。
- “Windows requires backslashes or escaped forward slashes”错误：JSON 反斜杠需转义，正斜杠本身无需转义。初稿已按 JSON 语法说明。
- `mvn.cmd`/`gradle.cmd` 是命令入口，不应笼统说 Maven/Gradle Wrapper；Wrapper 常见名为 `mvnw.cmd`/`gradlew.bat`。初稿改为命令入口。
- URL 拆分表中的 `url` 全部遗漏协议，与随后排障要求矛盾。定稿应补回 `http://`/`https://`，初稿表原值保留供主 agent 集中修正。
- 两处 Streamable-HTTP 示例端点叫 `/custom-sse`，虽可用作自定义路径但易误导；可改名 `/custom-mcp`，如改需记为示例字符串变更。
- 第二个 Streamable-HTTP 小节与前者重复；本块初稿保留全部表与代码，方便主 agent 去重并保留对照/锚点。
- MCP Roots 是协议声明的范围，不是 OS 沙箱或授权自动执行机制；若加说明，应明确由服务端落实访问控制。

## 格式

- 将来源 `::: important` 映射为 Starlight 支持的 `:::note`，`::: warning` 映射为 `:::caution`。
- 代码第 8 段结束围栏与 note 原始抽取黏连，已拆为独占行。
