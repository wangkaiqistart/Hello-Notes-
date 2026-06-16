# SSR、Actions 与中间件

## 启用按需渲染

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
