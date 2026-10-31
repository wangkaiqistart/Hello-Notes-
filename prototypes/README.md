# Hi, Agent! 首页原型

版本：V1 · 2026-11-01。该版本已验收，正式实现已接入 `src/pages/index.astro`。

## 预览

在知识库项目根目录运行：

```bash
python3 -m http.server 4333 --bind 127.0.0.1
```

打开 <http://127.0.0.1:4333/prototypes/homepage-v1-2026-11-01.html>。
需要通过 HTTP 预览，直接双击 HTML 时浏览器会限制 ES Module 加载。

## 可体验的内容

- 首屏 Three.js 知识网络：自动旋转、鼠标视差、流动光点、节点链接、暂停与播放。
- Spring AI、Deep Agents、RAG、上下文工程专题卡片。
- Java / Python / Agent 三条学习路线切换，支持键盘方向键。
- 搜索：按钮或 `⌘K` / `Ctrl+K` 打开，输入过滤，方向键选择，Enter 阅读，Esc 关闭。
- 手机导航、响应式布局、减少动态效果模式和静态回退。

专题和文章在新标签页打开现有站点，原型保留在当前页。搜索索引、精选阅读和学习路线是人工编排的演示内容，统一放在 `window.mockData`，没有接入业务接口或生成虚假更新日期。

## 文件

- `homepage-v1-2026-11-01.html`：原型入口。
- `homepage-assets/homepage.css`：样式与响应式布局。
- `homepage-assets/homepage.js`：交互、演示数据与三维场景。
- `homepage-assets/vendor/`：本地 Three.js 0.170.0 与 MIT 许可；预览不依赖远程 CDN。
- `exports/`：桌面和手机预览截图、验收检查记录。

以上为独立原型阶段的产物。验收后的正式实现见下节。

## 正式实现

- 首页入口：`src/pages/index.astro`；替代原来的 `src/content/docs/index.mdx`。
- 学习路线：`src/data/home.ts`，在构建时校验专题和路线指向已发布文档。
- 样式：`src/styles/home.css` 仅由首页加载；`src/styles/site-theme.css` 提供首页与文档页共用的配色，`src/styles/docs.css` 统一文档导航与阅读界面。
- 外观：共用 `SiteBrand.astro` 与 `ThemeSelect.astro`；浅色、深色、跟随系统使用同一个 `starlight-theme` 偏好，支持跨页面和标签页同步，Three.js 图形随主题配色。
- 交互：`src/scripts/home.ts`；三维场景独立放在 `src/scripts/home-graph.js`，按需加载 Three.js。
- 搜索：复用 Starlight 构建生成的 Pagefind 全文索引。`src/pages/home-search.json.ts` 从实际文档集合生成标题和描述索引，用于推荐、开发预览及全文搜索不可用时的回退。
- 文章链接使用站内路由，在当前标签页打开。图标和三条学习路线直接生成在 HTML 中，无 JavaScript 时仍可阅读。

验证正式实现：`npm run check`、`npm run build`。本目录保留验收原型，正式站点构建不会发布原型文件。
