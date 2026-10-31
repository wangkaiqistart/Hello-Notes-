# MCP Server 2.0.2 静态源码审校

核验日期：2026-10-31。证据为 Maven Central `org.springframework.ai` 2.0.2 sources.jar，工作快照位于 `../spring-ai-mcp-overview-zh-CN/api/`。本记录仅为静态 API / 条件核验，未启动 Java 应用或调用 MCP 服务。

## 1. protocol 属性值与自动配置缺省条件存在矛盾

- `McpServerProperties.java:100`：属性对象字段初始化为 `ServerProtocol.STREAMABLE`。
- `McpServerAutoConfiguration.java:375-376`：SSE 自动配置条件为 `havingValue="SSE", matchIfMissing=true`。
- 同文件 `395-396`：Streamable 自动配置条件为 `havingValue="STREAMABLE", matchIfMissing=false`。
- `McpServerSseWebMvcAutoConfiguration.java:75` 使用 `EnabledSseServerCondition`；`76` 标记此 SSE 自动配置自 2.0.0 起弃用并计划删除。
- `McpServerStreamableHttpWebMvcAutoConfiguration.java:46-48` 和 `McpServerStreamableHttpWebFluxAutoConfiguration.java:46-47` 使用 `EnabledStreamableServerCondition`。

**结论与建议**：不能把属性类字段默认值直接当作实际缺省传输。`@ConditionalOnProperty` 检查环境键，不会读取此绑定对象的 Java 字段初始值。按上述静态条件，未设置 protocol 会匹配旧式 SSE，而不是 Streamable 自动配置。正文建议明确要求 **显式设置 `spring.ai.mcp.server.protocol=STREAMABLE`**，表格无需写“或留空”；内部审校保留冲突证据，不向读者承诺省略配置就得到 Streamable。

## 2. 能力开关仅有四类，默认 true

- `McpServerProperties.java:228-236`：`capabilities.resource`、`tool`、`prompt`、`completion` 四个布尔字段均为 `true`。
- `McpServerAutoConfiguration.java:133-143`：tool 开关控制工具能力声明及工具规格注册。
- `148-170`：resource 开关控制静态资源与资源模板的能力声明及注册。
- `176-198`：prompt / completion 同样由对应开关控制。
- 异步分支 `255-319` 具有同样控制逻辑。

**建议**：保留来源 Tools、Resources、Prompts、Completions、Logging、Progress、Ping 的能力介绍，但将笼统的“所有能力默认启用”改成“工具、资源、提示词与参数补全四类配置开关默认开启；实际可用能力仍取决于传输、注册内容与协议协商”。不推断 Progress/Ping 有同名 Boot 属性。

## 3. 自定义 Provider Bean 会令自动 Provider 退让，但 Router Bean仍可自动注册

### WebMVC

- `McpServerStreamableHttpWebMvcAutoConfiguration.java:51-62`：Provider Bean 方法有 `@ConditionalOnMissingBean`，默认把 Boot 的 `mcpServerJsonMapper`、`mcpEndpoint`、`keepAliveInterval`、`disallowDelete` 传给构建器。
- 同文件 `67-71`：Router Bean 单独用 `@ConditionalOnMissingBean(name="webMvcStreamableServerRouterFunction")` 控制，接收容器中 `WebMvcStreamableServerTransportProvider` 并返回其 `getRouterFunction()`。
- 因此在该 Starter 自动配置激活（显式 STREAMABLE、非 STDIO 等条件成立）时，应用声明具体类型的自定义 Provider Bean 后，**无需额外重复注册 Router Bean**；自动 Router 会使用自定义 Provider。
- 脱离 Starter / 排除自动配置时，需要自行把 `provider.getRouterFunction()` 注册为 `RouterFunction<ServerResponse>` Bean，或以其他方式挂载路由；只创建 Provider 不会凭空将其内部 Router 发布给 Spring。

### WebFlux

- 对应 `McpServerStreamableHttpWebFluxAutoConfiguration.java:50-61`：Provider 退让条件相同；默认构建器调用 `.messageEndpoint(...)`（与 WebMVC 的 `.mcpEndpoint(...)` 方法名不同）。
- `66-70`：独立自动 Router Bean 采用名称 `webFluxStreamableServerRouterFunction`，返回容器中 Provider 的 Router。

