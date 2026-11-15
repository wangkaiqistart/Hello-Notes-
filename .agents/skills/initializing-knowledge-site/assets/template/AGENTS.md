# 知识站维护指南

- 站点配置：`site.config.json`。正文：`src/content/docs/`。首页：`src/pages/index.astro`，Three.js 仅首页加载。
- 采用中文解释概念、适用场景、代码示例和工程判断，不写空话与写作过程说明。frontmatter 必须含中文 title 和 description。
- 运行 `npm ci`、`npm run dev`；交付改动前运行 `npm run check` 与 `npm run build`，格式修改运行 `npm run format:check`。
- 新增分类同步 site.config.json topics、实际目录首页、总目录。不要生成 docs/index.md 与独立首页冲突。
- 每个图片使用本地 SVG，保存在 public/images/ 或 src/assets/，禁止外链、base64 位图和 SVG 包装 PNG。SVG 必须有 viewBox，图标统一线宽，说明图有准确 alt。
- 图片紧跟首次完整说明，不能直接跟在标题后装饰，不拆开代码解释与代码块。桌面和手机不溢出。
- 页面视觉采用 Unslop 方法：纸面/墨色为主，少量单一强调色；无渐变字、霓虹、emoji 图标与无意义循环动画；主视觉是可操作的知识分层页。
- 有 unslop 技能时先读取并使用，保留品牌与内容。方法署名见 README。
- 保留 Three.js 的减少动态效果、无 WebGL 降级、离屏停止与资源释放；正文不能加载 Three.js。
- Git 只处理任务相关改动。独立域名、DNS、HTTPS 和发布分别验证，不把本地构建当作上线完成。
