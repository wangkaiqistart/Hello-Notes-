# ChatModel 工具调用审校

## 准确性

- OllamaChatModel.Builder.options要求OllamaChatOptions；两个默认工具示例原用ToolCallingChatOptions不匹配，替换为提供方选项。覆盖示例还缺必填OllamaApi，补上。
- 源文流式说明提ChatClientMessageAggregator，但代码实际MessageAggregator，已按实际类型说明。
- 源文流式returnDirect直接break会丢失对外返回结果，增加buildGenerations封装与forwardToSse；聚合为空时安全退出。
- ChatModel不执行工具、请求工具替换默认、上下文Map合并规则均与2.0.2一致。
- 阻塞片段的return conversationHistory展示控制流，不是完整Controller；方法返回类型需按应用接口适配。

## 表达与格式

保留8段代码与全部来源章节。原文无图。代码注释中文，业务输入保留英文；说明示例非完整可运行项目。

## 证据

../spring-ai-tool-calling-zh-CN/api/ 的OllamaChatModel、ToolCallingChatOptions、ToolExecutionResult、MessageAggregator源码；Java未运行。
