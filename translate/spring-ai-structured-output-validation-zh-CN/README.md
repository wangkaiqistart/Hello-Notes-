# Schema 校验与自动纠正翻译记录

日期：2026-10-25。使用 baoyu-translate 精翻流程，沿用项目简体中文、开发者受众与简明技术文档风格。

- 来源：[Spring AI 2.0.2 Schema Validation & Self-Correction](https://docs.spring.io/spring-ai/reference/api/structured-output/validation.html)。
- [英文正文](../spring-ai-structured-output-validation.md) · [来源 HTML](source-article.html) · [代码快照](source-code.json)
- [分析](01-analysis.md) → [上下文](02-prompt.md) → [初稿](03-draft.md) → [审校](04-critique.md) → [修订](05-revision.md) → [专题定稿](translation.md)
- [站点正文](../../src/content/docs/frameworks/spring-ai/core/structured-output.mdx) · [补充前主文](before-merge.mdx) · [合并定稿](../spring-ai-structured-output-combined-zh-CN/translation.md)

## 覆盖与校正

保留全部 4 段来源代码，其中启用校验与原生组合两段复用主文已有示例；新增 2 段手动配置代码，合并后共 30 段代码、5 张图。校验章节位于可靠性配置之后，复用主文 URL 和侧边栏入口，Advisors 页的相关链接同步本地化。

按 Maven Central 同版 sources.jar 核对循环、构建器与 ChatClient 注册路径。Advisor 源码与 jsDelivr 同标签版本字节一致，见 [来源证据](source-evidence.json)、[Advisor 源码](source-StructuredOutputValidationAdvisor.java) 和 [ChatClient 源码](source-DefaultChatClient.java)。

- 默认 maxRepeatAttempts=3，实际循环最多 1+3 次；主文与 Advisors 篇的旧次数说明一并纠正。
- 显式注册后使用普通 entity()；再启用 validateSchema() 会追加默认校验器。
- 校验耗尽返回最后响应，再进入转换器，不能承诺最终合规或固定异常类型。
- 自定义转换器无有效 Schema 时启用 validateSchema()，在 2.0.2 会抛 IllegalArgumentException，修正原有“两项开关都无操作”的说明。

## 配图

新增中文循环图保留来源 PNG 的手绘布局、蓝色虚线、橙色主路径与红色失败回路，先解释流程再展示图片，提供替代文本、短图注和大图入口。其他图片文件不修改。来源校验值见 [source-assets.json](source-assets.json)，复现脚本见 [localize-self-correction.py](localize-self-correction.py)。

验证通过：4 段来源代码与专题定稿完全一致，全部对应到主文；原有 28 段代码与 Advisors 代码保持不变，当前两篇合并定稿与站点正文逐字节一致。已有图片哈希未变，新增 SVG 内嵌来源 PNG 字节一致。

`npm run check` 无错误、警告或提示；`npm run build` 成功生成 131 页，保留已有 i18n 空集合与 docs/404 缺失提示。桌面 1440px、手机 390px：30 段代码、8 个主章节、5 张图均正常，无横向页面溢出或脚本错误；正文链接、章节锚点、导航与大图入口通过检查。Markdown / MDX 格式及 `git diff --check` 通过。

详情见 [validation.jsonl](validation.jsonl)。Java 示例未编译，未调用真实模型。
