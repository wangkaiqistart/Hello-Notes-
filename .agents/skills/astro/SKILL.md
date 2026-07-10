---
name: astro
version: "2.0.0"
description: Astro - 高性能内容驱动 Web 框架，Islands 架构实现零 JS 静态输出和按需交互。Use when 用户需要创建 Astro 项目、页面、组件、路由、Content Collections、SSR 配置、部署、框架集成（React/Vue/Svelte）、图片优化、View Transitions、Actions、中间件、样式处理，或遇到 Astro 构建/配置问题时。
---

# Astro Skill

## Goal

为用户提供 Astro 框架的知识路由，快速定位到正确的配置、架构模式或 API 参考。

## Workflow

1. 识别用户需求类别（项目配置/组件/内容/SSR/部署/样式）
2. 根据决策树路由到对应 reference 文件
3. 从 reference 中提取并呈现相关信息
4. 如 reference 信息不足，使用 MCP astro-docs 工具搜索补充

## Decision Tree

```
用户需求
├── 项目创建/配置/环境变量/项目结构
│   └── → references/setup-and-config.md
├── 组件/Props/Slots/路由/动态路由/分页
│   └── → references/components-and-routing.md
├── Islands 架构/client: 指令/框架集成（React/Vue/Svelte）
│   └── → references/islands-and-frameworks.md
├── Content Collections/内容管理/数据查询
│   └── → references/content-collections.md
├── View Transitions/页面过渡/导航生命周期
│   └── → references/view-transitions.md
├── SSR/适配器/Actions/中间件/API 端点
│   └── → references/ssr-and-actions.md
├── 样式/CSS/Tailwind/图片优化
│   └── → references/styling-and-images.md
├── 部署（Vercel/Netlify/Cloudflare/GitHub Pages）
│   └── → references/deployment.md
└── Starlight 文档主题
    └── → 转交 starlight skill
```

## Constraints

- Starlight 文档主题功能 → 转交 starlight skill
- 纯客户端 SPA → 推荐原生框架而非 Astro
- 始终基于 Astro 6.x API
- 使用 MCP astro-docs 工具获取最新文档

## Validation

- 生成的配置能通过 `astro check` 和 `astro build`
- 路由和页面遵循文件系统路由规则
- client: 指令仅用于需要交互的 Islands 组件

## Resources

```bash
astro dev               # 开发服务器
astro build             # 构建
astro check             # 类型检查
astro add <integration> # 添加集成
astro sync              # 同步 content collections 类型
```

| 文件 | 内容 |
|------|------|
| [setup-and-config.md](references/setup-and-config.md) | 安装、项目结构、配置、环境变量 |
| [components-and-routing.md](references/components-and-routing.md) | 组件、Props/Slots、路由、分页 |
| [islands-and-frameworks.md](references/islands-and-frameworks.md) | Islands 架构、client: 指令、框架集成 |
| [content-collections.md](references/content-collections.md) | Content Collections 定义与查询 |
| [view-transitions.md](references/view-transitions.md) | View Transitions、过渡指令 |
| [ssr-and-actions.md](references/ssr-and-actions.md) | SSR、适配器、Actions、中间件 |
| [styling-and-images.md](references/styling-and-images.md) | 样式、CSS、Tailwind、图片优化 |
| [deployment.md](references/deployment.md) | 部署方案 |

## 故障排查

| 问题 | 方案 |
|------|------|
| Content collection 错误 | `rm -rf .astro && npm run build` |
| TypeScript 类型不识别 | `npx astro sync` |
| 图片优化失败 | `npm install sharp` |
