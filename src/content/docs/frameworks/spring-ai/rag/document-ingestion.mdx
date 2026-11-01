---
title: Spring AI：ETL 管道
description: Document、Reader、Transformer、Writer 的数据准备链路，含读取器选型、Token 切分与元数据增强参考。
sidebar:
  label: ETL 管道
  order: 2
---

抽取、转换、加载（Extract, Transform, Load，ETL）框架是检索增强生成（RAG）场景的数据处理基础。

ETL 管道把原始数据源中的内容转换并写入结构化的向量存储，使数据适合 AI 模型检索。

RAG 从资料中检索相关信息，补充生成式模型的能力，提高回答的质量和相关性。

:::tip[阅读路线]
先看 Document 与三段 ETL 链路，再选择一种读取器，重点掌握 `TokenTextSplitter` 和 `VectorStore` 写入。关键词、相邻摘要及其他格式读取器保留作参考，需要时再深入。
:::

本篇处理**提问前**的数据准备：读取资料 → 切分和转换 → 写入存储。[RAG](/frameworks/spring-ai/rag/retrieval-and-generation/) 负责提问时的检索与回答，两条链路通过 `Document` 和 `VectorStore` 衔接。这里的转换不一定调用模型；关键词、摘要增强会调用[聊天模型](/frameworks/spring-ai/models/chat-model/)，向量存储写入通常还会调用 [Embedding 模型](/frameworks/spring-ai/models/embedding-model/)。

<a id="_api_overview"></a>

## 一、API 概览（重点掌握）

ETL 管道负责创建、转换和存储 `Document` 实例。

2.0.2 的 `Document` 包含 ID、元数据，以及**文本或单个 `Media`，二者只能选一个**。文本通过 `getText()` 访问，媒体通过 `getMedia()` 访问；媒体可表示图像、音频或视频等数据，具体处理能力取决于读取器、Embedding 模型和存储实现。它不继承 `Content` 或 `MediaContent`。

下面的旧版结构图用于理解内容、元数据和媒体的概念关系；图中的 `getContent()`、`List<Media>` 与继承关系不对应 2.0.2 API，编写代码时以上述当前定义为准。

<figure>
  <a href="/images/spring-ai/etl/document-api-zh-CN.png" target="_blank" rel="noreferrer">
    <img
      src="/images/spring-ai/etl/document-api-zh-CN.png"
      alt="旧版 Document 结构示意，展示内容、元数据和媒体的概念关系；方法名和继承关系不代表 2.0.2 实现"
    />
  </a>
  <figcaption>内容与元数据的概念关系；点击查看原尺寸。</figcaption>
</figure>

ETL 管道有三个主要组件：

- `DocumentReader`：实现 `Supplier<List<Document>>`。
- `DocumentTransformer`：实现 `Function<List<Document>, List<Document>>`。
- `DocumentWriter`：实现 `Consumer<List<Document>>`。

`DocumentReader` 从 PDF、文本文件等文档中读取内容，创建 `Document`。

把这三类组件各取一个实例串起来，就能组成简单的 ETL 管道。

<figure>
  <a href="/images/spring-ai/etl/etl-pipeline-zh-CN.png" target="_blank" rel="noreferrer">
    <img
      src="/images/spring-ai/etl/etl-pipeline-zh-CN.png"
      alt="ETL 数据流：数据源经 DocumentReader 读取、DocumentTransformer 转换，再由 DocumentWriter 写入存储"
    />
  </a>
  <figcaption>从左到右查看 Reader、Transformer、Writer 的数据流。点击查看原尺寸。</figcaption>
</figure>

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

## 二、ETL 接口（理解职责）

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

三类接口分别对应 Java 的 `Supplier`、`Function` 和 `Consumer`。读取器从数据源产生文档，转换器处理文档列表，写入器把结果保存到文件或向量存储。下图上方展示函数式接口，下方列出常见实现，重点看这三组对应关系。

<figure>
  <a href="/images/spring-ai/etl/etl-class-diagram-zh-CN.png" target="_blank" rel="noreferrer">
    <img
      src="/images/spring-ai/etl/etl-class-diagram-zh-CN.png"
      alt="ETL 接口与实现类图：三类接口对应 Supplier、Function、Consumer，并列出读取器、转换器和向量存储实现"
    />
  </a>
  <figcaption>上层为函数式接口，下层为对应的组件与存储实现。点击查看原尺寸。</figcaption>
