---
title: AgentOS：Provider 原理与实现
description: 从模型显式映射、Profile 加载、工具执行边界到调用审计与验收测试，理解 AgentOS 的模型接入层
sidebar:
  label: Provider 原理与实现
  order: 5.1
---

Provider 是 AgentOS 的模型接入层：接收 Profile 和提示词，选择模型客户端，发起一次调用，返回模型响应。它让 ReAct 循环通过统一入口使用不同厂商的模型。

本文整理自第16节《Agent Provider 原理解析、实现与代码讲解》。课程使用 JDK 21、Spring Boot 3.x 和 Spring AI Alibaba；示例是设计骨架，具体类型、依赖及 API 以项目锁定版本为准。

## Provider 在 Agent 中的位置

Agent 由 LLM、Tools、Memory、Loop 和 Environment 协作组成。Provider 把 LLM 接入运行时，ReActLoop 则决定何时调用模型、何时执行工具、何时结束。

一次请求中，上层传入两类信息：

- **Profile**：当前 Agent 使用的 provider、model 和 temperature 等配置。
- **Prompt**：本轮消息与允许使用的工具描述。

Provider 按 `provider.name` 找到对应的 `ChatModel`，提交请求，再把文本或工具调用意图交回上层。新增提供方并完成适配后，上层循环可以通过配置切换模型。

[![Provider 位于 ReAct 循环与各厂商模型之间：接收 Profile 和 Prompt，通过显式选择的 ChatModel 访问 LLM API](/images/projects/agent-os/provider-overview.png)](/images/projects/agent-os/provider-overview.png)

_沿箭头阅读一次模型调用的路径；点击图片可查看大图。_

`ChatModel` 是 Spring AI 的模型客户端抽象。图中每个 provider 配置一个客户端是课程方案；实际也可以按端点、凭证或其他配置维护多个实例。

### 工具描述与工具执行分开

模型收到工具名称、用途和参数 Schema 后，可能返回“调用 `http_get`，参数为……”这样的结构化意图。真正访问网络的是运行时中的 `ToolExecutor`。

Provider 只负责传递工具描述和模型响应。工具调用的权限、沙箱、超时、执行及结果回填，由上层循环和统一执行入口处理。

## 先确定职责和三个设计约束

Provider 的职责应保持集中：选模型、组装单次请求、调用模型、记录本次用量与审计。循环控制、上下文构建和记忆存储分别交给其他模块。

[![Provider 职责对照：负责选模型、单次调用、工具格式转换和审计；ReActLoop、ToolExecutor、PromptBuilder、MemoryService 分别处理循环、执行、上下文和记忆](/images/projects/agent-os/provider-boundaries.png)](/images/projects/agent-os/provider-boundaries.png)

_按模块划分责任，避免把循环和工具执行重新塞回 Provider。_

厂商协议转换尽量复用 Spring AI 及对应集成。项目自己的 `ProviderService` 负责组合和治理，不重复实现 OpenAI、Anthropic、Gemini 等协议。

### 约束一：按名称显式映射模型

多个模型客户端都实现 `ChatModel`，仅收集同类型 Bean 不能自动得到业务上正确的 provider 名称映射。需要明确维护：

```text
deepseek → 对应的 ChatModel
kimi     → 对应的 ChatModel
qwen     → 对应的 ChatModel
```

可以用 `@Qualifier` 指定 Bean，也可以启动时手动构造 `Map<String, ChatModel>`。关键是名称对应关系可检查，未知名称直接报错。

### 约束二：执行权只交给一套运行时

Spring AI 支持框架管理的工具执行，也支持把工具调用交回应用处理。AgentOS 自己实现 ReActLoop 和 ToolExecutor 时，需要关闭所用调用路径中的框架自动执行。

两套循环同时参与，可能让工具绕过项目的权限、沙箱与审计入口，也可能造成重复执行。应保留工具 Schema 和协议适配，把执行交给 AgentOS。

关闭方式随 Spring AI 版本、提供方和调用路径变化。课件中的 `autoExecuteTools(false)` 是语义示意；验收应证明工具没有被实际执行，不能只检查一个配置值。

### 约束三：先验证依赖，再承诺支持厂商

`deepseek`、`kimi`、`qwen` 在本文中是配置名称示例，不能据此断定任意版本都能直接接入。

接入前需要确认对应集成依赖的真实坐标、BOM 管理范围、协议、端点和模型能力。某个 starter 不在 BOM 中，也不等于完全无法接入；可能需要显式管理兼容版本或评估兼容协议。

```bash
mvn dependency:tree
```

