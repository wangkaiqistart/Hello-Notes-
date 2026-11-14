# AgentOS：从需求拆解到 AI 协作实施整理

三份 PDF 的内容合并到现有 `src/content/docs/projects/agent-os/ai-development-guide.mdx`，不新增重复页面。正文按原资料的逻辑推进，但移除了课程导航、演示课旁白和未核验的工具版本承诺，改成面向当前 AgentOS 项目的独立实施指南。

## 页面结构

1. 从“写代码”转向“把事情做成”：对应第 10 节的传统开发、AI 协作、SDD/Harness/Loop 和人的责任边界。
2. 开发前准备：对应第 12 节的文档输入、9 个 Maven 模块、公共边界和规格化方式选择。
3. Spec-Kit 原理：对应第 13 节的 spec-as-source、constitution、阶段闭环、analyze 和产物目录。
4. AgentOS 落地：保留五个 User Story 的依赖、四条协作纪律和阶段验收，并以当前项目的 Spring Boot 4.1.2、Spring AI 2.0.2、PostgreSQL 和 9 模块为事实基线。

## 与当前项目对齐

- `/Volumes/Data/my_project/agent-os/CLAUDE.md` 是工程约束入口；当前仓库是 Maven 骨架加工程基线，不能把计划中的能力写成已实现。
- 当前核心阶段是 9 个 Maven 模块，五大能力为 Provider、ReAct、Memory、Tool、Web Service。
- ReActLoop 自实现；Spring AI 2.0 提供 `ChatModel`、`ToolCallback`、`ToolCallingManager` 等组件，不能引入第二条自动工具执行路径。
- PostgreSQL/JPA/Flyway 是持久化事实源，不使用 SQLite/H2；工具、权限、超时和审计必须从统一入口验证。
- Spec-Kit、OpenSpec 和轻量手工规格按任务类型选择；本文不宣称 Spec-Kit 已安装或当前工作区已初始化。

## 来源与证据

三份 PDF 的路径、页数和 SHA-256 见 `sources.json`，提取文本保存在 `lesson10-source.txt`、`lesson12-source.txt`、`lesson13-source.txt`。整理前页面保存在 `before-ai-development-guide.mdx`。项目文件基线和验证结果记录在 `validation.json`。

PDF 中的“时间安排”仅作为能力依赖示例，当前项目的真实验收以 [验收与演进](/projects/agent-os/roadmap/) 和项目文档为准。没有执行 PDF 中的安装、初始化或开发命令，也没有修改 `/Volumes/Data/my_project/agent-os`。
