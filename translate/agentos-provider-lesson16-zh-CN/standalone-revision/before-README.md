# 第16节 Provider 课件整理与 Spring AI 2.0 校订

## 来源与当前版本

- 原 PDF 路径、哈希与页数见 `source-metadata.json`；原文件未修改，提取正文保存在 `source.txt`。
- 原课件为中文，按项目 baoyu-translate 的简体中文、技术读者和简明技术风格整理。
- `01-analysis.md` 至 `05-revision.md` 是首次课件整理过程；当前技术修订说明见 `spring-ai-2.0/revision-notes.md`，旧正文保存为该目录下的 `before-spring-ai-2.0.mdx`。
- 当前正文：`src/content/docs/projects/agent-os/provider.mdx`，与 `translation.md` 字节一致。
- 路由：`/projects/agent-os/provider/`；沿用侧边栏顺序 5.1、总览和核心模块入口。

## 本轮优化

- 对照当前 Java AgentOS 工程锁定 Java 21、Spring Boot 4.1.1、Spring AI 2.0.1。
- 纠正 ChatModel 自动执行的旧表述，明确 2.0 移除内部工具循环，区分 ChatClient 的 ToolCallingAdvisor。
- 用当前 `.aegisos` 配置与核心接口替换课程旧标识和混合伪接口。
- 增加真实 ToolCallback/ToolDefinition、OpenAiChatOptions 和工具消息 ID 关联示例。
- 对齐审计 begin/complete、有限重试、UNKNOWN 外呼结果和可空用量字段。
- 验收改为检查最终 HTTP 协议与工具行为，不断言旧的自动执行开关。
- 当前工程源码清单与哈希、Spring AI 发布源码下载证据均在 `spring-ai-2.0/`，未修改 Java 工程。

## 图片

三张原图继续保留，裁图坐标和哈希见 `source-assets.json`。图前有解释、准确替代文本、图注和大图链接；第三张课程原图的旧标注与当前实现差异已明确说明，未重绘或增加标签。

## 验证

- `npm run check`：18 files，0 errors / warnings / hints。
- `npm run build`：通过，110 pages；保留原有 i18n 空集合与 /404 路由警告。
- 两个完整 Java 示例和一个工具消息片段使用 JDK 21、Spring AI 2.0.1 实际依赖离线编译通过，见 `spring-ai-2.0/snippet-compilation.json`。
- 桌面 1440×1000、手机 390×844：HTTP 200，3 张图片加载且可打开大图，5 个代码块、7 个二级标题；无页面横向溢出和脚本错误，内部链接、标题锚点、总览入口与侧边栏正常。截图已目视复核，详见 `browser-validation.json`。
- 原图片及其他 8 个受保护文件哈希未变；最终副本一致，见 `content-validation.json`。
- Java 工程测试与真实模型冒烟：NOT_RUN；本轮只验证文章示例和知识库页面，不调用外部模型。
- 未提交、推送或发布。
