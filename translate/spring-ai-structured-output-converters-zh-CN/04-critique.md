# 审校

## 准确性

- 来源多个底层示例声明局部变量后却用 this 引用；修订为对应局部变量，保留提示词、返回类型和调用过程。格式拼装例保留骨架性质，补分号并用 StructuredOutputConverter<?>。
- v2.0.2 BeanOutputConverter 源码实际包含空白、思考标签、Markdown 围栏清理，不能断言“只要有围栏就失败”或“必然在 Here's 的 H 处抛错”。应说明已有默认清理，需要特殊输出规则时再自定义。
- 自定义 FENCE 只匹配第一个小写 json / 无语言标记围栏，未匹配时仍可能解析失败，不宣称通用提取。
- getJsonSchema 默认空字符串可从已存源码确认；两项可靠性开关需要有效 Schema。
- 高层 .entity(ParameterizedTypeReference<Map<...>>) 只指定目标类型，不应断言一定选择 MapOutputConverter；显式 MapOutputConverter 与 ListOutputConverter 的路径分开说明。
- 来源类图的 ObjectMapper 已过时，2.0.2 使用 tools.jackson.databind.json.JsonMapper；API 图 ChatModel.call(Prompt) 返回 ChatResponse，文本应从响应提取。修图只覆盖这两处标签及说明文字，保留节点连线。

## 表达与合并

- PromptTemplate 本地链接需指向实际章节 prompttemplate将模板转换为提示词。
- 主文已定义 ActorsFilms，合并时不重复定义；分篇定稿仍保留来源代码块。
- 代码中嵌入 Markdown 围栏的示例外层用四反引号，避免截断渲染。
- Schema 顺序仅指生成 Schema 的属性顺序，不扩展为模型或所有序列化输出的绝对顺序。
