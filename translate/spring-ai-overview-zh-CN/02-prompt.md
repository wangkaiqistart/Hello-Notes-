# 翻译上下文

## 目标读者与风格

简体中文；熟悉 Java / Spring Boot 的开发者；technical 风格，简明、准确、自然，避免翻译腔。源文是官方参考文档。用户要求使用 baoyu-translate refined 模式精修之前两篇文档，保留之前确定的简明风格和原图。

## 内容背景

Spring AI 官方 Overview，说明其目标是连接企业数据、API 与 AI 模型，列出跨提供方抽象、模型类型、结构化输出、向量存储、工具、MCP、ETL、ChatClient、Advisors、对话记忆、RAG、可观测性和评估。

## 合并术语表

| 英文 | 本次用法 |
| --- | --- |
| Embedding | 首次写“嵌入（Embedding）”，强调内容的向量表示；嵌入模型负责向量化。 |
| Token | 首次写“词元（Token）”，后文保留 Token；不等同于单词或汉字。 |
| Prompt / Prompt Engineering | 提示词 / 提示词工程。 |
| Prompt Stuffing | 提示词填充：将参考资料补充进提示词。 |
| RAG | 检索增强生成：检索相关内容后再补充提示词。 |
| Tool Calling | 工具调用；模型提出请求，应用执行。 |
| Fluent API / streaming | 链式 API / 流式调用；两者不能混淆。 |
| Portable API | 可跨提供方复用的 API；不承诺厂商功能完全一致。 |
| Structured Output | 结构化输出；区分文本、JSON 文本和 Java 对象。 |
| ETL | 提取、转换、加载。 |
| MCP | 模型上下文协议（Model Context Protocol）。 |
| Hallucination | 幻觉。 |

## 翻译难点

1. 原译述保留核心功能，但跨提供方 API、Advisors 的可复用性不够明确。
2. 原译述把可观测性和评估合并，需区分观察调用与判断回答质量。
3. 统一嵌入、RAG、MCP、ETL 等首次出现的定义。
4. 源文列举的数据库可精简为示例，但保留完整列表的权威链接。
5. 现有原图与位置已验证，保留图片引用及图注，不改变资源。

## 原则

准确优先，保留逻辑、条件和执行主体，使用自然中文短句。首现专业术语中英对应，品牌/API/代码保持原名。保留现有 MDX frontmatter、图像引用与版式；必要时恢复被压缩掉的关键语义及具体官方文档链接。不能把现有准确内容包装为本次纠错，不为了显示修改而改写。历史型号数字不作为当前规格，相关取舍在审校记录中说明。
