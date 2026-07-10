# Islands 架构与框架集成

Astro 默认输出纯静态 HTML，交互组件需要通过 `client:*` 指令显式激活水合。

## 客户端指令

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

---

## 框架集成

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
