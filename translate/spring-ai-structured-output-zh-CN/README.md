# 结构化输出翻译记录

> 2026-10-25：原生结构化输出与输出转换器已合并进同一站点页面。以下为最初主篇翻译记录；当前定稿与验证见[扩展合并记录](../spring-ai-structured-output-combined-zh-CN/README.md)。

日期：2026-10-25。沿用 baoyu-translate 项目配置：简体中文、精翻、面向 Java / Spring Boot 开发者、简明技术文档风格。

- 来源：[Structured Output](https://docs.spring.io/spring-ai/reference/api/structured-output.html)，版本 2.0.2。
- [英文正文](../spring-ai-structured-output.md) · [来源 HTML](source-article.html) · [代码快照](source-code.json)
- [站点页面](../../src/content/docs/frameworks/spring-ai/core/structured-output.mdx) · [最终译稿](translation.md)
- [分析](01-analysis.md) → [翻译上下文](02-prompt.md) → [初稿](03-draft.md) → [审校](04-critique.md) → [修订](05-revision.md) → [定稿](translation.md)

## 内容与配图

保留 6 个主要章节、3 个子节、全部 8 段 Java 示例和 8 行用法速查表。本文介绍 ChatClient 高层 API，校验、原生结构化输出与转换器的详细专题保留来源链接。

区分默认提示词驱动、Schema 校验重试和提供方原生约束；保留默认最多尝试 3 次、call-only、泛型以及完整响应读取等限制。补明有限重试仍可能失败，结构校验不替代业务校验。Spring AI ResponseEntity 的包名已对照 2.0.2 Javadoc 确认。

中文版流程图内嵌未改动的来源 PNG，仅覆盖说明文字，保留人物、手绘节点、蓝色虚线、橙色流程箭头与黄色 LLM。默认方式中的格式合规标为目标，图注明确其非严格保证；可点击查看大图。原图及 SHA-256 见 [source-assets.json](source-assets.json)，复现脚本为 [localize-basic-flow.py](localize-basic-flow.py)。其他文章的图片不作改动。

## 页面集成与验证

- 已接入响应元数据之后的侧边栏，并将上一篇的继续阅读入口改为本地页面，同步最终译稿与 README 完成状态。
- 8 段代码与来源逐块一致，包括类名、提示词字符串和示例返回数据，未改写 API。
- `npm run check`：0 错误、0 警告、0 提示；`npm run build`：123 页生成成功，保留既有 i18n 空集合与 docs/404 缺失提示。
- 本次 Markdown / MDX 格式检查和 `git diff --check` 通过，配置文件沿用既有缩进。
- 桌面 1440px、手机 390px：页面、配图和导航正常；无横向页面溢出或脚本错误，大图入口和上一篇跳转有效，SVG 文字位于画布内。
- 最终译稿与页面逐字节一致。未编译 Java 示例或调用模型接口。

详细结果见 [validation.jsonl](validation.jsonl)。