依赖可解析只是前提，真实连通和工具调用能力仍需单独验证。

## Profile：先加载，再注册，再调用

Provider 是最先消费 Profile 的核心模块之一，需要一起明确 Profile 的数据结构、加载和查找方式。

| 组件 | 职责 |
| --- | --- |
| `Profile` | 承载 Agent 配置，包括模型、工具和后续扩展字段 |
| `ProfileLoader` | 启动时扫描 YAML，用 SnakeYAML 解析并校验 |
| `ProfileRegistry` | 维护 `Map<String, Profile>`，按名称查找有效配置 |

课程希望 Profile 一开始覆盖这些字段：`name`、`description`、`identity`、`provider`（含 `name/model/temperature`）、`tools`、`skills`、`mcp_servers`、`channels`、`notify_channels`、`schedules`、`bootstrap` 和 `settings`。

初期只开放启动扫描这一条注册路径；运行时 `register()` 属于后续扩展。定义字段不代表对应能力已经实现。

### 无效 Profile 怎么处理

课程采用“单个文件失败不阻断其他文件加载”的策略：

1. 读取并解析一个 Profile。
2. 校验 `provider.name` 能否在全局配置中找到。
3. 有效配置进入 Registry；无效配置记录清晰错误并跳过。

如果调用阶段再次遇到未知 provider，必须明确失败，不能静默切换默认模型。**跳过无效 Profile 与禁止错误路由是两个不同层面的规则。**

YAML 中的 `${ENV}` 占位符也要有明确的解析和校验机制；不能假定仅使用 SnakeYAML 就会自动完成环境变量替换。

## 全局连接配置与 Agent 调用配置

配置分两层，避免把凭证、连接参数和 Agent 行为混在一起。

| 层级 | 配置内容 | 解决的问题 |
| --- | --- | --- |
| 全局层 | 接入哪些 provider，凭证从哪里读取，必要的端点等连接配置 | 系统能连接哪些服务 |
| Profile 层 | 使用哪个 provider、model、temperature | 当前 Agent 如何使用模型 |

下面保留课程原始配置标识。`oryxos` 和 `.oryxos/profiles/` 是课程命名，不代表当前 AgentOS 工程实际使用这些配置键或目录。

```yaml title="application.yaml：课程全局配置示例"
oryxos:
  providers:
    - name: deepseek
      api-key: ${DEEPSEEK_API_KEY}
    - name: kimi
      api-key: ${KIMI_API_KEY}
```

```yaml title=".oryxos/profiles/ops-agent.yaml：课程 Profile 示例"
provider:
  name: deepseek
  model: deepseek-chat
  temperature: 0.7
```

Profile 的 `provider.name` 必须指向全局层已声明的配置。API Key 从环境变量或受控的凭证机制读取，配置文件中保留占位符。

模型路由与调用参数是两步：名称决定使用哪个客户端，`model` 和 `temperature` 必须传入该次请求，不能只写在 Profile 或审计记录里。

## 单次调用的实现骨架

Provider 对上层暴露 `chat(sessionId, Profile, Prompt)`。一次调用依次完成模型查找、消息和工具描述组装、模型请求、审计记录和响应返回。

[![ReActLoop 调用 ProviderService：先根据 Profile 查找 ChatModel，再组装关闭自动执行的请求，调用模型并记录 llm_calls，最后返回可能带工具意图的响应](/images/projects/agent-os/provider-call-flow.png)](/images/projects/agent-os/provider-call-flow.png)

_关注调用前的路由和请求设置，以及返回前的审计；图中包含成功与失败两条审计要求。_

下面按课件保留服务骨架，并修复 PDF 分页导致的断行。`Response`、`request(...)`、`prompt.getAvailableTools()` 和 `profile.getProvider()` 都是课程自定义抽象或简写；它们不是完整的 Spring AI API。Spring AI 的 `ChatModel.call(Prompt)` 通常返回 `ChatResponse`。

```java title="ProviderService：课程伪代码"
public Response chat(String sessionId, Profile profile, Prompt prompt) {
    ChatModel model = providerMap.get(profile.getProvider());
    if (model == null) {
        throw new ProviderNotFoundException(profile.getProvider());
    }

    var tools = adapter.toSpringAiTools(prompt.getAvailableTools());
    long startedAt = System.currentTimeMillis();
    try {
        Response resp = model.call(request(prompt, tools,
                /* autoExecuteTools */ false));
        audit.record(sessionId, profile.getProvider(), profile.getModel(),
                resp.usage(), true, null,
                System.currentTimeMillis() - startedAt);
        return resp;
    } catch (RuntimeException e) {
        audit.record(sessionId, profile.getProvider(), profile.getModel(),
                null, false, e.getMessage(),
                System.currentTimeMillis() - startedAt);
        throw e;
    }
}
```

