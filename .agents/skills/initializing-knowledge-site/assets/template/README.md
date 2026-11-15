# 技术知识库

一个可独立部署的 Astro + Starlight 静态站。首页用 Three.js 展示可拖动的分层知识页，文档支持目录、日夜主题、代码高亮和生产全文搜索。

## 本地运行

Node.js >= 22.23.4。首次执行 `npm install` 生成锁文件，此后执行 `npm ci`。

```bash
npm run dev
npm run check
npm run build
npm run preview
npm run format:check
```

修改 `site.config.json` 中的名称、简介与独立域名。`https://kb.example` 为未指定域名时的预览占位地址，发布前必须替换。新增文章放入 `src/content/docs/`；新增分类同时添加真实目录首页和 topics 配置。不要重新执行初始化器覆盖项目。

所有插图均是 `public/images/` 内的本地 SVG；Three.js 是本地打包的交互场景，没有 CDN 图片或运行时远程脚本。首页动画先短暂展开，然后静止，拖动可以检查各知识层次，只有点击播放才连续演示。

首页开发环境可搜索标题与简介；生产 build 后优先用 Pagefind 全文搜索，索引失败则回退标题与简介。正文搜索也需要构建后预览。起始文章不是完整 Java/前端教程。

部署操作与真实验证边界见 [DEPLOYMENT.md](DEPLOYMENT.md)。CI 仅检查，不发布。

## 设计方法署名

页面设计参考 **Unslop**，作者 **Damir Sokolovsky**（[@heydamir](https://x.com/heydamir)），来源 <https://heydamir.design/unslop>，采用 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) 许可。本模板调整为中文工程手册风格，并按项目需求使用本地原创 SVG 与可交互 Three.js 知识页；未使用原技能示例图片。
