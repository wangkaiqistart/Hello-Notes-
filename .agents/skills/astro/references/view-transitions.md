# View Transitions（视图过渡）

## 启用 SPA 模式过渡

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

---

## 过渡指令

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

---

## 导航控制

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

---

## 生命周期事件

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
