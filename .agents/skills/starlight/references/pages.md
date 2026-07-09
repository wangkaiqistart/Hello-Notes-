# 自定义页面

## Markdown/MDX 文档页面

在 `src/content/docs/` 中创建的文件自动成为文档页面，享有侧边栏、目录等完整功能。

## 非文档页面（Astro 页面）

在 `src/pages/` 中创建 `.astro` 文件可添加不在 docs 集合中的自定义路由。

## StarlightPage 组件

用 `<StarlightPage>` 在自定义页面中保持 Starlight 布局和样式：

```astro
---
// src/pages/custom.astro
import StarlightPage from '@astrojs/starlight/components/StarlightPage.astro';
---

<StarlightPage frontmatter={{ title: '我的自定义页面' }}>
  <p>这是一个自定义页面，但使用 Starlight 布局。</p>
</StarlightPage>
```

### Props

#### frontmatter（必填）

```javascript
frontmatter: {
  title: '页面标题',       // 必填
  description: '描述',
  template: 'doc',         // 'doc' | 'splash'
  editUrl: 'https://...',  // 编辑链接 URL
  draft: false,
}
```

#### sidebar（自定义侧边栏）

```astro
<StarlightPage
  frontmatter={{ title: 'Orion' }}
  sidebar={[
    { label: 'Home', link: '/' },
    {
      label: '星座',
      items: [
        { label: '仙女座', link: '/andromeda/' },
        { label: '猎户座', link: '/orion/' },
      ],
    },
  ]}
>
  内容
</StarlightPage>
```

#### hasSidebar

```javascript
hasSidebar: boolean  // 控制是否显示侧边栏，splash 模板默认 false
```

#### headings

```javascript
headings: [
  { depth: 2, slug: 'section-1', text: '第一节' },
  { depth: 3, slug: 'sub-section', text: '子节' },
]
// 手动提供标题列表以生成目录
```

#### dir

```javascript
dir: 'ltr' | 'rtl'  // 文字方向
```
