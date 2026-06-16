---
name: astro
version: "1.0.0"
description: Astro - 高性能 Web 框架，基于内容驱动和 Islands 架构，用于构建快速的静态网站和按需渲染的动态应用。当需要创建 Astro 项目、页面、组件、路由、SSR 配置、部署、框架集成、图片优化、样式处理时使用。
---

# Astro Skill

**Astro** 是一个以内容为中心的 Web 框架，采用 Islands 架构实现按需加载 JavaScript。默认输出零 JS 的静态 HTML，仅在需要交互的组件上加载框架代码。

**核心价值**: 用任何 UI 框架（React、Vue、Svelte、Solid 等）编写组件，输出极致快速的静态站点，同时支持按需服务端渲染。

## 适用场景

- 创建 Astro 项目、页面、布局、组件
- 配置文件路由和动态路由
- 使用 Content Collections 管理内容
- 集成 React/Vue/Svelte 等前端框架
- 配置 SSR 和部署适配器
- 实现 View Transitions 页面过渡
- 使用 Actions 处理表单和服务端函数
- 配置中间件、环境变量、图片优化
- 部署到 Vercel/Netlify/Cloudflare/GitHub Pages

## 不适用场景

- Starlight 文档主题的特有功能（使用 starlight skill）
- 纯客户端 SPA 应用（使用 React/Vue/Svelte 框架）
- 非 Web 开发任务

---

## 架构概览

```
┌─────────────────────────────────────────────────────────────────┐
│                        Astro 应用                               │
└─────────────────────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────────────────┐
│                       内容层                                    │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌───────────────┐  │
│  │ Markdown │  │   MDX    │  │ Markdoc  │  │  JSON/YAML    │  │
│  │  (.md)   │  │  (.mdx)  │  │ (.mdoc)  │  │  数据文件      │  │
│  └──────────┘  └──────────┘  └──────────┘  └───────────────┘  │
└───────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌───────────────────────────────────────────────────────────────┐
│                     Islands 架构                               │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌───────────────┐  │
│  │  Static  │  │  React   │  │   Vue    │  │   Svelte      │  │
│  │  HTML    │  │  Island  │  │  Island  │  │   Island      │  │
│  └──────────┘  └──────────┘  └──────────┘  └───────────────┘  │
└───────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌───────────────────────────────────────────────────────────────┐
│                      构建输出                                   │
│  静态 HTML + 按需 JS + 优化资源 + Sitemap + RSS               │
└───────────────────────────────────────────────────────────────┘
```

---

## 安装与项目创建

### 前置要求

- Node.js 18.17.1 或 20.3.0 及以上（不支持 v19）
- npm、pnpm 或 Yarn

### 快速开始

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

## 配置

### 基础配置

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

### 环境变量

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

---

## 组件

### Astro 组件结构

```astro
---
// frontmatter（服务端代码，构建时执行）
import Layout from '../layouts/Layout.astro';
import Card from '../components/Card.astro';

interface Props {
  title: string;
  description?: string;
}

const { title, description = '默认描述' } = Astro.props;
const data = await fetch('https://api.example.com/data').then(r => r.json());
---

<!-- 模板部分（HTML + 表达式） -->
<Layout title={title}>
  <h1>{title}</h1>
  <p>{description}</p>

  {data.map(item => (
    <Card title={item.name} href={item.url} />
  ))}

  <!-- 条件渲染 -->
  {isProd && <Analytics />}

  <!-- 插槽 -->
  <slot />
  <slot name="sidebar" />
</Layout>

<style>
  /* 默认 scoped 样式，仅作用于当前组件 */
  h1 {
    color: purple;
  }
</style>

<script>
  // 客户端 JavaScript，会被打包优化
  console.log('Hello from the client');
</script>
```

### Props 与 Slots

```astro
---
// src/components/Card.astro
interface Props {
  title: string;
  href?: string;
}
const { title, href = '#' } = Astro.props;
---

<div class="card">
  <h2><a href={href}>{title}</a></h2>
  <!-- 默认插槽 -->
  <slot />
  <!-- 具名插槽 -->
  <slot name="footer" />
  <!-- 回退内容 -->
  <slot name="optional">
    <p>默认内容</p>
  </slot>
</div>
```

使用组件：

```astro
<Card title="Hello">
  <p>正文内容放在默认插槽</p>
  <footer slot="footer">底部内容</footer>
</Card>
```

---

## 路由

### 静态路由

```
src/pages/index.astro        → /
src/pages/about.astro        → /about/
src/pages/blog/index.astro   → /blog/
src/pages/blog/post-1.md     → /blog/post-1/
```

### 动态路由

