# 音频模型审校

## 准确性

对照 Audio / Transcription / Speech 三篇及 2.0.2 Javadoc，确认 TranscriptionModel 的两类 transcribe、TextToSpeechModel 的 call / stream / getOptions、Prompt 构造器与返回类型。五段代码按来源方法精简，保留完整响应与元数据的获取方式。

音频返回 byte[] 而不是文本，不默认任何 byte[] 都是 MP3；HTTP Content-Type 与扩展名必须和编码一致。流式块不必独立可播放。桥接 InputStream 时保留限流、关闭取消与 HTTP/2 传输背压的边界，不承诺服务端停止合成或计费。

## 范围与中文

合并三页，省略重复的多 Service、Controller、配置清单与按类名组装 provider Map 的长示例，保留多 Bean / Profiles 的使用说明和五个提供方入口。每段示例独立使用且依赖应用配置，不宣称为完整项目。词语统一为转写、合成、音色、背压。
