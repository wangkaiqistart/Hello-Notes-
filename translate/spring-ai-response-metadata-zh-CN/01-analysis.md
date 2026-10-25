# 聊天响应元数据：翻译分析

来源：https://docs.spring.io/spring-ai/reference/api/usage-handling.html；版本 2.0.2；获取日期 2026-10-25。

## 范围与结构

约 1,158 个空白分隔词，5 个二级章节、2 个三级章节、8 段 Java 代码、1 张提供方支持表，无图片。正文依次说明 ChatResponseMetadata、RateLimit、Usage、缓存指标和多步调用累计用量。全文采用单篇精翻，不分块。

## 术语与风格

沿用项目 EXTEND.md：zh-CN、refined、technical。Chat Response Metadata 译为聊天响应元数据，Usage 译为用量，Rate Limit 译为限流信息，Prompt Cache 译为提示词缓存，Token 首次写词元（Token）。类名、方法名、字段、模型提供方名称均保留英文。

## 审校重点

- 限流周期与额度以服务计划及响应字段为准，不把月度举例当成固定周期，也不将模型限流信息当成 Spring 自动执行限流。
- EmptyRateLimit 的访问方法返回零，不代表真实额度为零；保留 instanceof 的区分方式。
- 标准 Token 计数和原生 Usage 对象分开说明，保留 getNativeUsage() 的具体 OpenAI 类型与 instanceof 判断。
- Usage 接口代码是节选，缓存方法在后文出现，避免将节选当成完整接口。
- 缓存支持表只代表本文版本的 Spring AI 适配情况，不泛化为提供方服务本身永远不支持缓存。
- 缓存指标的 null 表示不支持或无该项数据，不能等同于零；原文明确不支持缓存时返回 null。
- 多步流程的标准计数与缓存计数累计；多个模型调用合并后原生 Usage 为 null，不能误写为只看最后一次，也不能扩展为跨会话总账。
- 8 段代码只翻译注释，其余保持来源；保留省略号，注明代码片段未编译或实际请求模型。
