# Client 审校

## 准确性

- 第3、24段 YAML root-change-notification 放错层，改到 client 下；源码创建路径未消费该属性，不能保证仅开关即开启根能力。
- 第8段 build().initialize() 返回 InitializeResult，不符合方法返回 McpSyncClient，改为单独初始化后返回。
- ConditionalOnMissingBean 仅约束本方法，不能阻止自动配置客户端列表。明确全手动与自动连接生命周期不混用，手动工具需显式注册。
- Windows node.exe 与 .cmd 区分；JSON反斜杠需转义，正斜杠不需转义；URL 拆分表补协议。
- 第13段及对应表与第11段重复，定稿去重，保留全部英文锚点。
- 前缀生成器规范化、限长、幂等保证与实现不符，改为源码可支持的行为并说明自定义边界。
- 第19段上下文传递示例需注册 MCP 工具。第20段自定义转换保留默认exchange过滤。
- 第22段进度按 progress/total计算；total为空展示原始量。
- 工具过滤示例不是白名单；clients指连接配置名；共享协议会话不是用户/租户边界。沿用完整来源说明。

## 表达与排版

保持全部非重复章节、表格和代码，不展示翻译过程旁白。roots、sampling、elicitation统一术语；所有省略业务实现的代码注明为片段。

## 证据

api-client-lifecycle-review.md、api-client-tools-review.md 及 ../spring-ai-mcp-overview-zh-CN/api/。

## 链接与构建复核

来源 Java SDK 的3个旧地址已404，替换为 java.sdk.modelcontextprotocol.io/latest/ 及 client/server 子页；旧规范站迁到 modelcontextprotocol.io/specification/，Spring Boot 旧锚点改为当前自动配置页面。图片说明按实际图内容核对；MDX 正文行首 import 应写为行内代码，避免被解释成 ESM。
