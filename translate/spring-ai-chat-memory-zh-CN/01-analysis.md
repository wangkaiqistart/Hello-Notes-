# Chat Memory 翻译分析

来源：https://docs.spring.io/spring-ai/reference/api/chat-memory.html 。版本 2.0.2，采集日期 2026-10-25。正文约 3274 个英文词，34 段代码，无图片；低于分块阈值，按单篇精翻。

## 内容与读者

面向熟悉 Java / Spring Boot 的开发者，解释多轮对话上下文、会话隔离、窗口淘汰、各类存储以及 ChatClient / ChatModel 接入。保持完整主题范围，数据库的专有配置按需阅读，不把前一个任务中“模型精选”的范围限制套用到本篇。

## 术语

| 原文                   | 用语                      |
| ---------------------- | ------------------------- |
| Chat Memory            | 对话记忆                  |
| Chat History           | 完整聊天历史              |
| Conversation ID        | 会话 ID                   |
| Message Window         | 消息窗口                  |
| Turn-boundary eviction | 按完整轮次淘汰            |
| Repository             | 存储实现；类名不译        |
| TTL                    | 生存时间（TTL）           |
| Advisor                | 保留 Advisor              |
| Prompt                 | 提示词；API 名保留 Prompt |
| Token                  | 词元（Token），后文 Token |

## 表达与风险

- 用自然、简洁的中文解释职责，不把窗口记忆称为完整历史。
- 20 条消息不等于 20 轮；按轮次边界淘汰可使实际数量低于上限。
- 会话 ID 必须显式提供；服务端分配并校验所属关系，不能把唯一 ID 当鉴权机制。
- Cassandra 属性表与正文前缀矛盾，消息列默认值和创建示例也有误；按 Maven Central 2.0.2 源码和同版本 Javadoc 核对后修正，并记录差异。
- JDBC 初始化示例把同一个属性重复三次并附带行尾注释，改为互斥选项的合法 properties 写法。
- 工具消息支持分两层：Advisor 是否采集中间消息，Repository 是否支持保存；不把来源旧式限制写成所有实现的永久限制。
- 保留所有 34 段代码、各存储家族与配置含义；英文示例输入保留，注释中文化。
- 源文无图片，不新增概念图。桌面与手机检查表格和代码的滚动范围。
