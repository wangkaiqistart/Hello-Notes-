# 多模态精翻分析

来源：https://docs.spring.io/spring-ai/reference/api/multimodality.html；文档版本 2.0.2；核验日期 2026-10-25。正文约 563 个空白分隔词、2 个代码块、2 张图片，低于分块阈值，单篇完成精翻。

## 内容与风格

说明多模态输入与 Message / Media 的关系，通过水果图片分别展示 ChatModel 与 ChatClient 调用，最后给出七家提供方入口。面向熟悉 Java / Spring Boot 的开发者，使用项目 zh-CN / refined / technical 配置，中文简明自然，API 标识不翻译。

## 术语

Multimodality → 多模态；modality → 模态；Media → 媒体内容（保留类名）；MimeType → 媒体类型；Resource → Spring 资源对象；URI → 资源标识；fluent API → 链式 API。

## 准确性重点

- 模态指信息形式，不能把 MIME 类型等同于模型能力；Resource / URI 支持由具体适配器和模型决定。
- 来源笼统列出视频、音频等能力，译文不暗示所有型号都支持所有输入形式。
- 来源称 AssistantMessage 仅文本，但 2.0.2 Javadoc 明确实现 MediaContent 并有 getMedia()。应在版本说明中校正，不把旧限制当作当前规则。系统消息不要默认附媒体。
- 第一个示例定义局部变量却使用 this.imageResource / this.userMessage；修正为局部引用，保留其余非注释代码。
- 原图与已有提示词文章的消息类图哈希一致，复用已验收的中文 UML，不重画。水果照片保持来源字节，按 200px 展示，可点击大图。
- 保留开篇引语与响应示例，模型观察不作为确定事实；所有七家多模态入口保留。
