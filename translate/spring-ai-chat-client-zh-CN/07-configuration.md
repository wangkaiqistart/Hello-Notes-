# ChatClient 运行配置补充

日期：2026-10-25。以下保留初次补充的记录；按用户反馈精简后的当前结果见文末。

## 变更

- 页面“创建 ChatClient”前增加“运行前配置”；使用 Spring AI 2.0.2、Spring Boot 4.0.x / 4.1.x、Java 21 作为示例版本。
- 补充 OpenAI Starter、MVC Starter 和 BOM；流式调用说明 WebFlux 依赖。
- 用两个标签页分别给出 OpenAI 与 DeepSeek 兼容接口的 `application.yml`，解释适配器、地址、密钥和模型名。
- 说明 `application.properties` 与同位置 YAML 的优先级，避免旧配置覆盖。
- 给出 IDEA 环境变量入口和 zsh 隐藏输入密钥的命令，并说明终端变量的继承范围。
- 补充 `./mvnw spring-boot:run`、`curl /ai` 与常见配置失败定位，连接后文已有的 Controller 示例。

## 配置依据

来源：[OpenAI Chat](https://docs.spring.io/spring-ai/reference/api/chat/openai-chat.html) 与 Maven Central 发布的 `spring-ai-autoconfigure-model-openai:2.0.2` 源码。

已确认 `OpenAiChatProperties` 的配置前缀为 `spring.ai.openai.chat`，直接声明 `model` 属性；`Options.getModel()` 标记 `@DeprecatedConfigurationProperty(replacement = "spring.ai.openai.chat.model")`，并兼容转发到新属性。因此新示例使用 `chat.model`，不写旧的 `chat.options.model`。

源码 URL、哈希和字段核验见 [configuration-reference.json](configuration-reference.json)。密钥仅以环境变量占位符出现，文档不包含真实密钥。

## 验证

- 两份 YAML 解析通过，包含模型适配器、服务密钥和 `chat.model`，DeepSeek 示例还包含 `base-url`。
- 新增 7 段配置 / 命令，当前共 44 个代码块；原有 37 个代码块及“创建 ChatClient”之后的全部 API 正文保持不变。
- 站点页面与最终 `translation.md` 逐字节一致。
- `npm run check`：0 错误、0 警告、0 提示。
- `npm run build`：123 页成功生成；既有 i18n 空集合与 docs/404 缺失提示保留。
- 页面与最终译稿 Prettier、`git diff --check` 通过。

桌面 1440px、手机 390px：两组标签页均可切换，YAML 和环境变量示例显示正确；HTTP 200，无横向溢出、脚本错误或失效页内链接，原有配图及快速入门跳转正常。

浏览器核验见 [validation.jsonl](validation.jsonl) 中的 `configuration-update` 记录。没有执行 Java 项目、启动模型应用或调用付费模型；验证覆盖配置依据、语法和站点呈现。

## 后续精简

按用户要求将运行配置从 139 行压缩到 47 行，保留模型 Starter、两种 YAML、IDEA 密钥设置及 2.0.x 配置键说明。BOM 改为链接快速入门，删除重复的配置表、终端密钥命令、启动验证和排错段落。

当前新增 3 段配置，全文共 40 个代码块、13 个二级章节，原有 37 段示例及 API 正文不变。最终译稿已同步。最新验证见 `validation.jsonl` 中的 `configuration-concise` 记录。
