# Spring AI 两篇文档精修记录

日期：2026-10-25。使用 baoyu-translate 的 refined 流程，英译简体中文，面向熟悉 Java / Spring Boot 的开发者，采用简明技术文档风格。

原稿整体含义正确。本轮重点补足压缩后的语义、统一术语和澄清概念边界，保持原有篇幅层级，不扩写为逐句长译。

## 页面与最终译稿

| 文档        | 站点页面                                                              | 精修译稿                                                  |
| ----------- | --------------------------------------------------------------------- | --------------------------------------------------------- |
| 总览        | [index.mdx](../src/content/docs/frameworks/spring-ai/index.mdx)       | [translation.md](spring-ai-overview-zh-CN/translation.md) |
| AI 核心概念 | [concepts.mdx](../src/content/docs/frameworks/spring-ai/concepts.mdx) | [translation.md](spring-ai-concepts-zh-CN/translation.md) |

两份最终译稿与对应站点页面内容一致。英文来源分别保存在 [Overview](spring-ai-overview.md) 和 [AI Concepts](spring-ai-concepts.md)，均从 Spring AI 2.0.2 来源页面提取正文。

## 具体优化

| 位置                            | 原稿                                           | 精修后                                                                            | 原因                                                           |
| ------------------------------- | ---------------------------------------------- | --------------------------------------------------------------------------------- | -------------------------------------------------------------- |
| 总览：模型与向量存储 API        | 主要列出支持的模型和数据库                     | 明确跨提供方统一 API，同时保留模型特有能力，并限定具体调用方式以提供方文档为准    | 补回源文 portable API 的含义，避免误解为所有提供方能力完全一致 |
| 总览：Advisors                  | 封装常见模式、便于复用                         | 明确处理模型往返数据，可在不同模型和场景间复用                                    | 补回源文强调的复用范围                                         |
| 总览：可观测性与评估            | 合并为一行                                     | 分别说明运行情况观察与生成内容评估                                                | 澄清两个功能的职责，并非原稿存在事实错误                       |
| 核心概念：Embedding             | 主要以“把内容变成向量”解释                     | 先定义为内容的数值表示，再说明嵌入模型执行向量化                                  | 区分表示结果与生成过程，补上高维语义空间的直观说明             |
| 核心概念：提示词                | 说明角色和模板，SQL 对比侧重确定性             | 恢复“提示词工程”概念，SQL 对比回到表达任务意图的差异                              | 补回源文概念，收紧超出原意的推论                               |
| 核心概念：Token                 | 说明长度、费用和上下文                         | 首现“词元（Token）”，补明输入切分与输出还原                                       | 定义更完整；继续保留“不等于单词或汉字”的正确说明               |
| 核心概念：结构化输出            | 将两步转换笼统描述为结构化输出流程             | 限定为图示的“提示词驱动转换方式”，补回可能多次交互的条件                          | 不把一种转换机制概括为所有结构化输出的唯一实现                 |
| 核心概念：Prompt Stuffing / RAG | 已提到相关资料与检索，但术语主要写“上下文补充” | 统一为“提示词填充”，在正文明确先检索再补充的 RAG 关系；图示流程限定为向量检索实现 | 便于对应英文术语，进一步明确方法与实现范围                     |
| 核心概念：工具调用              | 模型根据任务返回工具名和参数                   | 补明“模型决定调用工具时”；方法注册后随请求提供工具定义，由应用执行                | 避免误解为每轮必须调用工具，或模型直接执行 Java 方法           |
| 核心概念：评估                  | “另一个评估调用”                               | “预训练模型也可以辅助评估”                                                        | 更贴近源文，避免暗示必须另选一个评估模型                       |
| 两篇：链接和术语                | 功能表的文档入口较少，部分缩写未展开           | 补充来源章节链接，展开 MCP、ETL，并统一 Embedding 等术语                          | 便于继续查阅和交叉核验                                         |

## 保留的取舍

