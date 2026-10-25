# 初稿待主审核验项

本文件只诊断；初稿代码保留源文 API，注释已中文化。

1. `ToolExecutionEligibilityChecker strictChecker` 示例使用 `response.getMetadata().getFinishReason()`。需要核对 2.0.2 结束原因是否位于 `response.getResult().getMetadata()`，以及空结果的判断。
2. `MyAuditingToolCallingAdvisor` 示例声明了 `final AuditService audit`，构建器调用一个接收 5 个参数的构造器，但类中没有构造器；不能直接编译，需要补构造器并调用父类构造器。
3. `ToolCallObservingAdvisor` 示例声明 `final Consumer<ChatClientResponse> observer`，随后以带参构造器创建实例，但没有声明构造器；`log` 也未声明。需补齐或明确为框架片段；核对 Advisor 接口是否还要求 `getName()`。
4. 用户控制流式示例两次 `.options(chatOptions)`，主审已确认 2.0.2 请求级 API 需要 Builder，后续可改 `.options(chatOptions.mutate())`。
5. 用户控制流式示例没有在 `executeToolCalls` 后判断 `result.returnDirect()`，因此直接返回工具也会被继续发给模型。应主审修正，或明确该片段假定工具均不启用 returnDirect。
6. 用户控制流式示例使用 `.blockLast()`，是聚合后阻塞驱动的演示，不是完全非阻塞编排；说明此边界有助于避免复制到 WebFlux 事件线程。
7. “恰好一个 ToolAdvisor”表述需结合关闭自动注册的场景理解：默认工具循环约束不能推导为全局禁用后仍必须有一个实例。
8. 使用 `MemoryAdvisor` 的相关请求仍需每次传入 `ChatMemory.CONVERSATION_ID`，本页只演示构建器；可在主审阶段加简短提醒，避免照抄后缺参数。

初稿保留 12 段代码，全部显式来源章节锚点，原文无图片。未运行 Java。
