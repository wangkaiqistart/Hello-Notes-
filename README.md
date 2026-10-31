# Starlight Starter Kit: Basics

[![Built with Starlight](https://astro.badg.es/v2/built-with-starlight/tiny.svg)](https://starlight.astro.build)

```
yarn create astro@latest -- --template starlight
```

> 🧑‍🚀 **Seasoned astronaut?** Delete this file. Have fun!

## 🚀 Project Structure

Inside of your Astro + Starlight project, you'll see the following folders and files:

```
.
├── public/
├── src/
│   ├── assets/
│   ├── content/
│   │   └── docs/
│   └── content.config.ts
├── astro.config.mjs
├── package.json
└── tsconfig.json
```

Starlight looks for `.md` or `.mdx` files in the `src/content/docs/` directory. Each file is exposed as a route based on its file name.

Images can be added to `src/assets/` and embedded in Markdown with a relative link.

Static assets, like favicons, can be placed in the `public/` directory.

## 🧞 Commands

All commands are run from the root of the project, from a terminal:

| Command                | Action                                           |
| :--------------------- | :----------------------------------------------- |
| `yarn install`         | Installs dependencies                            |
| `yarn dev`             | Starts local dev server at `localhost:4321`      |
| `yarn build`           | Build your production site to `./dist/`          |
| `yarn preview`         | Preview your build locally, before deploying     |
| `yarn astro ...`       | Run CLI commands like `astro add`, `astro check` |
| `yarn astro -- --help` | Get help using the Astro CLI                     |

## 👀 Want to learn more?

Check out [Starlight’s docs](https://starlight.astro.build/), read [the Astro documentation](https://docs.astro.build), or jump into the [Astro Discord server](https://astro.build/chat).

## Spring AI 四周学习计划

记录日期：2026-10-24。

适用基础：熟悉 Java、Spring Boot、Maven 和 REST API。每周投入 10–15 小时，按每周约 12 小时安排，总计约 48 小时。

学习目标：围绕“文档问答 + 订单查询助手”，掌握模型调用、多轮对话、检索增强生成（RAG）、工具调用、MCP，以及效果评估和问题定位，最终独立完成一个可运行的 Spring AI 应用。

### 环境与版本

- 使用 Java 21、Maven，通过 [Spring Initializr](https://start.spring.io/) 创建独立的学习项目，并使用 Spring AI BOM 管理依赖。
- 截至记录日期，官方文档默认版本为 Spring AI 2.0.2，入门页注明 Spring AI 2.0.x 适配 Spring Boot 4.0.x / 4.1.x。
- 如需贴近 Spring Boot 3 项目，选择 Spring AI 1.1.x 及其对应文档，适配 Spring Boot 3.4.x / 3.5.x。项目依赖、示例和文档应保持同一版本系列。
- 第一周先接入一个聊天模型；第二周再选择支持 Embedding 的模型和一种向量数据库。聊天模型与 Embedding 模型可以来自不同提供方。
- 模型密钥通过环境变量等外部配置提供，不提交到仓库。

版本参考：[当前版本入门文档](https://docs.spring.io/spring-ai/reference/getting-started.html)、[Spring AI 1.1 入门文档](https://docs.spring.io/spring-ai/reference/1.1/getting-started.html)。以下阅读链接指向当前默认版本；选择 1.1.x 时应切换到对应版本文档。

### 四周路线与验收标准

| 时间                    | 学习内容                                                                 | 实践任务                                                                           | 验收标准                                                                                      |
| ----------------------- | ------------------------------------------------------------------------ | ---------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| 第 1 周：模型调用与对话 | `ChatClient`、`ChatModel`、提示词模板、结构化输出、Chat Memory、Advisors | 实现普通聊天、SSE 流式聊天；从自然语言提取订单查询 DTO；增加多轮对话               | 能返回流式答案；结构化结果经过字段校验；不同会话互不串话                                      |
| 第 2 周：工具调用与 MCP | `@Tool`、参数描述、工具执行流程、异常处理；MCP Client / Server           | 接入模拟订单状态查询；把查询能力暴露为 MCP 工具，再由助手调用                      | 能检查实际调用参数和结果；正确处理查无订单、超时、参数缺失；能解释 Tool Calling 与 MCP 的关系 |
| 第 3 周：完整 RAG 链路  | 文档读取与切分、Embedding、向量存储、相似度检索、元数据过滤、RAG         | 导入一组 Markdown 文档，构建带来源引用的知识问答；比较不同切分大小与检索参数       | 能追溯回答来源；资料不足时明确说明；能区分检索错误和生成错误                                  |
| 第 4 周：整合与工程验证 | 工作流编排、模型评估、可观测性、超时与重试、Token 用量                   | 实现“识别问题 → 检索文档或查询订单 → 汇总回答”；建立回归题集，记录质量、耗时和用量 | 项目可完整演示；修改提示词或模型后能重复评估；失败原因可以定位                                |

### 官方文档阅读顺序

1. [AI Concepts](https://docs.spring.io/spring-ai/reference/concepts.html)：理解模型、Token、上下文窗口、消息角色、Embedding 和 RAG。
2. [ChatClient](https://docs.spring.io/spring-ai/reference/api/chatclient.html)：掌握同步调用、流式调用，以及与 `ChatModel` 的关系。
3. [Prompts](https://docs.spring.io/spring-ai/reference/api/prompt.html)：学习提示词模板、系统消息和输出约束。
4. [Structured Output](https://docs.spring.io/spring-ai/reference/api/structured-output.html)：将输出映射为 Java DTO，并处理校验和解析失败。
5. [对话记忆（Chat Memory）](src/content/docs/frameworks/spring-ai/core/chat-memory.mdx)：理解会话标识、记忆窗口和会话隔离。
6. [Advisors](https://docs.spring.io/spring-ai/reference/api/advisors.html)：理解请求处理链及上下文处理方式。
7. [工具调用基础](src/content/docs/frameworks/spring-ai/tools/tool-calling.mdx) → [工具调用 Advisor](src/content/docs/frameworks/spring-ai/tools/tool-calling-advisor.mdx)：理解工具定义、执行循环与记忆配合；[工具搜索](src/content/docs/frameworks/spring-ai/tools/tool-search-tool.mdx)和 [ChatModel 工具调用](src/content/docs/frameworks/spring-ai/tools/chatmodel-tool-calling.mdx)按需深入。
8. [MCP 概览](src/content/docs/frameworks/spring-ai/mcp/overview.mdx) → [MCP 客户端](src/content/docs/frameworks/spring-ai/mcp/client.mdx) → [MCP 服务端](src/content/docs/frameworks/spring-ai/mcp/server.mdx)：理解协议能力、传输、共享会话和工具接入；注解完整参考与高级配置按需查阅来源链接。
9. [ETL Pipeline](https://docs.spring.io/spring-ai/reference/api/etl-pipeline.html)、[Embeddings](https://docs.spring.io/spring-ai/reference/api/embeddings.html)、[Vector Stores](https://docs.spring.io/spring-ai/reference/api/vectordbs.html)：完成文档读取、切分、向量化与存储。
10. [RAG](https://docs.spring.io/spring-ai/reference/api/retrieval-augmented-generation.html)：学习检索增强、Top-K、相似度阈值和元数据过滤。
11. [Model Evaluation](https://docs.spring.io/spring-ai/reference/api/testing.html)、[Observability](https://docs.spring.io/spring-ai/reference/observability/index.html)：建立评估、耗时和用量记录。
12. [Building Effective Agents](https://docs.spring.io/spring-ai/reference/api/effective-agents.html)：先掌握明确步骤的工作流，再按需求深入复杂 Agent 编排。

### 每周时间安排

- 工作日选择 4 天，每天 1.5 小时：30 分钟读文档，60 分钟实现与实验。
- 周末投入 6 小时：3 小时整合功能，2 小时验证，1 小时整理笔记。
- 每周能投入到 15 小时时，将额外时间用于比较参数、检查调用链和分析失败案例。
- 阅读示例时记录：输入是什么、框架做了什么、模型返回什么、失败时怎么办。

### 第一周具体安排

| 学习日  | 任务                                                             |
| ------- | ---------------------------------------------------------------- |
| 第 1 天 | 创建项目，配置一个模型，跑通 `ChatClient`；理解请求与响应结构    |
| 第 2 天 | 完成 REST 和 SSE 接口，观察完整响应与流式响应的差异              |
| 第 3 天 | 编写提示词模板，将用户描述映射为 Java DTO，并校验结果            |
| 第 4 天 | 增加 Chat Memory，用两个会话验证上下文隔离                       |
| 周末    | 学习 Advisors，把本周功能整合起来，验证异常并整理学习项目 README |

### 贯穿四周的验证方法

从第一周起维护一份题集，逐渐扩充到约 30 条，覆盖普通问答、多轮追问、文档问答、工具查询、资料缺失和调用失败。固定测试输入和预期判断标准，每次修改提示词、模型或检索参数后重复执行并记录：

- 回答是否正确，是否有来源支撑。
- 是否检索到正确文档、调用了正确工具。
- 工具参数是否正确，耗时和 Token 用量是否符合预期。
- 失败发生在检索、生成、参数解析还是工具执行环节。

四周后的目标是能够解释：答案从哪里来、业务工具如何执行、效果怎么衡量、失败怎么定位。

### 学习进度

- [ ] 第 1 周：聊天、流式输出、结构化输出与会话隔离通过验证。
- [ ] 第 2 周：模拟订单工具与 MCP 调用通过验证。
- [ ] 第 3 周：文档入库、检索和带来源的 RAG 问答通过验证。
- [ ] 第 4 周：完成整合演示、约 30 条回归题集和评估记录。

后续按实际需求深入多模型路由、多模态和复杂 Agent 编排。

### 笔记目录规划

笔记按主题组织，学习进度按周推进。框架知识放在 `src/content/docs/frameworks/spring-ai/`，综合项目记录放在 `src/content/docs/projects/spring-ai-assistant/`。当前规划 31 篇笔记；[Spring AI 总览](src/content/docs/frameworks/spring-ai/index.mdx)、[AI 核心概念](src/content/docs/frameworks/spring-ai/concepts.mdx)、[快速入门](src/content/docs/frameworks/spring-ai/getting-started/quickstart.mdx)、[ChatClient API](src/content/docs/frameworks/spring-ai/core/chat-client.mdx)、[提示词](src/content/docs/frameworks/spring-ai/core/prompts.mdx)、[响应元数据](src/content/docs/frameworks/spring-ai/core/chat-response-metadata.mdx)、[结构化输出](src/content/docs/frameworks/spring-ai/core/structured-output.mdx)、[Advisors API](src/content/docs/frameworks/spring-ai/core/advisors.mdx)、[多模态](src/content/docs/frameworks/spring-ai/core/multimodality.mdx)和[模型小节](src/content/docs/frameworks/spring-ai/models/index.mdx)（概览、聊天、Embedding、图像、音频和审核模型），以及[对话记忆](src/content/docs/frameworks/spring-ai/core/chat-memory.mdx)已创建并接入侧边栏，其余页面随学习逐篇补充。提示词、响应元数据按来源章节整理；结构化输出将高层用法、校验与自动纠正、原生输出和转换器合为一篇，便于按需深入。以下为完整目录规划。

```text
src/content/docs/
├── frameworks/
│   └── spring-ai/
│       ├── index.mdx                          # Spring AI 总览：定位、核心组件、阅读路线
│       ├── concepts.mdx                       # AI 核心概念：模型、提示词、向量、RAG 与工具调用
│       ├── getting-started/
│       │   └── quickstart.mdx                  # 环境与版本、BOM、模型配置、首次调用
│       ├── core/
│       │   ├── chat-client.mdx                 # ChatClient / ChatModel、消息、同步与流式调用
│       │   ├── prompts.mdx                     # 提示词、消息角色、模板与 Token
│       │   ├── chat-response-metadata.mdx      # 响应元数据、限流信息、Token 与缓存用量
│       │   ├── structured-output.mdx           # DTO 映射、Schema 校验与纠正、原生约束、输出转换器
│       │   ├── multimodality.mdx               # 文字与媒体组合、图片输入、模型支持边界
│       │   ├── advisors.mdx                    # 处理链、执行顺序、自定义实现、递归循环与累计用量
│       │   └── chat-memory.mdx                 # 会话标识、记忆窗口、隔离与存储
│       ├── models/
│       │   ├── index.mdx                       # 模型分类、统一 API、选型与官网查询入口
│       │   ├── chat-model.mdx                  # ChatModel、流式响应、请求选项与响应结构
│       │   ├── embedding-model.mdx             # 文本向量、常用方法、维度与模型一致性
│       │   ├── image-model.mdx                 # 图片生成、请求选项、URL 与 Base64 输出
│       │   ├── audio-model.mdx                 # 语音转写、语音合成、音频流与元数据
│       │   └── moderation-model.mdx            # 风险标记、分类、评分与业务判断边界
│       ├── rag/
│       │   ├── document-ingestion.mdx          # 文档读取、切分、来源元数据、重复导入处理
│       │   ├── embeddings-and-vector-store.mdx # Embedding 模型、向量维度、存储与检索
│       │   └── retrieval-and-generation.mdx    # RAG 串联、过滤、参数比较、引用与拒答
│       ├── tools/
│       │   ├── tool-calling.mdx                # @Tool、参数描述、执行与结果回传、异常处理
│       │   ├── tool-calling-advisor.mdx        # 执行循环、顺序、钩子扩展与流式观察
│       │   ├── tool-search-tool.mdx            # 渐进式工具暴露、索引策略与会话隔离
│       │   └── chatmodel-tool-calling.mdx      # 底层请求、默认工具覆盖与手动循环
│       ├── mcp/
│       │   ├── overview.mdx                   # 协议能力、SDK 架构、传输与版本迁移
│       │   ├── client.mdx                     # 连接配置、共享会话、工具回调与客户端注解
│       │   └── server.mdx                     # 服务端传输、能力注册、注解与安全边界
│       └── engineering/
│           ├── workflows.mdx                   # 意图识别、路由、文档问答与业务工具组合
│           ├── evaluation.mdx                  # 题集设计、判断标准、质量与回归评估方法
│           └── observability-and-resilience.mdx # 耗时、Token、超时、重试与故障定位
└── projects/
    └── spring-ai-assistant/
        ├── index.mdx                          # 项目目标、架构、运行方式、阶段实现与演示
        └── experiments-and-evaluation.mdx      # 实验条件、参数对比、实际结果与失败复盘
```

#### 与四周计划对应

下表中的相对路径以 `src/content/docs/frameworks/spring-ai/` 为起点；项目记录单独标明完整目录。

| 阶段    | 本周笔记                                                                       | 项目记录                                                                                          |
| ------- | ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------- |
| 第 1 周 | `index.mdx`、`concepts.mdx`、`getting-started/quickstart.mdx`、`core/` 下 7 篇、`models/index.mdx` 与 `models/chat-model.mdx` | 在 `src/content/docs/projects/spring-ai-assistant/index.mdx` 记录运行方式、聊天接口和会话隔离验证 |
| 第 2 周 | `tools/tool-calling.mdx`、`tools/tool-calling-advisor.mdx`、`mcp/` 下 3 篇；工具搜索与底层 ChatModel 两篇按需阅读 | 补充订单工具和 MCP 接入过程，记录查无结果、参数缺失和超时案例                                     |
| 第 3 周 | `models/embedding-model.mdx`、`rag/` 下 3 篇                                                                 | 在项目记录中补充文档入库与问答链路；在 `experiments-and-evaluation.mdx` 记录切分、Top-K、阈值对比 |
| 第 4 周 | `engineering/` 下 3 篇                                                         | 完善完整架构、演示步骤、约 30 条题集及实际评估结果                                                |

项目总览和实验记录从第一周开始持续更新，第 4 周汇总。工具调用增加三个进阶页面，MCP 接入由单篇扩展为概览、客户端和服务端三篇，规划由 29 篇调整为 31 篇。译文完成不代表实践验收已完成，进度勾选仍以实际调用和验证为准。每周的笔记是实践结论的整理，不要求每篇等长；未验证的判断应明确标注“待验证”。

#### 页面内容约定

每篇主题笔记围绕一个工程问题展开，使用中文标题和说明、英文小写连字符文件名。优先写清以下内容：

1. **概念与适用场景**：解决什么问题，何时使用，有哪些边界。
2. **核心 API 与调用链**：关键类的职责，输入如何转换、结果如何返回。
3. **最小可运行示例**：标明 JDK、Spring Boot、Spring AI 版本和模型，提供必要配置与执行步骤。
4. **验证与工程判断**：记录预期、实际结果、异常案例和选型依据；实践代码链接到独立学习项目中的真实路径。
5. **官方来源**：链接到所用版本的具体章节，标注核验日期。

`index.mdx` 负责总览和阅读入口；项目笔记负责具体架构、配置、实验和结果。主题笔记解释通用方法，项目笔记引用这些方法并记录实际应用，避免重复维护同一段内容。

已有的模型、提示词、Embedding、RAG 和 MCP 通用原理，优先引用 `basics/`、`rag/` 和 `frameworks/mcp/` 中的对应笔记；Spring AI 专题聚焦 Java API、Spring 集成和实践中的差异。

实验记录至少包含：问题编号、输入与预期、版本与模型、提示词或参数变化、实际结果、来源或工具调用证据、耗时、Token 用量、结论。无法获得的指标标记为“未采集”。

#### 站点导航规划

- 在“开发框架”中增加“Spring AI”，按“总览 → 入门 → 核心 API → 工具调用 → MCP → RAG → 工程实践”排列；分组使用中文名称，组内页面按学习顺序排列。
- 在“实战项目”中展示“Spring AI 文档与订单助手”，由现有 `projects` 自动导航收录；框架总览与项目总览互相链接。
- 页面 frontmatter 使用 `title`、`description` 和 `sidebar`，与现有 MDX 笔记保持一致；在自动生成的分组中使用 `sidebar.order` 控制顺序。
- 页面路径跟随文件路径，例如 `frameworks/spring-ai/core/chat-client.mdx` 对应 `/frameworks/spring-ai/core/chat-client/`，无需另设 `slug`。
- 总览、AI 核心概念、快速入门、ChatClient API、提示词、响应元数据、结构化输出、Advisors API、多模态、模型小节与对话记忆已接入 `astro.config.mjs` 的“开发框架 → Spring AI”；后续页面有实质内容后再创建并加入导航。

Advisors API 与 ChatClient API 在 Spring AI 导航中同级。基础处理链与递归 Advisor 合并为一篇，先读基础，再结合 Chat Memory 与工具调用深入循环机制。对话记忆与 Advisor 机制分篇整理，不再合并为 `memory-and-advisors.mdx`。

模型小节整理概览及聊天、Embedding、图像、音频和审核的核心用法；提供方接入配置、完整参数与专有能力按需查询官网。图像、音频与审核作为选学内容，不增加主线四周计划的必做任务。多模态先用图片输入建立直观认识，Embedding 的实践放到第二周 RAG 阶段。

对话记忆放在模型小节之后，与 ChatClient API、Advisors API 同级。主线先理解会话 ID、消息窗口与 ChatClient 接入；数据库配置按需阅读。窗口记忆不替代完整聊天历史，工具消息是否保存还取决于 Advisor 位置和 Repository 能力。

工具调用小节接在对话记忆之后，已完成[基础](src/content/docs/frameworks/spring-ai/tools/tool-calling.mdx)、[Advisor](src/content/docs/frameworks/spring-ai/tools/tool-calling-advisor.mdx)、[工具搜索](src/content/docs/frameworks/spring-ai/tools/tool-search-tool.mdx)与 [ChatModel 底层调用](src/content/docs/frameworks/spring-ai/tools/chatmodel-tool-calling.mdx)四篇。按当前学习安排先完成工具调用与 MCP，再进入 RAG；后两篇进阶内容不增加第二周的必做任务。

MCP 小节已完成[概览](src/content/docs/frameworks/spring-ai/mcp/overview.mdx)、[客户端](src/content/docs/frameworks/spring-ai/mcp/client.mdx)和[服务端](src/content/docs/frameworks/spring-ai/mcp/server.mdx)。先理解协议和传输，再连接已有工具，最后发布自己的工具；完整注解、认证集成和各传输高级配置保留来源入口，按需深入。
