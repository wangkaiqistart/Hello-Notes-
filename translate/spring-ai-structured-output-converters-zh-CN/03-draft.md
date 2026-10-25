## 输出转换器

高层 `.entity(...)` 建立在 `StructuredOutputConverter<T>` 之上。通常直接使用高层 API 即可；需要处理额外包装的输出、生成 YAML / CSV，或直接调用底层 `ChatModel` 时，再使用转换器。

转换器参与模型调用前后的两个阶段：调用前提供格式指令，调用后把模型返回的文本解析为目标类型。下图将这两个职责放在同一个黄色框中，模型调用位于两者之间。

[![输出转换器的前后处理：输入与格式指令合并后调用模型，返回文本再转换为结构化结果](/images/frameworks/spring-ai/spring-ai-structured-output-zh.svg)](/images/frameworks/spring-ai/spring-ai-structured-output-zh.svg)

左侧看格式指令如何进入提示词，右侧看文本如何变为对象；点击可查看大图。

转换器是尽力而为的转换机制，单靠格式说明不能保证模型遵守要求。需要更可靠的结构时，可以结合 Schema 校验。它不用于工具调用协议本身的结构化数据。

### 接口与数据流

`StructuredOutputConverter<T>` 结合 Spring 的 `Converter<String, T>` 与 `FormatProvider`：

```java
public interface StructuredOutputConverter<T> extends Converter<String, T>, FormatProvider {

    /**
     * Returns the JSON schema for the structured output of an LLM call,
     * or NO_JSON_SCHEMA ("") if not available.
     */
    default String getJsonSchema() {
        return NO_JSON_SCHEMA;
    }

}
```

```java
public interface FormatProvider {
    String getFormat();
}
```

- `getFormat()` 返回给模型的格式指令。
- `convert(String)` 把模型返回的文本转换为目标类型 `T`。
- `getJsonSchema()` 返回 JSON Schema；默认返回 `NO_JSON_SCHEMA`，即空字符串。

下图把接口职责与调用路径对应起来：`FormatProvider` 将格式要求交给 `PromptTemplate`，模型响应再交给 `Converter<String, T>`。

[![结构化输出 API 数据流：FormatProvider 提供格式指令，PromptTemplate 构造请求，ChatModel 返回响应后由 Converter 转为目标类型](/images/frameworks/spring-ai/structured-output-api-zh.svg)](/images/frameworks/spring-ai/structured-output-api-zh.svg)

类名和方法名保留 API 原名，说明文字中文化；点击可查看大图。

格式指令可以要求只返回符合 RFC 8259 的 JSON，例如：

```text
  Your response should be in JSON format.
  The data structure for the JSON should match this Java class: java.util.HashMap
  Do not include any explanations, only provide a RFC8259 compliant JSON response following this format without deviation.
```

