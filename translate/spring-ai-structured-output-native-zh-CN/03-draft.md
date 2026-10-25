## 提供方原生结构化输出

默认 `.entity(...)` 将格式要求写进提示词。启用 `useProviderStructuredOutput()` 后，Schema 作为 API 字段传给提供方，由提供方在模型运行时约束输出结构。

```java
ActorsFilms films = chatClient.prompt()
    .user("Generate the filmography for a random actor.")
    .call()
    .entity(ActorsFilms.class, spec -> spec.useProviderStructuredOutput());
```

请求会发生三项变化：

- 系统提示词不再附带 JSON 格式说明，减少提示词中的格式指令与相应 Token。
- Schema 通过提供方 API 的专用字段传递。
- 提供方按其支持的 Schema 能力约束输出，提高格式可靠性，并可在内部优化生成过程。

### 能力检测与默认回退

Spring AI 检查模型的聊天选项是否实现 `StructuredOutputChatOptions`。如果没有实现，这个开关会被静默忽略，回退到默认的提示词驱动方式。

原生能力默认关闭，原因是兼容性：不同模型和提供方的支持范围差异较大，旧模型可能拒绝相应请求。需要更强的 API 约束时再开启，并用实际模型版本验证。

### 支持的模型

以下为 2.0.2 文档列出的支持范围，调用方式均为 `useProviderStructuredOutput()`；具体型号还需确认对应提供方的能力：

| 提供方        | 支持范围                                                      |
| ------------- | ------------------------------------------------------------- |
| OpenAI        | GPT-4o 及之后支持 JSON Schema 的模型。                        |
| Anthropic     | Claude 3.5 Sonnet 及之后的相应模型。                          |
| Google GenAI  | Gemini 1.5 Pro 及之后的相应模型。                             |
| Mistral AI    | Mistral Small 及之后支持 JSON Schema 的模型。                 |
| Ollama        | 支持 JSON Schema 的具体模型，稳定性因模型而异。               |
| Qxotic jinfer | 全部聊天模型；将 Schema 编译为语法，在 Token 采样时施加约束。 |

jinfer 的机制见 [jinfer Structured Output](https://docs.spring.io/spring-ai/reference/api/chat/jinfer-chat.html#structured-output)。

### 已知限制

提供方可能只支持 JSON Schema 的一部分。常见限制涉及 `$ref`、深层嵌套数组、`allOf` / `anyOf` / `oneOf`、正则表达式与递归类型。原生约束也不能替代应用的业务校验。

**Ollama：部分推理模型可能返回普通文本。** 来源列举 `qwen3:8b`、`qwen3.5:9b` 等内置思考模式的模型：它们可能输出推理过程，导致 `BeanOutputConverter` 无法解析，例如：

```text
StreamReadException: Unrecognized token 'The': was expecting (JSON String, Number, Array, Object or token 'null', 'true' or 'false')
```

遇到这种情况，可以更换模型，例如 `llama3.1:latest`，或回退到默认提示词方式；也可以组合原生约束与 Schema 校验，让格式不符的响应进入自动重试：

```java
ActorsFilms films = chatClient.prompt()
    .user("Generate the filmography for a random actor.")
    .call()
    .entity(ActorsFilms.class, spec -> spec
        .useProviderStructuredOutput()
        .validateSchema());
```

**OpenAI：Schema 顶层必须是对象，不能直接是数组。** 启用原生输出后直接请求 `List<T>` 会导致 API 错误：

```java
// Does NOT work with OpenAI native structured output:
List<ActorsFilms> films = chatClient.prompt()
    .user("Generate filmographies for Tom Hanks and Bill Murray.")
    .call()
    .entity(new ParameterizedTypeReference<List<ActorsFilms>>() {},
            spec -> spec.useProviderStructuredOutput()); // fails with OpenAI
```

可将列表包进一个 record，或使用默认提示词方式：

```java
// Option 1: wrap the list in a container record
record FilmographyList(List<ActorsFilms> films) {}

FilmographyList result = chatClient.prompt()
    .user("Generate filmographies for Tom Hanks and Bill Murray.")
    .call()
    .entity(FilmographyList.class, spec -> spec.useProviderStructuredOutput());
List<ActorsFilms> films = result.films();

// Option 2: use the default prompt-based approach (no native output required)
List<ActorsFilms> films = chatClient.prompt()
    .user("Generate filmographies for Tom Hanks and Bill Murray.")
    .call()
    .entity(new ParameterizedTypeReference<List<ActorsFilms>>() {});
```

默认方式没有这项顶层数组限制。相关背景见 [OpenAI 社区讨论](https://community.openai.com/t/support-top-level-array-in-json-schema/896048)。

### 按请求或全局启用

`useProviderStructuredOutput()` 是单次转换的开关。也可以使用 `AdvisorParams.ENABLE_NATIVE_STRUCTURED_OUTPUT`，在本次请求上设置，或在构建器上设置默认值：

```java
// Per request
ActorsFilms films = chatClient.prompt()
    .advisors(AdvisorParams.ENABLE_NATIVE_STRUCTURED_OUTPUT)
    .user("Generate the filmography for a random actor.")
    .call()
    .entity(ActorsFilms.class);

// Globally on the builder
@Bean
ChatClient chatClient(ChatClient.Builder builder) {
    return builder
        .defaultAdvisors(AdvisorParams.ENABLE_NATIVE_STRUCTURED_OUTPUT)
        .build();
}
```

### 提供方专用的 JSON 模式

除了统一的开关，各提供方还有独立配置。需要区分“生成有效 JSON”和“严格符合指定 JSON Schema”：前者不保证字段与类型满足业务定义的结构。

| 提供方                                                                                                  | 专用配置与含义                                                                                                                                         |
| ------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [OpenAI](https://docs.spring.io/spring-ai/reference/api/chat/openai-chat.html#_structured_outputs)      | `JSON_OBJECT` 要求有效 JSON；`JSON_SCHEMA` 搭配 Schema 约束结构。来源列出 `spring.ai.openai.chat.response-format` 选项。                               |
| [Ollama](https://docs.spring.io/spring-ai/reference/api/chat/ollama-chat.html)                          | 来源在内置 JSON 模式中列出 `spring.ai.ollama.chat.format=json`；模型的原生 Schema 支持另见上文。                                                       |
| [Qxotic jinfer](https://docs.spring.io/spring-ai/reference/api/chat/jinfer-chat.html#structured-output) | `JinferChatOptions.grammar(...)` 通过 [GBNF 语法](https://github.com/ggml-org/llama.cpp/blob/master/grammars/README.md)约束输出。                      |
| [Mistral AI](https://docs.spring.io/spring-ai/reference/api/chat/mistralai-chat.html)                   | `spring.ai.mistralai.chat.response-format` 设为 `{ "type": "json_object" }` 开启 JSON 模式；`{ "type": "json_schema" }` 搭配 Schema 开启原生结构约束。 |
