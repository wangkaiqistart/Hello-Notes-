# 验收与独立域名

## 本地验收

- `npm run check`、`npm run build`、`npm run format:check` 成功；记录警告，不混同为零告警。
- `npm run preview -- --host 127.0.0.1 --port 4321` 打开真实构建产物。
- 首页 `/`、总目录 `/start/`、主题首页和每篇文章可达；首页与正文之间导航不依赖 JS。
- 首页搜索词可检索起始文章并跳转；生产索引生成在 `dist/pagefind/`，正文 Starlight 搜索在生产预览中可用。开发回退索引只包含标题/描述，应据实说明。
- 检查桌面与手机没有横向溢出，键盘焦点可见；暂停、恢复、减少动态效果和无 WebGL 状态可用。
- 确认首页 bundle 包含 Three.js，而正文不请求 Three.js 文件。WebGL 未得到真实渲染验证时不能声称视觉验收通过。
- 生成项目无旧站域名/品牌/OSS 凭据，site 与 canonical/sitemap 使用同一个独立域名。
- 模板内容用于知识起步，不代表知识库已完整覆盖 Java/前端。

## 部署边界

默认输出静态 `dist/`，可部署到 OSS/CDN、Nginx、Cloudflare Pages、Netlify 或 Vercel 静态托管。域名和托管方式可后续决定，初始化不要求 DNS 或平台凭据。

1. 将 `site.config.json.site` 改为用户拥有的 HTTPS origin，再重新构建。占位 `https://kb.example` 只用于预览，不声称完成绑定。
2. 配置域名解析到实际托管入口，并为此域名签发/绑定证书。Nginx 按 `try_files $uri $uri/ =404` 处理；不要把所有不存在路径重写到首页。
3. 对 OSS/CDN 上传 `dist/` 原有目录结构，设置默认 index.html、404 页面和 HTTPS，确认深层 `/java/xxx/` 能回源到相应 index.html。静态资源可用长期缓存，HTML/index 使用短缓存。Pagefind 的 JS/WASM 需正确 MIME。
4. 上线后真实检查首页、文章深链、404、搜索、canonical 和 sitemap；本地构建通过不等于 DNS、证书或发布完成。

仅在用户指定部署平台并授权发布时实施发布。复制旧项目的 CI、远端地址、OSS bucket 或 Secrets 值不是初始化步骤。自动生成的 CI 只检查构建。