阅读时抓住六点：

1. **传入 `sessionId`**：让模型调用记录与 Session 关联。
2. **按名称查找模型**：未知 provider 立即失败。
3. **适配工具描述**：只转换名称、参数 Schema 等信息。
4. **提交单次请求**：关闭框架自动工具执行，带上当前模型参数。
5. **成功和失败都审计**：记录 provider、model、Token、耗时、状态与错误。
6. **把响应或异常交回上层**：响应可能含工具意图，Provider 不在这里执行它。

骨架省略了 model 和 temperature 的请求组装，实际实现必须补齐。它也只包住模型调用附近的异常路径；未知名称、工具适配失败等前置错误如何记录，应另行定义。

### 工具格式适配器

课程中的 `OryxTool.getInputSchema()` 提供参数结构说明，适配器将其转换为对应 Spring AI 集成需要的工具描述。名称、说明、字段、类型和必填约束要保持一致。

`OryxTool` 是原课件标识。若当前工程使用不同的 Tool 抽象，应适配现有接口；不能为了照搬课件而新造一套并行工具体系。

### 调用审计与持久化

课程用 `llm_calls` 记录每次模型调用，并配套交付 `LlmCall` 实体、`LlmCallRepository` 和建表脚本。

| 信息 | 用途 |
| --- | --- |
| Session 标识 | 关联会话与执行过程 |
| provider / model | 确认实际使用的服务与模型 |
| Token 用量 | 记录提供方返回的用量，供统计与追溯 |
| 耗时 | 定位慢请求 |
| `success` | 区分成功与失败 |
| `error_message` | 记录超时、限流或模型错误等原因 |

失败时可能拿不到 Token 用量，应允许为空。错误信息落库前需要脱敏，避免保存 API Key 或其他敏感内容。

模型调用和审计写入是两次不同操作。课件伪代码不能保证审计一定落库；还需要定义审计故障如何处理、是否阻止返回，以及事务回滚是否会同时抹掉失败记录。

课程使用 SQLite，建议显式维护建表和迁移脚本，不依赖 `hibernate.ddl-auto=update` 代替迁移。测试应执行真实脚本，再验证表结构与读写结果。

### 这一阶段暂不扩展什么

故障切换（fallback）、并行竞速（hedge racing）、熔断和成本看板放到后续阶段。初期先确保一次请求的路由、参数、响应、错误和审计都可验证。

## 验收 Harness：把边界变成测试

课程强调在实现前或实现时确定验收测试。单元测试验证路由、配置和执行边界，数据库集成测试验证真实建表脚本，真实模型冒烟验证外部连通性。

### 默认验证与真实模型冒烟分开

| 测试类 | 验证重点 |
| --- | --- |
| `ProfileLoaderTest` | YAML 全字段解析；未知 provider 错误；坏文件隔离；环境变量占位符解析 |
| `ProviderServiceTest` | 双 provider 不串台；未知名称失败；成功失败审计；关闭自动执行；模型参数传递 |
| `ToolSchemaAdapterTest` | Schema 字段与约束一致；适配过程中不执行工具 |
| `LlmCallRepositoryTest` | 执行项目 SQL 建表脚本；确认 `success/error_message` 列；真实存取成功与失败记录 |
| `ProviderSmokeIT` | 使用真实凭证调用模型；响应非空；审计中新增成功记录 |

前四类不需要访问真实模型。Repository 测试即使不访问网络，也属于数据库集成验证，不能仅靠 Mock 证明 SQL 正确。

真实模型冒烟会依赖网络、凭证和外部服务，课程建议默认不在 CI 执行，按需手动开启。`@Tag("integration")` 只是标签，还需要 Maven 测试插件配置匹配的发现与分组规则。

### 三个关键回归测试

以下保留课件的三个测试思路与伪代码，修复跨页断行；辅助方法、Mock 返回值和测试夹具需要在实际工程补全。

第一个验证显式映射：选择 Kimi 时只调用对应客户端，DeepSeek 不应收到请求。

```java title="按名称路由，两个 provider 不串台"
@Test
void 按名路由_两个provider不串台() {
    var deepseek = mock(ChatModel.class);
    var kimi = mock(ChatModel.class);
    var service = new ProviderService(
            Map.of("deepseek", deepseek, "kimi", kimi), adapter, audit);

    service.chat("s-1", profileUsing("kimi"), prompt);

    verify(kimi, times(1)).call(any());
    verify(deepseek, never()).call(any());
}
```

