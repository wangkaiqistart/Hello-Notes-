# 内容编写

## 支持格式

- `.md` — 标准 Markdown（默认）
- `.mdx` — MDX（支持组件导入，默认已安装集成）
- `.mdoc` — Markdoc（需额外配置）

所有文档文件放在 `src/content/docs/` 中。

## Frontmatter

每个页面必须有 frontmatter，至少包含 `title`：

```markdown
---
title: 我的页面
description: 页面描述
---

正文内容...
```

完整 frontmatter 参考 → `references/frontmatter.md`

## 标题层级

- 页面标题由 frontmatter `title` 自动生成（作为 h1）
- 正文从 `##`（h2）开始
- `##` 和 `###` 自动出现在右侧目录中

## Aside 提示框

```markdown
:::note
提示信息。
:::

:::tip[自定义标题]
有用的建议。
:::

:::caution
注意事项。
:::

:::danger
危险警告。
:::

:::tip{icon="heart"}
自定义图标。
:::
```

## 代码块（Expressive Code）

### 基础

````markdown
```javascript
const hello = 'world';
```
````

### 标题

````markdown
```javascript title="src/app.js"
console.log('Hello');
```
````

### 行高亮

````markdown
```javascript {2-3}
function demo() {
  const highlighted = true;
  return highlighted;
}
```
````

### 文本标记

````markdown
```javascript "search" ins="added" del="removed"
const search = 'found';
console.log('added text');
console.log('removed text');
```
````

### 禁用窗口框架

````markdown
```bash frame="none"
echo "无边框"
```
````

### Diff 语法

````markdown
```diff lang="js"
  function example() {
-   console.log('old');
+   console.log('new');
  }
```
````

## 链接

```markdown
[内部链接](/guides/getting-started/)
[相对链接](../other-page/)
[外部链接](https://example.com)
```

## 图片

```markdown
![说明文字](../../assets/image.png)
![远程图片](https://example.com/image.png)
```

本地图片放在 `src/assets/` 中，Astro 会自动优化。

如果用户提供的是本地图片，但希望文档里使用可公开访问的远程图片链接，先使用 `oss-image-publisher` skill 上传图片并获取 OSS 链接，再把返回的链接写成 Markdown 图片语法。文档 skill 不直接处理 OSS 密钥，也不自己实现上传。
