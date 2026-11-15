# 独立域名部署

默认输出静态 `dist/`，可部署到 OSS/CDN、Nginx、Cloudflare Pages、Netlify 或 Vercel 静态托管。域名和托管方式可后续决定，初始化不要求 DNS 或平台凭据。

1. 将 `site.config.json.site` 改为用户拥有的 HTTPS origin，再重新构建。占位 `https://kb.example` 只用于预览，不声称完成绑定。
2. 配置域名解析到实际托管入口，并为此域名签发/绑定证书。Nginx 按 `try_files $uri $uri/ =404` 处理；不要把所有不存在路径重写到首页。
3. 对 OSS/CDN 上传 `dist/` 原有目录结构，设置默认 index.html、404 页面和 HTTPS，确认深层 `/java/xxx/` 能回源到相应 index.html。静态资源可用长期缓存，HTML/index 使用短缓存。Pagefind 的 JS/WASM 需正确 MIME。
4. 上线后真实检查首页、文章深链、404、搜索、canonical 和 sitemap；本地构建通过不等于 DNS、证书或发布完成。

仅在用户指定部署平台并授权发布时实施发布。复制旧项目的 CI、远端地址、OSS bucket 或 Secrets 值不是初始化步骤。自动生成的 CI 只检查构建。
