# 多模型配置补充

日期：2026-10-25。按读者实践反馈，在“为不同模型类型创建 ChatClient”示例旁补充配置差异，保持简短。

- 多个提供方依赖自动配置时，删除 `spring.ai.model.chat`；固定为 `openai` 会阻止其他提供方的模型自动注册。
- 对照 DeepSeek 的兼容接口 / 专用接口，列明 Starter、配置前缀与注入类型。
- 提供专用接口的最小 YAML：`deepseek.api-key` 与 `deepseek.chat.model`，提醒合并到现有配置。
- 区分默认 `ChatClient` 与默认 `ChatModel`；需要注入 Builder 时，通过选定客户端的 `mutate()` 提供原型作用域 Builder。

## 依据与验证

配置规则按 Spring AI 2.0.2 的 OpenAI、DeepSeek、Anthropic 自动配置源码核对：`@ConditionalOnProperty` 均选择对应提供方，并使用 `matchIfMissing = true`。具体类名及源码包哈希见 [multi-model-reference.json](multi-model-reference.json)。

新增 YAML 和 Java 两段代码，原有 40 段代码保持不变，全文当前 42 段。三份 YAML 均可解析，最终译稿与页面逐字节一致。最新检查见 [validation.jsonl](validation.jsonl) 中的 `multi-model-update` 记录。

补充内容用于解释运行配置；没有调用真实模型，也不把学习项目的启动结果当成本文全部示例的运行验证。

检查结果：`npm run check` 为 0 错误 / 警告 / 提示，构建 123 页成功。桌面 1440px、手机 390px 均 HTTP 200，无页面横向溢出、脚本错误或失效页内链接；配置标签可切换，新增对照表、原有图片及导航入口正常。页面与最终译稿格式检查、`git diff --check` 通过。
