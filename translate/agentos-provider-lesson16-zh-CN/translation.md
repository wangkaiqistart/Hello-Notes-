---
title: AgentOS：Provider 原理与实现
description: 从职责边界、配置分层、具名路由到调用审计，理解模型接入层如何落地
sidebar:
  label: Provider 原理与实现
  order: 5.1
---

AgentOS 的模型接入层是 Provider。上层把 Agent 的 Profile 和本轮 Prompt 交给它，Provider 选择对应连接、发送消息与工具定义，再把 `ChatResponse` 交回 ReActLoop。Provider 负责一次模型调用，是否继续迭代、是否执行工具由运行时决定。

本文按“先理解，再实现，最后验收”的顺序展开：**全局配置连接，Agent 指定聊天模型；Provider 负责模型请求，ToolExecutor 负责工具执行。**

## 一、Provider 是什么，做什么

一次模型推理有两类输入：

- **Profile**：声明使用哪个 provider、哪个 model，以及推理强度、输出预算等生成参数。
- **Prompt**：包含系统指令、对话消息、工具定义和应用侧上下文。

Provider 按 Profile 中的名称选出一个 `ChatModel`，发起一次调用并返回结果。换用另一个已经配置的端点时，ReActLoop 不需要改变。

[![ReActLoop 根据 Profile 通过 ProviderService 选择 ChatModel，再访问对应模型服务](/images/projects/agent-os/provider-overview.png)](/images/projects/agent-os/provider-overview.png)

_按名称选择连接，再把本轮请求交给对应客户端；点击图片可查看大图。_

Provider 负责四类工作：

1. 根据 provider 名称路由到具名客户端。
2. 组装本次请求所需的模型参数、消息和工具定义。
3. 调用模型并处理同步或流式响应。
4. 提取响应元数据，记录每次调用的成功或失败。

上下文裁剪、轮次控制、工具权限、工具执行和记忆存储由其他模块负责。Provider 不应该变成一个包含整个 Agent 循环的“大服务”。

[![Provider 负责模型选择、模型调用、工具协议转换和用量审计；循环、工具执行、上下文与记忆由其他模块负责](/images/projects/agent-os/provider-boundaries.png)](/images/projects/agent-os/provider-boundaries.png)

_协议转换复用模型客户端，循环与工具执行保留独立入口。_

| 模块               | 在 Provider 链路中的职责                                         |
| ------------------ | ---------------------------------------------------------------- |
| `AgentOS-core`     | 定义 Profile、TurnContext 等契约，协调 ReActLoop 与 ToolExecutor |
| `AgentOS-provider` | 构建具名 ChatModel，组装请求、调用模型、提取元数据               |
| `AgentOS-tool`     | 注册 ToolCallback，并用 GovernedToolCallback 封装治理            |
| `AgentOS-storage`  | 通过 PostgreSQL、JPA 和 Flyway 持久化会话与调用审计              |
| `AgentOS-boot`     | 加载 application.yaml，注入基础组件并完成装配                    |

核心层直接使用 `Prompt`、`Message`、`ChatResponse` 和 `ToolCallback`。这些类型已经表达了消息、工具请求和响应元数据，不需要再造一套 `ModelRequest`、`ModelResponse` 或专用工具协议。

## 二、动手前先想清楚几件事

### 1. 把职责划窄

Provider 只管“选对模型、发起一次调用、把结果拿回来”。循环怎么转、工具怎么执行、上下文怎么裁剪、记忆怎么保存，都不归 Provider 管。

| Provider 负责                        | Provider 不负责                        |
| ------------------------------------ | -------------------------------------- |
| 选择具名 ChatModel                   | 循环如何继续 → ReActLoop               |
| 组装并发起一次模型调用               | 工具如何执行 → ToolExecutor            |
| 传递工具定义并解析 ChatResponse      | 上下文如何拼接 → PromptBuilder         |
| 读取用量、限流和结束原因并写调用审计 | 会话和长期记忆如何存储 → MemoryService |

Provider 如果自己执行工具或自己启动下一轮请求，就会和 ReActLoop 形成两条控制路径，造成重复执行、重复审计和无法统一限时。

### 2. 已有能力不要重新实现

各模型协议的消息、工具 Schema、流式分片和响应元数据转换由模型模块处理。ProviderService 只做薄包装：维护具名映射、构造请求选项、调用客户端和保存审计。

