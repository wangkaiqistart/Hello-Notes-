---
title: Spring AI：多模态
description: 通过 UserMessage 和 Media 组合文本与图片，掌握 ChatModel、ChatClient 的多模态调用方式及模型支持边界。
sidebar:
  label: 多模态
  order: 8
---

**多模态**是模型综合理解和处理文字、图片、音频等不同形式信息的能力。例如，发送一张图片和一个问题，让模型结合图像内容回答。

> “凡是自然相互关联的事物，都应结合起来教授。”——约翰·阿摩司·夸美纽斯，《世界图解》，1658 年。

人的学习和经验往往同时包含视觉、听觉与文字。过去，机器学习通常为单一模态构建专用模型，例如语音转文字、文字转语音、目标检测和图像分类。多模态大语言模型则把多种输入结合起来理解，并生成回答。

GPT、Gemini、Claude，以及 Llama、LLaVA、BakLLaVA 等模型系列提供了不同程度的多模态能力。**具体支持图片、音频还是视频，取决于所选型号与提供方 API。**

## 文本与媒体如何组合

Spring AI 的消息 API 用统一结构表达多模态输入：

| 组成                     | 作用                                                         |
| ------------------------ | ------------------------------------------------------------ |
| `UserMessage` 的文本     | 表达问题、任务或指令；通过 `.text(...)` 设置。               |
| `UserMessage` 的媒体集合 | 携带一项或多项图片、音频等内容。                             |
| `Media`                  | 包装媒体类型和媒体数据。                                     |
| `MimeType`               | 声明数据格式，例如 `image/png`；不会让模型自动获得相应能力。 |
| `Resource` 或 `URI`      | 提供媒体数据或媒体地址；可用形式取决于具体模型与适配器。     |

支持媒体的消息实现 `MediaContent` 接口，通过 `getMedia()` 访问媒体集合。消息文本通过 `getText()` 获取；角色与消息结构见[提示词](/frameworks/spring-ai/core/prompts/)。

下图展示 `Message`、`MediaContent` 与各消息类型的关系。重点看 `UserMessage` 如何同时承载文字与媒体，而不是把图片地址拼进普通提示词。

[![Spring AI 消息 API 类图：UserMessage 与 AssistantMessage 支持 MediaContent，媒体内容由 Media 表达，消息角色由 MessageType 区分](/images/frameworks/spring-ai/spring-ai-message-api-zh.svg)](/images/frameworks/spring-ai/spring-ai-message-api-zh.svg)

类名和方法名保留 API 标识，图例使用中文；点击可查看大图。

## 输入与输出的边界

本文的常见路径是：**用户发送文字和图片，模型返回文字描述。** 不应默认把媒体附加到系统消息中。

:::note[版本说明]
来源页仍写着“`AssistantMessage` 只包含文本，媒体只适用于用户输入”。但 [2.0.2 的 `AssistantMessage` API](https://docs.spring.io/spring-ai/docs/2.0.2/api/org/springframework/ai/chat/messages/AssistantMessage.html) 已实现 `MediaContent`，并提供 `getMedia()`。是否能返回音频等媒体，还要看所用模型与适配器；不能将来源的旧说明当作当前通用限制。
:::

生成图片、语音等输出时，按提供方文档选择专用模型 API，或其支持的多模态聊天接口。下文的 `.content()` 只提取回答文本，不负责提取媒体数据。

## 示例：让模型描述图片

把测试图片保存为 `src/main/resources/multimodal.test.png`，让模型描述其中的物品。下图是示例使用的输入：水果篮、香蕉和苹果。

<a href="/images/frameworks/spring-ai/multimodal.test.png">
  <img
    src="/images/frameworks/spring-ai/multimodal.test.png"
    alt="多模态示例输入：灰绿色背景中的金属水果篮，篮内有香蕉和苹果"
    width="200"
  />
</a>

图片本身随请求发送，问题说明需要观察什么；点击可查看大图。

### 使用 ChatModel

假设已配置支持图片输入的 `chatModel`，先创建图片资源和用户消息，再调用模型：

```java
var imageResource = new ClassPathResource("/multimodal.test.png");

var userMessage = UserMessage.builder()
    .text("Explain what do you see in this picture?") // 文本问题
    .media(new Media(MimeTypeUtils.IMAGE_PNG, imageResource)) // 图片媒体
    .build();

ChatResponse response = chatModel.call(new Prompt(userMessage));
```

示例中的 `imageResource` 和 `userMessage` 都是局部变量。

### 使用 ChatClient

通过 [ChatClient](/frameworks/spring-ai/core/chat-client/) 链式 API，可以在同一条用户消息中设置文本与媒体：

```java
String response = ChatClient.create(chatModel).prompt()
		.user(u -> u.text("Explain what do you see on this picture?")
				    .media(MimeTypeUtils.IMAGE_PNG, new ClassPathResource("/multimodal.test.png")))
		.call()
		.content();
```

来源给出的示例回答如下，实际措辞和判断会因模型而异：

> 这是一张设计简洁的水果篮图片。篮子由金属制成，弯曲的金属丝形成开放结构，可以从不同角度看到水果。篮内两根黄色香蕉放在一个看起来像红苹果的水果上。香蕉皮上的褐色斑点表明它们可能稍微熟过头了。篮子上方有一个金属圆环，可能是便于提拿的把手。篮子放在平面上，背景颜色中性，衬托出篮内水果。

## 支持入口

来源页列出以下多模态聊天模型实现。选择你正在使用的一家查阅即可，不需要逐家学习。

| 提供方        | 文档入口                                                                                                                |
| ------------- | ----------------------------------------------------------------------------------------------------------------------- |
| Anthropic     | [Claude 多模态支持](https://docs.spring.io/spring-ai/reference/api/chat/anthropic-chat.html#_multi_modal_support)       |
| AWS           | [Bedrock Converse 多模态](https://docs.spring.io/spring-ai/reference/api/chat/bedrock-converse.html#_multimodal)        |
| Mistral AI    | [Pixtral 等模型](https://docs.spring.io/spring-ai/reference/api/chat/mistralai-chat.html#_multimodal)                   |
| Ollama        | [LLaVA、BakLLaVA、Llama 等模型](https://docs.spring.io/spring-ai/reference/api/chat/ollama-chat.html#_multimodal)       |
| OpenAI        | [GPT 多模态](https://docs.spring.io/spring-ai/reference/api/chat/openai-chat.html#_multimodal)                          |
| Google        | [Gemini 多模态](https://docs.spring.io/spring-ai/reference/api/chat/google-genai-chat.html#_multimodal)                 |
| Qxotic jinfer | [Gemma 4、LFM2.5-VL、Qwen 3.5 等模型](https://docs.spring.io/spring-ai/reference/api/chat/jinfer-chat.html#_multimodal) |

接入时确认具体型号支持哪些模态、允许哪些 MIME 类型、能否传入媒体 URL，以及大小和数量限制。相同 `Media` 写法不代表各提供方的能力和限制相同。

继续阅读[模型概览](/frameworks/spring-ai/models/)，区分聊天、Embedding 与其他专用模型。

来源：[Multimodality API](https://docs.spring.io/spring-ai/reference/api/multimodality.html)。文档版本：2.0.2；核验日期：2026-10-25。
