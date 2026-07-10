# 快速开始

## 创建新项目

```bash
# npm
npm create astro@latest -- --template starlight

# pnpm
pnpm create astro --template starlight

# yarn
yarn create astro --template starlight
```

## 启动开发服务器

```bash
npm run dev    # 默认 http://localhost:4321
```

## 添加内容

在 `src/content/docs/` 目录创建 `.md` 或 `.mdx` 文件即可自动生成页面。

## 项目结构

```
my-docs/
├── public/              # 静态资源
├── src/
│   ├── assets/          # 优化的图片/logo
│   ├── content/
│   │   └── docs/        # 文档内容（文件即路由）
│   │       └── index.md # → /
│   ├── content.config.ts # 内容集合配置
│   └── styles/          # 自定义 CSS（可选）
├── astro.config.mjs     # Astro + Starlight 配置
└── package.json
```

## 更新 Starlight

```bash
npx @astrojs/upgrade
```

## 下一步

- 自定义站点 → `references/configuration.md`
- 设置侧边栏 → `references/sidebar.md`
- 使用组件 → `references/components.md`
- 部署 → `npm run build` 后部署 `dist/` 目录