工具也不应再造一套接口。内置工具、`@Tool` Bean 和 MCP 工具都统一为 `ToolCallback`，外面再包 `GovernedToolCallback`。Provider 把这些回调的定义放入请求，ToolExecutor 复用同一批受治理回调执行。

### 3. 三个容易出错的地方

#### 坑一：多个 provider 不能靠类型扫描区分

DeepSeek、Kimi、通义兼容模式或内部中转端点可能都使用 `OpenAiChatModel`。仅扫描容器中的 `ChatModel` 类型，无法可靠判断实例对应哪个连接；Bean 名称也不能当作业务 provider 名称。

因此要从配置开始维护显式映射：

```text
provider name  →  ChatModel
primary        →  primary ChatModel
internal       →  internal ChatModel
local          →  local ChatModel
```

Profile 只引用 provider name，ProviderService 通过映射取出客户端。未知名称在外呼前失败，不能静默落到另一个模型。

#### 坑二：模型返回工具请求，不等于工具已经执行

`ChatModel.call(Prompt)` 和 `ChatModel.stream(Prompt)` 返回模型的原始响应，其中可以包含工具调用请求，但不会自动执行工具。Provider 只传递工具定义和解析响应；真正的执行路径是：

```text
ReActLoop
  → ProviderService
  → ChatModel 返回工具调用请求
  → ToolExecutor
  → 注入的 ToolCallingManager
  → GovernedToolCallback
```

不能通过另一个 `ChatClient`、另一个 `ToolCallingManager` 或一个临时回调绕过这条路径。容器注入的 `ToolCallingManager` 才能继续使用工具限额、异常处理和观测配置。

#### 坑三：配置能加载，不代表模型一定可用

配置里的 provider 名称、凭证占位符和模型名称通过校验，只能证明字段基本完整；端点是否支持目标模型、工具调用、推理参数、流式响应和用量字段，必须通过协议测试或受控冒烟确认。

显式 `base-url` 也不能凭经验拼接。构建示例直接使用带 API 前缀的地址，例如 `https://api.openai.com/v1`，最终请求应断言为 `/v1/chat/completions`。有的兼容端点要求根地址，有的要求 `/v1`，不能统一追加。

## 三、代码怎么写

### 第零步：从 AGENT.md 派生 Profile

Agent 定义放在 `.AgentOS/agents/<name>/AGENT.md`。frontmatter 是运行配置，正文是任务指令；不再维护一份与 Agent 目录平行的 `profile.yml`。

```markdown title=".AgentOS/agents/ops-agent/AGENT.md"
---
name: ops-agent
description: 查询服务状态并说明排查建议
provider:
  name: primary
  model: ${AGENTOS_LLM_MODEL}
  reasoning_effort: low
tools:
  - http_get
---

查询用户指定服务的状态，结合工具返回结果说明问题与排查建议。
```

`AgentLoader.deriveProfile()` 负责解析 frontmatter、校验字段并建立运行时索引。应用配置里的 `${ENV_VAR}` 由配置环境解析；AGENT.md 中的占位符需要加载器显式解析，单独读取 Markdown/YAML 不会自动完成这一步。

加载时至少检查：名称唯一、provider 存在、model 非空、工具引用合法。无效 Agent 应记录脱敏诊断并隔离；调用未知 Agent 或 provider 时直接拒绝。模型是否实际可用、账号是否获授权，需要服务响应确认。

连接配置和 frontmatter 可以在启动时形成快照，AGENT.md 正文由 ContextLoader 在每轮读取。凭证只从受控环境注入，不进入日志、工具 Schema 或模型消息。

### 第一步：配置分两层

全局连接放在 `AgentOS-boot/src/main/resources/application.yaml`，通过 `@ConfigurationProperties(prefix = "agentos")` 绑定。`providers` 使用名称到连接配置的映射，同一协议可以配置多个端点。

```yaml title="application.yaml：聊天模型连接"
agentos:
  providers:
    primary:
      type: openai
      base-url: ${AGENTOS_LLM_BASE_URL}
      api-key: ${AGENTOS_LLM_API_KEY}
      timeout: 120s
```

全局连接配置只解决“连到哪里、使用什么协议、凭证从哪里来”。这里不设置聊天模型、温度、推理强度或模型白名单；本项目约定每个 Agent 在自己的 Profile 中显式选择聊天模型。

