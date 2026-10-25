# tool-search-tool 精翻记录

日期：2026-10-26。来源：[Spring AI](https://docs.spring.io/spring-ai/reference/api/tools/tool-search-tool.html)，页面版本 2.0.2。使用项目 baoyu-translate：zh-CN、refined、technical。

- [英文正文](../spring-ai-tool-search-tool.md) · [来源 HTML](source-article.html) · [来源清单](source-manifest.json)
- [站点正文](../../src/content/docs/frameworks/spring-ai/tools/tool-search-tool.mdx) · [定稿](translation.md)
- [分析](01-analysis.md) → [翻译上下文](02-prompt.md) → [初稿](03-draft.md) → [审校](04-critique.md) → [修订](05-revision.md) → [定稿](translation.md)

## 范围与导航

延迟加载流程、快速入门、完整配置、Regex/Lucene/Vector 索引、会话标识、工具引用累积、索引更新和淘汰。

保留 17 段代码、1 张来源图片和 17 个来源章节锚点。图片保留原始字节，添加中文替代文本与原尺寸查看链接。导航位于“Spring AI → 工具调用”，在对话记忆之后；四篇阅读顺序：基础 → Advisor → 工具搜索 → ChatModel 底层调用。后两篇可按场景查阅。

## 校正与优化

- 无 API 代码修改。

澄清 maxResults 为回退值而非硬上限，未配置时三类索引默认 10；Regex 查询经过转义，不是 glob；工具集合变化会重建索引，tenantId 分组不等同鉴权。两个 Gradle 围栏改为 groovy，代码内容不变。

## 核验材料

- [代码对照](code-fidelity.json)：区分 API 校正、注释和围栏语言调整。
- [同版本源码断言](../spring-ai-tool-calling-zh-CN/api-contract-checks.json) 与 [审校依据](../spring-ai-tool-calling-zh-CN/api-review-notes.md)。源码保留许可证；Jackson 注解证据为 2.22 补充契约，不代表 Spring AI BOM 版本。
- [外链核验](external-links.json)：四篇共 14 个去重外部页面及引用锚点通过。
- [页面验证](validation.jsonl)：桌面 1440px、手机 390px、导航、代码块、图片、站内链接和锚点检查通过，无页面横向溢出或脚本错误。

`npm run check`：0 错误、0 警告、0 提示；`npm run build`：136 页生成成功。定稿与站点正文一致。Java 示例仅做原文与 API 静态核对，未编译运行、未连接数据库、未调用真实模型或执行工具。
