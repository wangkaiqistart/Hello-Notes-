---
name: starlight
version: "1.0.0"
description: Starlight - Astro 官方文档主题，构建快速可定制的文档网站。Use when 用户需要配置 Starlight 站点、设置侧边栏导航、使用内置组件（Card/Tabs/Steps/FileTree/Aside/LinkButton）、编写文档内容、自定义样式/主题、覆盖组件、管理 frontmatter、创建自定义页面，或遇到 @astrojs/starlight 相关问题时。
---

# Starlight Skill

## Goal

为用户提供 Starlight（Astro 官方文档主题）的知识路由，快速定位到正确的配置、组件、样式或内容编写参考。

## Workflow

1. 识别用户需求类别（配置/组件/样式/内容/页面）
2. 根据决策树路由到对应 reference 文件
3. 从 reference 中提取并呈现相关信息
4. 如 reference 中信息不足，使用 MCP astro-docs 工具搜索补充

## Decision Tree

```
用户需求
├── 项目搭建/初始配置
│   └── → references/getting-started.md
├── 侧边栏/导航配置
│   ├── autogenerate → references/sidebar.md #自动生成
│   ├── 手动配置/分组/折叠/徽章 → references/sidebar.md
│   └── frontmatter sidebar 属性 → references/sidebar.md #frontmatter
├── 使用内置组件
│   ├── Card/CardGrid/LinkCard → references/components.md #卡片
│   ├── Tabs/TabItem → references/components.md #标签页
│   ├── Steps → references/components.md #步骤
│   ├── FileTree → references/components.md #文件树
│   ├── Badge/Icon → references/components.md #徽章图标
│   ├── Aside（提示框） → references/components.md #旁白
│   ├── LinkButton → references/components.md #链接按钮
│   └── 代码块增强（高亮/标题/diff） → references/components.md #代码
├── 编写文档内容
│   ├── Markdown/MDX 基础 → references/authoring.md
│   ├── Frontmatter 属性 → references/frontmatter.md
│   └── 代码块/Expressive Code → references/authoring.md #代码块
├── 样式/主题定制
│   ├── CSS 变量/颜色 → references/styling.md
│   ├── Tailwind 集成 → references/styling.md #tailwind
│   ├── 自定义字体 → references/styling.md #字体
│   └── 全局 CSS → references/styling.md #全局
├── 覆盖/扩展组件
│   └── → references/overrides.md
├── 自定义页面
│   └── → references/pages.md
└── 站点配置（logo/搜索/社交链接/sitemap）
    └── → references/configuration.md
```

---

## Constraints

- 始终使用 `@astrojs/starlight` 包的最新 API
- 组件导入路径：`@astrojs/starlight/components`
- 文档内容放在 `src/content/docs/` 目录
- 配置在 `astro.config.mjs` 的 `starlight()` 集成中
- 使用 MCP astro-docs 工具搜索最新文档以补充 references 中的信息
- 不适用：Astro 通用功能（路由/Islands/SSR）→ astro skill；非文档站点开发

## Validation

- 生成的配置能通过 `npm run build` 构建
- 组件导入路径正确，Props 类型匹配
- frontmatter 字段名和值类型符合 Starlight schema

## Resources

```bash
npm create astro@latest -- --template starlight  # 创建项目
npm run dev                                       # 开发
npm run build                                     # 构建
```

## 参考文档

| 文件 | 内容 |
|------|------|
| [sidebar.md](references/sidebar.md) | 侧边栏导航完整配置 |
| [components.md](references/components.md) | 内置组件用法与 Props |
| [authoring.md](references/authoring.md) | 内容编写、Markdown 增强、代码块 |
| [configuration.md](references/configuration.md) | 站点配置（logo/搜索/社交等） |
| [frontmatter.md](references/frontmatter.md) | 页面 frontmatter 属性参考 |
| [styling.md](references/styling.md) | CSS/Tailwind/自定义样式 |
| [overrides.md](references/overrides.md) | 覆盖内置组件 |
| [pages.md](references/pages.md) | 自定义页面和 StarlightPage 组件 |