</figure>

<a id="_documentreaders"></a>

## 三、文档读取器（按格式查阅）

:::caution
下面介绍的大多数 `DocumentReader` 和 `DocumentWriter` 实现使用 `Resource` 或资源模式构造，并在内部通过 `DefaultResourceLoader` 或其变体访问存储。直接用用户提供的 URL 构造这些实例会带来安全风险，使用时应谨慎。
:::

| 输入资料                 | 读取器                       | 选择要点                                     |
| ------------------------ | ---------------------------- | -------------------------------------------- |
| JSON                     | `JsonReader`                 | 选择文本字段、JSON Pointer 与自定义元数据    |
| 纯文本                   | `TextReader`                 | 整个文件生成一个 Document，再按需切分        |
| HTML                     | `JsoupDocumentReader`        | CSS 选择器、按元素分组、提取链接和 meta 信息 |
| Markdown                 | `MarkdownDocumentReader`     | 标题元数据，以及代码块、引用块的分组         |
| PDF 按页                 | `PagePdfDocumentReader`      | 控制每个 Document 包含的页数                 |
| 有目录的 PDF             | `ParagraphPdfDocumentReader` | 按目录结构组织段落；并非每份 PDF 都有目录    |
| DOCX、PPTX、PDF、HTML 等 | `TikaDocumentReader`         | 需要统一处理多种格式时使用                   |

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

#### 构造器

`JsonReader` 提供以下构造器：

1. `JsonReader(Resource resource)`
2. `JsonReader(Resource resource, String... jsonKeysToUse)`
3. `JsonReader(Resource resource, JsonMetadataGenerator jsonMetadataGenerator, String... jsonKeysToUse)`

<a id="_parameters"></a>

#### 参数

- `resource`：指向 JSON 文件的 Spring `Resource` 对象。
- `jsonKeysToUse`：指定哪些 JSON 字段的值用作生成的 `Document` 的文本内容。
- `jsonMetadataGenerator`：可选的 `JsonMetadataGenerator`，为每个 `Document` 生成元数据。

<a id="_behavior"></a>

#### 处理流程

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

###### 处理流程

- 使用指定的 JSON Pointer 定位 JSON 结构中的元素。
- 指针有效且目标元素存在时：
  - 目标为 JSON 对象：返回只含一个 `Document` 的列表。
  - 目标为 JSON 数组：为数组中的每个元素创建一个 `Document`，并返回列表。
- 指针无效或目标元素不存在时，抛出 `IllegalArgumentException`。

<a id="_example_2"></a>

###### 示例

