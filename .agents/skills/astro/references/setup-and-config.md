# 安装与配置

## 前置要求

- Node.js 18.17.1 或 20.3.0 及以上（不支持 v19）
- npm、pnpm 或 Yarn

## 快速开始

```bash
# 创建新项目
npm create astro@latest

# 使用模板
npm create astro@latest -- --template blog
npm create astro@latest -- --template starlight

# 启动开发服务器（默认 http://localhost:4321）
npm run dev

# 构建生产版本
npm run build

# 预览构建结果
npm run preview
```

---

## 项目结构

```
my-project/
├── public/                  # 静态资源（不经过构建处理）
│   └── favicon.svg
├── src/
│   ├── assets/             # 需要优化的资源（图片等）
│   ├── components/         # 组件（.astro, .jsx, .vue 等）
│   ├── content/            # Content Collections 内容
│   │   └── docs/
│   ├── layouts/            # 布局组件
│   ├── pages/              # 页面路由（文件即路由）
│   │   ├── index.astro     # → /
│   │   ├── about.astro     # → /about/
│   │   └── blog/
│   │       └── [slug].astro # → /blog/:slug/
│   ├── middleware.ts       # 请求中间件
│   ├── actions/            # 服务端 Actions
│   │   └── index.ts
│   └── content.config.ts   # 内容集合配置
├── astro.config.mjs        # Astro 配置
├── package.json
└── tsconfig.json
```

---

## 基础配置

```javascript
// astro.config.mjs
import { defineConfig } from 'astro/config';

export default defineConfig({
  // 站点 URL（用于 sitemap、canonical 等）
  site: 'https://example.com',

  // URL 路径前缀（部署到子路径时）
  base: '/docs',

  // 尾部斜杠处理: 'always' | 'never' | 'ignore'
  trailingSlash: 'always',

  // HTML 压缩
  compressHTML: true,

  // 集成
  integrations: [],

  // Vite 配置透传
  vite: {},

  // 图片服务
  image: {
    service: { entrypoint: 'astro/assets/services/sharp' },
  },
});
```

---

## 环境变量

```javascript
// astro.config.mjs
import { defineConfig, envField } from 'astro/config';

export default defineConfig({
  env: {
    schema: {
      // 公开变量（客户端可用）
      PUBLIC_API_URL: envField.string({
        context: 'client',
        access: 'public',
        default: 'https://api.example.com',
      }),
      // 私有变量（仅服务端）
      API_SECRET: envField.string({
        context: 'server',
        access: 'secret',
      }),
    },
  },
});
```

```typescript
// 使用环境变量
import { PUBLIC_API_URL } from 'astro:env/client';
import { API_SECRET, getSecret } from 'astro:env/server';

// 或通过 import.meta.env
const mode = import.meta.env.MODE; // 'development' | 'production'
const isProd = import.meta.env.PROD;
const isDev = import.meta.env.DEV;
const baseUrl = import.meta.env.BASE_URL;
const site = import.meta.env.SITE;

// 公开变量需要 PUBLIC_ 前缀
const publicVar = import.meta.env.PUBLIC_MY_VAR;
```
