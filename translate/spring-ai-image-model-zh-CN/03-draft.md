---
title: Spring AI：图像模型
description: 理解 ImageModel 的请求与响应，掌握图片生成、运行时选项及 URL 和 Base64 返回值的处理方式。
sidebar:
  label: 图像模型
  order: 4
---

**图像模型**根据提示词生成图片，可用于插图、商品展示图和设计草稿等场景。Spring AI 通过 `ImageModel` 统一请求和响应结构，减少接入不同图像生成服务时的代码差异。

图片理解通常使用支持视觉输入的聊天模型，见[多模态](/frameworks/spring-ai/core/multimodality/)；本篇介绍生成图片的模型 API。图像编辑等扩展能力按提供方文档查询。

## 核心 API

`ImageModel` 建立在通用模型 API 之上：

```java
@FunctionalInterface
public interface ImageModel extends Model<ImagePrompt, ImageResponse> {

	ImageResponse call(ImagePrompt request);

}
```

请求与响应之间的关系是：`ImagePrompt → ImageModel → ImageResponse`。

| 类型 | 职责 |
| --- | --- |
| `ImagePrompt` | 封装图片描述消息及可选的 `ImageOptions`。 |
| `ImageMessage` | 表达一段描述及其影响图片的权重。权重可用性取决于模型，支持时可能允许正值或负值。 |
| `ImageResponse` | 整体响应，包含生成结果集合和响应元数据。 |
| `ImageGeneration` | 某一张图片的生成结果及其元数据。 |
| `Image` | 承载图片地址或 Base64 数据等输出字段。 |

`getResult()` 获取首个生成结果，`getResults()` 获取全部结果；需要多张图片时，应遍历结果集合。

## 最小调用

假设应用已配置并注入 `imageModel`：

```java
ImageResponse response = imageModel.call(
    new ImagePrompt("A watercolor illustration of a quiet mountain village.")
);

Image image = response.getResult().getOutput();
String imageUrl = image.getUrl();
String imageBase64 = image.getB64Json();
```

`imageUrl` 和 `imageBase64` 的取值与所选返回格式、模型及适配器有关，**不能假定两者同时有值**。应用应检查返回字段，再选择访问 URL 或解码 Base64；仅拿到地址不代表图片已保存到自己的存储中。

以上是正常返回图片时的用法片段；业务代码还需处理调用异常和空结果。字段定义见 [Image API](https://docs.spring.io/spring-ai/docs/2.0.2/api/org/springframework/ai/image/Image.html)。

## 生成选项

`ImageOptions` 定义常用选项，具体实现还可以扩展其他能力：

| 选项 | 作用 |
| --- | --- |
| `model` | 指定图像生成型号。 |
| `n` | 请求生成图片的数量。 |
| `width` / `height` | 请求图片宽高。 |
| `responseFormat` | 选择图片数据的返回形式。 |
| `style` | 指定风格；可用值与实际效果取决于模型。 |

表格中的字段以 [2.0.2 ImageOptions API](https://docs.spring.io/spring-ai/docs/2.0.2/api/org/springframework/ai/image/ImageOptions.html) 为准。质量等额外选项查看提供方专有类型；不要把统一字段理解成所有模型都支持任意数量、尺寸或格式。

通常在模型初始化时配置默认值，再通过 `ImagePrompt` 传入本次请求的选项。假设 `imageOptions` 已按提供方要求构建：

```java
ImagePrompt prompt = new ImagePrompt(
    "A watercolor illustration of a quiet mountain village.",
    imageOptions
);
ImageResponse response = imageModel.call(prompt);
```

两个示例分别展示默认配置与请求级配置，不应直接拼接为同一个方法。具体默认值与运行时选项如何合并，以所用实现为准。

## 提供方入口

来源页列出以下实现：

- [OpenAI 图像生成](https://docs.spring.io/spring-ai/reference/api/image/openai-image.html)
- [Stability AI 图像生成](https://docs.spring.io/spring-ai/reference/api/image/stabilityai-image.html)
- [Google GenAI 图像生成](https://docs.spring.io/spring-ai/reference/api/image/google-genai-image.html)

接入时查询对应版本的依赖、认证、支持型号、尺寸、数量、返回格式和专有选项。统一 API 便于复用调用结构，切换模型后仍需验证提示词效果与输出处理。

继续阅读[音频模型](/frameworks/spring-ai/models/audio-model/)，了解转写与语音生成。

来源：[Image Model API](https://docs.spring.io/spring-ai/reference/api/imageclient.html)，精选翻译，补充最小调用与返回值处理说明。文档版本：2.0.2；核验日期：2026-10-25。
