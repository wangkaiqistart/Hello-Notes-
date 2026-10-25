# Chat Client API 内容分析

来源：https://docs.spring.io/spring-ai/reference/api/chatclient.html；文档版本 2.0.2；获取日期 2026-10-25。

## 内容与范围

约 4,823 个空白分隔词，分成 3 段：创建客户端与响应、返回值与默认配置、Advisors 与记忆及实现说明。保留整篇主要章节和代码，不只翻译入门的前五节。来源含 1 张配置合并示意图，需沿用已确认的原图布局并中文化标签。

## 术语

Fluent API → 链式 API；streaming → 流式；prototype scope → 原型作用域；ChatResponse → 模型响应，保留类名；entity → Java 对象；metadata → 元数据；TemplateRenderer → 模板渲染器；Advisor 保留 API 名称；Memory → 对话记忆；Marker Interface → 标记接口；imperative → 命令式；reactive → 响应式；observability → 可观测性；RAG → 检索增强生成。

## 重点与难点

- 使用项目 EXTEND.md 的 refined / zh-CN / technical 设置，保留代码、类名、URL、重要限制与默认值，删减重复解释。
- call() / stream() 选择执行方式，content()/chatResponse()/entity() 等终结调用取结果，不能沿用来源开头 call() 立即发请求的简化说法。流式的实际执行与订阅有关。
- 多模型需要保留可观测性与 ChatClientBuilderCustomizer：使用 ChatClientBuilderConfigurer；ChatClient 的 @Primary 不会解决 ChatModel 注入歧义，应明确两种 bean 层级。
- 来源流式转换示例混用 ActorFilms/ActorsFilms 与局部变量、this 字段，需在审校阶段统一并记录修改。
- 返回值有 ChatClientResponse（含执行上下文）与 Spring AI 的 responseEntity（模型响应加对象），不要混淆成 Spring MVC ResponseEntity。
- 模板渲染器只影响客户端 user/system 文本，不影响 Advisor 自身模板。
- Message metadata 的作用取决于后续消费者；不是通用模型参数。保留非空约束。
- 默认值可在调用时覆盖；保留 mutate() 在客户端与请求上都返回 Builder 的语义。
- 2.0.2 的 ToolCallingAdvisor 自动注册、禁用、顺序、标记接口和每次调用必须提供 conversationId 均须以当前来源为准，不套用旧版经验。
- 保留底部 HTTP 客户端、Servlet / Reactive 栈、阻塞工具调用和 observation 限制；此类说明明确是本文版本的实现说明。
- 未创建或运行 Java 项目，不宣称示例编译通过或模型请求成功。

## 分块说明

技能自带 chunk CLI 因 markdown-it 依赖缺失无法运行。以二级标题为边界使用本地脚本分为 3 段，代码围栏和完整章节不拆分，不改项目依赖。