```java
JsonReader jsonReader = new JsonReader(resource, "description");
List<Document> documents = jsonReader.get("/store/books/0");
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

如果将 `jsonKeysToUse` 配置为 `"description"`，`JsonReader` 会为数组中的每辆自行车创建一个 `Document`，内容是 `description: 字段值`。

这个数组与前面的 `/store/books/0` 是两个独立示例。对当前数组，`/0` 定位第一辆自行车；`/store/books/0` 则要求输入具有相应的嵌套对象结构。

<a id="_notes"></a>

#### 注意事项

- `JsonReader` 使用 Jackson 解析 JSON。
- 2.0.2 先用 Jackson `readTree()` 把整个 JSON 载入内存，再用 Java Stream 遍历数组；这不是逐条流式解析。大型文件需要评估内存，必要时采用自定义流式读取器。
- `jsonKeysToUse` 指定多个字段时，会按 `字段名: 字段值` 加换行的形式拼接；没有字段匹配时，回退到整个对象的字符串表示。
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

#### 构造器

`TextReader` 提供两个构造器：

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

#### 处理流程

`TextReader` 按以下方式处理文本：

- 将文本文件的全部内容读入一个 `Document`。
- 文件内容成为 `Document` 的内容。
- 自动为 `Document` 添加以下元数据：
  - `charset`：读取文件所用的字符集，默认为 `"UTF-8"`。
  - `source`：优先使用源文本文件名；没有文件名时依次回退到 URI、URL、资源描述。
- 将通过 `getCustomMetadata()` 添加的自定义元数据一并写入 `Document`。

<a id="_notes_2"></a>

#### 注意事项

- `TextReader` 将整个文件读入内存，可能不适合非常大的文件。
- 需要切成较小文本块时，可以在读取后使用 `TokenTextSplitter` 等文本切分器：

```java
List<Document> documents = textReader.get();
List<Document> splitDocuments = TokenTextSplitter.builder().build().apply(documents);
```

- 读取器使用 Spring 的 `Resource` 抽象，支持类路径、文件系统、URL 等不同来源。
- 通过 `getCustomMetadata()` 可以为该读取器创建的所有文档添加自定义元数据。

<a id="_html_jsoup"></a>

### HTML（JSoup）

`JsoupDocumentReader` 使用 JSoup 库解析 HTML 文档，将其转换为 `Document` 列表。

<a id="_dependencies"></a>

#### 依赖

通过 Maven 或 Gradle 添加依赖。

**Maven：**

```xml
<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>spring-ai-jsoup-document-reader</artifactId>
</dependency>
```

**Gradle：**

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
    <meta charset="UTF-8" />
    <title>My Web Page</title>
    <meta name="description" content="A sample web page for Spring AI" />
    <meta name="keywords" content="spring, ai, html, example" />
    <meta name="author" content="John Doe" />
    <meta name="date" content="2024-01-15" />
    <link rel="stylesheet" href="style.css" />
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

处理流程：

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

**Maven：**

```xml
<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>spring-ai-markdown-document-reader</artifactId>
</dependency>
```

**Gradle：**

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

处理流程：`MarkdownDocumentReader` 按配置解析 Markdown 内容并创建 `Document`：

- 标题文本写入 `title` 元数据，标题层级可写入 `category`，例如 `header_2`。
- 段落成为 `Document` 的内容。
- 代码块可以独立成为 `Document`，也可以与周围文本放在一起。
- 引用块可以独立成为 `Document`，也可以与周围文本放在一起。
- 水平分隔线可以将内容拆成不同的 `Document`。

读取器会提取行内代码、列表和样式节点中的文本，但不会原样保留 Markdown 标记及排版。例如行内代码的反引号和强调标记不会保留，部分节点类型会写入 `category` 等元数据。

<a id="_pdf_page"></a>

### 按页读取 PDF

`PagePdfDocumentReader` 使用 Apache PdfBox 库解析 PDF 文档。

<a id="_dependencies_3"></a>

#### 依赖

通过 Maven 或 Gradle 添加依赖。

**Maven：**

```xml
<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>spring-ai-pdf-document-reader</artifactId>
</dependency>
```

**Gradle：**

```groovy
dependencies {
    implementation 'org.springframework.ai:spring-ai-pdf-document-reader'
}
```

<a id="_example_6"></a>

#### 示例

```java
@Component
public class MyPagePdfDocumentReader {

	List<Document> getDocsFromPdf() {

		PagePdfDocumentReader pdfReader = new PagePdfDocumentReader("classpath:/sample1.pdf",
				PdfDocumentReaderConfig.builder()
					.withPageTopMargin(0)
					.withPageExtractedTextFormatter(ExtractedTextFormatter.builder()
						.withNumberOfTopTextLinesToDelete(0)
						.build())
					.withPagesPerDocument(1)
					.build());

		return pdfReader.read();
    }

}
```

<a id="_pdf_paragraph"></a>

### 按段落读取 PDF

`ParagraphPdfDocumentReader` 根据 PDF 的目录信息（如 TOC）将输入 PDF 切分为文本段落，每个段落生成一个 `Document`。

注意：并非所有 PDF 都包含目录信息。

<a id="_dependencies_4"></a>

#### 依赖

通过 Maven 或 Gradle 添加依赖。

**Maven：**

```xml
<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>spring-ai-pdf-document-reader</artifactId>
</dependency>
```

**Gradle：**

```groovy
dependencies {
    implementation 'org.springframework.ai:spring-ai-pdf-document-reader'
}
```

<a id="_example_7"></a>

#### 示例

```java
@Component
public class MyPagePdfDocumentReader {

