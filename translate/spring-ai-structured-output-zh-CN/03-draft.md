模型通常返回文本，但业务代码需要按字段分支、保存数据或调用其他服务。**结构化输出**让模型按指定结构生成内容，再将文本解析为 Java 对象。

Spring AI 在 [ChatClient](/frameworks/spring-ai/core/chat-client/) 链式 API 中提供 `.entity(...)`：定义目标 Java 类型后，框架生成 JSON Schema（描述字段、类型等结构约束），将格式要求交给模型，再把响应反序列化为该类型。

本文介绍高层用法；进一步配置见以下专题：

- [Schema 校验与自动纠正](https://docs.spring.io/spring-ai/reference/api/structured-output/validation.html)：通过 `validateSchema()` 校验输出，并自动重试。
- [提供方原生结构化输出](https://docs.spring.io/spring-ai/reference/api/structured-output/native.html)：通过 `useProviderStructuredOutput()` 在模型 API 层施加约束。
- [输出转换器](https://docs.spring.io/spring-ai/reference/api/structured-output/converters.html)：底层 `StructuredOutputConverter` API、内置实现，以及自定义或非 JSON 格式。

## 返回 Java 对象

先用 Java `record` 定义返回结构：

```java
record ActorsFilms(String actor, List<String> movies) {}
```

调用时以 `.entity(目标类型)` 结束链式请求。与返回原始文本的 `.content()` 不同，它会返回解析后的对象：

```java
ActorsFilms films = chatClient.prompt()
    .user("Generate the filmography for a random actor.")
    .call()
    .entity(ActorsFilms.class);
```

随后可以像访问其他 Java 对象一样读取字段：

```java
films.actor();     // "Tom Hanks"
films.movies();    // ["Forrest Gump", "Cast Away", ...]
```

默认方式在内部执行三步：

1. 根据 `ActorsFilms` 生成 JSON Schema。
2. 将 Schema 补充到提示词的系统上下文，要求模型按格式回答。
3. 将模型返回的 JSON 交给类型转换器，解析为 `ActorsFilms`。

下图展示这条默认流程：蓝色虚线传递返回类型及 Schema，橙色箭头连接问题、模型与转换器，底部蓝线返回对象。

[![结构化输出默认流程：由返回类型生成 Schema，加入系统上下文，模型返回 JSON 后转换为 Java 对象](/images/frameworks/spring-ai/structured-output-basic-zh.svg)](/images/frameworks/spring-ai/structured-output-basic-zh.svg)

图示为提示词驱动的转换方式，格式要求并非严格保证；点击可查看大图。

这种方式不依赖提供方专用的结构化输出功能，可用于 Spring AI 支持的模型。

**`.entity(...)` 仅用于 `.call()`。**对象解析需要完整响应，不能直接用于 `.stream()` 的文本片段流。这个限制覆盖本文所有重载：`Class`、`ParameterizedTypeReference`、自定义转换器，以及带可靠性配置的调用。

默认 `.entity(...)` 不保证模型严格遵守 Schema。模型可能多返回字段、漏掉必需字段，或在 JSON 外加入说明文字，从而导致校验或解析问题。下面两项配置用于提高可靠性。

## 泛型：List、Map 等

具体类型使用 `.entity(Class)`；`List<ActorsFilms>`、`Map<String, ActorsFilms>` 等泛型类型使用 `ParameterizedTypeReference`：

```java
List<ActorsFilms> films = chatClient.prompt()
    .user("Generate filmographies for three random actors.")
    .call()
    .entity(new ParameterizedTypeReference<List<ActorsFilms>>() {});
```

## 可靠性配置：EntityParamSpec

所有 `.entity(...)` 和 `.responseEntity(...)` 重载都可以额外接收 `Consumer<EntityParamSpec>`。其中两项能力相互独立，也可以组合使用。

### validateSchema()：校验失败后重试

启用后，Spring AI 按目标类型的 Schema 校验响应；如果失败，就把具体错误补充到提示词并重新请求模型，默认最多尝试 **3 次**。

```java
ActorsFilms films = chatClient.prompt()
    .user("Generate the filmography for a random actor.")
    .call()
    .entity(ActorsFilms.class, spec -> spec.validateSchema());
```

重试流程与定制方式见 [Schema 校验与自动纠正](https://docs.spring.io/spring-ai/reference/api/structured-output/validation.html)。

### useProviderStructuredOutput()：请求端约束

这项配置将 Schema 作为 API 级约束传递给提供方，由提供方运行时约束输出结构，而不只依靠提示词指令。

```java
ActorsFilms films = chatClient.prompt()
    .user("Generate the filmography for a random actor.")
    .call()
    .entity(ActorsFilms.class, spec -> spec.useProviderStructuredOutput());
```

底层模型必须支持原生结构化输出，适用提供方和限制见[提供方原生结构化输出](https://docs.spring.io/spring-ai/reference/api/structured-output/native.html)。

### 组合使用

可以同时开启请求端约束和响应端校验：

```java
ActorsFilms films = chatClient.prompt()
    .user("Generate the filmography for a random actor.")
    .call()
    .entity(ActorsFilms.class, spec -> spec
        .useProviderStructuredOutput()
        .validateSchema());
```

`useProviderStructuredOutput()` 从请求端降低格式不符的概率；`validateSchema()` 检查响应并纠正剩余问题，包括部分提供方边界情况或推理模型的特殊行为。下游代码对结构变化敏感时，可以组合使用。

## 同时获取对象与完整响应

`.entity(...)` 只返回对象。还需要 Token 用量、观测信息等元数据时，使用 `.responseEntity(...)` 同时取得对象与底层 `ChatResponse`：

```java
ResponseEntity<ChatResponse, ActorsFilms> result = chatClient.prompt()
    .user("Generate the filmography for a random actor.")
    .call()
    .responseEntity(ActorsFilms.class);

ActorsFilms films = result.entity();
ChatResponse raw = result.response();
long totalTokens = raw.getMetadata().getUsage().getTotalTokens();
```

这里的 `ResponseEntity` 是 Spring AI 的结果容器。它与 `.entity(...)` 支持相同类型的重载：`Class`、`ParameterizedTypeReference`、自定义 `StructuredOutputConverter`，以及 `EntityParamSpec` 配置。

元数据的读取方式见[聊天响应元数据](/frameworks/spring-ai/core/chat-response-metadata/)。

## 自定义与非 JSON 输出

内置 JSON 转换不足以满足需求时，可以实现 `StructuredOutputConverter<T>`，并传给 `.entity(...)`。例如，需要针对包裹在 Markdown 代码围栏中的输出做特殊处理，或解析 YAML、CSV 等非 JSON 格式。

内置转换器与自定义方式见[输出转换器](https://docs.spring.io/spring-ai/reference/api/structured-output/converters.html)。

## 用法速查

| 需求                                   | 调用方式                                                                           |
| -------------------------------------- | ---------------------------------------------------------------------------------- |
| 默认对象映射，不依赖原生结构化输出能力 | `.entity(Type.class)`                                                              |
| `List<T>`、`Map<K,V>` 等泛型           | `.entity(new ParameterizedTypeReference<...>() {})`                                |
| 格式校验失败后自动重试                 | `.entity(Type.class, spec -> spec.validateSchema())`                               |
| 使用提供方 API 约束输出格式            | `.entity(Type.class, spec -> spec.useProviderStructuredOutput())`                  |
| 同时启用请求约束与响应校验重试         | `.entity(Type.class, spec -> spec.useProviderStructuredOutput().validateSchema())` |
| 获取对象及模型响应、Token 用量等元数据 | `.responseEntity(...)`，支持相同类型的重载。                                       |
| 自定义处理或 YAML、CSV 等格式          | 实现 `StructuredOutputConverter<T>` 后传入 `.entity(...)`。                        |
| 流式响应直接映射对象                   | 不支持本文的 `.entity(...)` 用法；它仅用于 `.call()`。                             |

结构化输出默认是尽力而为的转换；需要更可靠的结构时，启用 `validateSchema()`、`useProviderStructuredOutput()`，或组合使用。

`StructuredOutputConverter` 不用于[工具调用](https://docs.spring.io/spring-ai/reference/api/tools.html)；工具调用本身通过工具协议提供结构化信息。
