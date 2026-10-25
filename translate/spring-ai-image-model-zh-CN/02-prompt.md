# 翻译上下文

将图像模型整理为简明中文技术文章，目标为知识库“Spring AI → 模型”小章节。采用 zh-CN / refined / technical，保留 API 标识与必要方法，不逐家翻译安装配置。

内容范围：完整覆盖 ImageModel、ImagePrompt、ImageMessage、ImageOptions、ImageResponse 与 ImageGeneration 的核心职责，保留提供方入口。用两段真实调用片段替代重复类定义。

术语：Image Model → 图像模型；Image Generation → 图像生成；weight → 权重；response format → 返回格式。

重点限制：Image.getUrl / getB64Json 都可能为 null，按返回格式处理；提示词权重和尺寸不是所有型号都支持；2.0.2 ImageOptions 已有 getStyle，不沿用旧页只把 style 视为 OpenAI 特有的绝对表述。

读取已保存原文、来源片段与版本 API，按用途 → 请求响应 → 调用示例 → 参数边界 → 提供方入口组织。新写片段注明已配置 Bean 和分段独立使用；正文与 translation.md 最终逐字节一致。工程建议明确标注。不添加来源没有的配图。
