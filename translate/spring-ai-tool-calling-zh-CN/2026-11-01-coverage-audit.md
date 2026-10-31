# 工具调用四篇官网覆盖审计

日期：2026-11-01。审计当前官网正文与当前站点，保留此前阅读结构。

## 结论

未发现需要补译的官网内容。本轮未修改站点正文、代码、图片或导航。四篇官网正文去除网站导航后，与此前保存的来源一致；当前页面哈希与结构调整记录一致。

| 页面                                                                      | 官网子章节 | 代码块 | 图片 | 内容表格 | 结果   |
| ------------------------------------------------------------------------- | ---------- | ------ | ---- | -------- | ------ |
| [工具调用基础](/frameworks/spring-ai/tools/tool-calling/)                 | 41         | 38     | 6    | 5        | 已覆盖 |
| [工具调用 Advisor](/frameworks/spring-ai/tools/tool-calling-advisor/)     | 15         | 12     | 0    | 2        | 已覆盖 |
| [工具搜索](/frameworks/spring-ai/tools/tool-search-tool/)                 | 17         | 17     | 1    | 5        | 已覆盖 |
| [ChatModel 工具调用](/frameworks/spring-ai/tools/chatmodel-tool-calling/) | 12         | 8      | 0    | 0        | 已覆盖 |

合计 **85 个子章节、75 段代码、7 张图片、12 张内容表格**。表格共 51 行，其中 17 项配置属性、11 项构建器选项；其余为工具定义方式、钩子、检索策略与淘汰策略。

## 重点核对

- 基础篇：工具定义与注册、AOT、默认与请求级工具合并、工具循环、记忆位置、存储兼容性、MCP 名称冲突和过滤、参数增强、手动执行、扩展钩子、Schema、上下文、直接返回、异常、次数限制、解析回退、观测与日志。
- Advisor 篇：构建器与执行判定、内部历史、阻塞与流式钩子、子类与 Builder 复制、单实例约束、手动流式循环、中间事件、直接返回与关闭自动注册。
- 工具搜索篇：适用条件、安装、搜索流程、会话、三种索引、继承与新增选项、ToolIndex API、五类淘汰策略、Boot 自动配置与示例。
- ChatModel 篇：适用范围、不自动执行工具、请求级与默认工具、覆盖规则、阻塞与流式手动循环、上下文合并、直接返回。

## 示例与图片

75 段代码逐段映射到来源：63 段除注释和空白外相同；12 段为此前有记录的 API 校正、必要分支补充或入门示例调整。它们保留对应主题与用法，没有将整段主题删掉。完整差异原因和位置见[机器记录](2026-11-01-coverage-audit.json)。

7 张图均重新下载官网当前文件比较，与本地资源及原始清单逐字节一致；页面引用、替代文本和原尺寸查看入口保留。

## 有意保留的差异

以下写法与官网不同，沿用此前源码核验后的校正，不将纠错回退成直译：

- 工具 Advisor 约束解释为至多一个；关闭自动注册不删除已有显式实例。
- JSON Schema 中 Jackson 注解元素、适用位置、Swagger 可选参数及结果转换器入口沿用已核验的 API 校正。
- 异常分类与重抛名单按既有源码说明，避免将 false 理解为捕获一切异常。
- 流式终结钩子只接收正常完成分支尾部发射，不能转换整条 Flux；与官网笼统说法的差异已说明。
- 搜索入门使用 RegexToolIndex，完整 VectorToolIndex 示例仍在语义检索章节；正则匹配名称及描述、maxResults 回退与索引默认数量按既有源码解释。
- 示例保留时区修正、OllamaChatOptions、options Builder、空聚合与 returnDirect 分支、构造器及 Builder 复制方法等已有改写。
- 观察示例记录消息数量而非完整消息，区分调用意图与真实执行成功；RAG 只有输出完整答案时才适合直接返回。
- Recursive Advisors 已合入站内 Advisors，MCP Client/Server 链接指向对应译文；保留官方升级说明及扩展参考。