```astro
---
// src/pages/blog/[slug].astro
import { getCollection } from 'astro:content';

export async function getStaticPaths() {
  const posts = await getCollection('blog');
  return posts.map(post => ({
    params: { slug: post.id },
    props: { post },
  }));
}

const { post } = Astro.props;
---
<h1>{post.data.title}</h1>
```

### Rest 参数路由

```astro
---
// src/pages/[...slug].astro — 匹配所有路径
export function getStaticPaths() {
  return [
    { params: { slug: undefined } },      // → /
    { params: { slug: 'about' } },        // → /about/
    { params: { slug: 'blog/post-1' } },  // → /blog/post-1/
  ];
}
---
```

### 分页

```astro
---
// src/pages/blog/[page].astro
export async function getStaticPaths({ paginate }) {
  const posts = await getCollection('blog');
  return paginate(posts, { pageSize: 10 });
}

const { page } = Astro.props;
// page.data — 当前页数据
// page.url.prev / page.url.next — 上下页 URL
// page.currentPage / page.lastPage — 页码信息
---
```

---

## Islands 架构与客户端指令

Astro 默认输出纯静态 HTML，交互组件需要通过 `client:*` 指令显式激活水合。

### 客户端指令

```astro
---
import ReactCounter from './Counter.jsx';
import VueWidget from './Widget.vue';
---

<!-- 页面加载时立即水合（高优先级） -->
<ReactCounter client:load />

<!-- 浏览器空闲时水合（中优先级） -->
<VueWidget client:idle />

<!-- 进入视口时水合（低优先级） -->
<ReactCounter client:visible />

<!-- 媒体查询匹配时水合 -->
<VueWidget client:media="(max-width: 768px)" />

<!-- 仅客户端渲染，跳过 SSR -->
<ReactCounter client:only="react" />
```

### 框架集成

```bash
# 添加框架支持
npx astro add react
npx astro add vue
npx astro add svelte
npx astro add solid-js
npx astro add preact
```

```javascript
// astro.config.mjs
import { defineConfig } from 'astro/config';
import react from '@astrojs/react';
import vue from '@astrojs/vue';

export default defineConfig({
  integrations: [react(), vue()],
});
```

---

## Content Collections（内容集合）

### 定义集合

```typescript
// src/content.config.ts
import { defineCollection } from 'astro:content';
import { glob, file } from 'astro/loaders';
import { z } from 'astro/zod';

const blog = defineCollection({
  loader: glob({ base: './src/content/blog', pattern: '**/*.{md,mdx}' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    pubDate: z.coerce.date(),
    updatedDate: z.coerce.date().optional(),
    tags: z.array(z.string()).default([]),
    draft: z.boolean().default(false),
  }),
});

const authors = defineCollection({
  loader: file('./src/data/authors.json'),
  schema: z.object({
    name: z.string(),
    avatar: z.string().url(),
  }),
});

export const collections = { blog, authors };
```

### 查询集合

```astro
---
import { getCollection, getEntry, render } from 'astro:content';

// 获取全部条目
const allPosts = await getCollection('blog');

// 过滤条目
const publishedPosts = await getCollection('blog', ({ data }) => {
  return data.draft !== true;
});

// 获取单个条目
const post = await getEntry('blog', 'my-post-id');

// 渲染 Markdown 内容
const { Content, headings } = await render(post);
---

<Content />
```

### Live Collections（实时集合）

```typescript
// src/live.config.ts
import { defineLiveCollection } from 'astro:content';

const products = defineLiveCollection({
  loader: storeLoader({ endpoint: process.env.API_URL }),
  schema: z.object({
    id: z.string(),
    name: z.string(),
    price: z.number(),
  }),
});

export const collections = { products };
```

```astro
---
// 使用实时集合（请求时获取数据）
import { getLiveCollection, getLiveEntry } from 'astro:content';
export const prerender = false;

const { entries } = await getLiveCollection('products');
const { entry } = await getLiveEntry('products', '123');
---
```

---

## View Transitions（视图过渡）

### 启用 SPA 模式过渡

```astro
---
// src/layouts/Layout.astro
import { ClientRouter } from 'astro:transitions';
---

<html>
  <head>
    <ClientRouter />
  </head>
  <body>
    <slot />
  </body>
</html>
```

### 过渡指令

```astro
<!-- 命名过渡对（匹配两个页面间的同名元素） -->
<h1 transition:name="title">{title}</h1>

<!-- 动画类型：fade | slide | none -->
<div transition:animate="slide">内容</div>

<!-- 自定义动画时长 -->
<div transition:animate={fade({ duration: '0.4s' })}>内容</div>

<!-- 跨页面保持元素状态（如视频播放器） -->
<video transition:persist src="..."></video>
```

