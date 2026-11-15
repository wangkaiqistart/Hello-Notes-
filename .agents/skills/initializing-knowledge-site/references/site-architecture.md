# 站点结构与扩展

## 文件与职责

- `site.config.json`：独立站名称、description、site URL、profile、topics。每个 topic 含 `id`、`label`、`description`、`href` 和首页知识索引节点名称；`href` 对应真实目录首页。
- `astro.config.mjs`：Astro `site` 取上述配置，Starlight 根语言为 `zh-CN`，sidebar 从 topics 生成。没有旧站域名或源码绝对路径。
- `src/content.config.ts`：保留 `docsLoader()` / `docsSchema()`，配置 `i18nLoader()` 避免空集合警告。新增字段通过 `docsSchema({ extend: ... })` 实现。
- `src/pages/index.astro`：静态 HTML 首页、SEO、真实文章计数、分类卡片和精选文章。构建时检查 topic 入口存在，首页不占据 docs 集合路径。
- `src/pages/home-search.json.ts`：已发布内容的标题/描述索引，开发和生产均可用；不包含草稿。
- `src/scripts/home.ts`：首页搜索，生产优先 Pagefind 全文索引，开发/索引失败回退标题与描述；DOM 使用 `textContent` 展示外部数据。
- `src/scripts/scene.ts`：动态导入 Three.js、渲染与生命周期；只由首页加载。
- `src/content/docs/start.md`：文档总入口。`java/` 与 `frontend/`：按 profile 生成的文档。
- `public/favicon.svg`、`src/styles/`：本地资源与主题，没有运行时 CDN 依赖。
- `.github/workflows/ci.yml`：安装、检查和构建；不自动发布。
- `DEPLOYMENT.md`：独立域名与静态托管操作说明。

## 主题与后续分类

`java` 含语言基础、JVM 与并发、Spring 工程；`frontend` 含 Web 基础、TypeScript、组件与工程；`mixed` 同时包含两组。每组有概览与三篇起始文章。首页网络节点、卡片、导航均读取 topic 数据。

未来添加前端到 Java 站：创建 `src/content/docs/frontend/` 概览和文章，再在 `site.config.json.topics` 增加前端项，最后更新 `/start/` 中的阅读入口。不要重新运行初始化脚本，它会拒绝非空目录。新增任意领域采取同样方式；索引节点数变化后检查画面密度。

不要把站点强制做成 Java 专属：骨架与视觉不依赖领域，只有 profile 选择初始内容。也不要把本技能与 `initializing-knowledge-base` 混用：后者建立 raw/wiki 与知识契约，本技能交付公开阅读网站。

## 依赖维护

模板依赖由 npm 正式发行版本组成。修改模板版本时先查询 npm `version/engines/peerDependencies`，在新空目录从头安装、check、build 后再更新基线。生成站点的锁文件是其实际依赖真值。不要让首次初始化运行交互式升级命令。
