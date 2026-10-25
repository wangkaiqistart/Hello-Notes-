# 翻译上下文

将音频模型整理为简明中文技术文章，目标为知识库“Spring AI → 模型”小章节。采用 zh-CN / refined / technical，保留 API 标识与必要方法，不逐家翻译安装配置。

内容范围：合并入口、STT 与 TTS 共享 API，覆盖输入输出、常用方法、完整响应、流式语音、通用与专有配置、跨提供方、InputStream 桥接及背压边界。保留必要片段，省略重复 Service / Controller / Profiles 全量代码和提供方配置。

术语：Transcription → 转写；Speech-to-Text → 语音转文字；Text-to-Speech → 文字转语音；backpressure → 背压；chunk → 数据块。

重点限制：不能把 Flux<byte[]> 当作每块都可独立播放的文件；MIME 与实际编码一致；有流式接口不代表任意适配器支持流式；InputStream 桥接需显式关闭并取消，传输背压不等于提供方停止合成或计费。

读取已保存原文、来源片段与版本 API，按用途 → 请求响应 → 调用示例 → 参数边界 → 提供方入口组织。新写片段注明已配置 Bean 和分段独立使用；正文与 translation.md 最终逐字节一致。工程建议明确标注。不添加来源没有的配图。
