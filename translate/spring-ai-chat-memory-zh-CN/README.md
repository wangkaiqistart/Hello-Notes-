# 对话记忆精翻记录

日期：2026-10-25。来源：[Chat Memory](https://docs.spring.io/spring-ai/reference/api/chat-memory.html)，版本 2.0.2。使用项目 baoyu-translate 配置：zh-CN、refined、technical。

- [英文正文](../spring-ai-chat-memory.md) · [来源 HTML](source-article.html) · [来源清单](source-manifest.json)
- [站点正文](../../src/content/docs/frameworks/spring-ai/core/chat-memory.mdx) · [定稿](translation.md)
- [分析](01-analysis.md) → [翻译上下文](02-prompt.md) → [初稿](03-draft.md) → [审校](04-critique.md) → [修订](05-revision.md) → [定稿](translation.md)

## 范围与导航

覆盖完整主题：记忆与完整历史的区别、会话 ID、消息窗口及完整轮次淘汰、七类存储、ChatClient 的两种记忆 Advisor，以及直接 ChatModel 管理上下文。保留全部 34 段代码，原文无图，没有新增配图。

导航放在“Spring AI → 模型”小节之后，与 ChatClient API、Advisors API 同级；并非模型小节的子页面。README 的阅读入口与已完成列表同步更新，规划总数仍为 26 篇。

## 校正与优化

| 项目               | 来源问题或易误解处                                           | 定稿处理与证据                                                                                       |
| ------------------ | ------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------- |
| Cassandra 前缀     | 属性表漏掉 `repository`。                                    | 使用 `spring.ai.chat.memory.repository.cassandra`；见 `source-cassandra-properties.java`。           |
| Cassandra 消息列   | 表中写为 `springframework`。                                 | 改为 `messages`，与 `CassandraChatMemoryRepositoryConfig.DEFAULT_MESSAGES_COLUMN_NAME` 一致。        |
| Cassandra 手动创建 | 把 Builder 传给要求配置对象的 `create(...)`。                | 补 `.build()`；见同版本 Config.Builder 与 Repository Javadoc。                                       |
| Cassandra 连接参数 | 来源把本地连接值列为默认值。                                 | 使用 Spring Boot 的 kebab-case 配置键，将这些值明确列为示例，要求填写实际集群信息。                  |
| JDBC 初始化        | 同一个键连续写三次，且使用 properties 不支持的行尾注释方式。 | 保留一个生效选项，其余作为独占行注释，明确三选一。                                                   |
| 向量记忆模板       | 来源写 `.promptTemplate()`。                                 | 按 2.0.2 Builder 改为 `.systemPromptTemplate()`，正文提供版本化 API 链接。两个占位符也对照源码核验。 |
| 工具消息限制       | 来源有笼统的“当前实现不保存中间消息”表述。                   | 区分默认 Advisor 位于循环外与 Repository 过滤消息，结合 `ToolCallingAdvisor` 源码解释条件。          |
| 窗口与轮次         | 20 条可能被误解为 20 轮或精确保留数。                        | 明确按完整轮次淘汰、实际数量可更少、单轮超过窗口可能清空非系统消息。                                 |
| 可复制性           | 来源把字段注入和记忆构建紧邻书写。                           | 提醒在依赖注入完成后构建，例如放入 `@Bean` 方法，不要复制成字段初始化器。                            |

## 核验材料

- [代码对照](code-fidelity.json)：34 段代码中，32 段除注释和空白外与来源一致；另外 2 段是上述 JDBC properties 与 Cassandra `.build()` 校正。
- [API 与源码核验](api-contract-checks.json)：14 项关键断言，来自 Maven Central 的 2.0.2 sources.jar 与同版本 Javadoc；源码快照保存在本目录，保留许可证声明。
- [外链核验](external-links.json)：8 个外部页面及引用锚点检查通过。社区 JDBC Session、Cosmos DB 页面曾连接超时，独立重试均成功。
- [页面验证](validation.jsonl)：内容、构建、导航、站内链接、桌面和移动端检查。
- Java 示例仅做原文与 API 静态核对，未编译运行、未连接数据库、未调用真实模型。

`npm run check`：0 错误、0 警告、0 提示；`npm run build`：132 页生成成功。桌面 1440px、手机 390px 的导航、站内链接和锚点正常，无页面横向溢出、脚本错误或粗体标记残留；34 个代码块均正常渲染。定稿与站点正文逐字节一致。

## 2026-11-01 阅读结构调整

将核心概念与 ChatClient 接入前置，数据库配置集中为存储参考，向量记忆模板与直接 ChatModel 调用归入进阶区。原有 30 个章节、34 段代码与旧锚点均保留，新增存储选择表和工具循环记忆的站内入口。

修订、定稿与站点正文同步；代码对照的 `block` 保留来源序号，新增 `targetBlock` 指向当前页面位置，原有校正说明保持。以[结构调整记录](2026-11-01-structure.md)为本次验证依据，历史核验材料保留。

## 2026-11-01 官网覆盖审计

逐节核对实时官网正文：33 个子章节、34 段代码、29 个配置项均覆盖。补齐自定义 Repository 扩展入口及 JDBC 嵌入式初始化的数据库示例；未删除原有内容。详细对照与差异说明见[覆盖审计](2026-11-01-coverage-audit.md)。当前页面哈希以本次审计 JSON 为准，结构调整记录保留补充前的历史快照。
