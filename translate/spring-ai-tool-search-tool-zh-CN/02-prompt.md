# 精翻上下文

使用项目 baoyu-translate 配置：zh-CN、refined、technical audience、technical style。面向熟悉 Java / Spring Boot 的开发者，用简明自然中文，保留全部来源主题、表格、代码、链接和图片。

# 工具搜索：翻译分析

来源：https://docs.spring.io/spring-ai/reference/api/tools/tool-search-tool.html。版本 2.0.2；日期 2026-10-26。保留 17 个代码块、1 张来源图片。

## 内容

How It Works、When to Use、Installation、Quick Start、Session Scoping、Search Strategies、VectorToolIndex (Semantic)、LuceneToolIndex (Keyword)、RegexToolIndex (Pattern)、Configuration、ToolIndex API、Index Eviction、Spring Boot Auto-Configuration、ToolIndex Auto-Selection、Configuration Properties Reference、Example Configurations、See Also

## 读者与风格

读者熟悉 Java / Spring Boot，已阅读 ChatClient、Advisors、ChatMemory；当前先学习工具调用，再学 RAG。精翻为自然简明的中文技术文档，完整保留本篇主题与必要引用；不把之前模型小节的精选范围延伸到这四篇。

## 术语

Tool Calling：工具调用；tool definition：工具定义；tool execution：工具执行；turn：轮次；iteration：迭代；progressive tool disclosure：渐进式工具暴露；tool index：工具索引；session scoping：会话隔离；hook：钩子方法；return direct：直接返回；Prompt：提示词；Advisor、ChatModel、ChatClient、ToolCallback 等保留 API 名称。Token 首次说明为词元，后文保留 Token。

## 风险与核验

- 模型请求调用，应用执行；2.0 ChatModel 无内部工具循环，ChatClient 自动注册 ToolCallingAdvisor。
- ChatClient 请求工具追加默认工具，ChatModel 请求工具替换默认工具；toolContext 合并且同名键运行时优先。
- Advisor order 小者在循环外、大者在循环内；自动注册与手动注册的内部历史开关不同。
- returnDirect 多工具同轮时要求全部为 true；手动循环也须判断，不能无条件继续调用模型。
- 会话 ID 必填，tenantId 示例仅代表索引分组粒度，不能推导为自动用户鉴权。
- 所有代码保持标识符、英文输入、依赖坐标和配置键；源码证实的错误单独记录后修正，未执行 Java。
- 图片靠近完整解释之后，保留来源版式与字节，中文替代文本；不额外重绘。

## 格式与策略

代码可翻译注释，保留英文字符串和 API 标识符；提示源文错误不要凭猜测改代码，记录给主审。来源单元格提示表（空表头）改成普通段落或 Starlight :::note/:::caution，真正的配置表保留。需要保持来源英文锚点，使用 Markdown 标题后的显式 <a id="source-id"></a> 独占一行放在对应标题前（H1 page-title 不需要）。保留来源 URLs，主审统一改成本地跨页链接。图片使用来源 URL 和中文 alt，主审下载并替换为本地。图片放在完整解释其用途的正文之后，不直接紧接标题。公开正文避免翻译过程旁白。

不删减源文内容，也不增加未经证实的功能承诺。正文以 H1 中文标题开头，主审添加 frontmatter。章节原有结构保留，嵌套列表按真实逻辑重建，避免转换器把有序/嵌套步骤摊平导致逻辑丢失。
