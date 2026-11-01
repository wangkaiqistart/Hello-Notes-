# Spring AI：评估测试

- 原文：[Evaluation Testing](https://docs.spring.io/spring-ai/reference/api/testing.html#_relevancy_evaluator)
- 版本与日期：2.0.2，2026-11-01。
- 方式：baoyu-translate，项目配置 zh-CN / refined / technical。单篇翻译，不分块。
- 站点正文：`src/content/docs/frameworks/spring-ai/engineering/evaluation.mdx`。
- 导航：Spring AI → 工程实践 → 评估测试，接在 RAG 后面。

## 文件

`../spring-ai-testing.md` 与 `source-article.html` 保存来源；`01-analysis.md` 至 `05-revision.md` 保存分析、提示、初稿、审校和修订；`translation.md` 是最终稿，与站点正文同步。

`source-manifest.json` 保存源章节、代码、图片与链接；`coverage-audit.json`、`code-fidelity.json`、`api-contract-checks.json` 分别保存覆盖映射、示例差异与同版本 API 静态核对。`api/manifest.json` 记录源码来源与哈希；`page-validation.json` 记录浏览器验证。

## 覆盖与校正

完整覆盖 6 个源小节、7 个源代码主题。新增自定义相关性模板和当前通用事实核查默认提示词，最终为 9 个代码块。正文原本没有图片，无需图片本地化。

以 v2.0.2 源码纠正原文的 `List<Content>`、`StPromptTemplate`、FactCheckingEvaluator 旧构造器和 Ollama 旧构造方式；修复事实核查示例将参考资料放进 userText、dataList 为空的问题。保留原始文档快照与初稿，不覆盖来源。详细差异见审校记录。

补充严格 YES 匹配、不同评估器分数含义、检索文档非空断言，以及评估结果不代表外部事实真伪的边界。

## 引用选择

RAG、ETL、ChatClient 与 PromptTemplate 引用已有站内笔记。原 StringTemplate 外链在当前模板用法语境下替换为站内 PromptTemplate；不宣称本站覆盖其完整语言规范。

两处 Spring AI 集成测试保留 GitHub 引用，并固定到 v2.0.2，因为本地没有等价源码页面。文末原文链接保留，便于追溯。

## 验证边界

API 通过同版本源码静态核对；未编译或执行 Java 示例，未调用 Ollama、云模型或向量库。页面检查和生产构建不能代替模型效果验收。

## 验证结果

`npm run check` 为 0 错误、0 警告、0 提示；`npm run build` 成功生成 86 页。桌面（1440 px）与手机（390 px）页面检查通过，14 个正文站内目标和锚点有效，6 个原始章节锚点保留；两处固定版本的 GitHub 测试引用均返回 200。12 项同版本 API 静态核对通过。
