# Advisors 合并记录

> 2026-10-25 追加核验：结构校验的默认次数已按同版源码纠正为首次调用加最多 3 次重试，相关链接改为本地校验章节。 详情见[校验专题记录](../spring-ai-structured-output-validation-zh-CN/README.md)。以下原有验证记录对应此前阶段。

日期：2026-10-25。将已精翻的 Advisors API 与 Recursive Advisors 整理为一篇，与 ChatClient API 在侧边栏同级。

- [站点正文](../../src/content/docs/frameworks/spring-ai/core/advisors.mdx) · [合并定稿](translation.md)
- 阅读顺序：核心组件与执行流程 → API 接口 → 自定义实现 → 递归 Advisors → 历史迁移。
- 移除分篇间的重复引导，合并来源说明，保留全部 16 段代码与 4 张图片；旧递归篇地址跳转到合并章节。
- 分篇译稿与审校记录保留在 [Advisors](../spring-ai-advisors-zh-CN/README.md) 和[递归篇](../spring-ai-advisors-recursive-zh-CN/README.md)。
- [合并前代码与图片校验基线](merge-baseline.json)。本次仅调整文章组织、页面入口及链接。

验证通过：16 段代码逐字一致，4 张图片 SHA-256 不变，合并定稿与站点正文一致；`npm run check` 无错误、警告或提示，`npm run build` 成功生成 124 页（保留既有 i18n 空集合与 docs/404 缺失提示）。桌面 1440px、手机 390px 均无横向溢出或脚本错误，图片加载、同级导航、正文链接与旧地址跳转正常。格式检查及 `git diff --check` 通过。

详细结果见 [validation.jsonl](validation.jsonl)。