- 两篇的标题、路由、frontmatter 与简明结构均保留。文字精修阶段保留 9 张原图；随后按用户要求优化 8 张示意图，Logo 继续使用原图。
- 源文中的旧型号容量、知识截止日期和训练集大小留在英文来源中，不作为当前规格写回正文；这一处理沿用原稿，不计为本轮新纠错。
- 提示技巧论文与引述的对应关系未在本轮独立核实，继续省略，不宣称其错误或普遍有效。
- 数据库仅保留代表性示例，通过来源链接提供完整范围。
- 原有准确内容，例如 Fluent API 译为“链式 API”、工具由应用执行、Token 不等于单词，均不冒充本轮纠错成果。

## 精翻过程

每篇目录保留：`00-before.mdx`（旧稿）、`01-analysis.md`（分析）、`02-prompt.md`（翻译上下文）、`03-draft.md`（初稿）、`04-critique.md`（对照审校）、`05-revision.md`（修订）、`translation.md`（最终译稿）、`changes.diff`（前后差异）。

- [总览审校](spring-ai-overview-zh-CN/04-critique.md) · [前后差异](spring-ai-overview-zh-CN/changes.diff)
- [核心概念审校](spring-ai-concepts-zh-CN/04-critique.md) · [前后差异](spring-ai-concepts-zh-CN/changes.diff)
- [图片中文优化记录](image-language-review.md)：8 张示意图已恢复来源图稿的布局、配色、图标和连线，替换中文组件标签；Token 改用经 `cl100k_base` 核对的中英文短句切分示例，品牌标识保持原样。

## 验证

- `npm run check`：通过，0 错误、0 警告、0 提示。
- `npm run build`：通过，两篇页面均正常生成；构建仍提示原有 i18n 集合和 404 内容缺失。
- 两篇页面的 Prettier 格式检查与 `git diff --check`：通过。
- 桌面宽度 1440px、手机宽度 390px：两篇均返回 HTTP 200，全部图片正常加载，无页面横向溢出、无浏览器脚本异常，导航入口存在。
- 9 张原图文件的 SHA-256 与精修前完全一致，作为来源保留；当前页面按原有顺序引用按来源版式中文化的 8 张图及原始 Logo，frontmatter 保留。
- 两份 `translation.md` 与站点 MDX 页面逐字节一致；逐页验证结果见各精翻目录中的 `validation.jsonl`。

## 配图后续优化

按用户要求，7 张结构图恢复来源版式：横向流程、黄色节点、绿色工具和原始图标连线；组件标签中文化，不再使用额外的卡片布局、标题栏和说明页脚。Token 图按后续反馈改为中英文短句与彩色 Token 片段，具体分词数据见 [token-example.json](token-example.json)。两份最终译稿同步新图片引用；历史初稿、修订稿和文字精修差异文件保留当时内容。具体逐图说明见[图片中文优化记录](image-language-review.md)。本次图片与页面核验见 [image-validation.jsonl](image-validation.jsonl)。

## 后续译文：快速入门

2026-10-25 新增 [Spring AI：快速入门](../src/content/docs/frameworks/spring-ai/getting-started/quickstart.mdx)，沿用简明技术文档风格和精翻流程。包含版本兼容、Maven / Gradle 仓库、镜像、BOM 与组件入口；全部 8 段配置与来源核对，原文无图。保留并注明文档 2.0.2 与 BOM 示例 2.0.0 的差异。过程与验证见[翻译记录](spring-ai-getting-started-zh-CN/README.md)。

## 后续译文：ChatClient API

2026-10-25 新增 [Spring AI：ChatClient API](../src/content/docs/frameworks/spring-ai/core/chat-client.mdx)，覆盖 12 个主要章节、37 个代码块及 1 张中文配图。沿用 baoyu-translate 精翻流程，校正流式转换示例中的类型名、局部变量引用，澄清调用时机、配置合并与 Advisor 顺序。过程与验证见[翻译记录](spring-ai-chat-client-zh-CN/README.md)。

