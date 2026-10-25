# 音频模型精翻分析

来源：https://docs.spring.io/spring-ai/reference/api/audio.html；版本 2.0.2；核验日期 2026-10-25。

## 内容与范围

音频入口 23 词；转写约 355 词、4 段代码；TTS 约 1210 词、12 段代码；均无图。 低于分块阈值，主 agent 完成分析、初稿、审校与修订。沿用用户既定模型小章节范围：核心概念、常用 API 与必要示例，提供方详情保留官网链接。

合并入口、STT 与 TTS 共享 API，覆盖输入输出、常用方法、完整响应、流式语音、通用与专有配置、跨提供方、InputStream 桥接及背压边界。保留必要片段，省略重复 Service / Controller / Profiles 全量代码和提供方配置。

## 术语与风格

项目 EXTEND.md：zh-CN、refined、technical；面向 Java / Spring Boot 开发者。Transcription → 转写；Speech-to-Text → 语音转文字；Text-to-Speech → 文字转语音；backpressure → 背压；chunk → 数据块。 代码、类名和路径保持准确，中文直接解释职责与边界，避免翻译过程旁白。

## 核验重点

不能把 Flux<byte[]> 当作每块都可独立播放的文件；MIME 与实际编码一致；有流式接口不代表任意适配器支持流式；InputStream 桥接需显式关闭并取消，传输背压不等于提供方停止合成或计费。

正文无来源配图，不额外生成装饰图。示例根据来源与 2.0.2 Javadoc 整理，不冒充原文逐字代码，不执行真实模型调用。
