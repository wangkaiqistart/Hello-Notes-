# 审核模型精翻分析

来源：https://docs.spring.io/spring-ai/reference/api/moderation.html；版本 2.0.2；核验日期 2026-10-25。

## 内容与范围

审核入口 23 词；补读 OpenAI 1018 词和 Mistral 688 词的相关结果解释及对应 API，均无图。 低于分块阈值，主 agent 完成分析、初稿、审校与修订。沿用用户既定模型小章节范围：核心概念、常用 API 与必要示例，提供方详情保留官网链接。

翻译用途和提供方入口，补充共享 ModerationModel / Prompt / Response、结果层级、flagged、categories、scores。按当前 API 整理最小片段，不展开提供方安装和属性大全。

## 术语与风格

项目 EXTEND.md：zh-CN、refined、technical；面向 Java / Spring Boot 开发者。Moderation → 内容审核；flagged → 风险标记；categories → 分类判断；category scores → 分类评分；PII → 个人身份信息。 代码、类名和路径保持准确，中文直接解释职责与边界，避免翻译过程旁白。

## 核验重点

来源两个提供方示例均混用 response / moderationResponse 和 this.result，重新整理局部引用。分类对象与评分可为空；评分不能当作跨模型通用概率或置信度；false 不是完整业务审核结论，不等同事实校验。

正文无来源配图，不额外生成装饰图。示例根据来源与 2.0.2 Javadoc 整理，不冒充原文逐字代码，不执行真实模型调用。
