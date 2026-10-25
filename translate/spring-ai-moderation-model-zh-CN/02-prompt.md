# 翻译上下文

将审核模型整理为简明中文技术文章，目标为知识库“Spring AI → 模型”小章节。采用 zh-CN / refined / technical，保留 API 标识与必要方法，不逐家翻译安装配置。

内容范围：翻译用途和提供方入口，补充共享 ModerationModel / Prompt / Response、结果层级、flagged、categories、scores。按当前 API 整理最小片段，不展开提供方安装和属性大全。

术语：Moderation → 内容审核；flagged → 风险标记；categories → 分类判断；category scores → 分类评分；PII → 个人身份信息。

重点限制：来源两个提供方示例均混用 response / moderationResponse 和 this.result，重新整理局部引用。分类对象与评分可为空；评分不能当作跨模型通用概率或置信度；false 不是完整业务审核结论，不等同事实校验。

读取已保存原文、来源片段与版本 API，按用途 → 请求响应 → 调用示例 → 参数边界 → 提供方入口组织。新写片段注明已配置 Bean 和分段独立使用；正文与 translation.md 最终逐字节一致。工程建议明确标注。不添加来源没有的配图。
