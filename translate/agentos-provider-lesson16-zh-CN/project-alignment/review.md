# Provider 文档复核与项目对齐

## 复核结论

正文已对照原 PDF、在线参考文档、2.0.2 发布源码，以及 `/Volumes/Data/my_project/agent-os` 的设计与当前代码修订。

当前项目锁定 Java 21、Spring Boot 4.1.2、Spring AI 2.0.2，仍处于工程骨架阶段。ProviderService、AgentLoader、Profile 和业务迁移脚本尚未实现。正文描述实现契约与验收要求，不将设计中的类、持久化和治理行为写成已完成能力。此次未修改 Java 项目。

## 已落实的优化

本轮又按原 PDF 的叙事顺序重排正文：先讲 Provider 定位，再讲职责、复用边界和三个常见坑；随后按第零步到第七步说明 Profile、配置、具名映射、请求、工具、响应、审计和 Embedding；最后单列验收 harness 与人工验收。这样保留原文的阅读节奏，同时不恢复旧版 API 或旧项目实现。

| 复核项       | 修订结果                                                                                                                                      |
| ------------ | --------------------------------------------------------------------------------------------------------------------------------------------- |
| 工程事实源   | 使用本次指定的 `agent-os`，清除旧 `java-agent-os` 的 `.aegisos`、SQLite、ProviderAdapter、自定义 ModelRequest/ModelResponse 等设计残留        |
| Agent 定义   | 使用 `.AgentOS/agents/<name>/AGENT.md`，frontmatter 派生 Profile；正文作为任务指令；明确自定义加载器需解析环境占位符                          |
| 配置分工     | 连接放在 `application.yaml` 的 `agentos.providers` 映射中；Agent 显式选 provider 和聊天 model；不引入聊天默认模型或模型白名单                 |
| 协议与客户端 | 具名 Map 显式路由；直接使用 Prompt、Message、ChatResponse 和 ToolCallback，避免重建一套协议                                                   |
| 工具执行     | 沿用注册表中的 GovernedToolCallback；Provider 仅传定义；ToolExecutor 使用注入的 ToolCallingManager；移除仅含 Schema、执行抛异常的占位回调方案 |
| 请求参数     | 提供两个可编译示例，显式填写 model、reasoningEffort、maxCompletionTokens、timeout、工具与上下文；说明直接 ChatModel 请求 Options 的替换语义   |
| 请求路径     | 纠正显式 base URL 一定自动补 `/v1` 的假设，使用 API 前缀并要求断言最终 HTTP 路径                                                              |
| 重试         | SDK 客户端构建时设置 maxRetries(0)；Provider 最多追加一次尝试，受整轮预算、退避、取消与流式输出状态约束                                       |
| 响应与循环   | 保留仅工具响应、调用 ID 和顺序；使用 conversationHistory，处理 returnDirect；流式聚合完整工具请求后再执行                                     |
| 审计         | 对齐 PostgreSQL、JPA、Flyway 与 llm_calls 字段；每次尝试分别记账；移除旧工程 begin/complete、UNKNOWN 结果枚举和不存在的审计错误码             |
| 缺失元数据   | 区分 EmptyUsage、EmptyRateLimit、NULL 和真实零值；请求模型与响应模型分别保存                                                                  |
| Embedding    | 说明独立全局模型及向量一致性，区分聊天模型的 Agent 级选择                                                                                     |
| 图片         | 概览与职责图保持原样；调用图保留布局配色，更新流程标签、审计步骤和 ChatResponse 返回类型                                                      |

原 PDF 中仍适用的薄 Provider、显式映射、配置分层、成功失败审计和真实请求验收原则已保留。依赖、工具执行和配置路径以当前目标技术与项目设计重新核对。

## 与目标项目仍存在的差异

以下是待实施事项，本次没有替用户改动 Java 项目：

1. `application.yaml` 与 `docs/TechnicalSolution.md` 仍含 `default-provider`、provider 级 `model` 和默认推理强度。正文按用户已明确的选择编写：聊天连接不选默认模型，每个 Agent 显式选择。后续需同步配置、绑定类、AgentLoader 校验和设计文档；独立辅助 ChatClient 的固定模型属于另一条调用链。
2. 项目配置将 `spring.ai.retry.max-attempts: 1` 注释为关闭模型重试。2.0.2 的 OpenAI 客户端通过 SDK 构建，不能仅凭这个属性认定编程式客户端已关闭重试。应在工厂中设置 maxRetries(0)，并核对辅助自动配置客户端及其他协议客户端。
3. 项目示意地址有的未带 API 前缀。2.0.2 OpenAiSetup 对显式 base URL 原样使用；需要逐个兼容端点验证路径，Embedding 也独立验证。
4. 运行时、工具执行、数据库审计和流式聚合尚未落地，文章中的验收表应作为后续实现标准，不能用现有骨架测试报告替代。

## 证据与验证

- 原 PDF：8 页，SHA256 `add507b4304ed0c4d3ef1f6ec73507df6abf70767533e609f73f57e8a34c301c`；完整路径与提取记录见上级 `source-metadata.json`、`source.txt`。
- 项目证据：`pom.xml`、`docs/TechnicalSolution.md`、`AgentOS-boot/src/main/resources/application.yaml`、模块 package-info 与架构约束测试。项目文件基线见 `project-baseline.json`。
- 在线文档：ChatModel Tool Calling、Chat Model API、OpenAI Chat、Tool Calling、Embeddings Model API；URL 与内容哈希见 `official-docs/sources.json`。
- 发布源码：2.0.2 的模型、工具、SDK 装配与元数据接口，下载坐标、入口与哈希见 `api-sources/sources.json`。例如 AbstractOpenAiOptions 的默认 SDK 重试数为 3，而在线配置表仍列出另一套重试默认值；正文因此采用显式关闭及行为验证，不照搬默认次数。
- 两个 Java 示例从最终 MDX 原样提取，使用 JDK 21 与项目 2.0.2 实际依赖离线编译；历史 Surefire XML 仅用于定位依赖 classpath，不作为本轮测试执行证据。
- `ProviderProtocolCheck.java` 驱动真实客户端访问本机 HTTP 替身。验证 Agent 参数、最终路径、工具定义、仅工具响应、响应模型、用量、ToolContext 不外传、回调未执行、503 不触发 SDK 重试、空 model 外呼前拒绝。合计 3 次本地 HTTP 请求、0 次工具执行，结果见 `snippet-validation.json`。
- 完整项目测试、真实模型冒烟、PostgreSQL 集成与流式端到端：未执行；本次协议验证不代表这些能力已实现。
- 站点检查、构建、浏览器与文件保护结果见上级 `content-validation.json`、`browser-validation.json`。

## 官方阅读入口

- [ChatModel Tool Calling](https://docs.spring.io/spring-ai/reference/api/tools/chatmodel-tool-calling.html)
- [Chat Model API](https://docs.spring.io/spring-ai/reference/api/chatmodel.html)
- [OpenAI Chat](https://docs.spring.io/spring-ai/reference/api/chat/openai-chat.html)
- [Tool Calling](https://docs.spring.io/spring-ai/reference/api/tools.html)
- [Embeddings Model API](https://docs.spring.io/spring-ai/reference/api/embeddings.html)

正文保持独立技术文档风格；资料来源、版本核验和工程差异统一留在本复核记录中。