第二个验证失败路径：异常继续向上抛，同时尝试写入 `success=false` 和错误原因。

```java title="模型调用失败仍记录审计"
@Test
void 调用失败_审计必须留下success为false的记录() {
    when(chatModel.call(any()))
            .thenThrow(new RuntimeException("connect timeout"));

    assertThrows(RuntimeException.class,
            () -> service.chat("s-1", profileUsing("deepseek"), prompt));

    verify(audit).record(eq("s-1"), eq("deepseek"), any(), isNull(),
            eq(false), contains("timeout"), anyLong());
}
```

Mock 验证证明的是“调用了审计方法”，真实落库还要靠 Repository 和事务相关测试确认。

第三个验证请求边界：工具描述保留，自动执行关闭。这里的 `Request`、`autoExecuteTools()` 和 `tools()` 仍是课件抽象。

```java title="携带工具 Schema，关闭自动执行"
@Test
void 带工具schema调用_请求里关闭了自动执行() {
    service.chat("s-1", profileUsing("deepseek"),
            promptWithTools(httpGetTool));

    var captor = ArgumentCaptor.forClass(Request.class);
    verify(chatModel).call(captor.capture());
    assertFalse(captor.getValue().autoExecuteTools());
    assertNotNull(captor.getValue().tools());
}
```

这三个测试分别锁住模型路由、失败审计和工具执行权。实际工程还应补一个行为测试：让模型返回工具调用意图，确认 Provider 完整返回该意图，工具执行次数为零。

### Maven 命令要与测试配置对应

课件给出的命令如下，凭证应预先通过安全方式注入环境变量：

```bash title="课程测试命令：以项目插件配置为准"
# 日常验证：需配置好默认测试范围
mvn test

# 真实模型冒烟：需配置好发现规则与 integration 标签
mvn test -Dgroups=integration
```

默认 Surefire 通常不会发现以 `IT` 结尾的测试类；仅添加 `-Dgroups=integration` 不一定能运行 `ProviderSmokeIT`。需要配置 `includes`，或用 Failsafe 在 `verify` 阶段执行，并核对报告中的实际用例数，避免“没有执行也显示成功”。

同样，裸 `mvn test` 是否跳过带标签的测试，也取决于插件的排除配置。不能把测试命名、标签与实际执行范围混为一谈。

## 交付范围与验收证据

本节可作为实现拆解的范围清单：

| 类别 | 课程要求 |
| --- | --- |
| 配置与加载 | Profile、ProfileLoader、ProfileRegistry、全局 providers 与 Profile provider 段 |
| 模型调用 | ProviderService、显式客户端映射、请求参数传递、工具格式适配器 |
| 数据与审计 | LlmCall、LlmCallRepository、包含成功失败字段的 SQL 脚本 |
| 验证 | 四类默认测试与按需开启的 ProviderSmokeIT |

完成后需要能提供以下证据：

- **依赖可用**：实际锁定版本下，对应依赖能下载并解析。
- **路由正确**：两个 provider 的调用互不串台，未知名称明确失败。
- **参数生效**：实际请求包含 Profile 选择的 model、temperature 及工具描述。
- **执行边界正确**：Provider 返回工具调用意图，不执行工具。
- **审计可读回**：成功、失败记录能通过真实 SQL 建表后的 Repository 查询。
- **凭证受控**：代码、配置和日志没有明文密钥；仅搜索 `sk-` 之类前缀不足以证明没有泄漏。
- **冒烟有证据**：需要验真连通时，实际执行测试并读回对应审计记录。

Provider 本身不构成完整的 Agent 对话入口。它需要与后续 ReAct 和 Tool 配合，才能支撑课程中的“查询天气并给出穿搭建议”等场景；模型接入成功也不等于整个 Demo 已完成。

## 与当前 AgentOS 的关系

本文是课程设计的整理，尚未核对当前 AgentOS Java 工程中的具体依赖、类名、配置和实现状态。示例代码未编译，真实模型冒烟未执行；课件中的安装、开发和测试步骤属于教学内容。

建议结合 [Agent 架构拆解](/projects/agent-os/agent-architecture/) 理解 Provider 与循环、工具的关系，再回到 [核心模块](/projects/agent-os/modules/) 查看整体实现顺序。Spring AI 的基础接口可继续阅读 [ChatModel](/frameworks/spring-ai/models/chat-model/) 和 [工具调用](/frameworks/spring-ai/tools/tool-calling/)。
