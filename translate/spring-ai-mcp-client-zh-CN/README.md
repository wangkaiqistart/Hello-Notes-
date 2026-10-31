# MCP 客户端精翻记录

日期：2026-10-31。来源：[Spring AI 参考文档](https://docs.spring.io/spring-ai/reference/api/mcp/mcp-client-boot-starter-docs.html)，页面版本 2.0.2。遵循项目 baoyu-translate 配置：简体中文、精翻、技术读者、简明技术文档风格。

- [英文正文](../spring-ai-mcp-client.md) · [来源 HTML](source-article.html) · [来源清单](source-manifest.json)
- [站点正文](../../src/content/docs/frameworks/spring-ai/mcp/client.mdx) · [定稿](translation.md)
- [分析](01-analysis.md) → [翻译上下文](02-prompt.md) → [初稿](03-draft.md) → [审校](04-critique.md) → [修订](05-revision.md) → [定稿](translation.md)

## 范围

通用和传输属性、Windows 启动、客户端定制、协议会话边界、工具过滤与命名、元数据转换和客户端注解。

导航位于“开发框架 → Spring AI → MCP”，接在工具调用之后。顺序：概览 → 客户端 → 服务端。完整注解、各传输高级配置与认证集成保留来源链接，未另翻译成独立页面。

## 校正与优化

- 来源第 3 段：Roots属性移动到client通用层级。
- 来源第 8 段：先build客户端，再initialize，最后返回客户端。
- 来源第 19 段：添加MCP工具Provider注册和占位声明分号。
- 来源第 20 段：自定义元数据转换器保留默认exchange过滤。
- 来源第 22 段：进度按progress/total计算，total未知时展示原始量。
- 来源第 24 段：Roots属性移动到client通用层级。

来源有两节完全重复的 Streamable-HTTP 属性表和 YAML，合并为一节，去掉来源第 13 段重复代码，同时保留两个锚点。完整保留共享客户端与协议会话边界说明。纠正默认前缀实现的限长/幂等过强承诺，说明过滤器并非严格白名单；自定义单客户端 Bean 不会阻止自动客户端集合创建。Roots 开关的声明与实际创建路径分开说明。

来源已失效的 Java SDK、MCP 旧规范与 Spring Boot 自动配置链接已更新到可访问地址；来源 HTML 仍保留原貌。

## 核验

- [代码对照](code-fidelity.json)：来源 26 段，定稿 25 段，逐段标记修改与去重。
- [API 静态断言](../spring-ai-mcp-overview-zh-CN/api-contract-checks.json)：29 项源码断言；同版本 Spring AI 2.0.2 与其实际依赖 MCP SDK 2.1.0。源码快照保留许可证，位于 [api](../spring-ai-mcp-overview-zh-CN/api/)。
- [图片清单](image-manifest.json)：0 张图片的路径、来源与 SHA-256。
- [外链核验](external-links.json)：三篇共 39 个去重页面及使用的锚点检查通过。
- [页面验证](validation.jsonl)：桌面 1440px 与手机 390px，导航、代码、图片、站内链接和锚点均通过；无页面横向溢出、脚本错误或 Markdown 标记残留。
- 来源 36 个英文锚点全部保留；修订、定稿和站点正文一致。

`npm run check`：0 错误、0 警告、0 提示。`npm run build`：139 页生成成功。构建仍有现存空 i18n 集合及 docs/404 条目提示。

Java 示例仅做原文和源码静态核对；未编译、未启动 MCP 客户端或服务端、未调用真实模型或工具。这些检查不代表订单助手的实践验收已完成。
