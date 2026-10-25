# 结构化输出扩展合并记录

> 2026-10-25 追加核验：结构化输出已进一步合入 Schema 校验与自动纠正，当前主文共 30 段代码、5 张图；重试次数、显式注册与空 Schema 行为按同版源码纠正。 详情见[校验专题记录](../spring-ai-structured-output-validation-zh-CN/README.md)。以下原有验证记录对应此前阶段。

日期：2026-10-25。将原生结构化输出与输出转换器并入原有结构化输出一篇，保留原 URL 和侧边栏入口。

- [站点正文](../../src/content/docs/frameworks/spring-ai/core/structured-output.mdx) · [合并定稿](translation.md) · [扩展前正文](before-merge.mdx)
- 阅读顺序：Java 对象与泛型 → 可靠性配置 → 完整响应 → 提供方原生结构化输出 → 输出转换器 → 用法速查。
- [原生输出精翻记录](../spring-ai-structured-output-native-zh-CN/README.md) · [转换器精翻记录](../spring-ai-structured-output-converters-zh-CN/README.md)。
- 两篇共 23 段来源代码，主文已包含的两个原生示例及 record 定义复用；保留现有 8 段代码，合并后共 28 段。非注释代码校正限定于模板骨架和局部变量引用，详见代码对照与审校记录。
- 新增引用 3 张图。架构图复用已接受的中文版本，API 图和类图保留原图节点、线条与配色，仅替换说明文字及已核验的旧 API 标签。
- 来源图中的 `call(Prompt): String` 改为实际的 `ChatResponse`，`ObjectMapper` 改为 2.0.2 使用的 `JsonMapper`。`BeanOutputConverter` 默认已具备围栏清理，译文按 2.0.2 源码修正来源的过度概括。

验证通过：原有 8 段代码保持不变，新增两篇的 23 段来源代码逐块对应到主文；4 张图正常加载，已有资源哈希不变，中文图内嵌来源图片字节一致。合并定稿与站点正文逐字节一致。

`npm run check` 无错误、警告或提示；`npm run build` 成功生成 124 页，保留已有 i18n 空集合与 docs/404 缺失提示。桌面 1440px、手机 390px 均无横向页面溢出或脚本错误，本地链接、锚点、导航及大图入口通过检查，代码围栏嵌套正常。相关 Markdown / MDX 格式与 `git diff --check` 通过。

详情见 [validation.jsonl](validation.jsonl)。未编译 Java 示例或调用真实模型。
