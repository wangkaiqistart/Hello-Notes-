# Content Collections（内容集合）

## 定义集合

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

---

## 查询集合

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

---

## Live Collections（实时集合）

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