	List<Document> getDocsFromPdfWithCatalog() {

        ParagraphPdfDocumentReader pdfReader = new ParagraphPdfDocumentReader("classpath:/sample1.pdf",
                PdfDocumentReaderConfig.builder()
                    .withPageTopMargin(0)
                    .withPageExtractedTextFormatter(ExtractedTextFormatter.builder()
                        .withNumberOfTopTextLinesToDelete(0)
                        .build())
                    .withPagesPerDocument(1)
                    .build());

	    return pdfReader.read();
    }
}
```

<a id="_tika_docx_pptx_html"></a>

### Tika（DOCX、PPTX、HTML 等）

`TikaDocumentReader` 使用 Apache Tika 从 PDF、DOC/DOCX、PPT/PPTX、HTML 等多种格式中提取文本。完整格式列表见 [Tika 文档](https://tika.apache.org/3.1.0/formats.html)。

<a id="_dependencies_5"></a>

#### 依赖

通过 Maven 或 Gradle 添加依赖。

**Maven：**

```xml
<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>spring-ai-tika-document-reader</artifactId>
</dependency>
```

**Gradle：**

```groovy
dependencies {
    implementation 'org.springframework.ai:spring-ai-tika-document-reader'
}
```

<a id="_example_8"></a>

#### 示例

```java
@Component
class MyTikaDocumentReader {

    private final Resource resource;

    MyTikaDocumentReader(@Value("classpath:/word-sample.docx")
                            Resource resource) {
        this.resource = resource;
    }

    List<Document> loadText() {
        TikaDocumentReader tikaDocumentReader = new TikaDocumentReader(this.resource);
        return tikaDocumentReader.read();
    }
}
```

<a id="_transformers"></a>

## 四、转换器（切分是重点）

<a id="_textsplitter"></a>

### TextSplitter

`TextSplitter` 是文本切分的抽象基类，用于将文档拆分到适合 AI 模型上下文窗口的大小。

分块边界与语义完整性的取舍，结合下文 [TokenTextSplitter 参数](#_parameters_4)和[注意事项](#_notes_3)理解，重点关注 Token 数、字符长度与标点断句的区别。下面介绍 Spring AI 的具体实现。

<a id="_tokentextsplitter"></a>

### TokenTextSplitter

`TokenTextSplitter` 实现了 `TextSplitter`，按词元（Token）数量切分文本。它支持配置编码类型，如 `CL100K_BASE`、`P50K_BASE`、`O200K_BASE`，默认使用 `CL100K_BASE`。

<a id="_usage"></a>

#### 用法

<a id="_basic_usage"></a>

##### 基本用法

```java
@Component
class MyTokenTextSplitter {

    public List<Document> splitDocuments(List<Document> documents) {
        TokenTextSplitter splitter = TokenTextSplitter.builder().build();
        return splitter.apply(documents);
    }

    public List<Document> splitCustomized(List<Document> documents) {
        TokenTextSplitter splitter = TokenTextSplitter.builder()
            .withChunkSize(1000)
            .withMinChunkSizeChars(400)
            .withMinChunkLengthToEmbed(10)
            .withMaxNumChunks(5000)
            .withKeepSeparator(true)
            .build();
        return splitter.apply(documents);
    }
}
```

<a id="_custom_encoding_type"></a>

##### 自定义编码类型

可以指定分词编码类型，适配使用不同分词器的模型：

```java
TokenTextSplitter splitter = TokenTextSplitter.builder()
    .withEncodingType(EncodingType.O200K_BASE)
    .withChunkSize(1000)
    .build();
```

<a id="_custom_punctuation_marks"></a>

##### 自定义标点

可以指定用于切分的标点，让文本块尽量保留完整语义，尤其适合多语言内容：

```java
@Component
class MyInternationalTextSplitter {

    public List<Document> splitChineseText(List<Document> documents) {
        // Use Chinese punctuation marks
        TokenTextSplitter splitter = TokenTextSplitter.builder()
            .withChunkSize(800)
            .withMinChunkSizeChars(350)
            .withPunctuationMarks(List.of('。', '？', '！', '；'))  // Chinese punctuation
            .build();

        return splitter.apply(documents);
    }

