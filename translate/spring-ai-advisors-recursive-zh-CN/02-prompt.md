# 精翻上下文

## 语气与术语

沿用项目 baoyu-translate 配置：zh-CN / refined / technical，面向 Java / Spring Boot 开发者。Advisor 保留 API 名称；advisor chain → Advisor 链；order → 顺序值；recursive advisor → 递归 Advisor；downstream → 下游；observability → 可观测性；short-circuit → 短路；streaming → 流式。链式 API 与流式调用区分，所有 API、示例字符串保持英文，代码注释中文化。

完整翻译该页并保留所有代码块、图和文档链接，简明表述，不省略关键约束和历史版本边界。先初稿，再对照来源与接口审校、修订及润色。

约 777 个词，5 段代码，1 张图。保留递归机制、copy(this) 下游子链、工具循环、Schema 校验循环和自定义累计用量。篇幅低于分块阈值，主 agent 完成初稿与审校。

## 准确性风险

- 递归指重复执行自身之后的子链，不重跑此前的 Advisor，也不等同于递归 Java 方法调用。
- 本页说工具存在时自动注册，与当前 ChatClient / Advisors 中即使无静态工具也注册的说明不完整；统一采用后两页明确规则，标记当前版本条件。
- returnDirect 只在相应工具结果要求直接返回时跳出，不再交给模型。
- outputType 与 outputJsonSchema 互斥，默认最多尝试 3 次，不写为额外重试 3 次。
- Token 累计包含所有模型调用；UsageAccumulator 按 adviseCall 或流订阅创建，不能跨会话共享，也不能单例反复累积。
- 源代码循环示意省略 loopAgain 与 request 的变更逻辑，明确为伪代码骨架，不能宣称直接复制即可执行。
- 原生用量跨多次调用不能合并，关联已有响应元数据说明。
- 原图保留上下游框、条件菱形、返回方向与循环范围，仅覆盖中文说明；章节顶部增加短阅读建议，与译文主体区分。

中文图片沿用原图版式、配色和连线，不加入“官方”字样。发布页采用中文标题、说明与标签，正文从二级标题开始，末尾记录来源版本与日期。
