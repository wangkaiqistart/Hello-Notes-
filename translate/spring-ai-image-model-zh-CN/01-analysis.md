# 图像模型精翻分析

来源：https://docs.spring.io/spring-ai/reference/api/imageclient.html；版本 2.0.2；核验日期 2026-10-25。

## 内容与范围

586 词、6 段接口/类结构示意，无图片。 低于分块阈值，主 agent 完成分析、初稿、审校与修订。沿用用户既定模型小章节范围：核心概念、常用 API 与必要示例，提供方详情保留官网链接。

完整覆盖 ImageModel、ImagePrompt、ImageMessage、ImageOptions、ImageResponse 与 ImageGeneration 的核心职责，保留提供方入口。用两段真实调用片段替代重复类定义。

## 术语与风格

项目 EXTEND.md：zh-CN、refined、technical；面向 Java / Spring Boot 开发者。Image Model → 图像模型；Image Generation → 图像生成；weight → 权重；response format → 返回格式。 代码、类名和路径保持准确，中文直接解释职责与边界，避免翻译过程旁白。

## 核验重点

Image.getUrl / getB64Json 都可能为 null，按返回格式处理；提示词权重和尺寸不是所有型号都支持；2.0.2 ImageOptions 已有 getStyle，不沿用旧页只把 style 视为 OpenAI 特有的绝对表述。

正文无来源配图，不额外生成装饰图。示例根据来源与 2.0.2 Javadoc 整理，不冒充原文逐字代码，不执行真实模型调用。