    public List<Document> splitWithCustomMarks(List<Document> documents) {
        // Mix of English and other punctuation marks
        TokenTextSplitter splitter = TokenTextSplitter.builder()
            .withChunkSize(800)
            .withPunctuationMarks(List.of('.', '?', '!', '\n', ';', ':', '。'))
            .build();

        return splitter.apply(documents);
    }
}
```

<a id="_configuration_2"></a>

#### 配置

使用 `TokenTextSplitter.builder()` 创建实例。所有构造器均已弃用，改用 Builder。

<a id="_parameters_4"></a>

#### 参数

- `encodingType`：分词器使用的编码类型，默认为 `CL100K_BASE`。支持 `CL100K_BASE`、`P50K_BASE`、`O200K_BASE` 等。
- `chunkSize`：每个文本块的目标 Token 数，默认为 800。
- `minChunkSizeChars`：按标点截断时使用的字符位置阈值，默认为 350；只有断点位置大于该值才截断，不保证每块至少有 350 个字符。
- `minChunkLengthToEmbed`：纳入结果的文本块最小长度，默认为 5；实际按 Java `String.length()` 比较，且必须严格大于该值。
- `maxNumChunks`：单段文本主切分循环的最大次数，默认为 10000；循环结束后仍可能追加剩余文本块，详见后面的注意事项。
- `keepSeparator`：是否保留换行符等分隔符，默认为 `true`。
- `punctuationMarks`：用于识别句子边界的字符列表，默认为 `.`、`?`、`!`、`\n`。

<a id="_behavior_4"></a>

#### 处理流程

`TokenTextSplitter` 按以下步骤处理文本：

1. 使用所配置的编码将输入文本编码为 Token，默认为 `CL100K_BASE`。
2. 根据 `chunkSize` 将 Token 序列分块。
3. 逐块处理：
   1. 将 Token 解码为文本。
   2. **仅当 Token 总数超过块大小时**，才尝试在 `minChunkSizeChars` 之后，依据配置的 `punctuationMarks` 查找合适的断点。
   3. 找到断点后，在该位置截断文本块。
   4. 去除文本块首尾空白，并根据 `keepSeparator` 决定是否移除换行符。
   5. 文本块长度大于 `minChunkLengthToEmbed` 时，将其加入输出。
4. 重复处理，直到全部 Token 处理完毕或达到 `maxNumChunks`。
5. 剩余文本的长度大于 `minChunkLengthToEmbed` 时，作为最后一个文本块加入结果。

:::note
只有 Token 数超过块大小时，才会按标点进一步切分。Token 数等于或小于块大小的文本不再按标点截断；去除首尾空白后仍须满足 `minChunkLengthToEmbed` 条件，才能进入结果。
:::

<a id="_example_9"></a>

#### 示例

```java
Document doc1 = new Document("This is a long piece of text that needs to be split into smaller chunks for processing.",
        Map.of("source", "example.txt"));
Document doc2 = new Document("Another document with content that will be split based on token count.",
        Map.of("source", "example2.txt"));

TokenTextSplitter splitter = TokenTextSplitter.builder().build();
List<Document> splitDocuments = splitter.apply(List.of(doc1, doc2));

for (Document doc : splitDocuments) {
    System.out.println("Chunk: " + doc.getText());
    System.out.println("Metadata: " + doc.getMetadata());
}
```

<a id="_notes_3"></a>

#### 注意事项

- `TokenTextSplitter` 使用 `jtokkit`，默认编码为 `CL100K_BASE`，也可以选择 `P50K_BASE`、`O200K_BASE`。应选择与目标模型匹配的编码，不能把默认编码当作所有模型通用的 Token 计数器。
- 切分器会尽可能在句子边界处断开，保留文本块的语义完整性。
- 原文档的元数据会复制到该文档生成的所有文本块。
- `copyContentFormatter` 为 `true` 时，原文档设置的内容格式化器也会复制到派生文本块；这是默认行为。
- 该切分器适合为有 Token 上限的模型准备输入，但 `chunkSize` 不是整个请求的上下文预算；还要为提示词、其他检索文档和输出预留空间。达到 `maxNumChunks` 后，剩余文本仍会追加为最后一块，可能超过 `chunkSize`，结果数量也可能比 `maxNumChunks` 多一块。
- **自定义标点**：默认标点（`.`、`?`、`!`、`\n`）适合英文。其他语言或特殊内容可通过 Builder 的 `withPunctuationMarks()` 自定义。
- **性能**：标点数量没有硬性限制，但每个文本块都要逐个检查标点，建议将列表控制在 20 个字符以内。
- **扩展**：`getLastPunctuationIndex(String)` 是 `protected` 方法，子类可重写它，为特殊场景定制标点检测逻辑。
- **短文本**：从 2.0 版开始，Token 数不超过块大小的文本不再按标点切分，避免将已符合大小要求的内容进一步碎片化。

<a id="_contentformattransformer"></a>

### ContentFormatTransformer

用于统一所有文档的内容格式。

<a id="_keywordmetadataenricher"></a>

### KeywordMetadataEnricher

`KeywordMetadataEnricher` 是 `DocumentTransformer` 的实现，使用生成式 AI 模型从文档内容中提取关键词，并将其写入元数据。

下面同时展示默认模板与自定义模板两种配置，实际使用时选择一种；示例返回 `enricher` 的处理结果，若选择自定义模板则使用 `customEnricher`。

<a id="_usage_2"></a>

#### 用法

```java
@Component
class MyKeywordEnricher {

