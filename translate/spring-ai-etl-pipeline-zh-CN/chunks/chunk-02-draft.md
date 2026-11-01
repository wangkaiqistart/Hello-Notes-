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

- Maven
- Gradle

```xml
<dependency>
    <groupId>org.springframework.ai</groupId>
    <artifactId>spring-ai-tika-document-reader</artifactId>
</dependency>
```

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

## 转换器

<a id="_textsplitter"></a>

### TextSplitter

`TextSplitter` 是文本切分的抽象基类，用于将文档拆分到适合 AI 模型上下文窗口的大小。

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
- `minChunkSizeChars`：每个文本块的最小字符数，默认为 350。
- `minChunkLengthToEmbed`：文本块纳入结果所需的最小长度，默认为 5。
- `maxNumChunks`：单段文本最多生成的块数，默认为 10000。
- `keepSeparator`：是否保留换行符等分隔符，默认为 `true`。
- `punctuationMarks`：用于识别句子边界的字符列表，默认为 `.`、`?`、`!`、`\n`。

<a id="_behavior_4"></a>

#### 处理流程

`TokenTextSplitter` 按以下步骤处理文本：

1. 使用 `CL100K_BASE` 编码将输入文本转换为 Token。
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
只有 Token 数超过块大小时，才会按标点进一步切分。Token 数等于或小于块大小的文本会直接作为一个文本块返回，避免对短文本进行不必要的截断。
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
    System.out.println("Chunk: " + doc.getContent());
    System.out.println("Metadata: " + doc.getMetadata());
}
```

<a id="_notes_3"></a>

#### 注意事项

- `TokenTextSplitter` 使用 `jtokkit` 库的 `CL100K_BASE` 编码，与较新的 OpenAI 模型兼容。
- 切分器会尽可能在句子边界处断开，保留文本块的语义完整性。
- 原文档的元数据会复制到该文档生成的所有文本块。
- `copyContentFormatter` 为 `true` 时，原文档设置的内容格式化器也会复制到派生文本块；这是默认行为。
- 该切分器适合为有 Token 上限的大语言模型准备输入，确保每个文本块位于模型的处理容量内。
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
        KeywordMetadataEnricher enricher = KeywordMetadataEnricher.builder(chatModel)
               .keywordsTemplate(YOUR_CUSTOM_TEMPLATE)
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

可以使用默认模板，也可以通过 `keywordsTemplate` 参数指定模板。默认模板如下：

```java
\{context_str}. Give %s unique keywords for this document. Format as comma separated. Keywords:
```

其中，`{context_str}` 会替换为文档内容，`%s` 会替换为指定的关键词数量。

<a id="_example_10"></a>

#### 示例

```java
ChatModel chatModel = // initialize your chat model
KeywordMetadataEnricher enricher = KeywordMetadataEnricher.builder(chatModel)
                .keywordCount(5)
                .build();

// Or use custom templates
KeywordMetadataEnricher enricher = KeywordMetadataEnricher.builder(chatModel)
                .keywordsTemplate(new PromptTemplate("Extract 5 important keywords from the following text and separate them with commas:\n{context_str}"))
                .build();

Document doc = new Document("This is a document about artificial intelligence and its applications in modern technology.");

List<Document> enrichedDocs = enricher.apply(List.of(this.doc));

Document enrichedDoc = this.enrichedDocs.get(0);
String keywords = (String) this.enrichedDoc.getMetadata().get("excerpt_keywords");
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
ChatModel chatModel = // initialize your chat model
SummaryMetadataEnricher enricher = new SummaryMetadataEnricher(chatModel,
    List.of(SummaryType.PREVIOUS, SummaryType.CURRENT, SummaryType.NEXT));

Document doc1 = new Document("Content of document 1");
Document doc2 = new Document("Content of document 2");

List<Document> enrichedDocs = enricher.apply(List.of(this.doc1, this.doc2));

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

## 写入器

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
- `append`：为 `true` 时，将数据追加到文件末尾，默认为 `false`。

<a id="_behavior_7"></a>

#### 处理流程

`FileDocumentWriter` 按以下步骤写入文档：

1. 根据指定的文件名打开 `FileWriter`。
2. 遍历输入列表中的文档：
   1. `withDocumentMarkers` 为 `true` 时，写入包含文档索引和页码的文档标记。
   2. 根据 `metadataMode` 写入格式化后的文档内容。
3. 全部文档写入后关闭文件。

<a id="_document_markers"></a>
