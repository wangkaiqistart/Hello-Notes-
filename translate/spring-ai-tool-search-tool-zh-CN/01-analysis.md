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
