# 部署

## 静态站点（默认）

```bash
# 构建输出到 dist/ 目录
npm run build

# 可直接部署到任何静态托管
```

---

## Vercel

```bash
npx astro add vercel
```

```javascript
// astro.config.mjs
import vercel from '@astrojs/vercel';
export default defineConfig({ adapter: vercel() });
```

---

## Netlify

```bash
npx astro add netlify
```

```javascript
import netlify from '@astrojs/netlify';
export default defineConfig({ adapter: netlify() });
```

---

## Cloudflare Pages

```bash
npx astro add cloudflare
```

```javascript
import cloudflare from '@astrojs/cloudflare';
export default defineConfig({ adapter: cloudflare() });
```

部署命令：`npx astro build && npx wrangler deploy`

---

## GitHub Pages

```javascript
// astro.config.mjs
export default defineConfig({
  site: 'https://username.github.io',
  base: '/repo-name/',
});
```

```yaml
# .github/workflows/deploy.yml
name: Deploy to GitHub Pages
on:
  push:
    branches: [main]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 20 }
      - run: npm ci && npm run build
      - uses: actions/upload-pages-artifact@v3
        with: { path: ./dist }
  deploy:
    needs: build
    runs-on: ubuntu-latest
    permissions: { pages: write, id-token: write }
    environment: { name: github-pages }
    steps:
      - uses: actions/deploy-pages@v4
```
