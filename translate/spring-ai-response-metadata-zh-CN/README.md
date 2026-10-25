# 聊天响应元数据翻译记录

日期：2026-10-25。沿用 baoyu-translate 项目配置：简体中文、精翻、面向开发者、简明技术文档风格。

- 来源：[Chat Response Metadata](https://docs.spring.io/spring-ai/reference/api/usage-handling.html)，版本 2.0.2。
- [英文正文](../spring-ai-response-metadata.md) · [来源 HTML](source-article.html) · [代码快照](source-code.json)
- [站点页面](../../src/content/docs/frameworks/spring-ai/core/chat-response-metadata.mdx) · [最终译稿](translation.md)
- [分析](01-analysis.md) → [翻译上下文](02-prompt.md) → [初稿](03-draft.md) → [审校](04-critique.md) → [修订](05-revision.md) → [定稿](translation.md)

## 翻译范围

完整保留 5 个主要章节、2 个子节、8 段 Java 示例和 8 家提供方的缓存指标支持表。原文没有图片。仅翻译代码注释，代码、提示词与输出字符串保持来源，接口节选的省略号明确说明。

保留并强调三项边界：EmptyRateLimit 返回零值时不能视为真实额度耗尽；缓存指标的 null 与零值不同；多步交互会累计标准用量与缓存指标，但原生用量对象不能合并。缓存支持表限定为本文版本的 Spring AI 统一接口支持情况。

页面接入提示词之后的侧边栏，提示词正文增加继续阅读入口，同步其最终译稿；README 更新笔记规划和已完成状态。

## 验证

- 8 段代码逐块对照，除注释和空白外与来源一致。
- `npm run check`：0 错误、0 警告、0 提示。
- `npm run build`：122 页生成成功，保留既有 i18n 空集合与 docs/404 条目缺失提示。
- 本次 Markdown / MDX 格式检查与 `git diff --check` 通过；站点配置沿用原缩进。
- 桌面 1440px、手机 390px：HTTP 200，无页面横向溢出、脚本异常或失效的本文锚点；侧边栏和提示词跳转正常。
- 最终译稿与发布页面逐字节一致；没有编译 Java 示例或调用真实模型。

详细记录见 [validation.jsonl](validation.jsonl)。
