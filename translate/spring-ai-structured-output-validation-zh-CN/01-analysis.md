# 内容分析

## 内容与风格

Spring AI 2.0.2 的 Schema Validation & Self-Correction，面向熟悉 Java / Spring Boot 的开发者。使用项目简体中文、精翻、简明技术文档风格。英文正文不足 4000 词，按单篇完成。

## 术语

- Schema Validation → Schema 校验
- Self-Correction → 自动纠正
- retry attempt → 首次调用后的重试
- StructuredOutputValidationAdvisor / JsonMapper / EntityParamSpec → 保留 API 标识
- request-side constraint / response-side validation → 请求端约束 / 响应端校验

## 难点

- 文档将“最多 3 次尝试”与“3 次重试”混用，需要核对源码。
- “额外字段或缺失字段一定导致解析抛错”不能替代 Schema 校验的实际语义。
- 手动注册是否替换自动 Advisor、空 Schema 的 validateSchema() 行为、重试耗尽后的处理，均需以 2.0.2 实现为准。
- 4 段来源代码中两段与主文完全重复；合并时复用，原始单篇定稿仍保留全部代码。
- 图片保留手绘布局、蓝色虚线、橙色调用箭头及红色失败回路，仅中文化说明。
