# 图像模型精翻记录

日期：2026-10-25。沿用 baoyu-translate 项目配置：zh-CN、refined、technical。继续按用户的模型小章节范围保留核心概念和必要示例，提供方详情保留官网入口。

- [英文正文](../spring-ai-image-model.md) · [来源 HTML](source-article.html) · [来源清单](source-manifest.json)
- [站点正文](../../src/content/docs/frameworks/spring-ai/models/image-model.mdx) · [最终定稿](translation.md)
- [分析](01-analysis.md) → [翻译上下文](02-prompt.md) → [初稿](03-draft.md) → [审校](04-critique.md) → [修订](05-revision.md) → [定稿](translation.md)

## 内容范围

覆盖六个核心类型、默认与请求级调用、返回值与选项边界。保留 3 段代码，其中 ImageModel 接口按来源逐字核对；其余是按 API 整理的最小调用片段。

相关来源页面均无图片，本次未添加生成配图或修改既有图片。页面放在“Spring AI → 模型”中，与聊天、Embedding 同级，概览和 README 同步更新。

## 核验

- [API 签名核验](api-contract-checks.json)：逐项确认必要构造器和方法；Javadoc 快照保存在本目录。
- [链接核验](external-links.json)：本次 22 个外部页面与引用锚点均可访问。
- 最终译稿与站点正文逐字节一致。示例按来源或 API 静态核对，未编译 Java、未调用真实模型。
- `npm run check`：0 错误、0 警告、0 提示；`npm run build`：131 页生成成功，保留既有 i18n / docs/404 提示。
- 桌面 1440px、手机 390px：导航、本地链接和锚点正常，无页面横向溢出、脚本错误或粗体标记残留。格式检查与 `git diff --check` 通过。详细结果见 [validation.jsonl](validation.jsonl)。
