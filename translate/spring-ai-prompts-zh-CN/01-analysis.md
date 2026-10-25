# Prompts 翻译分析

日期：2026-10-25。来源：Spring AI 2.0.2 的 Prompts 章节。

## 内容与结构

面向 Java 开发者，解释 Prompt、Message、角色、PromptTemplate 与 TemplateRenderer，再介绍变量、Resource、提示词工程和 Token。约 2831 个空格分隔单元，低于项目 4000 分块阈值；整篇执行分析、初译、审校、修订和润色。

保留 15 个代码块（含重复的自定义分隔符示例）、全部学习资源链接和一张消息类图。压缩重复说明，用表格整理 API 的重载和角色职责，不省略方法的行为差异。

## 术语

| 来源                             | 译法                          |
| -------------------------------- | ----------------------------- |
| Prompt                           | 提示词；类名保留 `Prompt`     |
| Message                          | 消息；类名保留 `Message`      |
| System / User / Assistant / Tool | 系统 / 用户 / 助手 / 工具     |
| TemplateRenderer                 | 模板渲染器；标识符保留        |
| placeholder / delimiter          | 占位符 / 分隔符               |
| Fluent API                       | 链式 API                      |
| streaming                        | 流式响应                      |
| Token                            | 首次词元（Token），后文 Token |
| Chain-of-Thought                 | 思维链（CoT）                 |
| zero-shot / few-shot             | 零样本 / 少样本               |

## 风格与边界

简体中文、面向熟悉 Java / Spring Boot 的开发者，句子简短，解释职责与工程含义；保留类、方法、枚举、路径、示例字符串与变量名，翻译 Java 注释。不给英语示例字符串换语言，便于逐块核对。

## 需要审校的来源问题

- 来源简化 `Content` 声明和类图仍使用 `getContent()`。已获取 2.0.2 Content Javadoc，实际方法为 `getText()`。译稿明确标注修正，类图保持原有布局而同步修正该方法名；英文原始快照和图片不变。
- 原文把思维链说明为对话串联。应按其链接的 Prompt Engineering Guide，解释为通过中间推理步骤处理复杂任务，不与 Chat Memory 混淆；在页面标注澄清。
- 原文以旧型号举例 Token 上限，且笼统给出 Llama 2 的 100K 数字，不作为当前规格复述。保留限制的含义，要求按具体型号查询，明确说明省略旧规格示例。
- `render()` 无参不等于永远没有变量：模板可能已有变量。用“不额外传入变量”描述，避免概括成只支持静态模板。
- `Prompt` 的 user 取最后一条、system 取第一条；工具结果属于 TOOL，工具调用请求可包含在 ASSISTANT 中。
- Token 与英文单词的 3/4 关系只作英文粗估，不可套用中文；保留莎士比亚例子并限定估算性质。
- 图片使用原始黄色 UML 布局与连线，仅翻译图题、图例、说明文字，API 标识符保留英文。与原有已接受图片相互独立。
