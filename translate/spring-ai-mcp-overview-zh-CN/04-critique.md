# 概览审校

## 准确性

- 来源将标准客户端描述为 Servlet 实现，与 Client 文档和 JDK HttpClient 自动配置不符，改为 JDK HttpClient。
- 来源概览说 protocol=SSE 或留空；属性字段默认 STREAMABLE，但自动配置 SSE 条件 matchIfMissing=true。不得推断省略配置会得到 STREAMABLE，显式配置该值。
- 来源迁移说明的 SDK 1.0 RC1 是历史基线，2.0.2 发布 POM 实际使用 MCP SDK 2.1.0，必须区分。
- Starter 引入传输依赖不等于提供用户项目的完整 BOM 管理，改为遵循 spring-ai-bom。

## 表达与结构

- 三张图均保留原字节，从来源左右栏表移为正文后图片；三层图放在完整三层解释之后。
- 增补从 Tool Calling 进入 MCP 的能力区别，不将资源与提示词描述成自动调用的工具。
- 初稿已按源缺陷线索澄清部分术语，定稿继续收紧默认协议措辞。

## 链接与构建复核

来源 Java SDK 的3个旧地址已404，替换为 java.sdk.modelcontextprotocol.io/latest/ 及 client/server 子页；旧规范站迁到 modelcontextprotocol.io/specification/，Spring Boot 旧锚点改为当前自动配置页面。图片说明按实际图内容核对；MDX 正文行首 import 应写为行内代码，避免被解释成 ESM。
