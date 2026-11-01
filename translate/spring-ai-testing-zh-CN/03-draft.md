---
title: Spring AI：评估测试
description: 使用 RelevancyEvaluator 和 FactCheckingEvaluator 检查 RAG 回答的相关性与上下文支持性，包含集成测试和自定义模板。
sidebar:
  label: 评估测试
  order: 1
---

测试 AI 应用时，除了检查请求是否成功，还需要评估生成内容，判断回答是否偏离问题、是否得到参考资料的支持。

一种做法是让模型评估模型的回答。评估模型应适合判断任务，可以与生成回答的模型不同。

:::tip[阅读路线]
先掌握 `EvaluationRequest` 的三个输入，再将 `RelevancyEvaluator` 接到现有 RAG 流程；有事实核查需求时，再看 `FactCheckingEvaluator`。本篇接在 [RAG](/frameworks/spring-ai/rag/retrieval-and-generation/) 与 [ETL 管道](/frameworks/spring-ai/rag/document-ingestion/) 之后，API 按 Spring AI 2.0.2 整理。
:::

## 一、评估接口与输入（重点掌握）

Spring AI 用 `Evaluator` 评估回答，核心方法如下：

```java
@FunctionalInterface
public interface Evaluator {
    EvaluationResponse evaluate(EvaluationRequest evaluationRequest);
}
```

`EvaluationRequest` 将问题、上下文和回答交给评估器。下面省略访问器等方法：

```java
public class EvaluationRequest {

    private final String userText;
    private final List<Document> dataList;
    private final String responseContent;

    public EvaluationRequest(String userText, List<Document> dataList, String responseContent) {
        this.userText = userText;
        this.dataList = dataList;
        this.responseContent = responseContent;
    }
}
```

| 字段              | 含义                                                                   |
| ----------------- | ---------------------------------------------------------------------- |
| `userText`        | 用户原始输入。                                                         |
| `dataList`        | 附加的上下文文档，例如 RAG 检索出的资料。2.0.2 使用 `List<Document>`。 |
| `responseContent` | 模型生成的回答文本。                                                   |

默认的 `Evaluator.doGetSupportingData()` 提取 `dataList` 中各个 `Document` 的文本，过滤空白内容，再用换行符拼接。评估时使用的资料来自这里；只有媒体、没有文本的文档不会提供文本依据。

`EvaluationResponse` 包含通过标记、分数、反馈和元数据。判断是否通过通常使用 `isPass()`，分数的含义取决于具体实现。

<a id="_relevancy_evaluator"></a>

## 二、RelevancyEvaluator：相关性评估（重点掌握）

`RelevancyEvaluator` 实现 `Evaluator`，结合**用户问题、模型回答、检索上下文**评估回答是否相关，并与给定资料一致，适合检查 RAG 流程的输出。

它将三个输入填入提示词，让评估模型回答 `YES` 或 `NO`。默认提示词如下，中文含义是“判断针对问题的回答是否与给定上下文一致；一致回答 YES，否则回答 NO”：

```text
Your task is to evaluate if the response for the query
is in line with the context information provided.

You have two options to answer. Either YES or NO.

Answer YES, if the response for the query
is in line with context information otherwise NO.

Query:
{query}

Response:
{response}

Context:
{context}

Answer:
```

2.0.2 的实现会去掉返回值首尾的空白，只在结果忽略大小写后**严格等于 `yes`** 时通过。通过时 `getScore()` 为 `1`，否则为 `0`；这不是连续的质量评分，也不是置信度。

