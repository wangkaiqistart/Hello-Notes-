# Server 初稿问题记录

- 两个 SSE 表格链接来源包含 `#<em>sse_webmvc_server` / `#<em>sse_webflux_server`，以及损坏的强调标记。初稿已修复为 `#_sse_webmvc_server` / `#_sse_webflux_server` 并整理正常表头。请核验目标锚点。
- 来源将 STDIO 描述成 in-process / server inside host application，与通常通过客户端启动服务端子进程的实现不一致。初稿正文已写标准输入输出与本地子进程，避免“同 JVM”误解。
- 来源将 STDIO、SSE 等称为 protocol versions，初稿改“传输和运行方式”，协议版本协商与传输选择应区分。
- 来源说所有能力默认启用，需要核验是否仅指可配置的 tools/resources/prompts/completions 开关，而不是每种传输都支持 sampling/progress/ping。初稿暂保留语义并加“取决于服务端与传输类型”。
- 2 个 contextExtractor 示例：缺少 Authorization 请求头时 `Map.of("authorization", authorization)` 会因 null 抛异常。请补空值处理，原代码初稿保持不动。
- `accessProtectedResource` 仅提取 Authorization 并返回成功字符串，完全没有认证或授权。请明确它只演示上下文读取，不是安全实现。
- 手动构建 Provider 只调用 `contextExtractor(...).build()`，默认 endpoint/session json mapper 等行为需源码确认。可能需要与自动配置的 RouterFunction bean 配合，但原文无说明。
- CalculatorTools 的 configData 未定义，是业务占位，不是可直接运行完整类；可在正文说明由应用提供。
- 特殊参数列表使用 Exchange 与后续 RequestContext；确认 SDK 1.0 推荐 API，避免错误推断为同一个类型。
- 来源 6 段代码未改；含 5 Java、1 YAML。无来源图片。18 个显式英文锚点均保留。
