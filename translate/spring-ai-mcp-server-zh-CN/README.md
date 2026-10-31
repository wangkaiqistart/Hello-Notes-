# MCP 服务端精翻记录

日期：2026-10-31。来源：[Spring AI 参考文档](https://docs.spring.io/spring-ai/reference/api/mcp/mcp-server-boot-starter-docs.html)，页面版本 2.0.2。遵循项目 baoyu-translate 配置：简体中文、精翻、技术读者、简明技术文档风格。

- [英文正文](../spring-ai-mcp-server.md) · [来源 HTML](source-article.html) · [来源清单](source-manifest.json)
- [站点正文](../../src/content/docs/frameworks/spring-ai/mcp/server.mdx) · [定稿](translation.md)
- [分析](01-analysis.md) → [翻译上下文](02-prompt.md) → [初稿](03-draft.md) → [审校](04-critique.md) → [修订](05-revision.md) → [定稿](translation.md)

## 范围

STDIO 与 HTTP 传输、能力开关、安全边界、同步异步 API、服务端注解、传输上下文与自动配置。

导航位于“开发框架 → Spring AI → MCP”，接在工具调用之后。顺序：概览 → 客户端 → 服务端。完整注解、各传输高级配置与认证集成保留来源链接，未另翻译成独立页面。

## 校正与优化

- 来源第 2 段：Authorization为空时返回EMPTY，避免Map.of接收null。
- 来源第 3 段：Authorization为空时返回EMPTY，避免Map.of接收null。
- 来源第 4 段：仅报告请求头是否存在，不伪装成鉴权成功。

修复来源两个损坏的 SSE 锚点；STDIO 描述为子进程通信。默认开启的能力开关限于 tool/resource/prompt/completion。自定义 Provider 会替换默认构建设置，而 Starter 仍注册路由；说明 SYNC/ASYNC 与 WebMVC/WebFlux 是不同维度。读取 Authorization 不代表鉴权。

来源已失效的 Java SDK、MCP 旧规范与 Spring Boot 自动配置链接已更新到可访问地址；来源 HTML 仍保留原貌。

## 核验

- [代码对照](code-fidelity.json)：来源 6 段，定稿 6 段，逐段标记修改与去重。
- [API 静态断言](../spring-ai-mcp-overview-zh-CN/api-contract-checks.json)：29 项源码断言；同版本 Spring AI 2.0.2 与其实际依赖 MCP SDK 2.1.0。源码快照保留许可证，位于 [api](../spring-ai-mcp-overview-zh-CN/api/)。
- [图片清单](image-manifest.json)：0 张图片的路径、来源与 SHA-256。
- [外链核验](external-links.json)：三篇共 39 个去重页面及使用的锚点检查通过。
- [页面验证](validation.jsonl)：桌面 1440px 与手机 390px，导航、代码、图片、站内链接和锚点均通过；无页面横向溢出、脚本错误或 Markdown 标记残留。
- 来源 18 个英文锚点全部保留；修订、定稿和站点正文一致。

`npm run check`：0 错误、0 警告、0 提示。`npm run build`：139 页生成成功。构建仍有现存空 i18n 集合及 docs/404 条目提示。

Java 示例仅做原文和源码静态核对；未编译、未启动 MCP 客户端或服务端、未调用真实模型或工具。这些检查不代表订单助手的实践验收已完成。

## 2026-11-01 阅读结构优化

沿用工具调用和对话记忆的阅读标准，将常用接入前置，配置、平台排查及底层定制集中供查阅。原有正文、代码、图片与旧锚点保留；概览中两处前后指向随章节移动修正。修订、定稿与站点同步，代码对照的 `targetBlock` 更新为当前位置。详细安排及验证见[结构优化记录](../spring-ai-mcp-overview-zh-CN/2026-11-01-structure.md)。
