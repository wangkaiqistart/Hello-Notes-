# 精翻上下文

将 Spring AI 2.0.2 Chat Memory 正文整理成中文知识库文章。配置来自项目 `.baoyu-skills/baoyu-translate/EXTEND.md`：zh-CN、refined、technical audience、technical style。

读者熟悉 Java / Spring Boot，每周学习 10–15 小时，已经阅读 ChatClient、Advisors、提示词、结构化输出、多模态与模型小节。先讲清原理与默认行为，再按需查存储配置。用中文标题、简短自然的技术说明，避免宣传、逐句翻译腔和翻译过程旁白。

术语统一：Chat Memory 对话记忆，Chat History 完整聊天历史，Conversation ID 会话 ID，Message Window 消息窗口，turn 轮次，TTL 生存时间，Prompt 提示词；Advisor、API、类名、方法、配置键保持原样。Embedding、Token 沿用项目词表。

正文必须覆盖：ChatMemory / Repository 分工与历史边界；自动配置；会话 ID 与用户隔离；默认 20 条消息与完整轮次淘汰；内存、JDBC、Cassandra、Neo4j、Cosmos DB、MongoDB、Redis；两种记忆 Advisor 和模板占位符；直接 ChatModel 维护上下文。

34 段代码按顺序保留，注释可翻译。仅在有 2.0.2 API 或源码证据时改正错误：Cassandra 配置前缀、消息列默认值、builder.build()；JDBC 初始化配置改成三选一的合法示例。区分工具循环采集与存储支持。完整轮次过大时可能淘汰全部非系统消息；不能把 maxMessages 当成轮数或精确保留条数。

本地已有主题可用站内链接，保留原始来源链接与版本日期。原文无图，不造图。公开正文不记录审校过程，过程与验证留在本目录。
