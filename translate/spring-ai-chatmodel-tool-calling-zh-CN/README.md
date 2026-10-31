# chatmodel-tool-calling 精翻记录

日期：2026-10-26。来源：[Spring AI](https://docs.spring.io/spring-ai/reference/api/tools/chatmodel-tool-calling.html)，页面版本 2.0.2。使用项目 baoyu-translate：zh-CN、refined、technical。

- [英文正文](../spring-ai-chatmodel-tool-calling.md) · [来源 HTML](source-article.html) · [来源清单](source-manifest.json)
- [站点正文](../../src/content/docs/frameworks/spring-ai/tools/chatmodel-tool-calling.mdx) · [定稿](translation.md)
- [分析](01-analysis.md) → [翻译上下文](02-prompt.md) → [初稿](03-draft.md) → [审校](04-critique.md) → [修订](05-revision.md) → [定稿](translation.md)

## 范围与导航

底层 ChatModel 行为、默认与请求级工具、选项优先级、同步及流式手动循环、returnDirect。

保留 8 段代码、0 张来源图片和 12 个来源章节锚点。图片保留原始字节，添加中文替代文本与原尺寸查看链接。导航位于“Spring AI → 工具调用”，在对话记忆之后；四篇阅读顺序：基础 → Advisor → 工具搜索 → ChatModel 底层调用。后两篇可按场景查阅。

## 校正与优化

- 第 2 段：OllamaChatModel.Builder.options 接收 OllamaChatOptions。
- 第 3 段：使用 OllamaChatOptions 并补充 OllamaApi 构建。
- 第 6 段：流式循环处理空聚合和 returnDirect，直接返回工具生成结果。

区分向模型提供工具定义与实际执行工具；说明 blockLast 的阻塞边界和直接返回的批次条件。

## 核验材料

- [代码对照](code-fidelity.json)：区分 API 校正、注释和围栏语言调整。
- [同版本源码断言](../spring-ai-tool-calling-zh-CN/api-contract-checks.json) 与 [审校依据](../spring-ai-tool-calling-zh-CN/api-review-notes.md)。源码保留许可证；Jackson 注解证据为 2.22 补充契约，不代表 Spring AI BOM 版本。
- [外链核验](external-links.json)：四篇共 14 个去重外部页面及引用锚点通过。
- [页面验证](validation.jsonl)：桌面 1440px、手机 390px、导航、代码块、图片、站内链接和锚点检查通过，无页面横向溢出或脚本错误。

`npm run check`：0 错误、0 警告、0 提示；`npm run build`：136 页生成成功。定稿与站点正文一致。Java 示例仅做原文与 API 静态核对，未编译运行、未连接数据库、未调用真实模型或执行工具。

## 2026-11-01 复审

已同步阅读导引、执行边界与示例优化，当前修订和定稿与站点正文一致。原文、初稿和初次审校保留。代码变更、源码依据及本次验证见[复审记录](../spring-ai-tool-calling-zh-CN/2026-11-01-review.md)；原有验证记录对应初次翻译。

## 2026-11-01 阅读结构调整

按学习层次重排全部章节，正文、代码、图片及原有锚点均保留。当前修订、定稿与站点一致；代码对照新增 `targetBlock` 指向重排后位置。以[结构调整记录](../spring-ai-tool-calling-zh-CN/2026-11-01-structure.md)为最新验证依据，前次复审记录保留历史快照。

## 2026-11-01 官网覆盖审计

已对照实时官网逐节核对正文、示例、配置及限制，未发现遗漏；本站正文保持不变。四篇总计 85 个子章节、75 段代码、7 张图均有对应内容，已有 API 校正与示例调整保留。详见[覆盖审计](../spring-ai-tool-calling-zh-CN/2026-11-01-coverage-audit.md)。
