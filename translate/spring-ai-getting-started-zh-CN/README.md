# Spring AI：快速入门翻译记录

日期：2026-10-25。使用 baoyu-translate 精翻流程与项目配置，英译简体中文，面向熟悉 Java / Spring Boot 的开发者。

- 来源：[Getting Started](https://docs.spring.io/spring-ai/reference/getting-started.html)，文档版本 2.0.2。
- [英文正文快照](../spring-ai-getting-started.md) · [原始正文 HTML](source-article.html)
- [最终译稿](translation.md) · [站点页面](../../src/content/docs/frameworks/spring-ai/getting-started/quickstart.mdx)
- [分析](01-analysis.md) → [翻译上下文](02-prompt.md) → [初稿](03-draft.md) → [审校](04-critique.md) → [修订](05-revision.md) → [最终译稿](translation.md)

## 处理要点

保留全部 8 个 Maven / Gradle 配置块和 6 类组件链接，仅翻译代码注释，使用标签页切换构建工具。原文没有配图。BOM 示例沿用原文的 2.0.0，并注明文档版本 2.0.2 的差异；不添加原文没有的模型调用应用。

页面遵循已有目录规划，新增“快速入门”导航，并更新总览入口与 README 完成状态。已有图片不作改动。

## 验证

- 8 个代码块除注释和空白外与来源一致；XML 片段解析通过。
- 内容检查：0 错误、0 警告、0 提示；构建：119 页生成成功。
- Markdown / MDX 格式检查、`git diff --check` 通过；`astro.config.mjs` 在修改前后都存在与 Prettier 默认风格不一致的问题，保留原有缩进。
- 桌面 1440px、手机 390px：HTTP 200，无页面横向溢出和脚本异常；3 组 Maven / Gradle 标签全部切换通过，导航与总览入口存在。
- 最终译稿与站点页面逐字节一致。没有运行 Maven / Gradle，也没有调用模型 API。

具体记录见 [validation.jsonl](validation.jsonl)。
