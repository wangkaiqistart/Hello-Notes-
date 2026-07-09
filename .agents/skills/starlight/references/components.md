# Starlight 组件使用参考

> 来源：https://starlight.astro.build/components/using-components/

## 概述

Starlight 支持在 MDX 和 Markdoc 文件中使用组件来增强文档内容。提供了一系列内置组件用于常见文档场景（卡片、标签页、步骤、文件树等），同时支持自定义组件和任何 UI 框架组件。

---

## 1. 在 MDX 中使用组件

导入组件后以 JSX 标签形式渲染（标签名首字母大写）：

```mdx
---
title: Welcome to my docs
---

import { Icon } from '@astrojs/starlight/components';
import CustomCard from '../../components/CustomCard.astro';

<Icon name="open-book" />

<CustomCard>组件可以包含 **嵌套内容**。</CustomCard>
```

支持所有 Astro 集成的 UI 框架组件（React、Vue、Svelte、Solid 等），需要时加 `client:` 指令。

---

## 2. 在 Markdoc 中使用组件

使用 `{% %}` 标签语法，无需导入（通过 Starlight Markdoc preset 自动注册）：

```markdoc
---
title: Welcome to my docs
---

{% card title="Stars" icon="star" %}
Sirius, Vega, Betelgeuse
{% /card %}
```

---

## 3. 内置组件一览

所有内置组件从 `@astrojs/starlight/components` 导入。

### 3.1 Card（卡片）

在一个带样式的盒子中展示内容。

```mdx
import { Card } from '@astrojs/starlight/components';

<Card title="Check this out">
  想要高亮的有趣内容。
</Card>

<!-- 带图标 -->
<Card title="Stars" icon="star">
  Sirius, Vega, Betelgeuse
</Card>
```

Props:
- `title`（必填）: 卡片标题
- `icon`（可选）: 内置图标名称

### 3.2 CardGrid（卡片网格）

将多个 Card 或 LinkCard 并排显示。

```mdx
import { Card, CardGrid } from '@astrojs/starlight/components';

<CardGrid>
  <Card title="功能一" icon="open-book">说明</Card>
  <Card title="功能二" icon="information">说明</Card>
</CardGrid>

<!-- 错位排列效果（适合首页） -->
<CardGrid stagger>
  <Card title="功能一" icon="open-book">说明</Card>
  <Card title="功能二" icon="information">说明</Card>
</CardGrid>
```

Props:
- `stagger`（可选）: 第二列向下错位，增加视觉层次感

### 3.3 LinkCard（链接卡片）

突出显示重要链接。

```mdx
import { LinkCard } from '@astrojs/starlight/components';

<LinkCard
  title="Authoring Markdown"
  href="/guides/authoring-content/"
  description="了解如何编写文档内容。"
/>
```

Props:
- `title`（必填）: 链接标题
- `href`（必填）: 链接 URL
- `description`（可选）: 描述文字

### 3.4 Tabs / TabItem（标签页）

将内容分组到可切换的标签中。

```mdx
import { Tabs, TabItem } from '@astrojs/starlight/components';

<Tabs>
  <TabItem label="Stars" icon="star">
    Sirius, Vega, Betelgeuse
  </TabItem>
  <TabItem label="Moons" icon="moon">
    Io, Europa, Ganymede
  </TabItem>
</Tabs>
```

TabItem Props:
- `label`（必填）: 标签文字
- `icon`（可选）: 内置图标名称

### 3.5 Steps（步骤）

为有序列表添加步骤样式。

````mdx
import { Steps } from '@astrojs/starlight/components';

<Steps>

1. 导入组件：

   ```js
   import { Steps } from '@astrojs/starlight/components';
   ```

2. 用 `<Steps>` 包裹你的有序列表。

</Steps>
````

不接受任何 Props。直接包裹标准 Markdown 有序列表即可。

### 3.6 FileTree（文件树）

展示目录结构，带文件图标和可折叠子目录。

```mdx
import { FileTree } from '@astrojs/starlight/components';

<FileTree>

- astro.config.mjs
- package.json
- src
  - components
    - **Header.astro** 一个重要文件
    - Title.astro
  - pages/

</FileTree>
```

功能：
- 加粗文件名 `**Header.astro**` 高亮显示
- 文件名后加文字作为注释
- 使用 `...` 或 `…` 作为占位符
- 以 `/` 结尾表示空目录

### 3.7 Aside（旁白/提示框组件）

除了 Markdown `:::` 语法，也可以作为组件在 MDX 中使用：

```mdx
import { Aside } from '@astrojs/starlight/components';

<Aside>这是默认的 note 类型提示。</Aside>

<Aside type="tip" title="你知道吗?">
  自定义标题和类型的提示框。
</Aside>

<Aside type="caution" title="注意" icon="warning">
  带自定义图标的警告。
</Aside>
```

