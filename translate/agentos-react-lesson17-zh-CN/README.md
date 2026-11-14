# ReAct 资料整理与项目对齐记录

正文为 `src/content/docs/projects/agent-os/react-loop.mdx`，路由为 `/projects/agent-os/react-loop/`。本文根据第 17 节课件整理，保留“原理 → 职责 → 实现 → 边界 → 验收”的学习顺序，并按当前 AgentOS 工程和 Spring AI 2.0.2 修订。

## 对齐结论

- 课件中的 OryxOS、Spring Boot 3.x、`ProfileContext` 和 `ThreadLocal` 没有直接沿用。
- 当前项目基线为 JDK 21、Spring Boot 4.1.2、Spring AI 2.0.2。
- 当前 Java 仓库仍是 Maven 工程骨架；正文给出 `ReActLoop`、`PromptBuilder`、`ToolExecutor` 和 `AgentService` 的实现契约与验收要求，不表示这些业务类已经全部实现。
- Spring AI 2.0 的 `ChatModel` 只返回 `ChatResponse`，工具执行统一交给注入的 `ToolCallingManager`；上下文通过 `ToolContext` 传递。

## 校订重点

- 把 ReAct 的 Reason 解释为可观察的下一步决策，不把隐藏思维过程当作需要保存的业务数据。
- 用 `ProviderRequest`、`ProviderResult`、`CallCorrelation` 和 `TurnContext` 对齐当前项目接口。
- 增加双重工具/迭代上限、四层超时、会话租约、按完整 Turn 截断历史和失败审计。
- 保留课件的单元测试 harness 和天气 Demo，但明确 Demo 不能替代边界测试。

## 验证范围

- PDF 已完成文本提取和页面渲染检查。
- 知识库正文应运行 `npm run check` 和 `npm run build`。
- 本次未修改 `/Volumes/Data/my_project/agent-os` Java 工程，也未执行真实模型、PostgreSQL 或生产环境验证。
