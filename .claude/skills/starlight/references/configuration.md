# 站点配置

所有配置在 `astro.config.mjs` 的 `starlight()` 集成中设置。

## 基础配置

```javascript
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

export default defineConfig({
  site: 'https://example.com',
  integrations: [
    starlight({
      title: '我的文档站',
      // 多语言标题
      // title: { 'zh-CN': '我的文档', en: 'My Docs' },
      description: '站点描述',
      defaultLocale: 'zh-cn',
    }),
  ],
});
```

## Logo

```javascript
starlight({
  logo: {
    src: './src/assets/my-logo.svg',
    replacesTitle: true, // 隐藏文字标题
  },
  // 或明暗模式分别设置
  logo: {
    light: './src/assets/logo-light.svg',
    dark: './src/assets/logo-dark.svg',
  },
})
```

## 社交链接

```javascript
starlight({
  social: [
    { icon: 'github', label: 'GitHub', href: 'https://github.com/...' },
    { icon: 'discord', label: 'Discord', href: 'https://...' },
  ],
})
```

## 编辑链接

```javascript
starlight({
  editLink: {
    baseUrl: 'https://github.com/user/repo/edit/main/',
  },
})
```

## 目录

```javascript
starlight({
  tableOfContents: { minHeadingLevel: 2, maxHeadingLevel: 3 },
  // 或禁用: tableOfContents: false
})
```

## 自定义 Head

```javascript
starlight({
  head: [
    {
      tag: 'script',
      attrs: { src: 'https://analytics.example.com/script.js', defer: true },
    },
    {
      tag: 'meta',
      attrs: { property: 'og:image', content: 'https://example.com/og.png' },
    },
  ],
})
```

## 国际化（i18n）

```javascript
starlight({
  defaultLocale: 'zh-cn',
  locales: {
    'zh-cn': { label: '简体中文', lang: 'zh-CN' },
    en: { label: 'English' },
    ar: { label: 'العربية', dir: 'rtl' },
  },
})
```

Root locale（默认语言无路径前缀）：

```javascript
locales: {
  root: { label: '简体中文', lang: 'zh-CN' },
  en: { label: 'English' },
}
```

## 标题分隔符

```javascript
starlight({
  titleDelimiter: '—', // 默认 '|'，页面标题格式：Page Title | Site Title
})
```

## 自定义 CSS

```javascript
starlight({
  customCss: [
    './src/styles/custom.css',
    '@fontsource/ibm-plex-serif/400.css',
  ],
})
```

## Sitemap

在 `astro.config.mjs` 中设置 `site` URL 即可自动生成 sitemap。
