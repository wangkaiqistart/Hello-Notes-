# 组件与路由

## Astro 组件结构

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

---

## Props 与 Slots

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

## 静态路由

```
src/pages/index.astro        → /
src/pages/about.astro        → /about/
src/pages/blog/index.astro   → /blog/
src/pages/blog/post-1.md     → /blog/post-1/
```

## 动态路由

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

## Rest 参数路由

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

## 分页

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