    private final ChatModel chatModel;

    MyKeywordEnricher(ChatModel chatModel) {
        this.chatModel = chatModel;
    }

    List<Document> enrichDocuments(List<Document> documents) {
        KeywordMetadataEnricher enricher = KeywordMetadataEnricher.builder(chatModel)
                .keywordCount(5)
                .build();

        // Or use custom templates
        KeywordMetadataEnricher customEnricher = KeywordMetadataEnricher.builder(chatModel)
               .keywordsTemplate(new PromptTemplate("Extract keywords from:\n{context_str}"))
               .build();

        return enricher.apply(documents);
    }
}
```

<a id="_constructor_options_3"></a>

#### 构造器

`KeywordMetadataEnricher` 提供两种构造器：

1. `KeywordMetadataEnricher(ChatModel chatModel, int keywordCount)`：使用默认模板，提取指定数量的关键词。
2. `KeywordMetadataEnricher(ChatModel chatModel, PromptTemplate keywordsTemplate)`：使用自定义关键词提取模板。

<a id="_behavior_5"></a>

#### 处理流程

`KeywordMetadataEnricher` 按以下步骤处理文档：

1. 为每个输入文档，根据其内容构造提示词。
2. 将提示词发送给指定的 `ChatModel`，生成关键词。
3. 将生成的关键词写入文档元数据的 `excerpt_keywords` 字段。
4. 返回增强后的文档。

<a id="_customization"></a>

#### 自定义

可以使用默认模板，也可以通过 `keywordsTemplate` 参数指定模板，模板变量的用法见 [PromptTemplate](/frameworks/spring-ai/core/prompts/#prompttemplate将模板转换为提示词)。默认模板如下：

```text
{context_str}. Give %s unique keywords for this document. Format as comma separated. Keywords:
```

其中，`{context_str}` 会替换为文档内容，`%s` 会替换为指定的关键词数量。

<a id="_example_10"></a>

#### 示例

```java
// chatModel is an already configured ChatModel
KeywordMetadataEnricher enricher = KeywordMetadataEnricher.builder(chatModel)
                .keywordCount(5)
                .build();

// Or use custom templates
KeywordMetadataEnricher customEnricher = KeywordMetadataEnricher.builder(chatModel)
                .keywordsTemplate(new PromptTemplate("Extract 5 important keywords from the following text and separate them with commas:\n{context_str}"))
                .build();

Document doc = new Document("This is a document about artificial intelligence and its applications in modern technology.");

List<Document> enrichedDocs = enricher.apply(List.of(doc));

Document enrichedDoc = enrichedDocs.get(0);
String keywords = (String) enrichedDoc.getMetadata().get("excerpt_keywords");
System.out.println("Extracted keywords: " + keywords);
```

<a id="_notes_4"></a>

#### 注意事项

- `KeywordMetadataEnricher` 需要可用的 `ChatModel` 来生成关键词。
- 关键词数量必须大于或等于 1。
- 每个处理后的文档都会新增 `excerpt_keywords` 元数据字段。
- 生成的关键词以逗号分隔的字符串返回。
- 该转换器适合改善文档的可检索性，以及为文档生成标签或分类。
- 使用 Builder 时，若设置了 `keywordsTemplate`，则忽略 `keywordCount`。

<a id="_summarymetadataenricher"></a>

### SummaryMetadataEnricher

`SummaryMetadataEnricher` 是 `DocumentTransformer` 的实现，使用生成式 AI 模型生成文档摘要，并写入元数据。它既能生成当前文档的摘要，也能为文档补充相邻文档（前一篇、后一篇）的摘要。

<a id="_usage_3"></a>

#### 用法

```java
@Configuration
class EnricherConfig {