Agent 层解决“这次怎么调用”：model、推理强度、输出预算、工具集合和轮次设置来自 `AGENT.md`。因此全局连接不设置默认聊天模型，不代表客户端可以偷偷使用库内部默认值；外呼前仍必须校验并显式写入 Profile 的 model。

`base-url` 应与客户端构建方式配套。2.0.2 的 OpenAI 客户端会使用显式传入的地址，不应假定它自动补上 `/v1`。连接测试必须断言最终 HTTP 路径，避免漏写或重复拼接。

### 第二步：建立 provider 到 ChatModel 的映射

ProviderService 维护 `Map<String, ChatModel>`：键来自 `agentos.providers`，值由 `type` 对应的工厂创建。不能根据 Java 类型猜测 provider，因为两个不同端点都可能使用同一个 ChatModel 实现。

模型模块由统一 BOM 管理版本。多连接采用编程式构建；自动配置的单个辅助模型不能替代主链路的具名映射。

下面展示 OpenAI 兼容连接的构建方式。`ObservationRegistry` 由容器注入；SDK 重试在创建客户端时关闭，重试预算留给 ProviderService。

```java title="OpenAiConnectionFactory.java"
import java.time.Duration;
import io.micrometer.observation.ObservationRegistry;
import org.springframework.ai.openai.OpenAiChatModel;
import org.springframework.ai.openai.OpenAiChatOptions;

public final class OpenAiConnectionFactory {
    public static OpenAiChatModel create(
            String apiBaseUrl, String apiKey, Duration timeout,
            ObservationRegistry observationRegistry) {
        var options = OpenAiChatOptions.builder()
                .baseUrl(apiBaseUrl)
                .apiKey(apiKey)
                .timeout(timeout)
                .maxRetries(0)
                .build();

        return OpenAiChatModel.builder()
                .options(options)
                .observationRegistry(observationRegistry)
                .build();
    }
}
```

不能只看 `spring.ai.retry.max-attempts` 就认定编程式客户端没有 SDK 重试；应核对对应客户端构建参数，并用本地 HTTP 替身验证物理请求次数。

### 第三步：组装一次完整的请求

直接调用 `ChatModel.call(Prompt)` 时，请求 Options 完整替代客户端默认 Options，不采用逐字段补齐。model、超时、生成参数、工具和 ToolContext 应由同一个请求构建入口确定。

推理模型使用 `reasoningEffort` 和 `maxCompletionTokens`，不发送 `temperature`。普通聊天模型按自身能力设置温度，不能对所有模型统一填入一个默认值。

```java title="OpenAiPromptFactory.java"
import java.time.Duration;
import java.util.List;
import java.util.Map;
import org.springframework.ai.chat.messages.Message;
import org.springframework.ai.chat.prompt.Prompt;
import org.springframework.ai.openai.OpenAiChatOptions;
import org.springframework.ai.tool.ToolCallback;

public final class OpenAiPromptFactory {
    public static Prompt create(
            List<Message> messages, String model, String reasoningEffort,
            Integer maxOutputTokens, Duration requestTimeout,
            List<ToolCallback> tools, Map<String, Object> toolContext) {
        if (model == null || model.isBlank()) {
            throw new IllegalArgumentException("Model is required");
        }
        var options = OpenAiChatOptions.builder()
                .model(model)
                .reasoningEffort(reasoningEffort)
                .maxCompletionTokens(maxOutputTokens)
                .timeout(requestTimeout)
                .toolCallbacks(List.copyOf(tools))
                .toolContext(Map.copyOf(toolContext))
                .build();
        return new Prompt(List.copyOf(messages), options);
    }
}
```

`requestTimeout` 取连接超时预算与整轮剩余时间中的较小值；模型请求不能拖过轮次截止时间。`maxCompletionTokens` 与 `maxTokens` 不同时设置，推理消耗的输出预算也要计算在内。

### 第四步：传递工具定义，但把执行交给 ToolExecutor

工具从 ToolRegistry 按 Profile 和权限过滤后，直接放入 `toolCallbacks(...)`。回调已经由 GovernedToolCallback 包装，不需要再创建只含 Schema、执行时抛异常的另一套对象。

需要守住四个细节：

