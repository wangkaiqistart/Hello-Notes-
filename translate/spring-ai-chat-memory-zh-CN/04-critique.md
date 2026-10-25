# Chat Memory 初稿审校

对照 `03-draft.md`、来源正文和 2.0.2 源码，以下为诊断，不在本文件重写正文。

## 准确性

- Cassandra 手动创建示例已补上 `.build()`：`create` 接收配置对象，`withCqlSession` 返回 Builder，同版本 Javadoc 与源码均可确认。
- Cassandra 前缀与消息列默认值已修正：源码分别为 `spring.ai.chat.memory.repository.cassandra` 与 `messages`。
- 连接属性表仍以“来源表列出的默认值”为表头。Spring Boot 连接行为不能只凭 Spring AI 表格认定；改为明确的本地连接示例值，并提醒填写实际集群信息，尤其是数据中心。
- 原文将工具消息限制泛化到整个当前实现，初稿已区分默认 Advisor 位置与 Repository 支持。保留这种分层表述，不承诺仅调整顺序就一定完整持久化。
- 原文把被过滤消息称为 silently filtered；实际 Cassandra 代码会写 warn 日志。正文使用“过滤”即可，避免承诺无日志或会抛异常。
- 20 条消息不是 20 轮；完整轮次对齐后可能低于 maxMessages，极端情况会清空非系统消息。已覆盖。
- Cassandra 保存历史窗口快照，但过滤工具消息且可设置 TTL，不能将其称为完整不可变审计日志。初稿已经限定。

## 中文表达

- “属性前缀、消息列默认值和手动创建示例按 2.0.2 API 与源码校正”属于翻译过程说明，应移出公开正文，保留在本目录记录。
- 初始化脚本表的完整 classpath 很长，改成表内说明加独立代码行，移动端仍须检查滚动范围；如已有表格内部滚动正常，可以保留来源完整路径。
- 34 段示例较长，但各存储类型结构一致、开头提供主线阅读入口，适合按需查阅；不额外拆页或生成配图。

## 说明与适配

- 只为会话 ID、Spring Bean 初始化顺序、Redis 跨会话查询增加必要解释，不扩写生产安全清单。
- 保留英文用户输入，避免把本地化输入后不同的模型行为当成原始示例结果。
- 默认内存的重启丢失与多实例不共享属于必要工程判断，表述清楚且未冒充来源逐字内容。

## 结论

需要修正 1 处连接默认值表述，移出 1 处过程旁白；两处代码修正及 Cassandra 配置纠错已有证据。定稿后验证代码差异、站内锚点与响应式布局。

## API 复核追加

- 来源正文使用 `.promptTemplate()`，但 2.0.2 版本 `VectorStoreChatMemoryAdvisor.Builder` 的真实方法为 `.systemPromptTemplate(PromptTemplate)`；定稿修正并补充版本化 API 链接。
- 同版本 Javadoc 明确 VectorStoreChatMemoryAdvisor 仅适用文本交互，补入支持边界，避免与前面的多模态章节混淆。
