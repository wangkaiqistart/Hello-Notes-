# 审校

## 准确性与源码复核

来源页面 2.0.2；从 Maven Central 下载同版 sources.jar，提取 StructuredOutputValidationAdvisor 与 DefaultChatClient 源码。Advisor 文件与 jsDelivr 提供的同标签源码 SHA-256 相同，来源证据见 source-evidence.json。

1. 重试与尝试混用：Builder 默认 maxRepeatAttempts = 3，adviseCall 循环从 1 + maxRepeatAttempts 开始。因此默认首次调用加最多 3 次重试，总计最多 4 次下游调用；示例 maxRepeatAttempts(5) 对应最多 6 次。校正主篇与 Advisors 页已存在的“最多尝试 3 次”。
2. 手动注册不会在 resolveAdvisorChain 中替换自动实例；spec.isValidated() 为 true 时始终 push 新实例。因此显式注册后使用普通 entity(...)，不再额外启用 validateSchema()。
3. 循环耗尽没有专门的“最终 Schema 错误”抛出分支，返回最后一次 ChatClientResponse 后进入类型转换。不能宣称耗尽一定抛错，也不能声称最终一定符合 Schema。
4. 类型转换不等同 Schema 校验。此前保存的 BeanOutputConverter 默认关闭 FAIL_ON_UNKNOWN_PROPERTIES，所以不能翻译为“额外字段一定让解析器抛错”。
5. getJsonSchema() 为空时，validateSchema() 路径会创建带空 Schema 的 Advisor，Builder 无类型且无有效 Schema 时抛 IllegalArgumentException。修正主篇原有“两项开关都无操作”的错误，原生约束缺少 Schema 与启用校验时失败需分开说明。
6. 确认 DRAFT_2020_12、互斥 Schema 来源、自定义 jsonMapper(...)、累计用量、流式不支持。工具调用轮次返回给工具 Advisor，不作最终内容校验。

## 表达与合并

- 保留来源 4 段代码，提示词与 API 不改写；两个已有示例合并时复用。
- 说明有限重试与应用校验职责，不加入新的业务策略。
- 图保持节点、手绘布局和红色循环范围，仅覆盖说明文字，不重画或加入标记。
- 主文链接统一指向本地章节；Advisors 篇相关链接同步指向新增小节。
