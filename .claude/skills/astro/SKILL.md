---
name: astro
version: '2.1.0'
description: Astro - 高性能内容驱动 Web 框架，Islands 架构实现零 JS 静态输出和按需交互。Use when 用户需要创建或维护 Astro 项目、页面、组件、路由、Content Collections、SSR/Actions、中间件、部署、框架集成、图片与样式，或排查 Astro 构建/配置问题。
---

# Astro Skill

## Goal

为用户提供 Astro 框架的知识路由，快速定位到正确的配置、架构模式或 API 参考。先以当前仓库的 `package.json`、锁文件和 `AGENTS.md` 为事实源，再用官方文档补充。

## Workflow

0. 读取仓库约束，并从 `package.json` 与锁文件确认 Astro、集成和包管理器版本
1. 识别用户需求类别（项目配置/组件/内容/SSR/部署/样式）
2. 根据决策树路由到对应 reference 文件；跨领域问题先拆成多个类别
3. 从 reference 中提取信息，标注与当前仓库版本相关的前提
4. 如 reference 信息不足或版本可能漂移，使用 MCP `astro-docs` 搜索官方文档补充
5. 涉及代码或配置修改时，运行仓库已有的检查命令，并说明未验证的运行时条件

## Decision Tree

```
用户需求
├── 项目创建/配置/环境变量/项目结构/重定向/输出模式
│   └── → references/setup-and-config.md
├── 组件/Props/Slots/路由/动态路由/分页
│   └── → references/components-and-routing.md
├── Islands 架构/client: 指令/框架集成（React/Vue/Svelte）
│   └── → references/islands-and-frameworks.md
├── Content Collections/内容管理/数据查询/Live Collections
│   └── → references/content-collections.md
├── View Transitions/页面过渡/导航生命周期
│   └── → references/view-transitions.md
├── SSR/适配器/Actions/中间件/API 端点
│   └── → references/ssr-and-actions.md
├── 样式/CSS/Tailwind/图片优化
│   └── → references/styling-and-images.md
├── 部署/适配器/静态或按需输出（Vercel/Netlify/Cloudflare/GitHub Pages）
│   └── → references/deployment.md
└── Starlight 文档主题
    └── → 转交 starlight skill
```

## Constraints

- Starlight 文档主题功能 → 转交 starlight skill
- 纯客户端 SPA → 推荐原生框架而非 Astro
- 不把固定版本写成永久事实：优先遵循仓库实际依赖；无仓库上下文时以官方文档当前 API 为准
- 当前仓库使用的 Astro 7 Content Layer、Live Collections、Actions、Transitions 等 API 需要按官方文档核对，不能用 Astro 5/6 的旧示例替代
- 使用 MCP `astro-docs` 工具获取最新文档；搜索结果不能替代本地构建验证
- 不假设适配器、第三方 loader 或运行时服务已经安装；先检查依赖，再给出安装或配置步骤

## Validation

- 生成的配置能通过仓库对应的 `npm run check`/`npm run build`（或项目实际包管理器脚本）
- 路由和页面遵循文件系统路由规则
- client: 指令仅用于需要交互的 Islands 组件
- 静态站点要检查 `dist/` 输出；SSR/Actions/Live Collections 要同时确认适配器和按需渲染条件

## Resources

```bash
astro dev               # 开发服务器
astro build             # 构建
astro check             # 类型检查
astro add <integration> # 添加集成
astro sync              # 同步 content collections 类型
```

| 文件                                                              | 内容                                 |
| ----------------------------------------------------------------- | ------------------------------------ |
| [setup-and-config.md](references/setup-and-config.md)             | 安装、项目结构、配置、环境变量与输出 |
| [components-and-routing.md](references/components-and-routing.md) | 组件、Props/Slots、路由、分页        |
| [islands-and-frameworks.md](references/islands-and-frameworks.md) | Islands 架构、client: 指令、框架集成 |
| [content-collections.md](references/content-collections.md)       | Content Collections 定义与查询       |
| [view-transitions.md](references/view-transitions.md)             | View Transitions、过渡指令           |
| [ssr-and-actions.md](references/ssr-and-actions.md)               | SSR、适配器、Actions、中间件         |
| [styling-and-images.md](references/styling-and-images.md)         | 样式、CSS、Tailwind、图片优化        |
| [deployment.md](references/deployment.md)                         | 部署方案与适配器选择                 |

## 故障排查

| 问题                    | 方案                                                                                      |
| ----------------------- | ----------------------------------------------------------------------------------------- |
| Content collection 错误 | 先运行 `npx astro sync`，再检查 `src/content.config.*`、loader 与 schema                  |
| TypeScript 类型不识别   | `npx astro sync` 后重启开发服务器或编辑器类型服务                                         |
| 图片优化失败            | 检查 `astro:assets` 输入、远程图片配置与 Sharp/运行时 image service；不要盲目重复安装依赖 |
| 构建与开发行为不一致    | 核对 `output`、`prerender`、适配器以及 Astro 实际版本                                     |
