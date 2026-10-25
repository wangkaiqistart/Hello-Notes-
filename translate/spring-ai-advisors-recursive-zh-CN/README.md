# 递归 Advisors 翻译记录

> 2026-10-25：站点已合并为 [Advisors 调用链与递归](../../src/content/docs/frameworks/spring-ai/core/advisors.mdx)，与 ChatClient API 同级。以下保留分篇翻译时的历史记录；当前定稿与合并验证见[合并记录](../spring-ai-advisors-combined-zh-CN/README.md)。

日期：2026-10-25。使用 baoyu-translate 精翻流程，沿用项目的简体中文、开发者受众和简明技术文档风格。

- 来源：[Recursive Advisors](https://docs.spring.io/spring-ai/reference/api/advisors-recursive.html)，版本 2.0.2。
- [英文正文](../spring-ai-advisors-recursive.md) · [来源 HTML](source-article.html) · [代码快照](source-code.json)
- [站点页面](../../src/content/docs/frameworks/spring-ai/core/advisors.mdx) · [最终译稿](translation.md)
- [分析](01-analysis.md) → [翻译上下文](02-prompt.md) → [初稿](03-draft.md) → [审校](04-critique.md) → [修订](05-revision.md) → [定稿](translation.md)

## 处理要点

完整保留 5 段代码、递归定义、copy(after) 下游子链、工具调用与结构校验两种内置循环，以及自定义累计用量。顶部阅读建议说明先理解循环范围，再结合工具调用深入。

来源对工具 Advisor 自动注册的简述不完整，按当前 ChatClient / Advisors 文档补明无静态工具也默认注册，除非明确禁用。两种 Schema 配置互斥、最多尝试 3 次、returnDirect、按调用或订阅创建累计器等限制均保留。循环骨架明确需要实现者提供 request 更新与停止策略。

5 段代码除注释和空白外与来源一致，见 [code-adjustments.diff](code-adjustments.diff)。原生用量无法跨模型调用合并的限制关联已有响应元数据译文。

## 图片与导航

唯一中文图保留来源 PNG，内嵌原图后覆盖标签，保持黄色节点、条件菱形、上下行箭头及虚线重复范围。图中 ABC 位于循环外、XYZ 位于下游，避免把递归误读为重跑整个链。来源与 SHA-256 见 [source-assets.json](source-assets.json)，生成脚本在 [Advisors 翻译目录](../spring-ai-advisors-zh-CN/localize-advisor-images.py)。

页面置于 ChatClient API → Advisors 分组，与主篇互相链接，图片提供替代文本、短图注和大图入口。

## 验证

- 5 段代码与来源逐块一致，源图 SHA-256 与中文 SVG 内嵌内容一致。
- `npm run check`：0 错误、0 警告、0 提示；`npm run build`：125 页生成成功，保留既有内容提示。
- 本次 Markdown / MDX 格式与 `git diff --check` 通过，配置文件保留原缩进。
- 桌面 1440px、手机 390px：HTTP 200，页面与图片无横向溢出，无脚本错误；嵌套导航、本地链接、锚点和大图入口正常。
- 最终译稿与页面逐字节一致。未编译 Java 示例或调用模型接口。

详细结果见 [validation.jsonl](validation.jsonl)。