### 不会自动合并 Boot 设置

自定义 Provider Bean 跳过整个默认 Provider 构建方法，**不会仅“追加”一个 contextExtractor**。来源只调用 `.contextExtractor(...).build()` 的示例将使用构建器自己的默认值，而不是自动沿用所有 `spring.ai.mcp.server.streamable-http.*` 设置。

建议在正文说明这一点；需要保留自定义 endpoint、keep-alive、delete 设置和 Boot JSON 映射器时，应像自动配置方法一样显式传入：

- WebMVC：`.jsonMapper(new JacksonMcpJsonMapper(jsonMapper))`、`.mcpEndpoint(properties.getMcpEndpoint())`、`.keepAliveInterval(properties.getKeepAliveInterval())`、`.disallowDelete(properties.isDisallowDelete())`。
- WebFlux：第二项使用 `.messageEndpoint(properties.getMcpEndpoint())`，其余相同。

## 4. Provider 默认 contextExtractor 与构建器细节

### WebMVC

- `WebMvcStreamableServerTransportProvider.java:180-184`：构造时建立 GET / POST / DELETE 内部 Router。
- `306-307`：`getRouterFunction()` 仅返回内部 Router。
- `334`、`443`、`565`：分别在相关请求处理路径调用 `this.contextExtractor.extract(request)`。
- `854-860`：默认 endpoint `/mcp`、`disallowDelete=false`、context extractor 返回 `McpTransportContext.EMPTY`、keep-alive 为空。
- `913-916`：`contextExtractor(...)` 直接替换构建器字段，不与旧 extractor 合并。
- `984-994`：未显式传入 JSON mapper 时回退 `McpJsonDefaults.getMapper()`，所以来源省略 `.jsonMapper(...)` 仍有 mapper，并非必然构建失败。

### WebFlux

- `WebFluxStreamableServerTransportProvider.java:129-133` 建立内部 Router；`230-231` 返回 Router。
- `598-606`：默认 mapper `McpJsonDefaults.getMapper()`、endpoint `/mcp`、empty context、`disallowDelete=false`、keep-alive 为空。
- `653-656`：`contextExtractor(...)` 直接替换 extractor；`734-742` 将字段传给 Provider 构造器。

**建议**：原文说 MCP 传输上下文默认空是准确的，但要解释“提取 HTTP 头只构造上下文，不执行安全校验”。Authorization 缺失时 `firstHeader(...)` 可返回 null，`Map.of("authorization", authorization)` 不接受 null；应返回 `McpTransportContext.EMPTY` 或空 Map，不应把缺头误变成空指针错误。

## 5. 注解扫描开关与同步异步模式

- `McpServerAnnotationScannerProperties.java:27-29`：前缀 `spring.ai.mcp.server.annotation-scanner`，`enabled=true`。
- `McpServerAnnotationScannerAutoConfiguration.java:48-49`：`enabled=true` 或缺省时启用扫描自动配置。
- `54-55`：扫描注解集合为 `McpTool`、`McpResource`、`McpPrompt`、`McpComplete`。
- `65-67`：通过 `ServerAnnotatedMethodBeanPostProcessor` 处理实际 Bean，不是遍历所有未注册类。
- `McpServerSpecificationFactoryAutoConfiguration.java:50-51`：SYNC 或缺省时使用同步规格工厂；`96`：ASYNC 时使用异步规格工厂。
- `McpServerProperties.java:96`：默认 API 类型 SYNC；它与使用 WebMVC/WebFlux 传输是不同配置维度。

**建议**：写“自动发现已注册 Spring Bean 上的注解方法”，不要说 Starter 会扫描并实例化任意类。保留来源关于同步/异步注解方法匹配模式的说明，不把 WebFlux 自动等同 ASYNC。

## 6. 与页面安全示例有关的边界

来源 `accessProtectedResource` 读取 `authorization` 变量后直接返回成功文本，没有验证凭据或执行授权。它只能演示上下文注入与读取。建议正文紧邻代码明确“示例不执行鉴权；实际访问控制由 Spring Security 等安全层完成”，不要将提取到 Authorization 当作授权成功。
