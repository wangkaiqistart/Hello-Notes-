# ETL 管道

抽取、转换、加载（Extract, Transform, Load，ETL）框架是检索增强生成（RAG）场景的数据处理基础。

ETL 管道把原始数据源中的内容转换并写入结构化的向量存储，使数据适合 AI 模型检索。

RAG 从资料中检索相关信息，补充生成式模型的能力，提高回答的质量和相关性。

<a id="_api_overview"></a>

## API 概览

ETL 管道负责创建、转换和存储 `Document` 实例。

![Spring AI 文档 API](https://docs.spring.io/spring-ai/reference/_images/spring-ai-document1-api.jpg)

`Document` 包含文本、元数据，也可以包含图像、音频、视频等媒体内容。

ETL 管道有三个主要组件：

- `DocumentReader`：实现 `Supplier<List<Document>>`。
- `DocumentTransformer`：实现 `Function<List<Document>, List<Document>>`。
- `DocumentWriter`：实现 `Consumer<List<Document>>`。

`DocumentReader` 从 PDF、文本文件等文档中读取内容，创建 `Document`。

把这三类组件各取一个实例串起来，就能组成简单的 ETL 管道。

![ETL 管道](https://docs.spring.io/spring-ai/reference/_images/etl-pipeline.jpg)

例如，使用以下三个实现：

- `PagePdfDocumentReader`：`DocumentReader` 的实现。
- `TokenTextSplitter`：`DocumentTransformer` 的实现。
- `VectorStore`：`DocumentWriter` 的实现。

下面用 Java 函数式接口的方法，把数据加载到向量数据库，供 RAG 检索：

```java
vectorStore.accept(tokenTextSplitter.apply(pdfReader.get()));
```

也可以使用更贴近领域含义的方法名：

```java
vectorStore.write(tokenTextSplitter.split(pdfReader.read()));
```

<a id="_etl_interfaces"></a>

## ETL 接口

ETL 管道由下列接口及其实现组成。完整关系见 [ETL 类图](#etl-class-diagram)。

<a id="_documentreader"></a>

### DocumentReader

从不同来源提供文档。

```java
public interface DocumentReader extends Supplier<List<Document>> {

    default List<Document> read() {
		return get();
	}
}
```

<a id="_documenttransformer"></a>

### DocumentTransformer

在处理流程中批量转换文档。

```java
public interface DocumentTransformer extends Function<List<Document>, List<Document>> {

    default List<Document> transform(List<Document> transform) {
		return apply(transform);
	}
}
```

<a id="_documentwriter"></a>

### DocumentWriter

负责 ETL 的最后一个阶段，将文档交给存储环节。

```java
public interface DocumentWriter extends Consumer<List<Document>> {

    default void write(List<Document> documents) {
		accept(documents);
	}
}
```

<a id="etl-class-diagram"></a>

### ETL 类图

下图展示 ETL 接口与实现类的关系。

![ETL 接口与实现类关系图](https://docs.spring.io/spring-ai/reference/_images/etl-class-diagram.jpg)

<a id="_documentreaders"></a>

## 文档读取器

:::caution
下面介绍的大多数 `DocumentReader` 和 `DocumentWriter` 实现使用 `Resource` 或资源模式构造，并在内部通过 `DefaultResourceLoader` 或其变体访问存储。直接用用户提供的 URL 构造这些实例会带来安全风险，使用时应谨慎。
:::

<a id="_json"></a>

### JSON

`JsonReader` 解析 JSON 文档，将其转换为 `Document` 列表。

<a id="_example"></a>

#### 示例

```java
@Component
class MyJsonReader {

	private final Resource resource;

    MyJsonReader(@Value("classpath:bikes.json") Resource resource) {
        this.resource = resource;
    }

	List<Document> loadJsonAsDocuments() {
        JsonReader jsonReader = new JsonReader(this.resource, "description", "content");
        return jsonReader.get();
	}
}
```

<a id="_constructor_options"></a>

#### 构造方法

`JsonReader` 提供以下构造方法：

1. `JsonReader(Resource resource)`
2. `JsonReader(Resource resource, String…​ jsonKeysToUse)`
3. `JsonReader(Resource resource, JsonMetadataGenerator jsonMetadataGenerator, String…​ jsonKeysToUse)`

<a id="_parameters"></a>

#### 参数

- `resource`：指向 JSON 文件的 Spring `Resource` 对象。
- `jsonKeysToUse`：指定哪些 JSON 字段的值用作生成的 `Document` 的文本内容。
- `jsonMetadataGenerator`：可选的 `JsonMetadataGenerator`，为每个 `Document` 生成元数据。

<a id="_behavior"></a>

#### 处理行为

`JsonReader` 按以下方式处理 JSON：

- 支持 JSON 数组和单个 JSON 对象。
- 对每个 JSON 对象（数组中的对象或单独的对象）：
  - 根据 `jsonKeysToUse` 提取内容。
  - 未指定字段时，使用整个 JSON 对象作为内容。
  - 使用传入的 `JsonMetadataGenerator` 生成元数据；未提供时使用空元数据生成器。
  - 用提取的内容和元数据创建 `Document`。

<a id="_using_json_pointers"></a>

#### 使用 JSON Pointer

`JsonReader` 支持通过 JSON Pointer 读取 JSON 文档中的指定部分，便于从复杂结构中提取嵌套数据。

<a id="_the_getstring_pointer_method"></a>

##### `get(String pointer)` 方法

```java
public List<Document> get(String pointer)
```

该方法通过 JSON Pointer 读取 JSON 文档中的指定部分。

<a id="_parameters_2"></a>

###### 参数

- `pointer`：符合 RFC 6901 的 JSON Pointer 字符串，用于定位 JSON 结构中的目标元素。

<a id="_return_value"></a>

###### 返回值

- 返回 `List<Document>`，其中包含从指针所定位的 JSON 元素解析出的文档。

<a id="_behavior_2"></a>

###### 处理行为

- 使用指定的 JSON Pointer 定位 JSON 结构中的元素。
- 指针有效且目标元素存在时：
  - 目标为 JSON 对象：返回只含一个 `Document` 的列表。
  - 目标为 JSON 数组：为数组中的每个元素创建一个 `Document`，并返回列表。
- 指针无效或目标元素不存在时，抛出 `IllegalArgumentException`。

<a id="_example_2"></a>

###### 示例

```java
JsonReader jsonReader = new JsonReader(resource, "description");
List<Document> documents = this.jsonReader.get("/store/books/0");
```

<a id="_example_json_structure"></a>

#### JSON 结构示例

```json
[
  {
    "id": 1,
    "brand": "Trek",
    "description": "A high-performance mountain bike for trail riding."
  },
  {
    "id": 2,
    "brand": "Cannondale",
    "description": "An aerodynamic road bike for racing enthusiasts."
  }
]
```

如果将 `jsonKeysToUse` 配置为 `"description"`，`JsonReader` 会为数组中的每辆自行车创建一个 `Document`，内容取自其 `description` 字段。

<a id="_notes"></a>

#### 注意事项

- `JsonReader` 使用 Jackson 解析 JSON。
- 通过流式处理数组，可以高效处理大型 JSON 文件。
- `jsonKeysToUse` 指定多个字段时，会拼接这些字段的值作为内容。
- 自定义 `jsonKeysToUse` 和 `JsonMetadataGenerator`，可以适配不同 JSON 结构。

<a id="_text"></a>

### 纯文本

`TextReader` 读取纯文本文档，将其转换为 `Document` 列表。

<a id="_example_3"></a>

#### 示例

```java
@Component
class MyTextReader {

    private final Resource resource;

    MyTextReader(@Value("classpath:text-source.txt") Resource resource) {
        this.resource = resource;
    }

	List<Document> loadText() {
		TextReader textReader = new TextReader(this.resource);
		textReader.getCustomMetadata().put("filename", "text-source.txt");

		return textReader.read();
    }
}
```

<a id="_constructor_options_2"></a>

#### 构造方法

`TextReader` 提供两个构造方法：

1. `TextReader(String resourceUrl)`
2. `TextReader(Resource resource)`

<a id="_parameters_3"></a>

#### 参数

- `resourceUrl`：待读取资源的 URL 字符串。
- `resource`：指向文本文件的 Spring `Resource` 对象。

<a id="_configuration"></a>

#### 配置

- `setCharset(Charset charset)`：设置读取文本文件所用的字符集，默认为 UTF-8。
- `getCustomMetadata()`：返回可修改的 Map，用于添加自定义文档元数据。

<a id="_behavior_3"></a>

#### 处理行为

`TextReader` 按以下方式处理文本：

- 将文本文件的全部内容读入一个 `Document`。
- 文件内容成为 `Document` 的内容。
- 自动为 `Document` 添加以下元数据：
  - `charset`：读取文件所用的字符集，默认为 `"UTF-8"`。
  - `source`：源文本文件的文件名。
- 将通过 `getCustomMetadata()` 添加的自定义元数据一并写入 `Document`。

<a id="_notes_2"></a>

#### 注意事项

- `TextReader` 将整个文件读入内存，可能不适合非常大的文件。
- 需要切成较小文本块时，可以在读取后使用 `TokenTextSplitter` 等文本切分器：

```java
List<Document> documents = textReader.get();
List<Document> splitDocuments = TokenTextSplitter.builder().build().apply(this.documents);
```

- 读取器使用 Spring 的 `Resource` 抽象，支持类路径、文件系统、URL 等不同来源。
- 通过 `getCustomMetadata()` 可以为该读取器创建的所有文档添加自定义元数据。

<a id="_html_jsoup"></a>

### HTML（JSoup）

`JsoupDocumentReader` 使用 JSoup 库解析 HTML 文档，将其转换为 `Document` 列表。

<a id="_dependencies"></a>

#### 依赖

通过 Maven 或 Gradle 添加依赖。

- Maven
- Gradle

```xml
<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>spring-ai-jsoup-document-reader</artifactId>
</dependency>
```

```groovy
dependencies {
    implementation 'org.springframework.ai:spring-ai-jsoup-document-reader'
}
```

<a id="_example_4"></a>

#### 示例

```java
@Component
class MyHtmlReader {

    private final Resource resource;

    MyHtmlReader(@Value("classpath:/my-page.html") Resource resource) {
        this.resource = resource;
    }

    List<Document> loadHtml() {
        JsoupDocumentReaderConfig config = JsoupDocumentReaderConfig.builder()
            .selector("article p") // Extract paragraphs within <article> tags
            .charset("ISO-8859-1")  // Use ISO-8859-1 encoding
            .includeLinkUrls(true) // Include link URLs in metadata
            .metadataTags(List.of("author", "date")) // Extract author and date meta tags
            .additionalMetadata("source", "my-page.html") // Add custom metadata
            .build();

        JsoupDocumentReader reader = new JsoupDocumentReader(this.resource, config);
        return reader.get();
    }
}
```

使用 `JsoupDocumentReaderConfig` 可以调整 `JsoupDocumentReader` 的行为：

- `charset`：HTML 文档的字符编码，默认为 `"UTF-8"`。
- `selector`：JSoup CSS 选择器，指定从哪些元素提取文本，默认为 `"body"`。
- `separator`：拼接多个选中元素的文本时使用的分隔符，默认为 `"\n"`。
- `allElements`：为 `true` 时，忽略 `selector`，提取 `<body>` 中的全部文本；默认为 `false`。
- `groupByElement`：为 `true` 时，为 `selector` 匹配的每个元素分别创建一个 `Document`；默认为 `false`。
- `includeLinkUrls`：为 `true` 时，提取绝对链接 URL 并加入元数据；默认为 `false`。
- `metadataTags`：要提取内容的 `<meta>` 标签名称列表，默认为 `["description", "keywords"]`。
- `additionalMetadata`：为所有创建的 `Document` 添加自定义元数据。

<a id="_sample_document_my_page_html"></a>

#### 示例文档：my-page.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>My Web Page</title>
    <meta name="description" content="A sample web page for Spring AI">
    <meta name="keywords" content="spring, ai, html, example">
    <meta name="author" content="John Doe">
    <meta name="date" content="2024-01-15">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header>
        <h1>Welcome to My Page</h1>
    </header>
    <nav>
        <ul>
            <li><a href="/">Home</a></li>
            <li><a href="/about">About</a></li>
        </ul>
    </nav>
    <article>
        <h2>Main Content</h2>
        <p>This is the main content of my web page.</p>
        <p>It contains multiple paragraphs.</p>
        <a href="https://www.example.com">External Link</a>
    </article>
    <footer>
        <p>&copy; 2024 John Doe</p>
    </footer>
</body>
</html>
```

处理行为：

`JsoupDocumentReader` 按配置解析 HTML 内容并创建 `Document`：

- `selector` 决定从哪些元素提取文本。
- `allElements` 为 `true` 时，将 `<body>` 内的全部文本提取到一个 `Document`。
- `groupByElement` 为 `true` 时，为每个匹配 `selector` 的元素分别创建一个 `Document`。
- `allElements` 和 `groupByElement` 都不为 `true` 时，使用 `separator` 拼接所有匹配元素的文本。
- 将文档标题、指定 `<meta>` 标签的内容，以及可选的链接 URL 加入 `Document` 元数据。
- 从 URL 资源中提取基础 URI，用于解析相对链接。

读取器保留所选元素的文本内容，去掉其中的 HTML 标签。

<a id="_markdown"></a>

### Markdown

`MarkdownDocumentReader` 解析 Markdown 文档，将其转换为 `Document` 列表。

<a id="_dependencies_2"></a>

#### 依赖

通过 Maven 或 Gradle 添加依赖。

- Maven
- Gradle

```xml
<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>spring-ai-markdown-document-reader</artifactId>
</dependency>
```

```groovy
dependencies {
    implementation 'org.springframework.ai:spring-ai-markdown-document-reader'
}
```

<a id="_example_5"></a>

#### 示例

```java
@Component
class MyMarkdownReader {

    private final Resource resource;

    MyMarkdownReader(@Value("classpath:code.md") Resource resource) {
        this.resource = resource;
    }

    List<Document> loadMarkdown() {
        MarkdownDocumentReaderConfig config = MarkdownDocumentReaderConfig.builder()
            .withHorizontalRuleCreateDocument(true)
            .withIncludeCodeBlock(false)
            .withIncludeBlockquote(false)
            .withAdditionalMetadata("filename", "code.md")
            .build();

        MarkdownDocumentReader reader = new MarkdownDocumentReader(this.resource, config);
        return reader.get();
    }
}
```

使用 `MarkdownDocumentReaderConfig` 可以调整 `MarkdownDocumentReader` 的行为：

- `horizontalRuleCreateDocument`：为 `true` 时，Markdown 中的水平分隔线会创建新的 `Document`。
- `includeCodeBlock`：为 `true` 时，代码块与周围文本放入同一个 `Document`；为 `false` 时，代码块单独创建 `Document`。
- `includeBlockquote`：为 `true` 时，引用块与周围文本放入同一个 `Document`；为 `false` 时，引用块单独创建 `Document`。
- `additionalMetadata`：为所有创建的 `Document` 添加自定义元数据。

<a id="_sample_document_code_md"></a>

#### 示例文档：code.md

````markdown
This is a Java sample application:

```java
package com.example.demo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class DemoApplication {
    public static void main(String[] args) {
        SpringApplication.run(DemoApplication.class, args);
    }
}
```

Markdown also provides the possibility to `use inline code formatting throughout` the entire sentence.

---

Another possibility is to set block code without specific highlighting:

```
./mvnw spring-javaformat:apply
```
````

处理行为：`MarkdownDocumentReader` 按配置解析 Markdown 内容并创建 `Document`：

- 标题成为 `Document` 的元数据。
- 段落成为 `Document` 的内容。
- 代码块可以独立成为 `Document`，也可以与周围文本放在一起。
- 引用块可以独立成为 `Document`，也可以与周围文本放在一起。
- 水平分隔线可以将内容拆成不同的 `Document`。

读取器会保留 `Document` 内容中的行内代码、列表和文本样式等格式。

<a id="_pdf_page"></a>

### 按页读取 PDF

`PagePdfDocumentReader` 使用 Apache PdfBox 库解析 PDF 文档。

<a id="_dependencies_3"></a>

#### 依赖

通过 Maven 或 Gradle 添加依赖。

- Maven
- Gradle

```xml
<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>spring-ai-pdf-document-reader</artifactId>
</dependency>
```

```groovy
dependencies {
    implementation 'org.springframework.ai:spring-ai-pdf-document-reader'
}
```

<a id="_example_6"></a>
