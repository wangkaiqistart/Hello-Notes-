# 聊天模型审校

## 准确性

已对照来源及 2.0.2 ChatModel、StreamingChatModel、ChatResponse、ChatClientRequestSpec Javadoc，确认继承、call / stream 返回类型、getResult / getResults。最终逐项核对发现初稿的 options(Consumer) 写法不适用：2.0.2 实际接收 B extends ChatOptions.Builder<?>，修订稿改用 ChatOptions.builder().temperature(0.2)，不调用 build()，并在正文明确。同步与流式示例是按 API 编写的补充片段，未冒充原文逐字代码。

保留来源强调的底层完整选项与 ChatClient 增量设置差异；不将 temperature 示例描述为所有型号通用。流式片段不是完整答案，媒体或工具结果需读取对应字段。

## 精选范围

省略八段类定义、重复 UML 和提供方配置，保留三段最小调用片段；提示词与响应元数据链接已有中文页面。说明片段按段独立使用，避免 text / response 重复声明被误认为同一方法。

## 中文表达

将“无需背源码”改为直接说明本节重点，减少学习过程旁白。官网入口集中在末尾。
