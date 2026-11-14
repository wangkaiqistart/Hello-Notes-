# Spring AI 2.0 修订记录

## 修订目标

沿用项目 baoyu-translate 的简体中文、技术读者、简明技术文档偏好；本轮属于既有文章的技术校订，不重新翻译原 PDF。保留原始课件、提取图与初稿阶段文件；旧站点正文保存为 before-spring-ai-2.0.mdx。

## 事实基线

- Java AgentOS 当前 POM：Java 21、Spring Boot 4.1.1、Spring AI 2.0.1。
- Spring AI API：Maven Central 2.0.1 发布源码，下载地址、条目和哈希见 source-evidence.json。
- 项目实现：文件与哈希见 project-source-evidence.json；只读查看，未修改 Java 工程。
- Java 示例：从最终 MDX 逐块提取，使用该工程已解析的 2.0.1 依赖与 JDK 21 离线编译；结果见 snippet-compilation.json。已有 Surefire 报告只用来取得依赖 classpath，不把历史测试结果当作本轮执行证据。

## 复核发现与修订

| 旧稿问题 | 修订 |
| --- | --- |
| 以 Boot 3 与 Spring AI Alibaba 为教学基线 | 明确当前工程版本，保留课程来源 |
| 要求 ChatModel 关闭自动执行，使用虚构 false 开关 | 明确 2.0 移除内部执行，区分 ChatClient 与 ToolCallingAdvisor |
| 课程 oryxos/.oryxos 配置名 | 更新为 aegisos/.aegisos，凭证引用、模型允许集合与端点规则 |
| 对外暴露混用 Profile、Prompt 和 Response 的伪接口 | 分开核心 ModelRequest/ModelResponse 与 Spring AI Prompt/ChatResponse |
| 只有概念工具适配，没有可核对 API | 增加 ToolCallback/ToolDefinition 描述符、真实 Options 与工具关联消息 |
| 调用后才写审计，默认不重试 | 对齐 begin/complete 独立短事务、服务层有限重试、UNKNOWN 外呼结果 |
| 测试断言自动执行开关 | 改为最终 HTTP 请求、完整工具意图与无额外推理请求的行为验收 |
| 未检查当前 Java 工程 | 对照源码和测试职责，明确本轮未运行工程测试或真实模型冒烟 |

## 图片处理

保留三张原始课程裁图，文件哈希不变。第三张的“关闭自动执行”、Response 和仅调用后审计均在图前明确说明版本及当前工程差异，图注标记为课程原图，不新增标签或重绘。

## 复核结论

示例不使用 1.x internalToolExecutionEnabled API，不把 ToolCallback 当真实执行器；区分 strict 工具 Schema 与结构化输出设置，区分底层重试和 ReAct 轮次，允许 tool-only 响应，保留 ID/参数/顺序。最终内容不宣称已验证外部模型连通。
