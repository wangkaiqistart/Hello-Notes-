# 模型概览精选记录

日期：2026-10-25。沿用项目 baoyu-translate 配置：zh-CN、refined、technical，面向 Java / Spring Boot 开发者。

- [英文正文](../spring-ai-models.md) · [来源 HTML](source-article.html) · [来源清单](source-manifest.json)
- [站点正文](../../src/content/docs/frameworks/spring-ai/models/index.mdx) · [定稿](translation.md)
- [分析](01-analysis.md) → [翻译上下文](02-prompt.md) → [初稿](03-draft.md) → [审校](04-critique.md) → [修订](05-revision.md) → [定稿](translation.md)

## 内容范围

按用户授权精选 Model API 核心抽象与六类任务，提供接入判断和查询入口。2026-10-25 补充图像、音频与审核三篇后，概览同步链接五类模型的本地笔记；提供方配置与完整参数仍按需查阅官网。此前的构建与链接检查记录保留于下方，新增验证见 validation.jsonl。

省略完整层级图、适配器清单与其他框架能力的重复介绍；工程检查项明确标注。

## 验证

- 最终译稿与站点正文逐字节一致；多模态两段代码除已列校正与注释外保持来源一致，两张来源图片哈希复核通过。
- `npm run check` 无错误、警告或提示；`npm run build` 成功生成 128 页，保留既有 i18n 空集合和 docs/404 缺失提示。
- 桌面 1440px、手机 390px：页面、导航、本地链接与锚点正常，无页面横向溢出、脚本异常或 Markdown 粗体标记残留。多模态两图加载正常，大图入口可用，照片比例正确。
- 23 个外部文档页面及引用锚点均验证可访问，见 [官网链接核验](external-links.json)。
- Java 示例完成来源 / API 核对，未编译执行或调用真实模型。

详细结果见 [validation.jsonl](validation.jsonl)。
