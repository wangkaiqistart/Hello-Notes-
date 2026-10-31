# 内容分析

来源：Spring AI 参考文档 2.0.2，采集日期 2026-10-31。英文→简体中文，refined，技术开发者，简明技术文档风格。

## 内容与范围

26 段代码与所有属性表；STDIO/Streamable-HTTP/SSE，Windows 进程启动，客户端作用域、定制、工具过滤、命名前缀、ToolContext 元数据与注解。

## 术语

Model Context Protocol → 模型上下文协议（MCP）；Client/Server → 客户端/服务端；transport → 传输；session → 协议会话；sampling → 采样；elicitation → 信息征询；Roots → 根目录（Roots）；capability negotiation → 能力协商；Tool Calling → 工具调用；ToolContext → 保留标识，解释为工具上下文。Streamable-HTTP、STDIO、SSE、SYNC、ASYNC、Java API 保留。

## 语气与结构

自然中文，准确交代配置入口和使用条件，避免翻译腔。代码、依赖坐标、配置键和参数原样保留；中文注释可简化。保留完整章节、属性、代码与图片，不将请求的 Starter 正文缩写成摘要。

## 翻译难点

- 协议会话与业务 ChatMemory 会话不等价；共享客户端不自动提供用户隔离。
- STDIO 通常连接由客户端启动的子进程，并非同一个 JVM 内的方法调用。
- Servlet Server 与 JDK HttpClient Client 分开；WebFlux 是传输实现，不等于 MCP ASYNC API 开关。
- 来源重复的 Streamable-HTTP 段可去重，但保留两个锚点和两段来源示例，避免丢失内容对照。
- 来源代码与正文可能有版本/示例缺陷，初稿保留，写入 draft-issues.md 供主 agent 结合源码审校。
- 部分外链损坏、SSE 弃用信息与默认协议矛盾，需审校；不凭印象增加版本事实。
- 图片放在用途说明之后；三张原图全部保留，禁止重绘。
