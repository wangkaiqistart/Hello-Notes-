# 审校记录

已逐段对照原文及 api/ 下 v2.0.2 源码。源文 6 个小节、7 个代码主题均有对应，无正文图片。

## 准确性

- EvaluationRequest：源文 List<Content> 与当前 List<Document> 不一致；初稿已纠正。
- FactCheckingEvaluator：源文单参数公开构造器不适用；初稿改为 builder 和 forBespokeMinicheck，并区分通用默认提示词和 Bespoke 专用模板。
- FactCheckingEvaluator：doGetSupportingData 只拼接 dataList 的文档文本，不读取 userText；初稿将参考资料包装为 Document 并明确指出源示例的空上下文问题。
- Ollama：源示例构造方式过时且缺分号，初稿改用 builder；模型名从未定义常量明确为 bespoke-minicheck。
- PromptTemplate：源文 StPromptTemplate 表述不对应当前默认 StTemplateRenderer；已按同版本 PromptTemplate.java 核对。
- 两个评估器均严格匹配去空白后的 yes。RelevancyEvaluator 分数为 1 或 0，FactCheckingEvaluator 使用默认分数 0；初稿未把分数描述为通用质量得分。
- 待改进：RAG 示例正文要求检索结果非空，但代码尚未断言；应将实际文档取为 List<Document> 后增加非空断言，再构造 EvaluationRequest，避免空上下文误通过。

## 中文与结构

- 初稿依照“接口 → 相关性 → 集成测试 → 事实核查”组织，符合本地阅读顺序。
- 两种评估器的对比表和源码字段行为说明有助于避免错误理解，保留。
- 默认英文提示词保留，中文解释与执行模板分开；API 标识符不翻译。
- 个别代码收尾可简化排版，PromptTemplate 文本块直接以三引号加右括号结束。

## 引用与边界

- RAG、ETL、ChatClient、PromptTemplate 均使用主题对应的站内页面与锚点，需浏览器核验。
- 两个集成测试引用固定到 v2.0.2；本地没有等价源码页，保留外链。
- 原文出处保留外链以便核对。
- 已明确模型评估不保证外部事实正确或回答完整；未声称运行 Java 示例、调用模型或完成实际评估。

## 结论

初稿已修正源文主要 API 与上下文问题；补充检索文档非空断言并完成格式整理后发布。