### 导航控制

```html
<!-- 强制全页面刷新 -->
<a href="/page" data-astro-reload>链接</a>

<!-- 替换历史记录（不新增） -->
<a href="/page" data-astro-history="replace">链接</a>
```

```typescript
// 编程式导航
import { navigate } from 'astro:transitions/client';
navigate('/new-page');
```

### 生命周期事件

```html
<script>
  document.addEventListener('astro:page-load', () => {
    // 每次页面加载/导航后触发
  });

  document.addEventListener('astro:after-swap', () => {
    // DOM 替换后、页面渲染前触发
  });
</script>
```

---

## SSR 与适配器

### 启用按需渲染

```javascript
// astro.config.mjs
import { defineConfig } from 'astro/config';
import vercel from '@astrojs/vercel';

export default defineConfig({
  adapter: vercel(),
  // output: 'server', // 全部页面按需渲染
});
```

```astro
---
// 单个页面启用按需渲染
export const prerender = false;

// 获取请求信息
const cookie = Astro.cookies.get('session');
const ip = Astro.request.headers.get('x-forwarded-for');
---
```

### 官方适配器

```bash
npx astro add vercel      # Vercel
npx astro add netlify     # Netlify
npx astro add cloudflare  # Cloudflare Pages
npx astro add node        # Node.js 自托管
```

---

## Actions（服务端函数）

### 定义 Action

```typescript
// src/actions/index.ts
import { defineAction } from 'astro:actions';
import { z } from 'astro/zod';

export const server = {
  // JSON 类型 Action
  subscribe: defineAction({
    accept: 'json', // 默认值
    input: z.object({
      email: z.string().email(),
      name: z.string().optional(),
    }),
    handler: async (input, context) => {
      // input 已通过 Zod 验证
      await db.insert({ email: input.email });
      return { success: true };
    },
  }),

  // 表单类型 Action
  comment: defineAction({
    accept: 'form',
    input: z.object({
      body: z.string().min(1),
      postId: z.string(),
    }),
    handler: async (input) => {
      const comment = await db.comments.create(input);
      return comment;
    },
  }),
};
```

### 调用 Action

```astro
---
// 服务端调用
import { actions } from 'astro:actions';
const result = await Astro.callAction(actions.subscribe, { email: 'a@b.com' });
---

<!-- 零 JS 表单提交 -->
<form method="POST" action={actions.comment}>
  <input name="postId" value="123" type="hidden" />
  <textarea name="body"></textarea>
  <button>提交评论</button>
</form>
```

```typescript
// 客户端调用
import { actions } from 'astro:actions';

const { data, error } = await actions.subscribe({ email: 'user@example.com' });
if (error) {
  console.error(error.message);
} else {
  console.log(data.success);
}
```

---

## 中间件

```typescript
// src/middleware.ts
import { defineMiddleware, sequence } from 'astro:middleware';

const auth = defineMiddleware(async (context, next) => {
  const token = context.cookies.get('token')?.value;
  if (token) {
    context.locals.user = await verifyToken(token);
  }
  return next();
});

const logging = defineMiddleware(async (context, next) => {
  console.log(`${context.request.method} ${context.url.pathname}`);
  const response = await next();
  console.log(`→ ${response.status}`);
  return response;
});

// 链式组合多个中间件
export const onRequest = sequence(logging, auth);
```

```typescript
// 在页面中访问 locals
---
const user = Astro.locals.user;
if (!user) return Astro.redirect('/login');
---
```

---

## 样式

### Scoped 样式（默认）

```astro
<h1>标题</h1>

<style>
  /* 自动 scoped，仅作用于当前组件 */
  h1 { color: red; }
</style>
```

### 全局样式

```astro
<style is:global>
  /* 全局生效 */
  body { margin: 0; }
</style>
```

### CSS 变量注入

```astro
---
const color = 'red';
const size = '16px';
---

<div class="box">内容</div>

<style define:vars={{ color, size }}>
  .box {
    color: var(--color);
    font-size: var(--size);
  }
</style>
```

### CSS 预处理器

```bash
# 安装预处理器
npm install sass
npm install less
npm install stylus
```

```astro
<style lang="scss">
  $primary: #4f46e5;
  .card {
    border: 1px solid $primary;
    &:hover { background: lighten($primary, 40%); }
  }
</style>
```

### Tailwind CSS

```bash
npx astro add tailwind
```

```javascript
// astro.config.mjs
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  vite: {
    plugins: [tailwindcss()],
  },
});
```

---

## 图片优化

### Image 组件

