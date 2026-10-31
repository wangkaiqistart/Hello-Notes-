# Server 审校

## 准确性

- 两个 SSE URL 含错误的<em标记，修成真实锚点；STDIO通常连接子进程，并非同JVM。
- 默认能力开关仅 resource/tool/prompt/completion 四种，不含所有列举的通知。
- 显式选择STREAMABLE，避免缺省条件与属性默认的冲突；SYNC/ASYNC与WebMVC/WebFlux分开。
- 第2、3段提取 Authorization 时应保护 null，Map.of不接受null。
- 第4段仅演示上下文读取，不鉴权，不能返回假成功，改为报告头是否存在。
- 自定义Provider替换自动Provider构建，需说明不会自动合并Boot属性；Starter仍注册路由。
- 说明configData为业务占位，注解仅扫描已注册Bean。

## 表达与排版

保留全部6段代码和18个来源英文锚点，安全说明随原文完整翻译。示例未启动，不称运行通过。

## 证据

api-server-review.md 与 ../spring-ai-mcp-overview-zh-CN/api/。

## 链接与构建复核

来源 Java SDK 的3个旧地址已404，替换为 java.sdk.modelcontextprotocol.io/latest/ 及 client/server 子页；旧规范站迁到 modelcontextprotocol.io/specification/，Spring Boot 旧锚点改为当前自动配置页面。图片说明按实际图内容核对；MDX 正文行首 import 应写为行内代码，避免被解释成 ESM。
