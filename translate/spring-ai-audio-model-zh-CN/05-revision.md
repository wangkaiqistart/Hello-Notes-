---
title: Spring AI：音频模型
description: 掌握语音转文字与文字转语音的共享接口、请求响应、流式语音和跨提供方配置边界。
sidebar:
  label: 音频模型
  order: 5
---

Spring AI 提供两类专用音频 API：**语音转文字（Speech-to-Text，STT）**与**文字转语音（Text-to-Speech，TTS）**。本篇合并音频总览、转写与语音合成章节，保留核心接口和常见用法。

| 任务 | 输入与输出 |
| --- | --- |
| 语音转文字 | 音频资源 → 转写文本，例如会议录音转文字。 |
| 文字转语音 | 文本 → 音频字节，例如朗读助手回答。 |

让聊天模型理解音频并回答问题属于[多模态交互](/frameworks/spring-ai/core/multimodality/)，应根据任务选择接口，确认具体模型与适配器的支持。

## 语音转文字

`TranscriptionModel` 提供统一转写入口，完整调用为 `AudioTranscriptionPrompt → AudioTranscriptionResponse`。

- `AudioTranscriptionPrompt`：输入音频 `Resource` 与可选 `AudioTranscriptionOptions`。
- `AudioTranscriptionResponse`：转写结果和元数据。
- `transcribe(Resource)`：便捷方法，直接返回转写文本。
- `transcribe(Resource, options)`：带选项的便捷方法。

假设应用已注入 `transcriptionModel`，音频文件位于实际可访问的路径：

```java
Resource audioFile = new FileSystemResource("/path/to/audio.mp3");
String text = transcriptionModel.transcribe(audioFile);
```

需要完整响应或请求选项时，显式构造提示对象。这里的 `options` 是已配置好的 `AudioTranscriptionOptions`：

```java
AudioTranscriptionPrompt prompt = new AudioTranscriptionPrompt(audioFile, options);
AudioTranscriptionResponse response = transcriptionModel.call(prompt);
String text = response.getResult().getOutput();
AudioTranscriptionResponseMetadata metadata = response.getMetadata();
```

不同提供方的语言设置、时间戳、返回格式与输入限制可能不同。业务服务依赖 `TranscriptionModel`，再由 Spring 配置选择实现；需要专有能力时使用对应选项类型。

## 文字转语音

`TextToSpeechModel` 提供同步合成，并继承 `StreamingTextToSpeechModel`。请求与响应为 `TextToSpeechPrompt → TextToSpeechResponse`。

| 方法 | 返回值与用途 |
| --- | --- |
| `call(String)` | 返回完整音频 `byte[]`，使用模型默认选项。 |
| `call(TextToSpeechPrompt)` | 返回包含音频及元数据的完整响应。 |
| `getOptions()` | 获取模型默认选项。 |
| `stream(String)` | 返回音频字节流 `Flux<byte[]>`。 |
| `stream(TextToSpeechPrompt)` | 返回带元数据的响应流。 |

假设已注入 `textToSpeechModel`，最简单的合成调用为：

```java
byte[] audioBytes = textToSpeechModel.call("Hello, this is a text-to-speech example.");
```

需要请求级选项和元数据时，假设 `options` 为已配置的 `TextToSpeechOptions`：

```java
TextToSpeechPrompt prompt = new TextToSpeechPrompt(
    "Hello, this is a text-to-speech example.", options
);
TextToSpeechResponse response = textToSpeechModel.call(prompt);
byte[] audioBytes = response.getResult().getOutput();
TextToSpeechResponseMetadata metadata = response.getMetadata();
```

`TextToSpeechOptions` 抽象了模型、音色、格式和语速等字段。字段相同不代表音色名称、格式标识或语速范围也通用；OpenAI、ElevenLabs 等实现仍有专有选项。

## 流式语音

在支持流式的实现上，可以边接收边处理音频：

```java
Flux<byte[]> audioChunks = textToSpeechModel.stream("Read this sentence aloud.");
```

流中的元素是按顺序到达的音频数据块。**单个数据块通常不是可独立播放的完整文件。** 接收端需要按实际编码持续消费；提供流式接口也不代表所有实现与型号都支持相同的流式能力。

通过 HTTP 返回音频时，响应的 `Content-Type` 和文件扩展名应匹配实际格式，例如确认返回 MP3 后才使用 `audio/mpeg` 与 `.mp3`。返回 `Flux<byte[]>` 本身不会自动提供浏览器所需的播放和封装能力。

### 对接阻塞 InputStream

如果播放器或存储 API 只接收 `InputStream`，需要将响应流桥接为阻塞输入流。来源强调两点：

1. 按消费速度请求数据，限制客户端缓冲。
2. 输入流提前关闭时，取消底层订阅并释放连接。

直接使用 `Flux.toIterable()` 的迭代器不提供取消入口。来源给出通过 `BaseSubscriber` 控制请求和关闭时取消的参考思路，完整实现位于 `OpenAiAudioSpeechModelIT` 中的 `FluxInputStream`。

对于采用 HTTP/2 的实现，读取变慢可能在传输窗口耗尽后形成背压；**暂停传输不保证服务端停止合成或停止计费**。这些行为取决于提供方，客户端桥接无法单方面保证。

## 选择提供方与组织业务代码

业务服务优先依赖 `TranscriptionModel` 或 `TextToSpeechModel` 接口，由 Spring 配置决定实际实现。同一应用需要多个模型时，显式选择对应 Bean；也可通过 Spring Profiles 切换接入配置。

尽量使用通用选项，确需专有功能时再引入提供方类型。切换服务后，检查音频格式、音色、语速、元数据与流式行为，尤其不要假定不同提供方的元数据完全一致。

上述示例分别展示用法，需应用提供对应 Bean、依赖和文件；并非一个可直接拼接运行的完整项目。

## 提供方入口

- 语音转写：[OpenAI](https://docs.spring.io/spring-ai/reference/api/audio/transcriptions/openai-transcriptions.html)、[Qxotic jinfer（JVM 内本地推理）](https://docs.spring.io/spring-ai/reference/api/audio/transcriptions/jinfer-transcriptions.html)。
- 语音合成：[OpenAI](https://docs.spring.io/spring-ai/reference/api/audio/speech/openai-speech.html)、[ElevenLabs](https://docs.spring.io/spring-ai/reference/api/audio/speech/elevenlabs-speech.html)、[Qxotic jinfer（JVM 内本地推理）](https://docs.spring.io/spring-ai/reference/api/audio/speech/jinfer-speech.html)。

接入时查阅依赖、认证、输入长度或文件大小限制、支持的格式和完整参数。共享 API 可减少业务代码改动，具体能力仍以选定实现为准。

继续阅读[审核模型](/frameworks/spring-ai/models/moderation-model/)，了解内容风险分类。

来源：[Audio Models](https://docs.spring.io/spring-ai/reference/api/audio.html)、[Transcription API](https://docs.spring.io/spring-ai/reference/api/audio/transcriptions.html)、[Text-To-Speech API](https://docs.spring.io/spring-ai/reference/api/audio/speech.html)，合并精简翻译。文档版本：2.0.2；核验日期：2026-10-25。
