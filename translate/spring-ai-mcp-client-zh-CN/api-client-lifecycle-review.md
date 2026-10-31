# MCP Client 生命周期与 Root 配置静态核验

核验日期：2026-10-31。只读核验 `../spring-ai-mcp-overview-zh-CN/api/` 中 Spring AI 2.0.2 自动配置、MCP Java SDK 2.1.0 源码快照。未启动 Spring 应用，未执行 `npx` 或 MCP 服务端，未调用模型。

以下文件名均相对于上述源码目录。此处行号依据当前快照；持久化时应复制相同源码后保留行号。主要结论由实际方法体支持，不以 Javadoc 意图代替实现。

## 1. `initialize()` 返回初始化结果，不能链式返回客户端

证据：

- `McpSyncClient.java:185-190`：返回类型为 `McpSchema.InitializeResult`，内部阻塞等待异步初始化结果。
- `McpClientAutoConfiguration.java:185-193`：自动配置先 `var client = customizedSpec.build()`，再按 `initialized` 开关调用 `client.initialize()`，最后将 **client** 加入结果集合。
- `McpAsyncClient.java:470`：异步 API 为 `Mono<McpSchema.InitializeResult> initialize()`；自动配置在 `McpClientAutoConfiguration.java:278-284` 单独 `.block()` 初始化后保留 client。

来源跨平台示例把 `.build().initialize()` 直接作为 `McpSyncClient` 方法返回值，静态类型不匹配。建议定稿改为：

```java
McpSyncClient client = McpClient.sync(
        new StdioClientTransport(stdioParams, McpJsonDefaults.getMapper()))
        .requestTimeout(Duration.ofSeconds(10))
        .build();
try {
    client.initialize();
    return client;
}
catch (RuntimeException e) {
    client.close();
    throw e;
}
```

以上只展示返回值和失败清理修正；`McpJsonDefaults` 的可用版本及 mapper 选择由主审校再核对，不以本段代码证明其他 API 已验证。若初稿只需最小修正，可不新增 try/catch，但至少拆开初始化并返回 `client`。

## 2. 单个手动客户端 Bean 不会让连接自动配置退让

### 自动配置如何创建客户端

- `McpClientAutoConfiguration.java:99-103`：类级别按 `spring.ai.mcp.client.enabled=true` 激活，缺省也激活。
- `McpClientAutoConfiguration.java:145-151`：`mcpSyncClients(...)` 声明为 `@Bean`，仅按 `type=SYNC` 选择，返回 **`List<McpSyncClient>`**。此 Bean 方法未声明 `@ConditionalOnMissingBean`。
- `McpClientAutoConfiguration.java:153-158`：将所有 `List<NamedClientMcpTransport>` 展开，逐条创建客户端。
- `McpClientAutoConfiguration.java:240-245`：异步路径同样返回 `List<McpAsyncClient>`，并未按用户客户端 Bean 退让。
- `McpClientAutoConfiguration.java:222-228` 的 `@ConditionalOnMissingBean` 约束的是 **`McpSyncClientConfigurer`**，不约束 `mcpSyncClients` 的创建；异步对应 297-302 行。

### STDIO 如何创建传输

- `StdioTransportAutoConfiguration.java:54-58`：同样按通用 `enabled` 开关激活，未检查用户已有客户端。
- `StdioTransportAutoConfiguration.java:72-84`：`stdioTransports` 返回 `List<NamedClientMcpTransport>`，无缺失 Bean 条件；对配置中的每条连接创建 `StdioClientTransport`。
- `McpStdioClientProperties.java:102-109`：先读取外部 JSON，再追加 `connections` 属性；同名连接由属性映射覆盖 JSON 条目。

因此，把 `@ConditionalOnMissingBean(McpSyncClient.class)` 放到用户示例方法上，只能决定 **用户自己的方法是否注册**，不能反向让上述自动配置停止。来源“加该注解就避免与 JSON 自动配置冲突”的说法不成立。

### 建议给读者的选择

- **继续使用 Starter 自动配置**：连接统一放在属性或 JSON 中，用 `McpClientCustomizer` 修改客户端规格，不额外声明同一服务端的手动客户端。
- **自行管理全部客户端**：明确设置 `spring.ai.mcp.client.enabled=false`，自行构造、初始化、关闭客户端，并自行创建/传递工具回调提供者。不要暗示关闭自动配置后仍会自动得到 MCP 工具。
- **有意混用多套客户端**：必须明确生命周期、连接去重和工具回调接入，不能依赖一个 `@ConditionalOnMissingBean` 注解解决。