依据见 [API 复核](api-review-notes.md)、[静态断言](api-contract-checks.json)及[前次复审](2026-11-01-review.md)。本轮重新验证仓内 27 项原始断言及 7 项补充断言；这些是已保存的 2.0.2 证据，并非本轮重新下载全部制品。

## 逐节对照

### 工具调用基础

| 官网章节                                                                                                                          | 中文位置                                                                                               | 结果   |
| --------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ | ------ |
| [Architecture Overview](https://docs.spring.io/spring-ai/reference/api/tools.html#_architecture_overview)                         | [架构概览](/frameworks/spring-ai/tools/tool-calling/#_architecture_overview)                           | 已覆盖 |
| [Quick Start](https://docs.spring.io/spring-ai/reference/api/tools.html#quick-start)                                              | [快速入门](/frameworks/spring-ai/tools/tool-calling/#quick-start)                                      | 已覆盖 |
| [Defining Tools](https://docs.spring.io/spring-ai/reference/api/tools.html#defining-tools)                                        | [定义工具](/frameworks/spring-ai/tools/tool-calling/#defining-tools)                                   | 已覆盖 |
| [Declarative: @Tool](https://docs.spring.io/spring-ai/reference/api/tools.html#declarative-tool)                                  | [声明式：@Tool](/frameworks/spring-ai/tools/tool-calling/#declarative-tool)                            | 已覆盖 |
| [Programmatic: MethodToolCallback](https://docs.spring.io/spring-ai/reference/api/tools.html#method-tool-callback)                | [编程式：MethodToolCallback](/frameworks/spring-ai/tools/tool-calling/#method-tool-callback)           | 已覆盖 |
| [Programmatic: FunctionToolCallback](https://docs.spring.io/spring-ai/reference/api/tools.html#function-tool-callback)            | [编程式：FunctionToolCallback](/frameworks/spring-ai/tools/tool-calling/#function-tool-callback)       | 已覆盖 |
| [ToolCallback Beans](https://docs.spring.io/spring-ai/reference/api/tools.html#tool-callback-beans)                               | [ToolCallback Bean](/frameworks/spring-ai/tools/tool-calling/#tool-callback-beans)                     | 已覆盖 |
| [Passing Tools to ChatClient](https://docs.spring.io/spring-ai/reference/api/tools.html#passing-tools)                            | [向 ChatClient 提供工具](/frameworks/spring-ai/tools/tool-calling/#passing-tools)                      | 已覆盖 |
| [The Tool Calling Loop](https://docs.spring.io/spring-ai/reference/api/tools.html#the-tool-calling-loop)                          | [工具调用循环](/frameworks/spring-ai/tools/tool-calling/#the-tool-calling-loop)                        | 已覆盖 |
| [Memory and the Tool Loop](https://docs.spring.io/spring-ai/reference/api/tools.html#memory-and-the-tool-loop)                    | [记忆与工具循环](/frameworks/spring-ai/tools/tool-calling/#memory-and-the-tool-loop)                   | 已覆盖 |
| [Outside the Loop (default)](https://docs.spring.io/spring-ai/reference/api/tools.html#outside-the-loop)                          | [循环外：默认行为](/frameworks/spring-ai/tools/tool-calling/#outside-the-loop)                         | 已覆盖 |
| [Inside the Loop](https://docs.spring.io/spring-ai/reference/api/tools.html#inside-the-loop)                                      | [循环内：保留工具消息](/frameworks/spring-ai/tools/tool-calling/#inside-the-loop)                      | 已覆盖 |
| [Backend Compatibility](https://docs.spring.io/spring-ai/reference/api/tools.html#backend-compatibility)                          | [存储兼容性](/frameworks/spring-ai/tools/tool-calling/#backend-compatibility)                          | 已覆盖 |
| [Scaling to Hundreds of Tools](https://docs.spring.io/spring-ai/reference/api/tools.html#scaling-to-hundreds-of-tools)            | [扩展到大量工具](/frameworks/spring-ai/tools/tool-calling/#scaling-to-hundreds-of-tools)               | 已覆盖 |
| [MCP Tools](https://docs.spring.io/spring-ai/reference/api/tools.html#mcp-tools)                                                  | [MCP 工具](/frameworks/spring-ai/tools/tool-calling/#mcp-tools)                                        | 已覆盖 |
| [Consuming MCP Server Tools](https://docs.spring.io/spring-ai/reference/api/tools.html#consuming-mcp-server-tools)                | [使用 MCP 服务器工具](/frameworks/spring-ai/tools/tool-calling/#consuming-mcp-server-tools)            | 已覆盖 |
| [Exposing Spring Tools as an MCP Server](https://docs.spring.io/spring-ai/reference/api/tools.html#exposing-mcp-server-tools)     | [将 Spring 工具暴露为 MCP 服务器](/frameworks/spring-ai/tools/tool-calling/#exposing-mcp-server-tools) | 已覆盖 |
| [Combining Local and MCP Tools](https://docs.spring.io/spring-ai/reference/api/tools.html#combining-local-and-mcp-tools)          | [混用本地工具与 MCP 工具](/frameworks/spring-ai/tools/tool-calling/#combining-local-and-mcp-tools)     | 已覆盖 |
| [Tool Argument Augmentation](https://docs.spring.io/spring-ai/reference/api/tools.html#tool-argument-augmentation)                | [工具参数增强](/frameworks/spring-ai/tools/tool-calling/#tool-argument-augmentation)                   | 已覆盖 |
| [Quick Start](https://docs.spring.io/spring-ai/reference/api/tools.html#augmentation-quick-start)                                 | [快速使用](/frameworks/spring-ai/tools/tool-calling/#augmentation-quick-start)                         | 已覆盖 |
| [Core Components](https://docs.spring.io/spring-ai/reference/api/tools.html#augmentation-components)                              | [核心组件](/frameworks/spring-ai/tools/tool-calling/#augmentation-components)                          | 已覆盖 |
| [User-Controlled Tool Execution](https://docs.spring.io/spring-ai/reference/api/tools.html#user-controlled-tool-execution)        | [自行控制工具执行](/frameworks/spring-ai/tools/tool-calling/#user-controlled-tool-execution)           | 已覆盖 |
| [Extending the Loop: Custom ToolAdvisor](https://docs.spring.io/spring-ai/reference/api/tools.html#extending-the-loop)            | [扩展循环：自定义 ToolAdvisor](/frameworks/spring-ai/tools/tool-calling/#extending-the-loop)           | 已覆盖 |
| [Hook Methods](https://docs.spring.io/spring-ai/reference/api/tools.html#hook-methods)                                            | [钩子方法](/frameworks/spring-ai/tools/tool-calling/#hook-methods)                                     | 已覆盖 |
| [Auto-Configuration Integration](https://docs.spring.io/spring-ai/reference/api/tools.html#custom-tool-advisor-autoconfig)        | [接入自动配置](/frameworks/spring-ai/tools/tool-calling/#custom-tool-advisor-autoconfig)               | 已覆盖 |
| [Tool Specification Reference](https://docs.spring.io/spring-ai/reference/api/tools.html#tool-specification-reference)            | [工具规格参考](/frameworks/spring-ai/tools/tool-calling/#tool-specification-reference)                 | 已覆盖 |
| [ToolCallback](https://docs.spring.io/spring-ai/reference/api/tools.html#tool-callback)                                           | [ToolCallback](/frameworks/spring-ai/tools/tool-calling/#tool-callback)                                | 已覆盖 |
| [ToolDefinition](https://docs.spring.io/spring-ai/reference/api/tools.html#tool-definition)                                       | [ToolDefinition](/frameworks/spring-ai/tools/tool-calling/#tool-definition)                            | 已覆盖 |
| [JSON Schema](https://docs.spring.io/spring-ai/reference/api/tools.html#json-schema)                                              | [JSON Schema](/frameworks/spring-ai/tools/tool-calling/#json-schema)                                   | 已覆盖 |
| [Tool Context](https://docs.spring.io/spring-ai/reference/api/tools.html#tool-context)                                            | [工具上下文](/frameworks/spring-ai/tools/tool-calling/#tool-context)                                   | 已覆盖 |
| [Return Direct](https://docs.spring.io/spring-ai/reference/api/tools.html#return-direct)                                          | [直接返回结果](/frameworks/spring-ai/tools/tool-calling/#return-direct)                                | 已覆盖 |
| [Result Conversion](https://docs.spring.io/spring-ai/reference/api/tools.html#result-conversion)                                  | [结果转换](/frameworks/spring-ai/tools/tool-calling/#result-conversion)                                | 已覆盖 |
| [Method Tool Limitations](https://docs.spring.io/spring-ai/reference/api/tools.html#method-tool-limitations)                      | [方法工具的类型限制](/frameworks/spring-ai/tools/tool-calling/#method-tool-limitations)                | 已覆盖 |
| [Exception Handling](https://docs.spring.io/spring-ai/reference/api/tools.html#exception-handling)                                | [异常处理](/frameworks/spring-ai/tools/tool-calling/#exception-handling)                               | 已覆盖 |
| [Tool Call Limits](https://docs.spring.io/spring-ai/reference/api/tools.html#tool-call-limits)                                    | [工具调用次数限制](/frameworks/spring-ai/tools/tool-calling/#tool-call-limits)                         | 已覆盖 |
| [Counting](https://docs.spring.io/spring-ai/reference/api/tools.html#_counting)                                                   | [如何计数](/frameworks/spring-ai/tools/tool-calling/#_counting)                                        | 已覆盖 |
| [Behavior When a Limit Is Exceeded](https://docs.spring.io/spring-ai/reference/api/tools.html#_behavior_when_a_limit_is_exceeded) | [达到上限后如何处理](/frameworks/spring-ai/tools/tool-calling/#_behavior_when_a_limit_is_exceeded)     | 已覆盖 |
| [Tool Resolution](https://docs.spring.io/spring-ai/reference/api/tools.html#tool-resolution)                                      | [工具解析](/frameworks/spring-ai/tools/tool-calling/#tool-resolution)                                  | 已覆盖 |
| [Observability](https://docs.spring.io/spring-ai/reference/api/tools.html#observability)                                          | [可观测性](/frameworks/spring-ai/tools/tool-calling/#observability)                                    | 已覆盖 |
| [Logging](https://docs.spring.io/spring-ai/reference/api/tools.html#logging)                                                      | [日志](/frameworks/spring-ai/tools/tool-calling/#logging)                                              | 已覆盖 |
| [ChatModel Tool Calling](https://docs.spring.io/spring-ai/reference/api/tools.html#chatmodel-tool-calling)                        | [直接使用 ChatModel 调用工具](/frameworks/spring-ai/tools/tool-calling/#chatmodel-tool-calling)        | 已覆盖 |

### 工具调用 Advisor

| 官网章节                                                                                                                                          | 中文位置                                                                                                | 结果   |
| ------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- | ------ |
| [Overview](https://docs.spring.io/spring-ai/reference/api/tools/tool-calling-advisor.html#overview)                                               | [概览](/frameworks/spring-ai/tools/tool-calling-advisor/#overview)                                      | 已覆盖 |
| [Builder](https://docs.spring.io/spring-ai/reference/api/tools/tool-calling-advisor.html#builder)                                                 | [构建器](/frameworks/spring-ai/tools/tool-calling-advisor/#builder)                                     | 已覆盖 |
| [Builder Options](https://docs.spring.io/spring-ai/reference/api/tools/tool-calling-advisor.html#builder-options)                                 | [构建器选项](/frameworks/spring-ai/tools/tool-calling-advisor/#builder-options)                         | 已覆盖 |
| [ToolExecutionEligibilityChecker](https://docs.spring.io/spring-ai/reference/api/tools/tool-calling-advisor.html#checker)                         | [ToolExecutionEligibilityChecker](/frameworks/spring-ai/tools/tool-calling-advisor/#checker)            | 已覆盖 |
| [Conversation History Behavior](https://docs.spring.io/spring-ai/reference/api/tools/tool-calling-advisor.html#conversation-history)              | [内部历史的行为](/frameworks/spring-ai/tools/tool-calling-advisor/#conversation-history)                | 已覆盖 |
| [Hook Methods](https://docs.spring.io/spring-ai/reference/api/tools/tool-calling-advisor.html#hooks)                                              | [钩子方法](/frameworks/spring-ai/tools/tool-calling-advisor/#hooks)                                     | 已覆盖 |
| [Call-Path Hooks](https://docs.spring.io/spring-ai/reference/api/tools/tool-calling-advisor.html#call-hooks)                                      | [阻塞调用钩子](/frameworks/spring-ai/tools/tool-calling-advisor/#call-hooks)                            | 已覆盖 |
| [Stream-Path Hooks](https://docs.spring.io/spring-ai/reference/api/tools/tool-calling-advisor.html#stream-hooks)                                  | [流式调用钩子](/frameworks/spring-ai/tools/tool-calling-advisor/#stream-hooks)                          | 已覆盖 |
| [Subclass Example](https://docs.spring.io/spring-ai/reference/api/tools/tool-calling-advisor.html#subclass-example)                               | [子类示例](/frameworks/spring-ai/tools/tool-calling-advisor/#subclass-example)                          | 已覆盖 |
| [Single- ToolAdvisor Invariant](https://docs.spring.io/spring-ai/reference/api/tools/tool-calling-advisor.html#single-tooladvisor-invariant)      | [单个 ToolAdvisor 约束](/frameworks/spring-ai/tools/tool-calling-advisor/#single-tooladvisor-invariant) | 已覆盖 |
| [User-Controlled Streaming](https://docs.spring.io/spring-ai/reference/api/tools/tool-calling-advisor.html#user-controlled-streaming)             | [手动控制流式工具执行](/frameworks/spring-ai/tools/tool-calling-advisor/#user-controlled-streaming)     | 已覆盖 |
| [Observing the Tool-Calling Loop](https://docs.spring.io/spring-ai/reference/api/tools/tool-calling-advisor.html#observing-the-tool-calling-loop) | [观察工具调用循环](/frameworks/spring-ai/tools/tool-calling-advisor/#observing-the-tool-calling-loop)   | 已覆盖 |
| [Return Direct](https://docs.spring.io/spring-ai/reference/api/tools/tool-calling-advisor.html#return-direct)                                     | [直接返回工具结果](/frameworks/spring-ai/tools/tool-calling-advisor/#return-direct)                     | 已覆盖 |
| [Opting Out of Auto-Registration](https://docs.spring.io/spring-ai/reference/api/tools/tool-calling-advisor.html#opting-out)                      | [关闭自动注册](/frameworks/spring-ai/tools/tool-calling-advisor/#opting-out)                            | 已覆盖 |
| [See Also](https://docs.spring.io/spring-ai/reference/api/tools/tool-calling-advisor.html#see-also)                                               | [相关阅读](/frameworks/spring-ai/tools/tool-calling-advisor/#see-also)                                  | 已覆盖 |

### 工具搜索

| 官网章节                                                                                                                                    | 中文位置                                                                                             | 结果   |
| ------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- | ------ |
| [How It Works](https://docs.spring.io/spring-ai/reference/api/tools/tool-search-tool.html#how-it-works)                                     | [工作流程](/frameworks/spring-ai/tools/tool-search-tool/#how-it-works)                               | 已覆盖 |
| [When to Use](https://docs.spring.io/spring-ai/reference/api/tools/tool-search-tool.html#when-to-use)                                       | [何时使用](/frameworks/spring-ai/tools/tool-search-tool/#when-to-use)                                | 已覆盖 |
| [Installation](https://docs.spring.io/spring-ai/reference/api/tools/tool-search-tool.html#installation)                                     | [安装](/frameworks/spring-ai/tools/tool-search-tool/#installation)                                   | 已覆盖 |
| [Quick Start](https://docs.spring.io/spring-ai/reference/api/tools/tool-search-tool.html#quick-start)                                       | [快速开始](/frameworks/spring-ai/tools/tool-search-tool/#quick-start)                                | 已覆盖 |
| [Session Scoping](https://docs.spring.io/spring-ai/reference/api/tools/tool-search-tool.html#session-scoping)                               | [会话隔离](/frameworks/spring-ai/tools/tool-search-tool/#session-scoping)                            | 已覆盖 |
| [Search Strategies](https://docs.spring.io/spring-ai/reference/api/tools/tool-search-tool.html#search-strategies)                           | [检索策略](/frameworks/spring-ai/tools/tool-search-tool/#search-strategies)                          | 已覆盖 |
| [VectorToolIndex (Semantic)](https://docs.spring.io/spring-ai/reference/api/tools/tool-search-tool.html#vector-tool-index)                  | [VectorToolIndex：语义检索](/frameworks/spring-ai/tools/tool-search-tool/#vector-tool-index)         | 已覆盖 |
| [LuceneToolIndex (Keyword)](https://docs.spring.io/spring-ai/reference/api/tools/tool-search-tool.html#lucene-tool-index)                   | [LuceneToolIndex：关键词检索](/frameworks/spring-ai/tools/tool-search-tool/#lucene-tool-index)       | 已覆盖 |
| [RegexToolIndex (Pattern)](https://docs.spring.io/spring-ai/reference/api/tools/tool-search-tool.html#regex-tool-index)                     | [RegexToolIndex：模式匹配](/frameworks/spring-ai/tools/tool-search-tool/#regex-tool-index)           | 已覆盖 |
| [Configuration](https://docs.spring.io/spring-ai/reference/api/tools/tool-search-tool.html#configuration)                                   | [配置](/frameworks/spring-ai/tools/tool-search-tool/#configuration)                                  | 已覆盖 |
| [ToolIndex API](https://docs.spring.io/spring-ai/reference/api/tools/tool-search-tool.html#tool-index-api)                                  | [ToolIndex API](/frameworks/spring-ai/tools/tool-search-tool/#tool-index-api)                        | 已覆盖 |
| [Index Eviction](https://docs.spring.io/spring-ai/reference/api/tools/tool-search-tool.html#index-eviction)                                 | [索引淘汰](/frameworks/spring-ai/tools/tool-search-tool/#index-eviction)                             | 已覆盖 |
| [Spring Boot Auto-Configuration](https://docs.spring.io/spring-ai/reference/api/tools/tool-search-tool.html#spring-boot-auto-configuration) | [Spring Boot 自动配置](/frameworks/spring-ai/tools/tool-search-tool/#spring-boot-auto-configuration) | 已覆盖 |
| [ToolIndex Auto-Selection](https://docs.spring.io/spring-ai/reference/api/tools/tool-search-tool.html#tool-index-auto-selection)            | [自动选择 ToolIndex](/frameworks/spring-ai/tools/tool-search-tool/#tool-index-auto-selection)        | 已覆盖 |
| [Configuration Properties Reference](https://docs.spring.io/spring-ai/reference/api/tools/tool-search-tool.html#properties-reference)       | [配置属性参考](/frameworks/spring-ai/tools/tool-search-tool/#properties-reference)                   | 已覆盖 |
| [Example Configurations](https://docs.spring.io/spring-ai/reference/api/tools/tool-search-tool.html#example-configurations)                 | [配置示例](/frameworks/spring-ai/tools/tool-search-tool/#example-configurations)                     | 已覆盖 |
| [See Also](https://docs.spring.io/spring-ai/reference/api/tools/tool-search-tool.html#see-also)                                             | [相关阅读](/frameworks/spring-ai/tools/tool-search-tool/#see-also)                                   | 已覆盖 |

### ChatModel 工具调用

| 官网章节                                                                                                                                  | 中文位置                                                                                               | 结果   |
| ----------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ | ------ |
| [When to Use ChatModel Directly](https://docs.spring.io/spring-ai/reference/api/tools/chatmodel-tool-calling.html#when-to-use)            | [什么时候直接使用 ChatModel](/frameworks/spring-ai/tools/chatmodel-tool-calling/#when-to-use)          | 已覆盖 |
| [No Internal Tool Execution](https://docs.spring.io/spring-ai/reference/api/tools/chatmodel-tool-calling.html#no-internal-tool-execution) | [ChatModel 不执行工具](/frameworks/spring-ai/tools/chatmodel-tool-calling/#no-internal-tool-execution) | 已覆盖 |
| [Passing Tools to ChatModel](https://docs.spring.io/spring-ai/reference/api/tools/chatmodel-tool-calling.html#passing-tools)              | [向 ChatModel 提供工具](/frameworks/spring-ai/tools/chatmodel-tool-calling/#passing-tools)             | 已覆盖 |
| [Per-Request Tools](https://docs.spring.io/spring-ai/reference/api/tools/chatmodel-tool-calling.html#per-request-tools)                   | [请求级工具](/frameworks/spring-ai/tools/chatmodel-tool-calling/#per-request-tools)                    | 已覆盖 |
| [Default Tools (Configured on the Model)](https://docs.spring.io/spring-ai/reference/api/tools/chatmodel-tool-calling.html#default-tools) | [模型默认工具](/frameworks/spring-ai/tools/chatmodel-tool-calling/#default-tools)                      | 已覆盖 |
| [Override Semantics](https://docs.spring.io/spring-ai/reference/api/tools/chatmodel-tool-calling.html#override-semantics)                 | [覆盖规则](/frameworks/spring-ai/tools/chatmodel-tool-calling/#override-semantics)                     | 已覆盖 |
| [Driving the Loop Manually](https://docs.spring.io/spring-ai/reference/api/tools/chatmodel-tool-calling.html#driving-the-loop-manually)   | [手动驱动工具循环](/frameworks/spring-ai/tools/chatmodel-tool-calling/#driving-the-loop-manually)      | 已覆盖 |
| [Blocking](https://docs.spring.io/spring-ai/reference/api/tools/chatmodel-tool-calling.html#blocking-loop)                                | [阻塞调用](/frameworks/spring-ai/tools/chatmodel-tool-calling/#blocking-loop)                          | 已覆盖 |
| [Streaming](https://docs.spring.io/spring-ai/reference/api/tools/chatmodel-tool-calling.html#streaming-loop)                              | [流式调用](/frameworks/spring-ai/tools/chatmodel-tool-calling/#streaming-loop)                         | 已覆盖 |
| [Tool Context](https://docs.spring.io/spring-ai/reference/api/tools/chatmodel-tool-calling.html#tool-context)                             | [工具上下文](/frameworks/spring-ai/tools/chatmodel-tool-calling/#tool-context)                         | 已覆盖 |
| [Return Direct](https://docs.spring.io/spring-ai/reference/api/tools/chatmodel-tool-calling.html#return-direct)                           | [直接返回工具结果](/frameworks/spring-ai/tools/chatmodel-tool-calling/#return-direct)                  | 已覆盖 |
| [See Also](https://docs.spring.io/spring-ai/reference/api/tools/chatmodel-tool-calling.html#see-also)                                     | [相关文档](/frameworks/spring-ai/tools/chatmodel-tool-calling/#see-also)                               | 已覆盖 |

## 验证与范围

- 四篇均在桌面 1440px、手机 390px 重新检查，代码、图片、导航、旧锚点和页面宽度正常，无脚本错误或 Markdown 标记残留。
- 153 个去重站内链接及锚点检查通过。
- 四篇站点、修订、定稿逐字节一致；页面哈希与此前结构调整记录一致。
- 本次只新增审计记录，未修改站点正文，未重跑 check/build；本审计不用于证明其他并行改动或依赖变更的构建结果。
- 语义覆盖与配置描述由人工逐节核对，脚本用于辅助检查数量、标识、映射与字节；没有把锚点存在等同于内容完整。
- 范围限于四篇正文，不包含所有外链页面全文；Java 未编译运行，模型、MCP 与业务工具未调用。
