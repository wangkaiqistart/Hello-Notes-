# 结构化输出翻译分析

来源：https://docs.spring.io/spring-ai/reference/api/structured-output.html；版本 2.0.2；获取日期 2026-10-25。

## 范围

约 965 个空白分隔词，6 个主要章节、3 个子节、8 段 Java 示例、1 张速查表和 1 张基础流程图。篇幅低于分块阈值，主 agent 完成单篇精翻。本文只覆盖高层 ChatClient 用法，校验、原生输出与转换器的详细章节保留来源链接，后续逐篇整理。

## 术语与风格

沿用 baoyu-translate 项目配置：zh-CN、refined、technical。Structured Output → 结构化输出；Typed Response → 返回类型明确的对象；Schema → 结构约束（首次解释，后文保留 JSON Schema）；Self-Correction → 自动纠正；Provider-Native → 提供方原生；Output Converter → 输出转换器。

简明中文解释用途与差异，保留全部示例、代码字符串、Java 泛型和链接。ActorsFilms 为本文来源的类型名称，不与其他文章的 ActorFilms 强行统一。

## 重点

- 默认 .entity() 通过提示词要求 JSON 格式后转换，不保证输出一定符合 Schema，更不能保证业务事实正确。
- 默认方式不依赖原生结构化输出 API；原生方式则要求模型支持，两者范围不同。
- validateSchema 默认最多尝试 3 次，不误译为额外重试 3 次；有限重试不代表永远不失败。
- useProviderStructuredOutput 约束格式，不替代业务校验；只在支持的提供方与模型上使用。
- .entity()/.responseEntity() 的全部重载只在 .call() 路径，.stream() 没有直接返回对象的这些重载；不扩展为永远不能聚合流后自行转换。
- ResponseEntity 是 Spring AI 结果容器，与 Spring MVC HTTP ResponseEntity 区分。
- 工具调用的结构化参数机制不使用 StructuredOutputConverter，不将其解释为工具业务结果自动完成对象校验。
- 配图需沿用来源图形与配色并中文化，放在完整解释默认转换步骤的正文之后，不修改其他页面的已有图片。