:::note[自定义提示词]
可以通过构建器的 `.promptTemplate()` 传入自己的 `PromptTemplate`，见[自定义模板](#_custom_template)。仍需让模型只输出 `YES` 或 `NO`；额外解释会导致严格匹配失败。
:::

<a id="_usage_in_integration_tests"></a>

## 三、接入 RAG 集成测试

下面先用 [`RetrievalAugmentationAdvisor`](/frameworks/spring-ai/rag/retrieval-and-generation/#retrievalaugmentationadvisor) 执行检索与生成，再把实际检索到的文档和回答交给评估器。

示例假定已有配置完成的 `chatModel` 和包含测试资料的 `pgVectorStore`；问题询问的是测试资料中 Anacletus 与 Birba 的冒险地点。`ChatClient` 的调用方式见 [ChatClient API](/frameworks/spring-ai/core/chat-client/)。

```java
@Test
void evaluateRelevancy() {
    String question = "Where does the adventure of Anacletus and Birba take place?";

    RetrievalAugmentationAdvisor ragAdvisor = RetrievalAugmentationAdvisor.builder()
        .documentRetriever(VectorStoreDocumentRetriever.builder()
            .vectorStore(pgVectorStore)
            .build())
        .build();

    ChatResponse chatResponse = ChatClient.builder(chatModel).build()
        .prompt(question)
        .advisors(ragAdvisor)
        .call()
        .chatResponse();

    EvaluationRequest evaluationRequest = new EvaluationRequest(
        // 用户原始问题
        question,
        // 此次 RAG 调用实际检索到的上下文
        chatResponse.getMetadata().get(RetrievalAugmentationAdvisor.DOCUMENT_CONTEXT),
        // 模型生成的回答
        chatResponse.getResult().getOutput().getText()
    );

    RelevancyEvaluator evaluator = new RelevancyEvaluator(ChatClient.builder(chatModel));
    EvaluationResponse evaluationResponse = evaluator.evaluate(evaluationRequest);

    assertThat(evaluationResponse.isPass()).isTrue();
}
```

`RetrievalAugmentationAdvisor.DOCUMENT_CONTEXT` 用于从响应元数据取出本次检索到的文档。测试应同时确认检索结果非空；空上下文下的一次通过不能说明 RAG 流程有效。

示例复用生成模型进行评估。需要不同的评估模型时，将它传给评估器使用的 `ChatClient.builder(...)`，保留生成端的模型配置。

更多用例可参考同版本的 [QuestionAnswerAdvisor 集成测试](https://github.com/spring-projects/spring-ai/blob/v2.0.2/spring-ai-integration-tests/src/test/java/org/springframework/ai/integration/tests/client/advisor/QuestionAnswerAdvisorIT.java)和 [RetrievalAugmentationAdvisor 集成测试](https://github.com/spring-projects/spring-ai/blob/v2.0.2/spring-ai-integration-tests/src/test/java/org/springframework/ai/integration/tests/client/advisor/RetrievalAugmentationAdvisorIT.java)。

<a id="_custom_template"></a>

### 自定义模板

`RelevancyEvaluator` 默认使用 `PromptTemplate`，并通过基于 StringTemplate 的 `StTemplateRenderer` 渲染。可以为 `PromptTemplate` 配置其他 `TemplateRenderer` 实现，模板和占位符的基本用法见 [PromptTemplate](/frameworks/spring-ai/core/prompts/#prompttemplate将模板转换为提示词)。

模板应保留三个变量：

| 占位符       | 对应内容     |
| ------------ | ------------ |
| `{query}`    | 用户问题。   |
| `{response}` | 模型回答。   |
| `{context}`  | 上下文资料。 |

例如，把评估规则写得更明确，并继续要求只返回 `YES` 或 `NO`：

```java
PromptTemplate template = new PromptTemplate("""
    Evaluate whether the response answers the query and is supported by the context.
    Return only YES or NO, without explanation.

    Query: {query}
    Response: {response}
    Context: {context}
    ""
);

RelevancyEvaluator evaluator = RelevancyEvaluator.builder()
    .chatClientBuilder(ChatClient.builder(evaluationModel))
    .promptTemplate(template)
    .build();
```

这里的 `evaluationModel` 是已配置好的评估模型。自定义规则会改变判断标准，应配合固定题集检查结果。

<a id="_factcheckingevaluator"></a>

## 四、FactCheckingEvaluator：事实核查（按需深入）

`FactCheckingEvaluator` 也是 `Evaluator` 的实现，用于检查回答中的陈述（claim）是否得到参考文档（document）的逻辑支持，帮助发现缺乏依据的生成内容。

评估器把文档和待核查陈述一起交给模型。可以使用专门执行这类任务、规模较小的模型，例如 Bespoke 的 MiniCheck；它也可以通过 Ollama 使用。与使用 GPT-4 等大型通用模型相比，这类模型可用于降低核查成本，实际效果仍需用自己的资料与题集验证。

| 评估器                  | 关注的问题                                 |
| ----------------------- | ------------------------------------------ |
| `RelevancyEvaluator`    | 针对用户问题的回答，是否与给定上下文一致？ |
| `FactCheckingEvaluator` | 参考文档是否支持这段待核查陈述？           |

两者都依赖所给资料和评估模型的判断；通过评估不代表结论在外部世界中一定正确，也不保证回答完整。

<a id="_usage"></a>

### 使用方式与提示词

2.0.2 使用构建器创建通用评估器，并传入评估端的 `ChatClient.Builder`：

```java
FactCheckingEvaluator evaluator = FactCheckingEvaluator
    .builder(ChatClient.builder(evaluationModel))
    .build();
```

通用模式的默认提示词包含明确的核查指令与输出约束：

```text
Evaluate whether or not the following claim is supported by the provided document.
Respond with "yes" if the claim is supported, or "no" if it is not.

Document:
{document}

Claim:
{claim}
```

使用 Bespoke MiniCheck 时，通过 `FactCheckingEvaluator.forBespokeMinicheck(...)` 选择专用的文档／陈述模板，其结构如下：

```text
Document: {document}
Claim: {claim}
```

`{document}` 是 `dataList` 中文档文本的拼接结果，`{claim}` 是待评估的 `responseContent`。`FactCheckingEvaluator` 不会把 `userText` 当作核查资料。

该实现同样只有在输出去掉首尾空白、忽略大小写后严格等于 `yes` 时通过。应读取 `isPass()` 判断结果；当前实现的 `getScore()` 默认是 `0`，即使核查通过也不会变成 `1`。

<a id="_example"></a>

### 示例：Ollama 与 Bespoke MiniCheck

下面的测试用“地球是太阳系第三颗行星”作为参考资料，核查“地球是第四颗行星”这一错误陈述，预期评估不通过。

先启动 Ollama，并准备 `bespoke-minicheck` 模型。`numPredict(2)` 延续原示例的短输出设置，`temperature(0.0d)` 减少采样随机性；这些设置不保证评估完全确定。

```java
@Test
void testFactChecking() {
    OllamaApi ollamaApi = OllamaApi.builder()
        .baseUrl("http://localhost:11434")
        .build();

    ChatModel chatModel = OllamaChatModel.builder()
        .ollamaApi(ollamaApi)
        .options(OllamaChatOptions.builder()
            .model("bespoke-minicheck")
            .numPredict(2)
            .temperature(0.0d)
            .build())
        .build();

    FactCheckingEvaluator evaluator = FactCheckingEvaluator
        .forBespokeMinicheck(ChatClient.builder(chatModel));

    String context = "The Earth is the third planet from the Sun and the only astronomical object known to harbor life.";
    String claim = "The Earth is the fourth planet from the Sun.";

    EvaluationRequest request = new EvaluationRequest(
        "",
        List.of(new Document(context)),
        claim
    );

    EvaluationResponse response = evaluator.evaluate(request);

    assertFalse(response.isPass(), "The claim should not be supported by the context");
}
```

:::caution[上下文传参]
参考资料必须放入 `dataList`。若写成 `new EvaluationRequest(context, Collections.emptyList(), claim)`，`context` 只会存进 `userText`，事实核查时得到的参考文档仍为空。
:::

## 五、放进回归测试时关注什么

先为现有 RAG 应用固定一组问题、资料和预期判断，记录实际检索文档、生成回答、模型版本与评估结果。修改提示词、模型或检索参数后，重复运行同一题集，才能比较变化。

重点保留以下几类用例：回答相关且有依据、答非所问、回答与资料矛盾、资料不足、检索为空。对于关键事实和业务结果，还应加入人工核对或明确断言，不能仅凭模型给出的 `YES` 验收。

本篇示例会真实调用生成或评估模型；运行前需准备模型访问、依赖和测试资料。评估会增加调用次数、耗时与费用。

---

来源：[Evaluation Testing](https://docs.spring.io/spring-ai/reference/api/testing.html#_relevancy_evaluator)，按 Spring AI 2.0.2 API 整理。
