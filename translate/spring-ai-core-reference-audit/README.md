# Spring AI 基础与模型笔记引用优化

日期：2026-11-01。沿用“内容保留、站内优先、仅引用 Spring AI 模块”的标准。

本次覆盖总览、AI 核心概念、快速入门、ChatClient、Advisors、提示词、响应元数据、结构化输出、多模态，以及模型分组的六篇笔记。

- 41 处外部文档引用改为已有 Spring AI 笔记，模板、流式响应、用量、工具循环与 RAG 模块尽量定位到小节。
- 补充模型类型、媒体生成、文本切分、向量入库与评估之间的上下文链接。
- 快速入门说明“先选组件，再查提供方依赖和配置”，避免把精选模型笔记当成完整接入手册。
- 138 个代码块逐块比对一致，22 张图片引用、标题、已有锚点与来源行均保留。
- 15 份 translation.md 与站点正文同步；此前的初稿与审校修订文件保留历史版本。

## 修改页面

| 页面 | 替换外链数量 |
| --- | ---: |
| [index](../../src/content/docs/frameworks/spring-ai/index.mdx) | 8 |
| [concepts](../../src/content/docs/frameworks/spring-ai/concepts.mdx) | 5 |
| [getting-started/quickstart](../../src/content/docs/frameworks/spring-ai/getting-started/quickstart.mdx) | 6 |
| [core/chat-client](../../src/content/docs/frameworks/spring-ai/core/chat-client.mdx) | 15 |
| [core/advisors](../../src/content/docs/frameworks/spring-ai/core/advisors.mdx) | 5 |
| [core/prompts](../../src/content/docs/frameworks/spring-ai/core/prompts.mdx) | 0 |
| [core/chat-response-metadata](../../src/content/docs/frameworks/spring-ai/core/chat-response-metadata.mdx) | 0 |
| [core/structured-output](../../src/content/docs/frameworks/spring-ai/core/structured-output.mdx) | 2 |
| [core/multimodality](../../src/content/docs/frameworks/spring-ai/core/multimodality.mdx) | 0 |
| [models/index](../../src/content/docs/frameworks/spring-ai/models/index.mdx) | 0 |
| [models/chat-model](../../src/content/docs/frameworks/spring-ai/models/chat-model.mdx) | 0 |
| [models/embedding-model](../../src/content/docs/frameworks/spring-ai/models/embedding-model.mdx) | 0 |
| [models/image-model](../../src/content/docs/frameworks/spring-ai/models/image-model.mdx) | 0 |
| [models/audio-model](../../src/content/docs/frameworks/spring-ai/models/audio-model.mdx) | 0 |
| [models/moderation-model](../../src/content/docs/frameworks/spring-ai/models/moderation-model.mdx) | 0 |

## 保留外链

Spring AI 模块没有完整可观测性笔记；模型提供方专有配置、完整 API、价格与限额、StringTemplate 引擎、论文、提示词工作坊及交互工具也没有等价的站内替代。来源链接继续用于溯源。逐项理由见[保留外链清单](external-links.md)。

## 验证

- `npm run check`：18 个 Astro 文件，0 错误、0 警告、0 提示。
- `npm run build`：成功构建 93 页。
- `git diff --check`：通过。
- 15 页 × 桌面 1440px / 手机 390px，共 30 项页面检查通过；215 个站内目标（含锚点和图片大图入口）可访问。
- 图片加载与替代文本正常，无页面横向溢出或脚本异常。

详细记录：[静态审查](audit.json)、[浏览器检查](browser.json)、[验证汇总](validation.json)。

本次不代表对官方内容覆盖率的重新审计；未编译执行 Java 示例或调用真实模型。
