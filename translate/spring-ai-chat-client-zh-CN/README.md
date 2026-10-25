# ChatClient API 翻译记录

日期：2026-10-25。使用 baoyu-translate 精翻流程与项目配置，面向 Java / Spring Boot 开发者，采用简明技术文档风格。

- 来源：[Chat Client API](https://docs.spring.io/spring-ai/reference/api/chatclient.html)，版本 2.0.2。
- [英文正文](../spring-ai-chat-client.md) · [来源 HTML](source-article.html) · [来源代码](source-code.json)
- [最终译稿](translation.md) · [站点页面](../../src/content/docs/frameworks/spring-ai/core/chat-client.mdx)
- [分析](01-analysis.md) → [翻译上下文](02-prompt.md) → [分块初稿](03-draft.md) → [审校](04-critique.md) → [修订](05-revision.md) → [最终译稿](translation.md)

## 内容处理

来源译述保留 12 个主要章节和全部 37 个代码块，覆盖客户端创建、多模型、同步与流式响应、结构化输出、模板、元数据、默认配置、Advisors、工具调用、对话记忆和实现限制。后续按读者反馈补充“运行前配置”，当前页面共 13 个二级章节、42 个代码块。

36 个代码块除注释与空白外和来源一致。第 12 个代码块统一为 `ActorFilms`，并将误写为 `this.converter`、`this.flux`、`this.content` 的引用改为已声明的局部变量。提示词、配置键和模型名保留；模型名注明使用前需确认提供方支持。

澄清 `call()` 的执行时机、流式响应的订阅、两类 Bean 的 `@Primary`、Advisor 的 `order`，以及 `ChatClient` 增量配置与直接调用 `ChatModel` 的区别。对话记忆、工具 Advisor 自动注册与实现说明均限定在来源版本。

来源配图存在裁切，保留原 PNG 作为资料；发布页采用中文重绘图，沿用蓝色嵌套层级、橙色连线与黄色模型节点，支持点击查看大图。已有文章图片保持不变。

## 初次翻译验证

- `npm run check`：0 错误、0 警告、0 提示。
- `npm run build`：120 页生成成功；保留既有 i18n 空集合与 docs/404 缺失提示。
- 本次修改的页面与最终译稿格式检查、`git diff --check` 通过。配置文件沿用现有缩进。
- 桌面 1440px、手机 390px：HTTP 200，无页面横向溢出、脚本错误和失效的本文锚点；配图加载完整。
- 侧边栏当前页、快速入门跳转已验证；总览入口和 README 状态已更新。
- 最终译稿与站点页面逐字节一致。未编译 Java 示例，未调用模型接口。

详细结果见 [validation.jsonl](validation.jsonl) 和[页面核验](06-validation.md)。

## 后续补充：依赖与 YAML

2026-10-25 在创建 ChatClient 前增加运行前配置，现已精简为模型 Starter、OpenAI / DeepSeek 的 YAML、IDEA 密钥设置和版本提示；BOM 引导至快速入门，删除重复步骤与排错说明。

配置补充引用 [OpenAI Chat](https://docs.spring.io/spring-ai/reference/api/chat/openai-chat.html)，与来源 ChatClient API 的 37 段代码分开核验。2.0.2 模型字段采用 `spring.ai.openai.chat.model`；对照 Maven Central 发布的 `OpenAiChatProperties` 源码，确认旧 `chat.options.model` 为兼容但弃用的入口。代码来源与校验摘要见 [configuration-reference.json](configuration-reference.json)。

当前页面和最终译稿已同步；详细验证及限制见 [配置补充记录](07-configuration.md)。

## 后续补充：多模型配置差异

在多模型示例旁增加单模型 / 多模型的选择规则、DeepSeek 两种接入方式的对应关系、专用 YAML 和默认 Builder 示例。共新增 2 个代码块，之前 40 段代码保持不变，当前总计 42 段。配置条件按 2.0.2 的自动配置源码核对，过程见 [多模型补充记录](08-multi-model.md)。