直接使用底层 API 时，通常通过[提示词模板](/frameworks/spring-ai/core/prompts/#提示词模板)把 `getFormat()` 的结果填入用户输入：

```java
    StructuredOutputConverter outputConverter = ...
    String userInputTemplate = """
        ... user text input ....
        {format}
        """; // user input with a "format" placeholder.
    Prompt prompt = new Prompt(
            PromptTemplate.builder()
                    .template(this.userInputTemplate)
                    .variables(Map.of(..., "format", this.outputConverter.getFormat())) // replace the "format" placeholder with the converter's format.
                    .build().createMessage()
    );
```

这是模板拼装骨架，转换器与业务输入需要由应用提供。使用高层 `.entity(...)` 时，框架负责相应的格式处理。

### getJsonSchema()：连接可靠性配置

`getJsonSchema()` 是 2.0 新增的默认方法，让转换器可以参与 `useProviderStructuredOutput()` 与 `validateSchema()`。

自定义转换器返回有效 Schema（通常委托给 `BeanOutputConverter`）后，两项开关才能基于这个 Schema 工作；保留空字符串默认值时，两项开关对该转换器不起作用。

### 内置实现与选型

| 转换器                                        | 职责                                                                                                                |
| --------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| `AbstractConversionServiceOutputConverter<T>` | 预置 `GenericConversionService`，供子类完成转换；不提供默认格式指令实现。                                           |
| `AbstractMessageOutputConverter<T>`           | 预置 `MessageConverter`，供子类完成转换；不提供默认格式指令实现。                                                   |
| `BeanOutputConverter<T>`                      | 接收 Java 类型或 `ParameterizedTypeReference`，生成 `DRAFT_2020_12` JSON Schema，并使用 `JsonMapper` 反序列化响应。 |
| `MapOutputConverter`                          | 要求 RFC 8259 JSON，通过 `MessageConverter` 转为 `Map<String, Object>`。                                            |
| `ListOutputConverter`                         | 要求逗号分隔的列表文本，通过 `ConversionService` 转为列表。                                                         |

下图展示继承与依赖关系：`MapOutputConverter`、`ListOutputConverter` 分别基于消息转换与类型转换服务；`BeanOutputConverter` 直接实现结构化输出转换接口。

[![输出转换器类关系：StructuredOutputConverter 继承格式与转换接口，Map、Bean、List 三种实现分别使用对应的转换能力](/images/frameworks/spring-ai/structured-output-hierarchy-zh.svg)](/images/frameworks/spring-ai/structured-output-hierarchy-zh.svg)

空心箭头表示继承，普通箭头表示持有或依赖；点击可查看大图。

### BeanOutputConverter：映射 Java 类型

仍以演员与电影列表为例：

```java
record ActorsFilms(String actor, List<String> movies) {
}
```

高层 API 通过目标类型选择对象转换方式：

```java
ActorsFilms actorsFilms = ChatClient.create(chatModel).prompt()
        .user(u -> u.text("Generate the filmography of 5 movies for {actor}.")
                    .param("actor", "Tom Hanks"))
        .call()
        .entity(ActorsFilms.class);
```

底层 `ChatModel` 则需要自己准备格式说明，再转换返回文本：

```java
BeanOutputConverter<ActorsFilms> beanOutputConverter =
    new BeanOutputConverter<>(ActorsFilms.class);

String format = this.beanOutputConverter.getFormat();

String actor = "Tom Hanks";

String template = """
        Generate the filmography of 5 movies for {actor}.
        {format}
        """;

Generation generation = chatModel.call(
    PromptTemplate.builder().template(this.template).variables(Map.of("actor", this.actor, "format", this.format)).build().create()).getResult();

ActorsFilms actorsFilms = this.beanOutputConverter.convert(this.generation.getOutput().getText());
```

**属性顺序。** `@JsonPropertyOrder` 可控制生成 Schema 中的属性顺序，适用于 record 与普通 Java 类；它描述 Schema 顺序，不保证模型输出或业务序列化的所有行为：

```java
@JsonPropertyOrder({"actor", "movies"})
record ActorsFilms(String actor, List<String> movies) {}
```

**泛型类型。** 高层 API 使用 `ParameterizedTypeReference`：

```java
List<ActorsFilms> actorsFilms = ChatClient.create(chatModel).prompt()
        .user("Generate the filmography of 5 movies for Tom Hanks and Bill Murray.")
        .call()
        .entity(new ParameterizedTypeReference<List<ActorsFilms>>() {});
```

底层方式将同一个泛型类型传给 `BeanOutputConverter`：

```java
BeanOutputConverter<List<ActorsFilms>> outputConverter = new BeanOutputConverter<>(
        new ParameterizedTypeReference<List<ActorsFilms>>() { });

String format = this.outputConverter.getFormat();
String template = """
        Generate the filmography of 5 movies for Tom Hanks and Bill Murray.
        {format}
        """;

Prompt prompt = PromptTemplate.builder().template(this.template).variables(Map.of("format", this.format)).build().create();

Generation generation = chatModel.call(this.prompt).getResult();

List<ActorsFilms> actorsFilms = this.outputConverter.convert(this.generation.getOutput().getText());
```

### MapOutputConverter：键值结果

高层 API 可以通过泛型目标类型取得 Map：

```java
Map<String, Object> result = ChatClient.create(chatModel).prompt()
        .user(u -> u.text("Provide me a List of {subject}")
                    .param("subject", "an array of numbers from 1 to 9 under they key name 'numbers'"))
        .call()
        .entity(new ParameterizedTypeReference<Map<String, Object>>() {});
```

这里指定的是目标类型；需要显式使用 `MapOutputConverter` 时，可以像下面这样在底层流程中调用，也可以将实例传给 `.entity(...)`：

```java
MapOutputConverter mapOutputConverter = new MapOutputConverter();

String format = this.mapOutputConverter.getFormat();
String template = """
        Provide me a List of {subject}
        {format}
        """;

Prompt prompt = PromptTemplate.builder().template(this.template)
.variables(Map.of("subject", "an array of numbers from 1 to 9 under they key name 'numbers'", "format", this.format)).build().create();

Generation generation = chatModel.call(this.prompt).getResult();

Map<String, Object> result = this.mapOutputConverter.convert(this.generation.getOutput().getText());
```

### ListOutputConverter：逗号分隔列表

`ListOutputConverter` 面向逗号分隔的文本列表，与“将 JSON 数组映射为 `List<T>`”不同。高层 API 传入转换器实例：

```java
List<String> flavors = ChatClient.create(chatModel).prompt()
                .user(u -> u.text("List five {subject}")
                            .param("subject", "ice cream flavors"))
                .call()
                .entity(new ListOutputConverter(new DefaultConversionService()));
```

底层 API 则自行添加格式指令并转换：

```java
ListOutputConverter listOutputConverter = new ListOutputConverter(new DefaultConversionService());

String format = this.listOutputConverter.getFormat();
String template = """
        List five {subject}
        {format}
        """;

Prompt prompt = PromptTemplate.builder().template(this.template).variables(Map.of("subject", "ice cream flavors", "format", this.format)).build().create();

Generation generation = this.chatModel.call(this.prompt).getResult();

List<String> list = this.listOutputConverter.convert(this.generation.getOutput().getText());
```

### 自定义转换器：提取 JSON

模型可能在 JSON 前加说明文字，或使用 Markdown 代码围栏包装：

````text
Here's the filmography:
```json
{ "actor": "Tom Hanks", "movies": ["Forrest Gump", "Cast Away"] }
```
````

这样的完整响应并非纯 JSON，不能直接假定解析成功。来源给出一个宽容转换器：先提取代码围栏内的内容，再交给默认解析器。

````java
public class LenientJsonOutputConverter<T> implements StructuredOutputConverter<T> {

    private static final Pattern FENCE = Pattern.compile("```(?:json)?\\s*([\\s\\S]*?)```");

    private final BeanOutputConverter<T> delegate;

    public LenientJsonOutputConverter(Class<T> targetType) {
        this.delegate = new BeanOutputConverter<>(targetType);
    }

    @Override public String getFormat()     { return delegate.getFormat(); }
    @Override public String getJsonSchema() { return delegate.getJsonSchema(); }

    @Override
    public T convert(String source) {
        var matcher = FENCE.matcher(source);
        String json = matcher.find() ? matcher.group(1).trim() : source.trim();
        return delegate.convert(json);
    }
}
````

将实例传入 `.entity(...)`：

```java
ActorsFilms films = chatClient.prompt()
    .user("Generate the filmography for a random actor.")
    .call()
    .entity(new LenientJsonOutputConverter<>(ActorsFilms.class));
```

示例通过委托 `getJsonSchema()` 保留 Schema，因此仍可搭配 `validateSchema()` 和 `useProviderStructuredOutput()`。

这里的正则只提取第一个符合模式的代码围栏；未匹配时会把原文本直接交给委托转换器。它不是任意混合文本的通用 JSON 提取器。

### 非 JSON 格式：YAML、CSV

对于 YAML 配置或 CSV 数据，实现自己的 `getFormat()` 格式指令和 `convert(...)` 解析器即可。

这类转换器通常不提供 JSON Schema，保留 `getJsonSchema()` 默认值即可；此时原生 JSON Schema 约束与 Schema 校验开关不起作用，格式与业务校验由应用负责。
