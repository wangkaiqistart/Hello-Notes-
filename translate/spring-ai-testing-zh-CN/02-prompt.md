# 翻译要求

将 source-article.html 的正文及 ../spring-ai-testing.md 精翻为简体中文。风格 concise technical，受众熟悉 Java 和 Spring Boot。遵循 01-analysis.md 的术语表，保留全部源小节与 7 个源代码主题，按 api/ 下 v2.0.2 源码修正失效签名和示例。

先讲评估接口和请求，再讲 RelevancyEvaluator、集成测试、自定义模板，最后讲 FactCheckingEvaluator 和 Ollama / Bespoke 示例。优先突出阅读顺序与可操作用法；补充明确有依据的评估边界。不得把相关性通过等同于事实正确，不把模型判断当成确定性测试。默认英文提示词和占位符保持原样，API 标识符不翻译。

原文的旧 API 和上下文传参问题在审校记录单列；正文展示当前正确用法，不堆叠写作过程说明。保留原始锚点以承接官方章节链接。使用知识库的已有 RAG、ChatClient 和 PromptTemplate 页面；没有同等内容的测试源码保持 GitHub 引用，固定到 v2.0.2。新增内容仅用于解释机制、用法和边界。
