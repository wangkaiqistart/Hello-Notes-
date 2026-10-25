# Spring AI：提示词翻译记录

日期：2026-10-25。使用 baoyu-translate 精翻流程，英译简体中文，面向 Java / Spring Boot 开发者，采用简明技术文档风格。

- 来源：[Prompts](https://docs.spring.io/spring-ai/reference/api/prompt.html)，文档版本 2.0.2。
- [英文正文](../spring-ai-prompts.md) · [来源正文 HTML](source-article.html) · [代码快照](source-code.json)
- [站点页面](../../src/content/docs/frameworks/spring-ai/core/prompts.mdx) · [最终译稿](translation.md)
- [分析](01-analysis.md) → [翻译上下文](02-prompt.md) → [初稿](03-draft.md) → [审校](04-critique.md) → [修订](05-revision.md) → [润色定稿](translation.md)

## 处理要点

保留 15 段 Java 示例及全部学习资源入口，用表格整理角色、消息访问方法和模板重载。英语示例字符串、参数名和资源路径保持不变；注释中文化。原文的错误 `#StringTemplate` 锚点改为 StringTemplate 站点。

单独建立 `core/prompts.mdx`，方便按“ChatClient → 提示词 → 结构化输出”的顺序逐章阅读；这篇只覆盖来源的 Prompts 章节，不把后续 Structured Output 混入译文。

## 已明确标注的来源澄清

1. 来源页 `Content` 代码和图片仍写 `getContent()`；对照 [2.0.2 Javadoc](https://docs.spring.io/spring-ai/docs/2.0.2/api/org/springframework/ai/content/Content.html)，修正为 `getText()`，页面版本注中说明。[核验快照](source-content-javadoc.html) 保留。
2. 思维链按来源链接的定义说明为中间推理步骤，并明确区分多轮对话记忆；不重复原文的“串联回答”定义。
3. Token 与英文单词的比例保留为粗估，限定不适用于中文；旧型号的上下文容量数字不作为当前规格复述，正文说明这一取舍。

## 配图

保留原始 `spring-ai-message-api.jpg`，SHA-256 记录在 [source-assets.json](source-assets.json)。中文版使用 SVG 包含原图，保留黄色 UML 类图、类名、角色、连线与层级，只覆盖图题、说明、图例，并同步修正 `getText()`。没有重画已有的其他图片，也没有添加“官方”字样。

可通过 [localize-message-api.py](localize-message-api.py) 重现中文版；图片放在消息与角色完整说明之后，提供替代文本、短图注和点击查看全图的入口。

## 验证

- `npm run check`：0 错误、0 警告、0 提示。
- `npm run build`：121 页构建成功；保留既有 i18n 空集合与 404 条目缺失提示。
- 15 段示例逐块核对通过；唯一 API 名称修正在正文注明。原图 SHA-256 未变，SVG 可解析，最终译稿与页面逐字节一致。
- 新页面与精翻 Markdown / MDX 的 Prettier、`git diff --check` 通过；既有配置缩进和 README 表格间距保留。
- 桌面 1440px、手机 390px 均 HTTP 200，15 段代码可见，图片加载正常、替代文本和图注存在，点击可查看完整 SVG；导航存在，无横向页面溢出或脚本错误。

详细结果见 [validation.jsonl](validation.jsonl)。只验证文档、示例静态一致性与站点呈现，没有运行 Java 项目或调用模型 API。