- 每次请求显式提供本轮工具清单。非空请求工具列表会替代默认工具；空清单在某些合并路径可能回退到默认工具，不能依赖空列表清除权限。
- 工具名唯一，Schema 与实际参数契约一致；直接调用 ChatModel 时要在 ToolRegistry 自己校验重名。
- ToolContext 携带 TurnContext、会话与权限等应用数据，不作为模型参数发送；运行时上下文同名键覆盖默认键，权限值必须由应用生成。
- ToolCallingManager 使用容器中统一配置的实例，由 ToolExecutor 调用。辅助 ChatClient 调用不传工具。

**Provider 只传递工具定义，绝不执行 ToolCallback。** ReActLoop 执行工具后，使用 `ToolExecutionResult.conversationHistory()` 继续构造 Prompt；其中已经包含助手的工具调用请求和工具结果。`returnDirect()` 为 true 时直接结束；同一次请求多个工具时，只有它们全部设置直接返回才会为 true。

### 第五步：处理同步、工具响应和流式分片

`ChatModel.call(Prompt)` 返回完整 `ChatResponse`。先检查 `getResult()` 是否存在，再从输出消息读取文本和工具意图；不要只调用返回字符串的重载，否则工具请求和元数据无法完整保留。

只有工具调用、没有文本，也是有效响应。保留每条工具调用的 ID、名称、参数和顺序；工具结果通过调用 ID 与助手请求关联。模型拒答、达到输出上限等结束原因要单独处理，没有 generation 的响应按协议异常处理。

`ChatModel.stream(Prompt)` 返回分片。一个工具调用的名称、ID 和参数 JSON 可能跨多个分片到达，单片参数不一定是合法 JSON。流式路径按以下顺序处理：

1. 将允许展示的文本增量交给输出端，同时用 `MessageAggregator` 聚合整次迭代。
2. 等流结束后检查完整响应，提取工具意图、结束原因和可用用量。
3. 把完整工具请求交给 ToolExecutor，保存新增历史，再开始下一次模型推理。

不在参数尚未拼完整时执行工具，不对每个分片重复写一次成功审计，也不把累计用量重复相加。流中断时记录失败；已经向用户发送增量后，不自动重放本次请求。

### 第六步：超时、重试和调用审计

ProviderService 统一控制模型重试：对 429、可重试的 5xx 和临时连接错误，最多追加一次尝试；鉴权、参数、未知模型和配置错误直接失败。重试前预留完整的单次调用超时预算，退避或 `Retry-After` 也计入整轮时间；流式内容尚未对外发送时才允许重试。

取消、截止时间、Provider 重试预算和 ReAct 最大迭代数是四个不同限制。Provider 不以重试名义执行工具，也不静默切换模型。对外 Provider 故障使用 `PROVIDER_UNAVAILABLE`，HTTP 状态映射留给 Web 层。

Provider 按 Profile 选模型、组装 Prompt、发起调用，再把本次结果与耗时写入 `llm_calls`，最后将响应或错误交回上层。

[![ProviderService 按 Profile 选择 ChatModel，组装完整消息与工具定义，发起模型调用并写入成功或失败审计，返回 ChatResponse](/images/projects/agent-os/provider-call-flow.png)](/images/projects/agent-os/provider-call-flow.png)

_一次外呼对应一条审计；模型重试也分别记账。_

审计至少记录以下信息：

| 字段                                                   | 获取方式与含义                                       |
| ------------------------------------------------------ | ---------------------------------------------------- |
| `session_id` / `turn_id` / `iteration`                 | 从 TurnContext 显式传入，定位会话、轮次与迭代        |
| `provider` / `requested_model`                         | 记录实际选择的连接和请求模型                         |
| `response_id` / `response_model`                       | 从 ChatResponseMetadata 读取，区分请求模型与响应模型 |
| `mode` / `finish_reason` / `tool_call_count`           | 记录 call 或 stream、结束原因及工具请求数            |
| `prompt_tokens` / `completion_tokens` / `total_tokens` | 从 Usage 读取已提供的指标                            |
| `cache_read_tokens` / `cache_write_tokens`             | 从 Usage 的缓存指标读取，不支持时为 NULL             |
| `requests_remaining` / `tokens_remaining`              | 从 RateLimit 读取，缺失时为 NULL                     |
| `success` / `error_message` / `duration_ms`            | 成功或失败、脱敏原因与单调时钟计算的耗时             |

