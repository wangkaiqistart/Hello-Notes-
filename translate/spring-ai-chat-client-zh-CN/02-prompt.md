# 共享翻译上下文

目标：将 Spring AI 2.0.2 的 Chat Client API 完整译为简明自然的中文技术文档，服务于熟悉 Java / Spring Boot 的读者。保留主要章节与代码，减少长句、重复解释和宣传性形容词。

词汇：Fluent API=链式 API；streaming=流式；prototype scope=原型作用域；metadata=元数据；imperative=命令式；reactive=响应式；Marker Interface=标记接口；observability=可观测性；RAG=检索增强生成。ChatClient、ChatModel、Advisor、Bean、Flux 等 API 名称保留。

约束：
- 各分块只写中文正文，不写 frontmatter、来源行或额外总标题；所有原有二级及以下标题都翻译保留（可以压缩冗余小标题）。
- 保留所有代码块；代码注释可译，类名、方法、属性、常量、配置键与 URL 保留，避免将 prompt 字符串随意中文化影响源码对照。
- 来源中 call() 发起请求的开头描述须澄清为选择同步方式，取结果的方法才触发调用。不要把 Flux 的组装说成已执行请求。
- ChatClient 的 @Primary 与 ChatModel 的注入歧义分开。多模型示例保留 configurer 对可观测性/customizer 的处理。
- 流式转换示例统一使用 ActorFilms、converter、flux、content 局部变量，修正来源混用 this.xxx 的问题，并在分块末尾用 HTML 注释记录调整供审校。
- Message Metadata 仅说明随消息传递和供下游使用，不保证模型提供方都消费。
- return entity 与 responseEntity 保留全部重载，可用表格合并相似描述；responseEntity 不译成 HTTP 响应。
- 配图路径替换为 /images/frameworks/spring-ai/chat-client-options-merging-zh.svg；替代文本准确说明默认配置与单次请求配置的合并。图片位置保持在默认配置说明之后。
- 图和正文不添加“官方”字样。片段内没有来源署名、写作旁白、测试通过宣称。
- 保留当前 2.0.2 的工具自动注册、conversationId 必填和实现限制；不套用旧版行为。
- 不使用 MDX 导入或组件；普通 Markdown 即可。尖括号泛型写在行内代码或代码块里。

三段边界：第 1 段为介绍、创建、多模型、链式 API、响应和模板；第 2 段为返回值、元数据、默认配置和 mutate；第 3 段为 Advisors、工具调用、记忆和实现说明。
