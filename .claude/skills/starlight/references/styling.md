# CSS 和样式定制

## 自定义 CSS

1. 创建 CSS 文件（如 `src/styles/custom.css`）
2. 在 `astro.config.mjs` 中注册：

```javascript
starlight({
  customCss: ['./src/styles/custom.css'],
})
```

## CSS 自定义属性（变量）

Starlight 使用 CSS 变量控制主题颜色。可通过官方颜色主题编辑器可视化调整：
https://starlight.astro.build/zh-cn/guides/css-and-tailwind/#主题编辑器

编辑器生成的色阶代码直接复制到自定义 CSS 中即可：

```css
/* src/styles/custom.css */
:root {
  --sl-color-accent-low: #1a1a2e;
  --sl-color-accent: #4a9eff;
  --sl-color-accent-high: #b3d9ff;
  --sl-color-white: #ffffff;
  --sl-color-gray-1: #eeeeee;
  --sl-color-gray-2: #c2c2c2;
  --sl-color-gray-3: #8b8b8b;
  --sl-color-gray-4: #585858;
  --sl-color-gray-5: #383838;
  --sl-color-gray-6: #272727;
  --sl-color-black: #181818;
}
:root[data-theme='light'] {
  --sl-color-accent-low: #c5e4ff;
  --sl-color-accent: #005fa3;
  --sl-color-accent-high: #003157;
  --sl-color-white: #181818;
  --sl-color-gray-1: #272727;
  --sl-color-gray-2: #383838;
  --sl-color-gray-3: #585858;
  --sl-color-gray-4: #8b8b8b;
  --sl-color-gray-5: #c2c2c2;
  --sl-color-gray-6: #eeeeee;
  --sl-color-black: #ffffff;
}
```

## 字体自定义

```css
:root {
  --sl-font: 'IBM Plex Serif', serif;     /* 正文字体 */
  --sl-font-mono: 'JetBrains Mono', mono; /* 代码字体 */
}
```

### 本地字体

1. 将字体文件放入 `src/fonts/`
2. 创建 `src/fonts/font-face.css`：

```css
@font-face {
  font-family: 'Custom Font';
  src: url('./CustomFont.woff2') format('woff2');
  font-weight: normal;
  font-style: normal;
  font-display: swap;
}
```

3. 注册：`customCss: ['./src/fonts/font-face.css']`

### Fontsource 字体

```bash
npm install @fontsource/ibm-plex-serif
```

```javascript
customCss: ['@fontsource/ibm-plex-serif/400.css']
```

## Tailwind CSS

### 新项目集成

创建 Starlight 项目时直接选择 Tailwind 即可自动配置。

### 已有项目集成

```bash
npx astro add tailwind
```

然后安装 Starlight Tailwind 插件：

```bash
npm install @astrojs/starlight-tailwind
```

配置 `astro.config.mjs`：

```javascript
starlight({
  customCss: ['./src/styles/global.css'],
})
```

### 使用 Tailwind 设置 Starlight 的样式

`src/styles/global.css` 中用 `@theme` 覆盖 Starlight 的设计 token：

```css
@layer base, starlight, theme, components, utilities;
@import '@astrojs/starlight-tailwind';
@import 'tailwindcss/theme.css' layer(theme);
@import 'tailwindcss/utilities.css' layer(utilities);

@theme {
  /* 正文字体 */
  --font-sans: 'Atkinson Hyperlegible';
  /* 代码字体 */
  --font-mono: 'IBM Plex Mono';

  /* 强调色（accent）— 用于链接和当前项高亮 */
  --color-accent-50: var(--color-indigo-50);
  --color-accent-100: var(--color-indigo-100);
  --color-accent-200: var(--color-indigo-200);
  --color-accent-600: var(--color-indigo-600);
  --color-accent-900: var(--color-indigo-900);
  --color-accent-950: var(--color-indigo-950);

  /* 灰色（gray）— 用于背景和边框 */
  --color-gray-50: var(--color-zinc-50);
  --color-gray-200: var(--color-zinc-200);
  --color-gray-800: var(--color-zinc-800);
  --color-gray-900: var(--color-zinc-900);
  --color-gray-950: var(--color-zinc-950);
}
```

映射关系：
- `--color-accent-*` → 链接、当前项高亮
- `--color-gray-*` → 背景、边框
- `--font-sans` → UI 和正文
- `--font-mono` → 代码块
