# Embedding 模型精选翻译分析

来源：Embeddings Model API，文档版本 2.0.2，核验日期 2026-10-25。完整英文正文、HTML 与来源清单保留在本次翻译目录及上层 source Markdown 中。正文低于 4000 词，采用单篇精翻审校。

## 授权范围

用户要求模型内容精简成小章节，非必要内容保留官网查询。精选向量含义、EmbeddingModel 核心方法、请求与响应、维度与模型一致性。省略完整接口源码与 UML、提供方逐项配置。示例使用 float[] 与 vector.length，避免照抄来源数组.size()错误；dimensions() 默认可能调用远端，此事实按 2.0.2 Javadoc注明。模型一致性与更换模型后的索引处理为工程提示，不伪装来源逐句翻译。

## 术语与风格

使用项目 zh-CN / refined / technical 配置。Model API → 模型 API；Chat Model → 聊天模型；Embedding → 嵌入 / 向量表示；Streaming → 流式；Provider → 提供方；Prompt → 提示词；fluent API → 链式 API。保留所有类名、方法名及配置键。

## 准确性

统一 API 降低迁移成本，不保证能力、结果和参数完全相同；不能推导所有模型类型支持流式。模型、适配器与提供方的概念需要区分。工程建议与来源摘要分别标注，不重复其他已译文章。示例为补充用法，按来源与对应版本 API 复核，不宣称编译或调用成功。
