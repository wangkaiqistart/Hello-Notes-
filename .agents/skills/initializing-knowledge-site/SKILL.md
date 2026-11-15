---
name: initializing-knowledge-site
description: 在空目录初始化可独立部署的 Astro + Starlight 技术知识网站，包含 Three.js 交互首页、文档搜索、Java/前端分类与独立域名配置。Use when 用户要求新建类似当前知识库的文档站、Java 知识库或前端知识站；仅维护已有文章、初始化 raw/wiki 资料仓库时不使用。
---

# 初始化知识网站

交付一个能继续写作、能构建、能部署到独立域名的静态知识站。随包脚本生成可运行基线，模型负责按用户主题完善视觉与内容并验证结果。

## 确定输入

- 目标目录：采用用户给出的路径；未提供时使用当前目录。先检查，目录非空时不要覆盖或另选路径。脚本允许已有 `.git/` 与 `.DS_Store`，其他文件均拒绝写入；已有项目改造另行处理。
- 主题：`java`、`frontend`、`mixed`。用户只说“Java，以后可能加前端”时采用 `java`，说明可扩展；明确两者都要时采用 `mixed`。
- 名称与简介：优先用户提供的值，否则按主题生成可编辑默认值。
- 域名：有域名时设置 HTTPS 根域名（例如 `https://java.example.com`）；没有域名时先使用 `https://kb.example`，交付时明确它是待替换值，不为本地初始化阻塞提问。
- 本技能创建网站项目，不建立远端仓库、不推送、不发布、不修改 DNS。只有用户要求这些动作时才继续相应工作。

## 生成项目

技能目录应取本次实际读取的 `SKILL.md` 所在目录，不假设当前目录是技能所在仓库。页面风格必须使用 `unslop` 技能（本仓库随包提供），先读取其 SKILL.md、signs.md 与 tokens.md；保持其作者/CC BY 4.0 署名。执行前阅读 [站点结构](references/site-architecture.md)；定制首页时阅读 [视觉与 Three.js](references/homepage-design.md)。

```bash
python3 /绝对路径/initializing-knowledge-site/scripts/init_site.py \
  --target /绝对路径/空目录 \
  --profile java \
  --title 'Java 工程笔记' \
  --site https://java.example.com
```

`--dry-run` 仅校验输入并列出计划。脚本不执行安装、Git 或发布；目标不存在时创建，非空时退出。不要通过清空目录或使用其他模板命令规避检查。

生成后在目标目录依次执行：

```bash
npm install
npm run format
npm run check
npm run build
npm run format:check
```

首次安装生成并保留 `package-lock.json`；之后使用 `npm ci`。模板依赖是已验证基线，不自动升级所有包。若需调整版本，核对 Node engines、Astro/Starlight peerDependencies 与 Three.js 类型版本，修复后重新验证。网络或权限失败时保留生成文件，报告具体阻塞和继续命令，不宣称构建通过。

## 按主题完成内容与视觉

- `site.config.json` 是标题、独立域名、分类、首页入口与导航的数据源，修改后同步实际文档；新增领域参照 [站点结构](references/site-architecture.md)。不要复制参考仓库的域名、账号、分析脚本、OSS 配置或业务文章。
- `/` 是独立 Astro 首页；Starlight 负责 `/start/` 与主题文档。不要生成 `src/content/docs/index.md` 抢占首页。
- 首页必须有真正的 Three.js 场景：可展开、拖动查看的分层知识页，节点连线表示知识层次，默认短暂展开后静止，连续演示由读者主动开启。用暖白纸面、墨色文字、少量青绿强调；以 `unslop` 的方向和九轮检查决定排版，避免霓虹、光晕、渐变字、悬浮球与无意义循环动画。
- 所有插图和图标生成真正的本地 SVG，放入 `public/images/` 或 `src/assets/`，用相对资源路径引用；禁止外链图片、SVG 内嵌位图和 SVG 仅包装 PNG。交互 Three.js 使用 canvas，静态图与降级图仍必须是 SVG。截图仅作为验收证据，不作为产品图片。
- 初始 Java/前端文章是可继续扩写的真实入门内容。首页卡片指向已生成路由，内容数量来自集合，不伪造阅读量、文章量或作者信息。没有内容的未来分类不展示成可点击入口。
- 首页提供搜索、键盘可达入口和演示播放/暂停；正文沿用 Starlight 主题/目录/搜索/代码高亮。长文阅读页面不加载 Three.js。
- WebGL 不可用、关闭 JS、减少动态效果时保留可读标题、静态示意与普通链接。窄屏降低像素比和模型细节，离屏/后台停止渲染，销毁场景释放 GPU 与监听器。
- 生成项目的 `AGENTS.md` 是后续维护入口，`CLAUDE.md` 相对软链接指向它。

## 验证与交付

1. 检查上述命令结果，构建输出包含首页、目录、各分类文章、404 和 Pagefind 索引。
2. 在真实浏览器预览构建产物（开发模式不能证明 Pagefind 可用），检查 1440px 桌面与 390px 手机首屏、导航、搜索结果跳转、暂停/恢复、减少动态效果、无横向溢出与控制台错误。无浏览器能力时明确标为未验证，保留可供检查的启动命令。
3. 对照 [验收与域名部署](references/acceptance-and-deployment.md)，确认独立域名的 `site`、canonical、sitemap、深层路由与静态托管方式。未实际部署时只报告“部署配置已生成”。
4. 输出项目绝对路径、启动命令、主题与域名、已验证项和未验证项。必要时展示桌面/手机截图。提交、推送、创建远端项目遵循用户本次授权。

## 参考技能与资源

- `unslop`：页面风格的必用依赖。优先读取已安装版本，否则从本技能旁的 `../unslop/SKILL.md` 加载；都缺失时搜索该技能，仍不可用则报告缺失，不能把自拟视觉规则冒称为已使用 unslop。用户已明确视觉意图时自行落实，不添加额外审批流程。
- `astro`：版本、构建、资源优化、Astro 页面问题。
- `starlight`：导航、docs loader/schema、MDX 和组件覆盖。相关技能不可用时直接查官方文档与本项目类型，不把技能缺失当作生成项目的阻塞。
- `scripts/init_site.py`：路径与参数检查、模板复制和主题内容生成。
- `assets/template/`：可直接构建的站点源码；`assets/content/`：按主题选择的起始文章。
- `scripts/test_init_site.py`：运行 `python3 -m unittest discover -s /技能绝对路径/scripts -p 'test_*.py'` 校验非空目录保护与不同主题的生成行为。
