# 样式与图片优化

## Scoped 样式（默认）

```astro
<h1>标题</h1>

<style>
  /* 自动 scoped，仅作用于当前组件 */
  h1 { color: red; }
</style>
```

## 全局样式

```astro
<style is:global>
  /* 全局生效 */
  body { margin: 0; }
</style>
```

## CSS 变量注入

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

---

## CSS 预处理器

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

---

## Tailwind CSS

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

## Image 组件

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

## Picture 组件（响应式）

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

## 在 Content Collections 中使用图片

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