```astro
---
import { Image } from 'astro:assets';
import heroImage from '../assets/hero.png';
---

<!-- 本地图片（自动优化） -->
<Image src={heroImage} alt="Hero 图片描述" />

<!-- 指定尺寸和格式 -->
<Image src={heroImage} alt="..." width={800} height={600} format="webp" />

<!-- 远程图片 -->
<Image
  src="https://example.com/photo.jpg"
  alt="远程图片"
  width={400}
  height={300}
  inferSize
/>
```

### Picture 组件（响应式）

```astro
---
import { Picture } from 'astro:assets';
import img from '../assets/photo.jpg';
---

<Picture
  src={img}
  formats={['avif', 'webp']}
  alt="响应式图片"
  widths={[400, 800, 1200]}
  sizes="(max-width: 800px) 100vw, 800px"
/>
```

### 在 Content Collections 中使用图片

```typescript
// src/content.config.ts
const blog = defineCollection({
  schema: ({ image }) => z.object({
    title: z.string(),
    cover: image(), // 验证图片路径
    coverAlt: z.string(),
  }),
});
```

---

## 部署

### 静态站点（默认）

```bash
# 构建输出到 dist/ 目录
npm run build

# 可直接部署到任何静态托管
```

### Vercel

```bash
npx astro add vercel
```

```javascript
// astro.config.mjs
import vercel from '@astrojs/vercel';
export default defineConfig({ adapter: vercel() });
```

### Netlify

```bash
npx astro add netlify
```

```javascript
import netlify from '@astrojs/netlify';
export default defineConfig({ adapter: netlify() });
```

### Cloudflare Pages

```bash
npx astro add cloudflare
```

```javascript
import cloudflare from '@astrojs/cloudflare';
export default defineConfig({ adapter: cloudflare() });
```

部署命令：`npx astro build && npx wrangler deploy`

### GitHub Pages

```javascript
// astro.config.mjs
export default defineConfig({
  site: 'https://username.github.io',
  base: '/repo-name/',
});
```

```yaml
# .github/workflows/deploy.yml
name: Deploy to GitHub Pages
on:
  push:
    branches: [main]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 20 }
      - run: npm ci && npm run build
      - uses: actions/upload-pages-artifact@v3
        with: { path: ./dist }
  deploy:
    needs: build
    runs-on: ubuntu-latest
    permissions: { pages: write, id-token: write }
    environment: { name: github-pages }
    steps:
      - uses: actions/deploy-pages@v4
```

---

## API 端点

```typescript
// src/pages/api/users.ts
import type { APIRoute } from 'astro';

export const GET: APIRoute = async ({ params, request }) => {
  const users = await db.users.findAll();
  return new Response(JSON.stringify(users), {
    headers: { 'Content-Type': 'application/json' },
  });
};

export const POST: APIRoute = async ({ request }) => {
  const body = await request.json();
  const user = await db.users.create(body);
  return new Response(JSON.stringify(user), { status: 201 });
};

// 需要按需渲染
export const prerender = false;
```

---

## 常用 CLI 命令

```bash
astro dev              # 启动开发服务器
astro build            # 构建生产版本
astro preview          # 预览构建结果
astro check            # TypeScript 类型检查
astro add <integration> # 添加集成（react, vue, tailwind 等）
astro sync             # 同步 content collections 类型
```

---

## 故障排查

**构建失败（content collection 错误）：**
```bash
rm -rf .astro && npm run build
```

**样式不更新：**
```bash
npm run dev -- --force
```

**TypeScript 类型不识别：**
```bash
npx astro sync
```

**图片优化失败：**
```bash
# 确认安装了 sharp
npm install sharp
```

---

## 资源

### 官方文档
- [Astro 中文文档](https://docs.astro.build/zh-cn/)
- [Astro 英文文档](https://docs.astro.build/en/)
- [GitHub 仓库](https://github.com/withastro/astro)

### 生态
- [集成目录](https://astro.build/integrations/)
- [主题市场](https://astro.build/themes/)
- [Starlight 文档主题](https://starlight.astro.build/)

### 相关技术
- [Vite](https://vite.dev/) — 构建工具
- [Expressive Code](https://expressive-code.com/) — 代码高亮
- [Pagefind](https://pagefind.app/) — 静态搜索

---

## 版本历史

- **1.0.0** (2026-06-16): 初始版本
  - 覆盖 Astro 6.x 核心功能
  - 项目结构、配置、路由、组件
  - Islands 架构与客户端指令
  - Content Collections（构建时 + 实时）
  - View Transitions、SSR、Actions、中间件
  - 样式、图片优化、环境变量
  - 部署方案（Vercel/Netlify/Cloudflare/GitHub Pages）