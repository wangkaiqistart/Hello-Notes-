# 多模态精翻记录

日期：2026-10-25。沿用项目 baoyu-translate 配置：zh-CN、refined、technical，面向 Java / Spring Boot 开发者。

- [英文正文](../spring-ai-multimodality.md) · [来源 HTML](source-article.html) · [来源清单](source-manifest.json)
- [站点正文](../../src/content/docs/frameworks/spring-ai/core/multimodality.mdx) · [定稿](translation.md)
- [分析](01-analysis.md) → [翻译上下文](02-prompt.md) → [初稿](03-draft.md) → [审校](04-critique.md) → [修订](05-revision.md) → [定稿](translation.md)

## 内容范围

完整精翻多模态概念、媒体结构、两种调用方式、回答示例与七家支持入口。保留两段代码与两张图片。消息 UML 复用已验收中文图，水果图保持来源字节与原始比例。

修正首例 this.imageResource / this.userMessage 局部引用；按 2.0.2 Javadoc 更正 AssistantMessage 只能输出文本的过时说明。

## 验证

- 最终译稿与站点正文逐字节一致；多模态两段代码除已列校正与注释外保持来源一致，两张来源图片哈希复核通过。
- `npm run check` 无错误、警告或提示；`npm run build` 成功生成 128 页，保留既有 i18n 空集合和 docs/404 缺失提示。
- 桌面 1440px、手机 390px：页面、导航、本地链接与锚点正常，无页面横向溢出、脚本异常或 Markdown 粗体标记残留。多模态两图加载正常，大图入口可用，照片比例正确。
- 23 个外部文档页面及引用锚点均验证可访问，见 [官网链接核验](external-links.json)。
- Java 示例完成来源 / API 核对，未编译执行或调用真实模型。

详细结果见 [validation.jsonl](validation.jsonl)。