`EmptyUsage` 表示未提供用量，`EmptyRateLimit` 表示没有限流信息，都应按缺失数据落库。NULL、真实的 0 和未知值不能混用。

审计采用 PostgreSQL 与 Flyway，网络调用放在数据库事务之外；失败记录通过独立短事务保存，避免业务回滚时一起丢失。审计写入失败不能静默返回成功，也不能因此自动重放模型请求。日志只记录必要标识和脱敏错误，不输出凭证、完整 Prompt、工具参数或底层响应体。

### 第七步：Embedding 单独处理

Provider 模块还可以提供独立的 `EmbeddingModel`。它的模型、维度和连接需要全局一致，同一张向量表的文档向量和查询向量必须使用同一模型。因此 Embedding 的全局 model 配置与 Agent 自己选择聊天模型是两件事。

容器只保留所需的 `EmbeddingModel`，避免辅助模型 Starter 再创建一个指向聊天端点的实例。未启用 Embedding 时不创建向量化组件；更换模型或维度时，需要配套的数据迁移和重新向量化。

## 四、验收 harness：把边界变成测试

验收不以“类已经创建”作为完成标准，而是验证行为。至少要覆盖以下场景：

| 验收层次   | 必须证明的行为                                                                          |
| ---------- | --------------------------------------------------------------------------------------- |
| 配置与路由 | 两个端点不串台；未知 provider、缺少 model 在外呼前失败；AGENT.md 正确派生 Profile       |
| 请求协议   | 最终 URL、model、推理参数、输出预算和工具 Schema 正确；推理模型不发送 temperature       |
| 工具边界   | Provider 不执行 ToolCallback；ToolExecutor 使用同一受治理回调；仅工具响应与调用顺序保留 |
| 运行时衔接 | ToolContext 不进入请求 JSON；工具结果与调用 ID 对应；直接返回不触发下一次推理           |
| 流式与重试 | 分片完整聚合后才执行工具；截止时间、取消与重试次数生效；发出增量后不重放                |
| 审计持久化 | PostgreSQL 迁移成功；成功、失败及各次重试可查询；元数据缺失不伪装为零                   |
| 观测       | 编程式模型接入容器的 ObservationRegistry，提示词、工具参数与密钥不进入观测内容          |

测试分两层：

- **离线单元与协议测试**：用 ChatModel 桩或本地 HTTP 替身检查路由、请求 JSON、响应解析、工具未执行和物理请求次数。
- **数据库集成测试**：使用独立 PostgreSQL 验证 Flyway 脚本、`llm_calls` 成功/失败记录和读回结果，不连接共享库。

真实模型冒烟单独开启，只验证服务连通、工具调用、流式响应和用量字段，不把依赖可解析或配置可加载当作接入成功。

## 五、做完怎么验

实现完成后，按以下顺序人工确认：

1. 根 POM、模型模块和配置绑定使用项目锁定的 JDK 21、Spring Boot 4.1.2 与 Spring AI 2.0.2；不引入旧版或不允许的厂商依赖。
2. 所有密钥从环境变量注入，代码、配置、日志和测试输出中没有真实凭证。
3. 两个 provider 的最终 HTTP 路径、请求模型、推理参数、工具 Schema 和返回解析都经过本地替身验证。
4. 失败、超时、限流和未知模型均留下 `success=false` 的 `llm_calls`，并把脱敏错误继续交给上层。
5. Provider 没有执行工具，工具结果通过调用 ID 回填；流式参数聚合完整后才执行。
6. PostgreSQL 迁移和审计读回通过；`EmptyUsage` 与 `EmptyRateLimit` 没有被误记为真实零值。
7. 真实模型冒烟通过后，再把 ReActLoop、Memory、Tool 和入口串成一个完整 Demo；仅 Provider 单独返回一次文本，不代表 Agent 运行时已经完成。

当前 `/Volumes/Data/my_project/agent-os` 仍是 Maven 骨架与工程基线，ProviderService、AgentLoader、Profile 和业务迁移脚本尚未实现。本文描述的是与项目设计对齐的实现契约和验收标准，不把目标能力写成已经交付。

继续阅读 [核心模块](/projects/agent-os/modules/)、[Agent 架构拆解](/projects/agent-os/agent-architecture/) 与 [ChatModel 工具调用](/frameworks/spring-ai/tools/chatmodel-tool-calling/)，把 Provider 放回完整运行时中理解。
