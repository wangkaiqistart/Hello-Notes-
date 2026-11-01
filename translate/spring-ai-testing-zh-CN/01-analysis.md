# 内容分析

来源：Spring AI 2.0.2 Evaluation Testing；用户入口为 Relevancy Evaluator 锚点，按此前整页翻译习惯覆盖全文。原文约 828 个空白分隔词，6 个小节、7 个代码块、0 张正文图片，单篇处理。

面向熟悉 Java / Spring Boot 的开发者，沿用项目 zh-CN / refined / technical 配置。页面落在 engineering/evaluation.mdx，导航位于 RAG 后面的工程实践，README 同步。

## 术语

| 原文                           | 中文                     |
| ------------------------------ | ------------------------ |
| Evaluation Testing             | 评估测试                 |
| Evaluator                      | 评估器；API 名称保留     |
| Relevancy                      | 相关性                   |
| Fact Checking                  | 事实核查                 |
| context                        | 上下文、参考资料         |
| claim / document               | 待核查陈述 / 参考文档    |
| hallucination                  | 幻觉                     |
| integration test               | 集成测试                 |
| PromptTemplate                 | 提示词模板；API 名称保留 |
| Retrieval Augmented Generation | 检索增强生成（RAG）      |

## 翻译难点

- 保留默认英文提示词、模型名称与模板占位符，中文解释用于理解，不改变实际模板。
- 相关性和相对于上下文的支持性不能表述为外部事实真伪的保证；源码只对严格 YES/NO 结果作判断。
- 原文 EvaluationRequest 使用 List<Content>，2.0.2 源码为 List<Document>。
- 原文 StPromptTemplate 名称过时；PromptTemplate 默认使用 StTemplateRenderer。
- 原文 FactCheckingEvaluator 单参数公开构造器已不适用；当前使用 builder 或 forBespokeMinicheck。
- 原文 Ollama API/模型构造方式过时，模型语句缺分号；改成源码对应的 builder。
- 原文 context 放进 userText 且 dataList 为空，Evaluator.doGetSupportingData 只读取 dataList 的文档文本，必须将 context 包装成 Document。
- 原文短 Document/Claim 模板对应 Bespoke 专用模式；当前通用模式另有 yes/no 指令。
- 查阅本站 RAG、ChatClient、提示词和 ETL 笔记，匹配时优先站内链接；GitHub 测试代码和原文出处保留外链。
