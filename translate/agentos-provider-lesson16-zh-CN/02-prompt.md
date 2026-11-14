# 精炼改写约束

面向熟悉 Java / Spring Boot 的开发者，用简明技术文档风格整理中文 PDF。正文从职责与工程判断切入，保留三张原图、两层配置、服务骨架、三个测试方法和完整验收范围。

统一术语：Provider、Profile、ChatModel、ChatResponse、ReActLoop、ToolExecutor、PromptBuilder、MemoryService、Schema、llm_calls。标题用 AgentOS；课程配置标识 oryxos、.oryxos、OryxTool 不悄悄改写。

依据 01-analysis.md 处理 API、Profile 错误边界、model/temperature 参数传递、自动执行、审计和 Maven 测试发现的问题。澄清只作为工程提示，不能声称已验证课程 Java 实现。保留原始文本 source.txt，代码仅修复 PDF 分页造成的换行。图放在相应解释之后，不直接贴标题。
