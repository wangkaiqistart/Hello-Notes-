---
title: Spring AI：递归 Advisors
description: 理解下游处理链的重复执行、工具调用与结构化输出校验循环，以及每轮模型调用的累计用量。
sidebar:
  label: 递归 Advisors
  order: 2
---

建议先阅读 [Advisors API](/frameworks/spring-ai/core/advisors/)。本篇先掌握循环范围与执行顺序；自定义循环和用量统计可以结合工具调用实践深入。

## 什么是递归 Advisor

递归 Advisor 可以多次执行其后的处理链，直到满足停止条件。常见用途包括：

- 反复执行模型请求的工具，直到模型不再要求调用工具。
- 校验结构化输出，失败后重新请求。
- 评估结果，并修改请求后再次调用模型。
- 根据重试条件调整请求后继续执行。

核心方法是 `CallAdvisorChain.copy(CallAdvisor after)`：根据原链创建一条新链，只包含指定 Advisor **之后**的部分。递归 Advisor 可按需要重复调用这条下游子链。

这样既能让下游 Advisor 观察、拦截每轮交互，保留顺序与可观测性，也不会重新执行递归 Advisor 之前的组件。

下图用黄色虚线标出可重复执行的范围：上游 `ABC` 位于循环外，`XYZ` 和模型位于下游；递归 Advisor 的条件判断决定继续循环还是向上返回。

<a href="/images/frameworks/spring-ai/advisors-recursive-zh.svg">
  <img
    src="/images/frameworks/spring-ai/advisors-recursive-zh.svg"
    alt="递归 Advisor 循环范围：上游 ABC 在循环外，下游 XYZ 和模型可重复执行，由条件判断决定是否结束"
    width="291"
  />
</a>

重点看虚线循环范围及上下行箭头；点击可查看大图。

## 内置递归 Advisor

Spring AI 提供两个内置实现：工具调用循环与结构化输出校验。

### ToolCallingAdvisor：工具调用循环

`ToolCallingAdvisor` 在 Advisor 链中驱动工具调用，而不是依赖每个 `ChatModel` 内部实现循环。它是 `ChatClient` 组织工具增强对话的默认机制。

主要行为：

- 反复执行下游链，直到 `ToolExecutionEligibilityChecker` 判断无需继续工具调用。
- 通过 `callAdvisorChain.copy(this)` 创建下游子链，其他下游 Advisor 可以观察并拦截每轮执行。
- 支持直接返回：工具结果要求 `returnDirect = true` 时退出循环，将工具结果直接交给调用方，不再发回模型。
- 实现 `ToolAdvisor` 标记接口，供 `DefaultChatClient` 识别已有工具 Advisor，避免重复自动注册；自定义子类也能作为替代实现。
- 累加每轮模型调用的 Token 用量，最终 `ChatResponse` 返回整个循环的累计值。

手动配置示例：

```java
var toolCallingAdvisor = ToolCallingAdvisor.builder()
    .toolCallingManager(toolCallingManager)
    .advisorOrder(BaseAdvisor.HIGHEST_PRECEDENCE + 300)
    .build();

var chatClient = ChatClient.builder(chatModel)
    .defaultAdvisors(toolCallingAdvisor)
    .build();
```

当前版本中，除非明确禁用，工具 Advisor 即使没有静态工具也会自动注册，以支持运行时动态加入工具。