## 后续译文：提示词

2026-10-25 新增 [Spring AI：提示词](../src/content/docs/frameworks/spring-ai/core/prompts.mdx)，覆盖 Prompt、消息角色、模板与渲染器、资源加载、提示词工程和 Token，保留全部 15 段代码与学习链接。消息类图沿用来源布局并中文化说明；按 2.0.2 Javadoc 修正 `getText()`，澄清 CoT 含义，并说明旧型号 Token 上限的取舍。过程与验证见[翻译记录](spring-ai-prompts-zh-CN/README.md)。

## 后续译文：聊天响应元数据

2026-10-25 新增[聊天响应元数据](../src/content/docs/frameworks/spring-ai/core/chat-response-metadata.mdx)，保留 8 段 Java 代码与 8 家提供方的缓存指标支持表，原文无图。重点说明 EmptyRateLimit、缓存 null 与零值、多步模型调用累计用量及原生对象无法合并的边界。新增提示词后的导航与阅读入口，具体过程见[翻译记录](spring-ai-response-metadata-zh-CN/README.md)。

## 后续译文：结构化输出

2026-10-25 新增[结构化输出](../src/content/docs/frameworks/spring-ai/core/structured-output.mdx)，保留 8 段 Java 示例、8 行用法速查表和 1 张流程图。区分默认提示词方式、Schema 校验重试和提供方原生约束，说明泛型与完整响应用法。中文版配图保留来源手绘布局、配色与连线，仅替换说明文字。过程见[翻译记录](spring-ai-structured-output-zh-CN/README.md)。

## 后续译文：Advisors API 与递归 Advisors

2026-10-25 将 Advisors API 与 Recursive Advisors 合并为 [Advisors 调用链与递归](../src/content/docs/frameworks/spring-ai/core/advisors.mdx)，与 ChatClient API 同级。按基础调用链、自定义实现、递归循环、历史迁移组织，完整保留 16 段代码和 4 张配图，旧递归篇地址跳转到合并章节。当前定稿与验证见[合并记录](spring-ai-advisors-combined-zh-CN/README.md)；分篇精翻过程保留于 [Advisors](spring-ai-advisors-zh-CN/README.md) 和[递归篇](spring-ai-advisors-recursive-zh-CN/README.md)。

## 结构化输出扩展：原生输出与转换器

2026-10-25 将 [Provider-Native Structured Output](spring-ai-structured-output-native-zh-CN/README.md) 与 [Output Converters](spring-ai-structured-output-converters-zh-CN/README.md) 精翻后并入[结构化输出](../src/content/docs/frameworks/spring-ai/core/structured-output.mdx)。新增支持检测与回退、模型限制、全局启用、转换器接口与实现、高低层用法及非 JSON 输出；主篇已有示例复用，补入 3 张来源版式配图。当前定稿与检查见[合并记录](spring-ai-structured-output-combined-zh-CN/README.md)。

## 后续译文：多模态与模型精选

2026-10-25 新增[多模态](../src/content/docs/frameworks/spring-ai/core/multimodality.mdx)，保留两段调用代码、消息类图与水果照片，按 2.0.2 API 校正助手消息媒体支持及局部变量引用。过程见[多模态精翻记录](spring-ai-multimodality-zh-CN/README.md)。

按用户要求，将模型内容精选为三页小章节：[模型概览](../src/content/docs/frameworks/spring-ai/models/index.mdx)、[聊天模型](../src/content/docs/frameworks/spring-ai/models/chat-model.mdx)、[Embedding 模型](../src/content/docs/frameworks/spring-ai/models/embedding-model.mdx)。保留核心抽象与常用方法，提供方配置、完整参数和其他专用模型详情仅保留官网入口；非完整逐页翻译。范围及核验分别见[模型概览](spring-ai-models-zh-CN/README.md)、[聊天模型](spring-ai-chat-model-zh-CN/README.md)、[Embedding 模型](spring-ai-embedding-model-zh-CN/README.md)。

