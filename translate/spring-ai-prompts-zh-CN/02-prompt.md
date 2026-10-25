# 翻译上下文

将 `../spring-ai-prompts.md` 改写为简洁自然的简体中文技术文档。读者熟悉 Java 与 Spring Boot，每周学习 10–15 小时，已读概念和快速入门，ChatClient 正在另行翻译。

使用项目 `.baoyu-skills/baoyu-translate/EXTEND.md` 与 `01-analysis.md` 的术语：提示词、消息、占位符、分隔符、模板渲染器、词元（Token）、思维链；类与方法标识符保持英文。

按 API 概览、示例、提示词工程、Token 保留来源结构。角色及重载说明可用表格压缩；所有 15 段代码与学习链接均保留，StringTemplate 的错误片内锚点改为有效站点链接。代码中的英语字符串、变量名、调用顺序不改，只翻译注释；`Content.getContent()` 根据 2.0.2 Javadoc 更新为 `getText()` 并显式说明这一修正。

图置于消息、多模态与角色职责的完整解释之后，保留来源画面布局，说明文字中文化，不添加“官方”字样。保持英文原始文件，用准确替代文本与短图注解释阅读重点。

审校以下边界：最后一条 USER / 第一条 SYSTEM；ASSISTANT 携带工具调用请求、TOOL 回传结果；render/createMessage/create 的返回类型不同；自定义 `< >` 解决模板与 JSON 花括号冲突；Resource 路径不变。将 CoT 错误描述澄清为中间推理步骤，旧模型 Token 上限不当作当前规格，英文词数比例不套用于中文。修正与省略在页面版本注中交代，禁止假称运行 Java 或调用过模型。

落地页面 `src/content/docs/frameworks/spring-ai/core/prompts.mdx`，标题“Spring AI：提示词”，路由跟随文件路径。精翻过程文件单独保存；最终 translation.md 与站点页面逐字节一致。
