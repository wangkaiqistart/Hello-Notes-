# Advisors API 翻译记录

> 2026-10-25：站点已合并为 [Advisors 调用链与递归](../../src/content/docs/frameworks/spring-ai/core/advisors.mdx)，与 ChatClient API 同级。以下保留分篇翻译时的历史记录；当前定稿与合并验证见[合并记录](../spring-ai-advisors-combined-zh-CN/README.md)。

日期：2026-10-25。使用 baoyu-translate 精翻流程及项目配置，面向 Java / Spring Boot 开发者，采用简明技术文档风格。

- 来源：[Advisors API](https://docs.spring.io/spring-ai/reference/api/advisors.html)，版本 2.0.2。
- [英文正文](../spring-ai-advisors.md) · [来源 HTML](source-article.html) · [来源代码](source-code.json)
- [站点页面](../../src/content/docs/frameworks/spring-ai/core/advisors.mdx) · [最终译稿](translation.md)
- [分析](01-analysis.md) → [翻译上下文](02-prompt.md) → [初稿](03-draft.md) → [审校](04-critique.md) → [修订](05-revision.md) → [定稿](translation.md)

## 范围与校正

完整覆盖核心组件、请求与响应流程、order、接口、日志与 Re2 示例、全部内置 Advisor、流式差异、实践建议及历史迁移。保留 11 个代码块（含 Re2 提示词模板），深层重复标题整理为表格。

来源将 Advisor 的实现方法误写为 nextCall/nextStream，已根据 2.0.2 Javadoc 修正为 adviseCall/adviseStream，区分它们与 Chain 的继续执行方法。核验文本保存在本目录的 source-\*-javadoc.txt。

代码校正仅包括首例 this.chatClient 改为局部 chatClient，以及流式骨架补 return request / return response；移除 HTML 生成的 (1)/(2)/(3) 说明标号，注释中文化。详细对照见 [code-adjustments.diff](code-adjustments.diff)。保留初始化与业务逻辑占位，不将示意片段宣称为独立可运行项目。

历史 updateContext 与不可变 Map 说明限定为 1.0 M3，避免将其当成当前 ChatClientRequest API。

## 配图与导航

3 张中文 SVG 内嵌未改动的来源 JPG，保留 UML、黄色节点、箭头和编号，只覆盖图例与说明。流式图旧 AdvisedResponse 标签更正为 ChatClientResponse。来源校验值见 [source-assets.json](source-assets.json)，可用 [localize-advisor-images.py](localize-advisor-images.py) 重现，包括递归篇配图。图片位于相关解释之后，并提供替代文本、图注和大图入口。

导航归入 ChatClient API → Advisors，与递归篇互相链接；ChatClient 的专题入口改为本地译文。README 将对话记忆与 Advisor 机制拆为独立笔记。

## 验证

- 11 个来源代码块逐块对照，非注释代码调整只在第 1、11 块，其他代码保持一致。
- 来源图片 SHA-256 与 SVG 内嵌原图一致，已有其他文章图片不作改动。
- `npm run check`：0 错误、0 警告、0 提示；`npm run build`：125 页生成成功，保留既有 i18n 空集合和 docs/404 缺失提示。
- 本次 Markdown / MDX 格式检查与 `git diff --check` 通过；站点配置保持既有缩进。
- 桌面 1440px、手机 390px 验证页面、图片、分组导航、本地链接和锚点；无页面横向溢出或脚本错误，图片大图入口正常。
- 最终译稿与页面逐字节一致。未编译 Java 示例或调用真实模型。

详细结果见 [validation.jsonl](validation.jsonl)。
