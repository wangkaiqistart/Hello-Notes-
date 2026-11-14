# 第 17 节 ReAct 项目对齐复核

## 事实基线

- `/Volumes/Data/my_project/agent-os/CLAUDE.md`：循环自实现，主链路直接调用 Spring AI `ChatModel`；工具只经 `ToolExecutor` 调用注入的 `ToolCallingManager`；上下文使用 `ToolContext`。
- `/Volumes/Data/my_project/agent-os/pom.xml`：JDK 21、Spring Boot 4.1.2、Spring AI BOM 2.0.2、9 个核心 Maven 模块。
- `/Volumes/Data/my_project/agent-os/AgentOS-core/src/main/java/com/agentos/core/provider/`：已有 `ProviderService`、`ProviderRequest`、`ProviderResult`、`Profile`、`CallCorrelation` 和 `LlmCallRecord` 契约；ReAct 业务实现尚未完成。
- `/Volumes/Data/my_project/agent-os/docs/TechnicalSolution.md`：定义 `TurnContext`、`ReActLoop`、`PromptBuilder`、`ToolExecutor`、会话租约、历史截断、超时和审计要求。
- 知识库的[ChatModel 工具调用](/frameworks/spring-ai/tools/chatmodel-tool-calling/)：说明 Spring AI 2.0 的手动工具循环、`ToolCallingManager`、`ToolExecutionResult`、`conversationHistory()` 和 `returnDirect()`。

## 与课件的主要差异

| 课件内容                                           | 当前项目修订                                            |
| -------------------------------------------------- | ------------------------------------------------------- |
| OryxOS、Spring Boot 3.x                            | AgentOS、Spring Boot 4.1.2、Spring AI 2.0.2             |
| `providerService.chat(sessionId, profile, prompt)` | `ProviderService.call(ProviderRequest)` / `stream(...)` |
| `ProfileContext` / `ThreadLocal`                   | `TurnContext` 放入 Spring AI `ToolContext`              |
| Provider 或框架自动执行工具                        | `ToolExecutor` 通过注入的 `ToolCallingManager` 唯一执行 |
| 只按最大轮数停止                                   | `max_iterations` 加 `spring.ai.tools.limits.*` 双重限制 |
| 最近 N 轮简单截断                                  | 按完整 Turn，同时受轮数和 Token 上限约束                |

## 未宣称为已完成的能力

当前工程仍处于骨架阶段，因此正文中的 `ReActLoop`、`PromptBuilder`、`ToolExecutor`、`AgentService`、`ContextLoader`、Session 持久化和 `tool_invocations` 都是实现契约或验收对象。编译通过、伪代码可读或天气 Demo 成功，都不能单独证明完整 ReAct 运行时已经交付。