Props:
- `type`（可选）: `'note'`（默认） | `'tip'` | `'caution'` | `'danger'`
- `title`（可选）: 自定义标题，默认使用类型对应的标题
- `icon`（可选）: 内置图标名称，覆盖默认图标

### 3.8 LinkButton（链接按钮）

显示醒目的行动号召按钮。

```mdx
import { LinkButton } from '@astrojs/starlight/components';

<LinkButton href="/getting-started/">开始使用</LinkButton>
<LinkButton href="/reference/configuration/" variant="secondary">
  配置参考
</LinkButton>
<LinkButton
  href="https://docs.astro.build"
  variant="minimal"
  icon="external"
  iconPlacement="start"
>
  Astro 文档
</LinkButton>
```

Props:
- `href`（必填）: 链接 URL
- `variant`（可选）: `'primary'`（默认） | `'secondary'` | `'minimal'`
- `icon`（可选）: 内置图标名称
- `iconPlacement`（可选）: `'start'` | `'end'`（默认）

### 3.9 Badge（徽章）

显示状态或分类标签。

```mdx
import { Badge } from '@astrojs/starlight/components';

<Badge text="New" variant="tip" />
<Badge text="Deprecated" variant="caution" />
```

Props:
- `text`（必填）: 显示文字
- `variant`（可选）: `note` | `tip` | `caution` | `danger` | `success` | `default`
- `size`（可选）: `small` | `medium` | `large`

### 3.10 Icon（图标）

显示 Starlight 内置图标。

```mdx
import { Icon } from '@astrojs/starlight/components';

<Icon name="star" />
```

Props:
- `name`（必填）: 图标名称（参见内置图标列表）

---

## 4. Aside Markdown 语法 + 代码块（Expressive Code）

### Aside `:::` 语法（无需导入）

```markdown
:::note
这是一个提示。
:::

:::tip[你知道吗?]
自定义标题的提示。
:::

:::caution
注意事项。
:::

:::danger
危险警告。
:::

:::tip{icon="heart"}
自定义图标的提示。
:::
```

类型：`note`、`tip`、`caution`、`danger`

### 代码块增强（Expressive Code）

Starlight 使用 Expressive Code 渲染代码块，支持标题、行高亮、文本标记等：

````markdown
```js title="src/app.js"
// 带标题的代码块
console.log('Hello');
```

```bash title="安装依赖"
npm install
```

```js {2-3}
// 高亮第 2-3 行
function demo() {
  const highlighted = true;
  return highlighted;
}
```

```js "search term" /regex/
// 高亮匹配的文本
const search term = 'found';
const regex = /match/;
```

```js ins="added" del="removed"
// 标记插入和删除的文本
console.log('added text here');
console.log('removed text here');
```

```bash frame="none"
echo "禁用窗口边框"
```
````

功能总结：
- `title="..."` — 添加文件名/标题标签
- `{2-3}` — 高亮指定行
- `"text"` — 高亮匹配文本
- `/regex/` — 正则匹配高亮
- `ins="..."` / `del="..."` — 标记插入/删除
- `frame="none"` — 禁用窗口边框
- Shell 语言自动显示终端窗口样式

---

## 5. 与 Starlight 样式兼容

Starlight 会为 Markdown 内容添加默认样式（如元素间距）。如果这些样式与你的组件冲突，用 `not-content` 类禁用：

```astro
<!-- src/components/Example.astro -->
<div class="not-content">
  <p>不受 Starlight 默认内容样式影响。</p>
</div>
```

---

## 6. 获取组件 Props 类型

用 `ComponentProps` 工具类型引用内置组件的 Props（方便扩展和包装）：

```astro
---
import type { ComponentProps } from 'astro/types';
import { Badge } from '@astrojs/starlight/components';

type BadgeProps = ComponentProps<typeof Badge>;
---
```

---

## 速查表

| 组件 | 导入 | 用途 |
|------|------|------|
| `Aside` | `@astrojs/starlight/components` | 提示框（也支持 `:::` Markdown 语法） |
| `Card` | 同上 | 带样式的内容盒子 |
| `CardGrid` | 同上 | 卡片网格布局 |
| `LinkCard` | 同上 | 突出显示的链接 |
| `LinkButton` | 同上 | 行动号召按钮 |
| `Tabs` + `TabItem` | 同上 | 可切换标签页 |
| `Steps` | 同上 | 步骤指南 |
| `FileTree` | 同上 | 目录结构展示 |
| `Badge` | 同上 | 状态/分类标签 |
| `Icon` | 同上 | 内置图标 |