    @Bean
    public SummaryMetadataEnricher summaryMetadata(OpenAiChatModel aiClient) {
        return new SummaryMetadataEnricher(aiClient,
            List.of(SummaryType.PREVIOUS, SummaryType.CURRENT, SummaryType.NEXT));
    }
}

@Component
class MySummaryEnricher {

    private final SummaryMetadataEnricher enricher;

    MySummaryEnricher(SummaryMetadataEnricher enricher) {
        this.enricher = enricher;
    }

    List<Document> enrichDocuments(List<Document> documents) {
        return this.enricher.apply(documents);
    }
}
```

<a id="_constructor"></a>

#### 构造器

`SummaryMetadataEnricher` 提供两种构造器：

1. `SummaryMetadataEnricher(ChatModel chatModel, List<SummaryType> summaryTypes)`
2. `SummaryMetadataEnricher(ChatModel chatModel, List<SummaryType> summaryTypes, String summaryTemplate, MetadataMode metadataMode)`

<a id="_parameters_5"></a>

#### 参数

- `chatModel`：用于生成摘要的 AI 模型。
- `summaryTypes`：需要生成的摘要类型，由 `SummaryType` 枚举值组成，可选 `PREVIOUS`、`CURRENT`、`NEXT`。
- `summaryTemplate`：自定义摘要生成模板，可选。
- `metadataMode`：生成摘要时如何处理文档元数据，可选。

<a id="_behavior_6"></a>

#### 处理流程

`SummaryMetadataEnricher` 按以下步骤处理文档：

1. 为每个输入文档，根据文档内容和指定的摘要模板构造提示词。
2. 将提示词发送给指定的 `ChatModel`，生成摘要。
3. 根据 `summaryTypes`，向每个文档写入以下元数据：
   - `section_summary`：当前文档的摘要。
   - `prev_section_summary`：前一篇文档的摘要；仅在前一篇存在且请求了该类型时添加。
   - `next_section_summary`：后一篇文档的摘要；仅在后一篇存在且请求了该类型时添加。
4. 返回增强后的文档。

<a id="_customization_2"></a>

#### 自定义

通过 `summaryTemplate` 可以自定义摘要生成提示词。默认模板如下：

```java
"""
Here is the content of the section:
{context_str}

Summarize the key topics and entities of the section.

Summary:
"""
```

<a id="_example_11"></a>

#### 示例

```java
// chatModel is an already configured ChatModel
SummaryMetadataEnricher enricher = new SummaryMetadataEnricher(chatModel,
    List.of(SummaryType.PREVIOUS, SummaryType.CURRENT, SummaryType.NEXT));

Document doc1 = new Document("Content of document 1");
Document doc2 = new Document("Content of document 2");

List<Document> enrichedDocs = enricher.apply(List.of(doc1, doc2));

// Check the metadata of the enriched documents
for (Document doc : enrichedDocs) {
    System.out.println("Current summary: " + doc.getMetadata().get("section_summary"));
    System.out.println("Previous summary: " + doc.getMetadata().get("prev_section_summary"));
    System.out.println("Next summary: " + doc.getMetadata().get("next_section_summary"));
}
```

该示例的预期行为如下：

- 列表包含两篇文档，两篇都会获得 `section_summary`。
- 第一篇文档有 `next_section_summary`，没有 `prev_section_summary`。
- 第二篇文档有 `prev_section_summary`，没有 `next_section_summary`。
- 第一篇文档的 `section_summary` 与第二篇文档的 `prev_section_summary` 相同。
- 第一篇文档的 `next_section_summary` 与第二篇文档的 `section_summary` 相同。

<a id="_notes_5"></a>

#### 注意事项

- `SummaryMetadataEnricher` 需要可用的 `ChatModel` 来生成摘要。
- 文档列表的长度不限；转换器会处理首篇、末篇文档等边界情况。
- 该转换器适合生成包含相邻上下文的摘要，帮助理解一组有序文档之间的关系。
- `MetadataMode` 决定生成摘要时，如何将已有元数据纳入提示词。

<a id="_writers"></a>

## 五、写入器（入库与调试）

<a id="_file"></a>

### 文件写入

`FileDocumentWriter` 是 `DocumentWriter` 的实现，将一组 `Document` 对象的内容写入文件。

<a id="_usage_4"></a>

#### 用法

```java
@Component
class MyDocumentWriter {

