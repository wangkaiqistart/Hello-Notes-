---
title: Spring AI：审核模型
description: 理解 ModerationModel 的内容风险分类、结果层级与评分，掌握文本审核调用及其业务边界。
sidebar:
  label: 审核模型
  order: 6
---

**内容审核（Moderation）**用于识别文本中潜在的不当或风险内容，例如仇恨、骚扰、暴力、自伤或性相关内容。模型返回风险标记、分类判断与评分，应用再据此决定放行、拒绝或转人工处理。

审核结果用于内容风险分类，**不用于证明回答真实、业务合法或资料准确**。来源总览只列出接入入口，本篇结合提供方文档和共享 API 补充核心用法。

## 核心 API 与结果层级

`ModerationModel` 通过 `call(ModerationPrompt)` 返回 `ModerationResponse`，延续 Spring AI 的统一模型调用结构。

- `ModerationPrompt`：待审核文本及可选审核参数。
- `ModerationResponse`：整体响应及元数据。
- `response.getResult().getOutput()`：取得 `Moderation` 输出。
- `Moderation.getResults()`：取得实际的 `ModerationResult` 列表。

这里有两层结果：外层是 Spring AI 的模型响应结果，内层是审核服务返回的各项分类结果。不能把二者混为一个列表。

## 最小调用

假设应用已配置并注入 `moderationModel`：

```java
ModerationResponse response = moderationModel.call(
    new ModerationPrompt("Text to be moderated")
);
Moderation moderation = response.getResult().getOutput();
```

遍历本次审核的全部结果：

```java
for (ModerationResult result : moderation.getResults()) {
    boolean flagged = result.isFlagged();
    Categories categories = result.getCategories();
    CategoryScores scores = result.getCategoryScores();

    // 根据风险标记、可用分类和业务策略决定后续处理。
}
```

上述片段展示正常响应的读取方式。业务代码还需处理请求异常、空结果，以及缺失的分类与评分；`getCategories()`、`getCategoryScores()` 在当前 API 中允许返回 `null`。

来源示例存在 `response` / `moderationResponse` 混用及局部变量被写成 `this.result` 的问题，本文统一使用局部变量。

## 三类结果分别表示什么

| 字段 | 含义与使用方式 |
| --- | --- |
| `flagged` | 提供方对本项内容的整体风险标记；`true` 表示内容被标记。 |
| `categories` | 各风险类别的判断结果，可帮助解释触发原因。 |
| `categoryScores` | 各类别的评分，适合辅助分流和阈值评估。 |

常见分类包括仇恨、骚扰、暴力、自伤、性相关内容及若干细分类。Mistral 的文档还展示法律、金融、个人身份信息（PII）等分类；不要假定每个提供方都支持同一组类别，也不要默认这些扩展类别一定表示内容违法。

**分类评分不能直接当作跨模型通用的风险概率。** 分值范围、阈值、支持类别与标记规则应结合提供方定义理解；更换模型后需要重新评估阈值。

## 在应用中如何使用

以下是应用侧的工程判断，不是接口自动提供的流程：

1. 需要时在模型调用前审核用户输入，或在完整回答生成后审核输出。
2. 根据风险类别和产品规则决定处理方式，不必把所有类别都视为同一等级。
3. 为请求失败、缺失结果和边界分数明确降级或人工处理策略。

`flagged = false` 仅代表该次审核未被提供方标记，不能替代业务校验。单次文本审核也不会自动检查后续流式输出的每一个片段；需要审核完整答案时，应在展示策略中考虑这一点。

## 提供方入口

Spring AI 的来源页列出：

- [OpenAI Moderation](https://docs.spring.io/spring-ai/reference/api/moderation/openai-moderation.html)
- [Mistral AI Moderation](https://docs.spring.io/spring-ai/reference/api/moderation/mistral-ai-moderation.html)

具体依赖、认证、支持型号、请求选项、分类与评分定义，接入时查询对应提供方文档。共享 API 便于复用调用代码，审核政策与阈值仍由应用明确。

回到[模型概览](/frameworks/spring-ai/models/)，按任务选择需要深入的模型类型。

来源：[Moderation Models](https://docs.spring.io/spring-ai/reference/api/moderation.html)及上述提供方文档，精选翻译与 API 整理；工程流程单独标明。版本：2.0.2；核验日期：2026-10-25。
