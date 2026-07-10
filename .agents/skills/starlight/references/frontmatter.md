# Frontmatter 参考

每个文档页面可通过 frontmatter 设置元数据和行为。

## 必填字段

```yaml
---
title: 页面标题  # 必填，显示在页面顶部和浏览器标签
---
```

## 常用字段

```yaml
---
title: 页面标题
description: 页面描述（用于 SEO 和社交分享）
slug: custom-slug           # 自定义 URL slug
template: doc               # 'doc'（默认）| 'splash'（无侧边栏落地页）
editUrl: false              # 禁用编辑链接，或提供自定义 URL
draft: true                 # 标记为草稿，生产构建时排除
tableOfContents: false      # 禁用目录，或 { minHeadingLevel: 2, maxHeadingLevel: 3 }
---
```

## sidebar（侧边栏控制）

用于自动生成链接组中自定义页面的显示：

```yaml
---
title: 我的页面
sidebar:
  label: 自定义标签         # 覆盖标题
  order: 1                  # 排序（越小越靠前）
  hidden: true              # 从自动生成的侧边栏隐藏
  badge:
    text: 新
    variant: tip            # note | tip | caution | danger | success
  attrs:
    target: _blank          # HTML 属性
---
```

## hero（英雄区域）

配合 `template: splash` 使用，创建落地页：

```yaml
---
title: 我的项目
template: splash
hero:
  title: '欢迎使用我的项目'
  tagline: 快速、简单、强大。
  image:
    file: ~/assets/logo.png
    alt: 项目 Logo
  actions:
    - text: 开始使用
      link: /getting-started/
      icon: right-arrow
    - text: GitHub
      link: https://github.com/...
      icon: external
      variant: minimal
---
```

## banner（横幅通知）

```yaml
---
title: 页面标题
banner:
  content: |
    新版本发布！<a href="/changelog">查看更新日志</a>
---
```

## head（自定义头部标签）

```yaml
---
title: 页面标题
head:
  - tag: meta
    attrs:
      property: og:image
      content: https://example.com/og.png
  - tag: script
    attrs:
      src: https://analytics.example.com/script.js
      defer: true
---
```

## prev / next（导航链接）

```yaml
---
title: 页面标题
prev: false                 # 隐藏上一页
next:
  link: /advanced/
  label: 进阶指南
---
```

## 扩展 Schema

在 `src/content.config.ts` 中添加自定义字段：

```typescript
import { docsSchema } from '@astrojs/starlight/schema';
import { z } from 'astro/zod';

export const collections = {
  docs: defineCollection({
    loader: docsLoader(),
    schema: docsSchema({
      extend: z.object({
        category: z.enum(['tutorial', 'guide', 'reference']).optional(),
      }),
    }),
  }),
};
```