    public void writeDocuments(List<Document> documents) {
        FileDocumentWriter writer = new FileDocumentWriter("output.txt", true, MetadataMode.ALL, false);
        writer.accept(documents);
    }
}
```

<a id="_constructors"></a>

#### 构造器

`FileDocumentWriter` 提供三种构造器：

1. `FileDocumentWriter(String fileName)`
2. `FileDocumentWriter(String fileName, boolean withDocumentMarkers)`
3. `FileDocumentWriter(String fileName, boolean withDocumentMarkers, MetadataMode metadataMode, boolean append)`

<a id="_parameters_6"></a>

#### 参数

- `fileName`：输出文件名。
- `withDocumentMarkers`：是否在输出中加入文档标记，默认为 `false`。
- `metadataMode`：指定写入文件的文档内容，默认为 `MetadataMode.NONE`。
- `append`：为 `true` 时追加到文件末尾；为 `false` 时覆盖已有文件内容，默认为 `false`。

<a id="_behavior_7"></a>

#### 处理流程

`FileDocumentWriter` 按以下步骤写入文档：

1. 根据指定的文件名打开 `FileWriter`。
2. 遍历输入列表中的文档：
   1. `withDocumentMarkers` 为 `true` 时，写入包含文档索引和页码的文档标记。
   2. 根据 `metadataMode` 写入格式化后的文档内容。
3. 全部文档写入后关闭文件。

<a id="_document_markers"></a>

#### 文档标记

`withDocumentMarkers` 为 `true` 时，写入器会为每个文档添加以下格式的标记：

```
### Doc: [index], pages:[start_page_number,end_page_number]
```

<a id="_metadata_handling"></a>

#### 元数据处理

写入器使用以下两个元数据字段生成文档标记：

- `page_number`：文档的起始页码。
- `end_page_number`：文档的结束页码。

<a id="_example_12"></a>

#### 示例

```java
// documents is an already initialized List<Document>
FileDocumentWriter writer = new FileDocumentWriter("output.txt", true, MetadataMode.ALL, true);
writer.accept(documents);
```

该示例将所有文档写入 `output.txt`，包含文档标记及全部可用元数据。如果文件已经存在，则追加写入。

<a id="_notes_6"></a>

#### 注意事项

- 写入器使用 `FileWriter`，采用 JVM 的默认字符集；现代 JDK 通常为 UTF-8，不能简单假定它等于操作系统本地编码。
- 写入出错时，抛出 `RuntimeException`，并将原始异常作为其原因。
- `metadataMode` 决定如何将已有元数据纳入写入内容。
- 该写入器适合调试，或将一组文档输出为便于阅读的文本。

<a id="_vectorstore"></a>

### VectorStore

`VectorStore` 承接 ETL 的加载阶段，将文档交给具体向量存储实现，通常由该实现调用配置的 Embedding 模型生成向量，再存储文档、向量和元数据。普通 `FileDocumentWriter` 只写文本文件，不会建立向量检索索引。

向量存储与相似度检索的基本用法，见[向量存储总览：API 概览](/frameworks/spring-ai/rag/vector-stores/#api-overview)。完整后端列表与阅读顺序见[向量存储实现](/frameworks/spring-ai/rag/vector-stores/#_vectorstore_implementations)，具体接入可从 [PGvector](/frameworks/spring-ai/rag/vector-stores/pgvector/) 开始。

来源：[Spring AI ETL Pipeline](https://docs.spring.io/spring-ai/reference/api/etl-pipeline.html)。文档版本：2.0.2；核验日期：2026-11-01。
