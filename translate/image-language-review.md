# Spring AI 配图中文化

日期：2026-10-25。除 Token 示例外，其余 7 张示意图沿用来源图稿的版式、配色、图标与连线，只替换组件和流程标签；Logo 保留原样。Token 图改用短句展示真实的中英文切分。

图中不添加额外标题栏、卡片背景、说明页脚或来源字样。来源入口统一保留在正文末尾。

| 图片       | 当前处理                                                                          | 文件                                                                               |
| ---------- | --------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| 集成关系   | 保留左右应用与模型、中央图标和上下双向箭头，中文替换数据、API、应用与请求响应标签 | [中文图](../public/images/frameworks/spring-ai/spring-ai-integration-zh.svg)       |
| 模型类型   | 保留输入、模型、输出三列，以及四组能力和黄色节点                                  | [中文图](../public/images/frameworks/spring-ai/spring-ai-model-types-zh.svg)       |
| Embedding  | 保留原始散点图、连接曲线、词语和向量示例，只翻译组件标签                          | [中文图](../public/images/frameworks/spring-ai/spring-ai-embeddings-zh.svg)        |
| Token      | 用短句展示真实的中英文分词；以颜色区分 Token，标明数量、分词器及空格              | [示例图](../public/images/frameworks/spring-ai/spring-ai-tokens-zh.svg)            |
| 结构化输出 | 保留调用前后分区、转换器范围与回转连线                                            | [中文图](../public/images/frameworks/spring-ai/spring-ai-structured-output-zh.svg) |
| 提示词填充 | 保留问题与资料合并、提示词展开、模型输出的横向布局                                | [中文图](../public/images/frameworks/spring-ai/spring-ai-prompt-stuffing-zh.svg)   |
| RAG        | 保留上方 ETL、下方运行时检索、共享向量库与文档图标                                | [中文图](../public/images/frameworks/spring-ai/spring-ai-rag-zh.svg)               |
| 工具调用   | 保留原有六个编号、绿色工具、黄色模型与请求分派连线                                | [中文图](../public/images/frameworks/spring-ai/spring-ai-tool-calling-zh.svg)      |

## 示例与来源

Token 示例由 `tiktoken` 的 `cl100k_base` 编码器实际生成：中文“这是一个测试。”为 5 个 Token，英文“ChatGPT generates tokens.”为 6 个 Token。每段按真实边界着色，使用 `·` 显示空格。原文、Token ID 与解码片段保存在 [token-example.json](token-example.json)；没有手工指定分词边界。Embedding 的词语、散点与向量示例继续保留原始内容，数值标注为示意。

7 张结构图通过 SVG 将中文标签叠加到内嵌的原始图稿上，保持图形与连接位置一致；Token 图单独以 SVG 文字和色块绘制，无需外部图片地址即可加载。原始文件没有改写，校验值见 [spring-ai-images-before.json](spring-ai-images-before.json)。

- [Spring AI Overview](https://docs.spring.io/spring-ai/reference/index.html)
- [Spring AI Concepts](https://docs.spring.io/spring-ai/reference/concepts.html)
- 两份 `translation.md` 同步当前页面；历史翻译稿与过程记录保留当时版本。
- 当前图片与页面核验：[image-validation.jsonl](image-validation.jsonl)。
