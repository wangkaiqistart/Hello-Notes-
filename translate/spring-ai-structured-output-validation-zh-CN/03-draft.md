## Schema 校验与自动纠正

默认 `.entity(...)` 用提示词要求模型遵守结构，不能强制它照做。额外字段、必需字段缺失或 JSON 外的说明文字都可能造成格式问题；启用 `validateSchema()` 后，框架会检查响应并反馈错误，要求模型重新生成。

```java
ActorsFilms films = chatClient.prompt()
    .user("Generate the filmography for a random actor.")
    .call()
    .entity(ActorsFilms.class, spec -> spec.validateSchema());
```

### 纠正循环如何执行

1. 模型返回完整响应。
2. Spring AI 根据目标类型的 JSON Schema 校验输出。
3. 校验通过后，将 JSON 转换为目标 Java 对象。
4. 如果失败，将具体错误补充到用户提示词，再请求模型，默认最多尝试 3 次。

错误包含具体原因，例如缺少必需字段 `actor`，或要求 `array` 却返回 `string`。模型下一轮能看到问题所在，重试会带上纠正依据。

下图中，橙色箭头表示请求和结果的主路径，红色回路表示校验失败后把错误加入下一轮请求；通过校验后才进入右侧类型转换器。

[![Schema 校验与自动纠正：模型响应通过校验后转换为对象，失败时将错误反馈到下一轮请求](/images/frameworks/spring-ai/structured-output-self-correction-zh.svg)](/images/frameworks/spring-ai/structured-output-self-correction-zh.svg)

重点看红色错误回路与右侧判断节点；点击可查看大图。

这套机制由 `StructuredOutputValidationAdvisor` 实现。调用 `validateSchema()` 会自动注册它，无需手动装配。它是[递归 Advisor](/frameworks/spring-ai/core/advisors/#structuredoutputvalidationadvisor结构校验循环)，可重复执行下游链。

**校验需要完整响应，不支持流式调用。**

### 定制 StructuredOutputValidationAdvisor

默认使用 Spring AI 的 `JsonMapper`。需要调整尝试次数、提供现有 Schema 或使用其他映射器时，可以自己构建 Advisor 并注册到 `ChatClient`；显式注册的实例替换自动注册实例：

```java
var validationAdvisor = StructuredOutputValidationAdvisor.builder()
    .outputType(ActorsFilms.class)
    .maxRepeatAttempts(5)
    .build();

ChatClient chatClient = ChatClient.builder(chatModel)
    .defaultAdvisors(validationAdvisor)
    .build();
```

也可以使用已有 Schema 字符串：

```java
var validationAdvisor = StructuredOutputValidationAdvisor.builder()
    .outputJsonSchema(myConverter.getJsonSchema())
    .build();
```

**`outputType` 与 `outputJsonSchema` 互斥，只能设置其中一种。** 前者从目标 Java 类型生成 Schema，后者直接使用传入的字符串。

主要行为：

- 使用 JSON Schema `DRAFT_2020_12` 校验响应。
- 校验失败时，将错误消息加入下一轮用户提示词。
- 在尝试次数限制内重复请求；默认最多尝试 3 次。
- 累计各轮 Token 用量，最终 `ChatResponse` 报告整个流程的用量，详见[多步流程的累计用量](/frameworks/spring-ai/core/chat-response-metadata/#多步流程的累计用量)。
- 可以通过构建器的 `jsonMapper(...)` 指定自定义 `JsonMapper`。

### 与提供方原生约束组合

`validateSchema()` 在响应端检查结果并触发纠正，`useProviderStructuredOutput()` 在请求端向提供方传入 Schema 约束，二者可以同时启用：

```java
ActorsFilms films = chatClient.prompt()
    .user("Generate the filmography for a random actor.")
    .call()
    .entity(ActorsFilms.class, spec -> spec
        .useProviderStructuredOutput()
        .validateSchema());
```

这对原生支持不完整的模型尤其有用，例如部分 Ollama 推理模型可能返回普通推理文本。具体情况见[已知限制](#已知限制)。两项配置都不能替代应用的业务校验。