## 模型小节补充：图像、音频与审核

2026-10-25 补充[图像模型](../src/content/docs/frameworks/spring-ai/models/image-model.mdx)、[音频模型](../src/content/docs/frameworks/spring-ai/models/audio-model.mdx)与[审核模型](../src/content/docs/frameworks/spring-ai/models/moderation-model.mdx)，与聊天和 Embedding 同级。图像篇覆盖生成 API 与输出；音频篇合并 Audio / STT / TTS；审核篇结合提供方文档解释共享结果。继续沿用精翻流程，提供方配置与专有参数保留官网入口。来源页面无图；10 段必要代码按原文或对应版本 API 核对，未执行模型调用。分析、审校与验证见[图像](spring-ai-image-model-zh-CN/README.md)、[音频](spring-ai-audio-model-zh-CN/README.md)、[审核](spring-ai-moderation-model-zh-CN/README.md)记录。

## 后续译文：对话记忆

2026-10-25 新增[对话记忆（Chat Memory）](../src/content/docs/frameworks/spring-ai/core/chat-memory.mdx)，接在模型小节之后，与 ChatClient API、Advisors API 同级。保留 34 段示例与全部存储类型，原文无图；重点说明会话隔离、消息窗口的完整轮次淘汰、记忆与历史的区别，以及工具消息的采集与存储边界。对照 2.0.2 源码修正 Cassandra 配置与构建示例，修正向量记忆模板配置方法名，并将 JDBC 初始化配置改为明确的三选一写法。过程与核验见[翻译记录](spring-ai-chat-memory-zh-CN/README.md)。

## 结构化输出补全：Schema 校验与自动纠正

2026-10-25 将 [Schema Validation & Self-Correction](spring-ai-structured-output-validation-zh-CN/README.md) 精翻后并入结构化输出。覆盖错误反馈、显式 Advisor 配置、Schema 来源互斥、用量累计和原生约束组合，并补入来源版式中文循环图。4 段来源代码复用 2 段既有示例，全文共 30 段代码、5 张图。按 2.0.2 源码纠正文档次数歧义：默认最多额外重试 3 次，最多调用 4 次；补明手动注册后不再叠加 validateSchema()，空 Schema 启用校验会失败。过程和当前验证见[专题记录](spring-ai-structured-output-validation-zh-CN/README.md)。

## 后续译文：工具调用小章节

2026-10-26 完成四篇：

- [工具调用基础](../src/content/docs/frameworks/spring-ai/tools/tool-calling.mdx)：工具定义、执行循环、记忆、MCP、参数增强、上下文、异常与次数限制；[翻译记录](spring-ai-tool-calling-zh-CN/README.md)。
- [工具调用 Advisor](../src/content/docs/frameworks/spring-ai/tools/tool-calling-advisor.mdx)：构建器、钩子、流式观察与扩展；[翻译记录](spring-ai-tool-calling-advisor-zh-CN/README.md)。
- [工具搜索](../src/content/docs/frameworks/spring-ai/tools/tool-search-tool.mdx)：渐进式工具暴露、索引策略、会话与淘汰；[翻译记录](spring-ai-tool-search-tool-zh-CN/README.md)。
- [ChatModel 工具调用](../src/content/docs/frameworks/spring-ai/tools/chatmodel-tool-calling.mdx)：底层工具定义与手动循环；[翻译记录](spring-ai-chatmodel-tool-calling-zh-CN/README.md)。

共保留 75 段代码与 7 张来源图片。基础长文按技能分两块翻译，统一审校；对照 2.0.2 源码修正部分版本不一致的 API、缺失的构造器、手动循环的直接返回分支、Schema 注解与工具搜索配置语义。Java 示例仅做静态核验，未调用真实模型或执行工具。导航新增“工具调用”小节，README 调整为先工具调用/MCP、再 RAG 的学习顺序。
