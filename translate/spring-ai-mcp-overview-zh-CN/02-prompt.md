# 翻译上下文

目标 zh-CN；技术开发者；简明准确的中文技术文档。内容来源 Spring AI 2.0.2：协议、Java SDK 三层架构、Client/Server 职责、Boot Starter 矩阵、注解概览与 2.0 迁移。

统一术语：MCP=模型上下文协议；transport=传输；sampling=采样；elicitation=信息征询；roots=根目录（Roots）；session=协议会话。保留所有 API/依赖/配置/代码字符串。按当前项目技术文档风格，代码注释可译，正文需自然简洁且完整。

保留所有标题、显式英文 <a id="..."> 锚点、属性表、代码段和来源图片。不要伪造配图或删减配置表。不添加 frontmatter，保留来源 H1 供主 agent 集成。所有代码围栏必须独占行，保留正确缩进。来源缺陷记入 draft-issues.md，不擅改代码。新链接保持来源 URL，主 agent 再统一本地化。

STDIO 不是“同一进程”；WebFlux 与 ASYNC 不等同；共享协议会话不等于用户边界。JSON 示例路径应保留转义。来源含标题附近奇怪 |、<em URL 为抽取/原文问题，可修正格式并记录。Client Windows node 通常 exe 不应一概说 .cmd；进度不一定 0..1；配置和 API 问题先记录。
