# Provider 资料整理与文档修订记录

## 当前文档

正文为 `src/content/docs/projects/agent-os/provider.mdx`，与 `translation.md` 字节一致；路由为 `/projects/agent-os/provider/`。保持独立、简明的中文技术文档风格，不在正文加入来源、品牌或版本迁移旁白。

本轮对照原 PDF、在线参考文档、2.0.2 发布源码与 `/Volumes/Data/my_project/agent-os` 修订；正文叙事顺序尽量保持原文的“定位 → 关键判断 → 实现步骤 → 验收”结构。详细结论、工程差异与证据见 [项目对齐复核](project-alignment/review.md)。当前 Java 项目仍为骨架，正文给出实现契约与验收要求；此次没有改动 Java 项目。

## 本轮优化

- 按新项目对齐 AgentOS 模块、`.AgentOS/agents/<name>/AGENT.md`、Profile 派生、PostgreSQL/JPA/Flyway 与审计字段。
- 恢复原文的学习路径：Provider 定位、动手前的职责与三个坑、按步骤实现、验收 harness 和人工验收；技术内容仍按 2.0.2 修订。
- 清除旧项目的配置路径、自定义响应协议、ProviderAdapter、begin/complete 审计与错误枚举等残留。
- 全局 `application.yaml` 只配置聊天连接，Agent 显式选择聊天模型及生成参数；Embedding 独立配置全局模型。
- 复用受治理的 ToolCallback，由 ToolExecutor 调用注入的 ToolCallingManager 执行；补齐历史、直接返回与流式聚合边界。
- 增加可编译客户端与请求构建示例，纠正 API 前缀、SDK 重试和请求参数误区。
- 补充截止时间、有限重试、取消、元数据缺失与审计失败处理，以及按行为验收的落地顺序。
- 调用图沿用布局、配色和箭头，仅修订流程与类型标签；概览图、职责图保持原样。

## 验证

- `npm run check`：18 files，0 errors / warnings / hints。
- `npm run build`：通过，110 pages；保留原有 i18n 空集合与 /404 路由警告。
- 两个完整 Java 示例使用 JDK 21 与项目 Spring AI 2.0.2 实际依赖编译通过。
- 本地 HTTP 替身验证通过：3 次 HTTP 请求、0 次工具执行，覆盖实际路径、Agent 参数、工具 Schema、仅工具响应、元数据、ToolContext、不重试和空模型拒绝。见 `project-alignment/snippet-validation.json`。
- 浏览器检查与截图复核见 `browser-validation.json`；内容副本与文件保护结果见 `content-validation.json`。
- 未执行完整 Java 项目测试、真实模型请求、PostgreSQL 集成或流式端到端验证；未提交、推送或发布。

## 来源与历史记录

- 原 PDF：路径、哈希与页数见 `source-metadata.json`，正文提取为 `source.txt`，图片来源为 `source-assets.json`。原文件未修改。
- `01-analysis.md` 至 `05-revision.md`：首次整理过程。
- `spring-ai-2.0/`：先前基于旧项目的修订证据，仅作为历史记录，不代表当前目标项目。
- `standalone-revision/`：先前独立成文改写及图片备份。
- `project-alignment/`：本轮改写前备份、项目文件基线、在线资料、2.0.2 源码、代码验证与复核结论；为当前复核入口。

正文图片保留准确替代文本、简短图注和大图链接；调用图可通过 `project-alignment/update-call-flow.py` 复现。