自动注册和禁用方式见 [ChatClient：工具调用](/frameworks/spring-ai/core/chat-client/#工具调用)。构建器、扩展钩子、记忆 Advisor 顺序、用户控制执行及自定义子类，见 [ToolCallingAdvisor](https://docs.spring.io/spring-ai/reference/api/tools/tool-calling-advisor.html)。

更多资料：

- [工具调用循环](https://docs.spring.io/spring-ai/reference/api/tools.html#the-tool-calling-loop)：了解它在整体工具调用架构中的位置。
- [Tool Search Tool](https://docs.spring.io/spring-ai/reference/api/tools/tool-search-tool.html)：通过扩展钩子实现按需暴露工具的子类示例。
- [多步流程的累计用量](/frameworks/spring-ai/core/chat-response-metadata/#多步流程的累计用量)：理解循环的 Token 统计。

### StructuredOutputValidationAdvisor：结构校验循环

`StructuredOutputValidationAdvisor` 按 JSON Schema 校验模型输出；失败后补充具体错误并重新请求，直到成功或达到次数上限。

主要能力：

- 从目标 Java 类型生成 Schema，或接收现有 Schema 字符串。
- 校验模型返回的 JSON，失败时将错误信息加入提示词，帮助模型自行纠正。
- 默认最多尝试 **3 次**，可配置上限。
- 使用 `callAdvisorChain.copy(this)` 重复执行下游链。
- 累加所有尝试的用量，最终报告累计值，而不只是最后一次的用量。
- 可选配置自定义 `JsonMapper`。

**`outputType` 与 `outputJsonSchema` 互斥，只能选择其中一种。**

根据 Java 类型生成 Schema：

```java
var validationAdvisor = StructuredOutputValidationAdvisor.builder()
    .outputType(MyResponseType.class)
    .maxRepeatAttempts(3)
    .build();

var chatClient = ChatClient.builder(chatModel)
    .defaultAdvisors(validationAdvisor)
    .build();
```

使用已有 Schema：

```java
var validationAdvisor = StructuredOutputValidationAdvisor.builder()
    .outputJsonSchema(myConverter.getJsonSchema())
    .build();
```

也可以直接在 `entity()` 中启用校验，无需手动创建 Advisor：

```java
ActorFilms actorFilms = chatClient.prompt()
    .user("Generate the filmography for a random actor.")
    .call()
    .entity(ActorFilms.class, spec -> spec.validateSchema());
```

高层用法见[结构化输出](/frameworks/spring-ai/core/structured-output/)，详细流程见 [Schema 校验与自动纠正](https://docs.spring.io/spring-ai/reference/api/structured-output/validation.html)。

## 自定义递归 Advisor 的用量累计

递归 Advisor 一次执行可能调用多次模型。如果只返回最后一轮响应，调用方就只能看到最后一轮用量。

`org.springframework.ai.chat.client.advisor.UsageAccumulator` 用于累计这些用量：

1. 每次 `adviseCall()` 创建一个新实例。
2. 每轮得到响应后，调用 `addRoundResponse(...)` 累加用量。
3. 返回前，用 `applyAccumulatedUsage(...)` 将累计值写入最终响应。

如果实现流式循环，应在 `Flux.defer` 内创建实例，使它属于本次订阅。不要跨调用或跨订阅复用同一个累计器。

```java
UsageAccumulator usage = new UsageAccumulator();
ChatClientResponse response;
do {
    response = callAdvisorChain.copy(this).nextCall(request);
    usage.addRoundResponse(response.chatResponse());
    // ... 根据本轮结果决定是否继续，并更新下一轮请求 ...
}
while (loopAgain);
return usage.applyAccumulatedUsage(response);
```

上例是循环骨架：`request`、`loopAgain` 和停止策略需由实现者提供，并按每轮结果更新。

底层计算由 `org.springframework.ai.support.UsageCalculator` 的 `accumulateResponseUsage`、`withUsage` 等方法完成，`UsageAccumulator` 对其进行了封装。

多个模型调用合并后，提供方原生用量对象不能合并，`getNativeUsage()` 会返回 `null`，详见[累计用量的限制](/frameworks/spring-ai/core/chat-response-metadata/#多步流程的累计用量)。

回到 [Advisors API](/frameworks/spring-ai/core/advisors/)，或先学习[工具调用](https://docs.spring.io/spring-ai/reference/api/tools.html)，再结合实际循环深入本篇。

来源：[Spring AI Recursive Advisors](https://docs.spring.io/spring-ai/reference/api/advisors-recursive.html)。文档版本：2.0.2；核验日期：2026-10-25。
