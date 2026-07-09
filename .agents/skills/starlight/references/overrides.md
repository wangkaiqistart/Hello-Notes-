# 覆盖内置组件

Starlight 允许你替换默认 UI 组件来自定义外观和行为。

## 配置覆盖

在 `astro.config.mjs` 中使用 `components` 选项：

```javascript
starlight({
  components: {
    // 用自定义组件替换默认 Header
    Header: './src/components/CustomHeader.astro',
    // 覆盖社交图标
    SocialIcons: './src/components/MySocialIcons.astro',
  },
})
```

## 可覆盖的组件列表

主要可覆盖组件：

- `Header` — 页面头部
- `Footer` — 页面底部
- `Sidebar` — 侧边栏
- `PageFrame` — 页面框架
- `TwoColumnContent` — 两栏内容布局
- `PageTitle` — 页面标题
- `ContentPanel` — 主内容面板
- `TableOfContents` — 目录
- `Pagination` — 上/下页导航
- `SocialIcons` — 社交图标
- `Search` — 搜索
- `SiteTitle` — 站点标题
- `Head` — HTML head
- `Hero` — Hero 区域
- `Banner` — 横幅通知
- `DraftContentNotice` — 草稿通知

## 复用内置组件

在自定义组件中导入并渲染原始组件，实现"包裹"效果：

```astro
---
// src/components/CustomSocialIcons.astro
import Default from '@astrojs/starlight/components/SocialIcons.astro';
---

<a href="mailto:hello@example.com">Email</a>
<Default><slot /></Default>
```

## 命名 Slot 传递

某些组件包含命名 slot，需要手动传递：

```astro
---
// src/components/CustomContent.astro
import Default from '@astrojs/starlight/components/TwoColumnContent.astro';
---

<Default>
  <slot />
  <slot name="right-sidebar" slot="right-sidebar" />
</Default>
```

## 覆盖 Head 以引入本地资源

```astro
---
// src/components/CustomHead.astro
import Default from '@astrojs/starlight/components/Head.astro';
---

<Default><slot /></Default>
<link rel="stylesheet" href="/custom-local.css" />
<script src="/custom-local.js"></script>
```