`enabled=false` 的相关证据：`McpClientAutoConfiguration.java:101-102`、`StdioTransportAutoConfiguration.java:56-57`，以及 `McpToolCallbackAutoConfiguration.java:104-120` 的共同激活条件。

## 3. 自动工具回调集成消费客户端集合

- `McpToolCallbackAutoConfiguration.java:68-85`：同步提供者注入 `ObjectProvider<List<McpSyncClient>>`，76 行使用 `stream().flatMap(List::stream)` 汇总。
- `McpToolCallbackAutoConfiguration.java:88-101`：异步提供者同样消费客户端集合。

这进一步说明不能把“声明一个 `McpSyncClient` Bean”直接等同于“替代 Starter 自动客户端且自动接入工具提供者”。单个手动 Bean 不符合源码明确声明的集合提供者入口。实际 Spring 集合候选解析细节需要上下文测试，但文档不应承诺其必然被此配置收集。

## 4. 生命周期清理

- `McpClientAutoConfiguration.java:205-209`：创建同步客户端集合的可关闭包装对象。
- `McpClientAutoConfiguration.java:313-318`：包装对象 `close()` 遍历关闭所有客户端。
- 异步对应 `McpClientAutoConfiguration.java:291-295`、321-325 行。
- 手动 `@Bean(destroyMethod = "close")` 有助于成功注册后的正常关闭，但初始化过程中抛错的对象尚未成为 Bean，不能仅依赖销毁回调清理。上面的 try/catch 属于可选补强。

## 5. Root 属性位置与实际实现范围

### 属性归属与默认值

- `McpClientCommonProperties.java:31-34`：配置前缀为 `spring.ai.mcp.client`。
- `McpClientCommonProperties.java:93-99`：`rootChangeNotification` 默认 `true`。
- `McpClientCommonProperties.java:156-161`：对应 getter/setter。
- `McpStdioClientProperties.java:45-64`：STDIO 前缀为 `spring.ai.mcp.client.stdio`，声明的是 JSON 资源与连接映射，未声明 `rootChangeNotification`。

来源 YAML 把该键放到 `client.stdio` 下不符合属性类；正确归属是 **`spring.ai.mcp.client.root-change-notification`**。请求超时默认 20 秒也由 `McpClientCommonProperties.java:59-63` 确认。

### 不能承诺仅改属性就启用了 Roots 能力

在本次提供的源码快照中全文检索 `rootChangeNotification` / `isRootChangeNotification`，仅命中 `McpClientCommonProperties` 的字段与访问器；`McpClientAutoConfiguration` 同步、异步创建路径未读取该属性。

- 同步路径：`McpClientAutoConfiguration.java:166-185`，处理器注册表的 `getCapabilities(...)` 在 183 行传入规格，随后在 185 行运行定制器。
- 异步路径：`McpClientAutoConfiguration.java:258-276`，相同行为见 274、276 行。

这是“快照中未找到该属性被自动配置消费”的静态观察，不扩展为所有版本均无效。建议在属性表保留来源键与默认值，同时加简短说明：**该键的 2.0.2 声明已确认，但要使用根目录能力，应显式配置客户端 capabilities 和根目录列表，不能只把此开关当作完整 Roots 配置。** 如不希望增加疑似缺陷旁注，可将实现差异仅留在翻译记录，正文避免效果保证。

### SDK 实际条件

- `McpAsyncClient.java:205-208`：客户端保存 `features.clientCapabilities()` 与 `features.roots()`。
- `McpAsyncClient.java:223-225`：只有 `clientCapabilities.roots() != null` 时才安装 `roots/list` 处理器。
- `McpAsyncClient.java:496-520`：`addRoot` 要求 Roots 能力存在；只有 `roots().listChanged()` 为真且客户端已初始化时才自动发送变更通知。
- `McpAsyncClient.java:528-549`：`removeRoot` 采用相同条件。
- `McpSchema.java:742-743`：`ClientCapabilities.Builder.roots(Boolean listChanged)` 创建对应 `RootCapabilities`。
- `McpSyncClient.java:196-211`：同步的通知、增加和删除根目录 API 委托上述异步实现并阻塞。

Roots 是对服务端声明的协议信息，不代表操作系统级沙箱或文件访问授权已经自动落实。

## 6. STDIO 的进程边界

`StdioClientTransport.java:141-152` 将命令和参数交给 `ProcessBuilder`，随后调用 `processBuilder.start()` 启动 **服务端子进程**。`177-178` 行默认构建普通 `ProcessBuilder`。因此来源把 STDIO 称为 “in-process” 容易误导，译文应明确为同机进程间的标准输入输出通信，而非同一 JVM 内部调用。
