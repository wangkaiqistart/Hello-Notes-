# 翻译分析

来源：https://docs.spring.io/spring-ai/reference/api/advisors.html；版本 2.0.2；日期 2026-10-25。

## 内容范围

约 1,993 个词，11 个代码块（其中 1 个提示词模板）、3 张图。全文保留核心组件、顺序、接口、自定义实现、日志、Re2、内置 Advisor、流式、实践与历史 API 迁移。篇幅低于分块阈值，主 agent 单篇初译后审校。

## 准确性风险

- 来源把自定义实现方法误写为 nextCall/nextStream，应为 adviseCall/adviseStream，前两者是链的继续执行方法。
- 首例声明局部 chatClient 却调用 this.chatClient，需统一为局部变量并记录。
- HTML 代码中的 (1)/(2)/(3) 是说明标号，不是 Java 语法；移出代码并保留对应文字说明。
- 流式示意缺少 map 返回值，补 return request / return response，让其成为能表达数据流的框架片段，仍不宣称独立可运行。
- order 小的先处理请求、后处理响应，同值顺序无保证，不使用插入顺序替代。
- 请求与响应携带上下文状态，不能把共享状态误读为所有版本均共享同一个可变 Map 实例。历史 immutable/updateContext 说明限定为 1.0 M3。
- 原生 Re2 论文的效果只描述策略与出处，不保证所有模型都会提高准确率。
- SafeGuardAdvisor 是简单内容防护，不能承诺彻底消除有害输出。
- 日志聚合回调只能观察，不修改原流，不能将整个 Flux 输出改为单一响应。
- 图片保留来源 UML 与黄色流程框，仅中文化图例及说明，纠正旧 AdvisedResponse 标签。

## 语气与术语

沿用项目 baoyu-translate 配置：zh-CN / refined / technical，面向 Java / Spring Boot 开发者。Advisor 保留 API 名称；advisor chain → Advisor 链；order → 顺序值；recursive advisor → 递归 Advisor；downstream → 下游；observability → 可观测性；short-circuit → 短路；streaming → 流式。链式 API 与流式调用区分，所有 API、示例字符串保持英文，代码注释中文化。
