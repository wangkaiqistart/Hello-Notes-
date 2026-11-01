#### Example

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

### PDF Paragraph

The `ParagraphPdfDocumentReader` uses the PDF catalog (e.g. TOC) information to split the input PDF into text paragraphs and output a single `Document` per paragraph.
NOTE: Not all PDF documents contain the PDF catalog.

<a id="_dependencies_4"></a>

#### Dependencies

Add the dependency to your project using Maven or Gradle.

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

#### Example

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

### Tika (DOCX, PPTX, HTML…​)

The `TikaDocumentReader` uses Apache Tika to extract text from a variety of document formats, such as PDF, DOC/DOCX, PPT/PPTX, and HTML. For a comprehensive list of supported formats, refer to the [Tika documentation](https://tika.apache.org/3.1.0/formats.html).

<a id="_dependencies_5"></a>

#### Dependencies

Add the dependency to your project using Maven or Gradle.

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

#### Example

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

## Transformers

<a id="_textsplitter"></a>

### TextSplitter

The `TextSplitter` an abstract base class that helps divides documents to fit the AI model’s context window.

<a id="_tokentextsplitter"></a>

### TokenTextSplitter

The `TokenTextSplitter` is an implementation of `TextSplitter` that splits text into chunks based on token count. It supports configurable encoding types (e.g., `CL100K_BASE`, `P50K_BASE`, `O200K_BASE`) and defaults to `CL100K_BASE`.

<a id="_usage"></a>

#### Usage

<a id="_basic_usage"></a>

##### Basic Usage

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

##### Custom Encoding Type

You can configure the encoding type used for tokenization. This is useful when working with models that use different tokenizers:

```java
TokenTextSplitter splitter = TokenTextSplitter.builder()
    .withEncodingType(EncodingType.O200K_BASE)
    .withChunkSize(1000)
    .build();
```

<a id="_custom_punctuation_marks"></a>

##### Custom Punctuation Marks

You can customize the punctuation marks used for splitting text into semantically meaningful chunks. This is particularly useful for internationalization:

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

#### Configuration

Use `TokenTextSplitter.builder()` to create instances. All constructors are deprecated in favor of the builder.

<a id="_parameters_4"></a>

#### Parameters

- `encodingType`: The tokenizer encoding type to use (default: `CL100K_BASE`). Supported values include `CL100K_BASE`, `P50K_BASE`, and `O200K_BASE`.
- `chunkSize`: The target size of each text chunk in tokens (default: 800).
- `minChunkSizeChars`: The minimum size of each text chunk in characters (default: 350).
- `minChunkLengthToEmbed`: The minimum length of a chunk to be included (default: 5).
- `maxNumChunks`: The maximum number of chunks to generate from a text (default: 10000).
- `keepSeparator`: Whether to keep separators (like newlines) in the chunks (default: true).
- `punctuationMarks`: List of characters to use as sentence boundaries for splitting (default: `.`, `?`, `!`, `\n`).

<a id="_behavior_4"></a>

#### Behavior

The `TokenTextSplitter` processes text content as follows:

1. It encodes the input text into tokens using the CL100K_BASE encoding.
2. It splits the encoded text into chunks based on the `chunkSize`.
3. For each chunk:

   1. It decodes the chunk back into text.
   2. **Only if the total token count exceeds the chunk size**, it attempts to find a suitable break point (using the configured `punctuationMarks`) after the `minChunkSizeChars`.
   3. If a break point is found, it truncates the chunk at that point.
   4. It trims the chunk and optionally removes newline characters based on the `keepSeparator` setting.
   5. If the resulting chunk is longer than `minChunkLengthToEmbed`, it’s added to the output.
4. This process continues until all tokens are processed or `maxNumChunks` is reached.
5. Any remaining text is added as a final chunk if it’s longer than `minChunkLengthToEmbed`.

:::note
Punctuation-based splitting only applies when the token count exceeds the chunk size. Text that exactly matches or is smaller than the chunk size is returned as a single chunk without punctuation-based truncation. This prevents unnecessary splitting of small texts.
:::

<a id="_example_9"></a>

#### Example

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

#### Notes

- The `TokenTextSplitter` uses the CL100K_BASE encoding from the `jtokkit` library, which is compatible with newer OpenAI models.
- The splitter attempts to create semantically meaningful chunks by breaking at sentence boundaries where possible.
- Metadata from the original documents is preserved and copied to all chunks derived from that document.
- The content formatter (if set) from the original document is also copied to the derived chunks if `copyContentFormatter` is set to `true` (default behavior).
- This splitter is particularly useful for preparing text for large language models that have token limits, ensuring that each chunk is within the model’s processing capacity.
- **Custom Punctuation Marks**: The default punctuation marks (`.`, `?`, `!`, `\n`) work well for English text. For other languages or specialized content, customize the punctuation marks using the builder’s `withPunctuationMarks()` method.
- **Performance Consideration**: While the splitter can handle any number of punctuation marks, it’s recommended to keep the list reasonably small (under 20 characters) for optimal performance, as each mark is checked for every chunk.
- **Extensibility**: The `getLastPunctuationIndex(String)` method is `protected`, allowing subclasses to override the punctuation detection logic for specialized use cases.
- **Small Text Handling**: As of version 2.0, small texts (with token count at or below the chunk size) are no longer split at punctuation marks, preventing unnecessary fragmentation of content that already fits within the size limits.

<a id="_contentformattransformer"></a>

### ContentFormatTransformer

Ensures uniform content formats across all documents.

<a id="_keywordmetadataenricher"></a>

### KeywordMetadataEnricher

The `KeywordMetadataEnricher` is a `DocumentTransformer` that uses a generative AI model to extract keywords from document content and add them as metadata.

<a id="_usage_2"></a>

#### Usage

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

#### Constructor Options

The `KeywordMetadataEnricher` provides two constructor options:

1. `KeywordMetadataEnricher(ChatModel chatModel, int keywordCount)`: To use the default template and extract a specified number of keywords.
2. `KeywordMetadataEnricher(ChatModel chatModel, PromptTemplate keywordsTemplate)`: To use a custom template for keyword extraction.

<a id="_behavior_5"></a>

#### Behavior

The `KeywordMetadataEnricher` processes documents as follows:

1. For each input document, it creates a prompt using the document’s content.
2. It sends this prompt to the provided `ChatModel` to generate keywords.
3. The generated keywords are added to the document’s metadata under the key "excerpt_keywords".
4. The enriched documents are returned.

<a id="_customization"></a>

#### Customization

You can use the default template or customize the template through the keywordsTemplate parameter.
The default template is:

```java
\{context_str}. Give %s unique keywords for this document. Format as comma separated. Keywords:
```

Where `{context_str}` is replaced with the document content, and `%s` is replaced with the specified keyword count.

<a id="_example_10"></a>

#### Example

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

#### Notes

- The `KeywordMetadataEnricher` requires a functioning `ChatModel` to generate keywords.
- The keyword count must be 1 or greater.
- The enricher adds the "excerpt_keywords" metadata field to each processed document.
- The generated keywords are returned as a comma-separated string.
- This enricher is particularly useful for improving document searchability and for generating tags or categories for documents.
- In the Builder pattern, if the `keywordsTemplate` parameter is set, the `keywordCount` parameter will be ignored.

<a id="_summarymetadataenricher"></a>

### SummaryMetadataEnricher

The `SummaryMetadataEnricher` is a `DocumentTransformer` that uses a generative AI model to create summaries for documents and add them as metadata. It can generate summaries for the current document, as well as adjacent documents (previous and next).

<a id="_usage_3"></a>

#### Usage

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

#### Constructor

The `SummaryMetadataEnricher` provides two constructors:

1. `SummaryMetadataEnricher(ChatModel chatModel, List<SummaryType> summaryTypes)`
2. `SummaryMetadataEnricher(ChatModel chatModel, List<SummaryType> summaryTypes, String summaryTemplate, MetadataMode metadataMode)`

<a id="_parameters_5"></a>

#### Parameters

- `chatModel`: The AI model used for generating summaries.
- `summaryTypes`: A list of `SummaryType` enum values indicating which summaries to generate (PREVIOUS, CURRENT, NEXT).
- `summaryTemplate`: A custom template for summary generation (optional).
- `metadataMode`: Specifies how to handle document metadata when generating summaries (optional).

<a id="_behavior_6"></a>

#### Behavior

The `SummaryMetadataEnricher` processes documents as follows:

1. For each input document, it creates a prompt using the document’s content and the specified summary template.
2. It sends this prompt to the provided `ChatModel` to generate a summary.
3. Depending on the specified `summaryTypes`, it adds the following metadata to each document:

   - `section_summary`: Summary of the current document.
   - `prev_section_summary`: Summary of the previous document (if available and requested).
   - `next_section_summary`: Summary of the next document (if available and requested).
4. The enriched documents are returned.

<a id="_customization_2"></a>

#### Customization

The summary generation prompt can be customized by providing a custom `summaryTemplate`. The default template is:

```java
"""
Here is the content of the section:
{context_str}

Summarize the key topics and entities of the section.

Summary:
"""
```

<a id="_example_11"></a>

#### Example

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

The provided example demonstrates the expected behavior:

- For a list of two documents, both documents receive a `section_summary`.
- The first document receives a `next_section_summary` but no `prev_section_summary`.
- The second document receives a `prev_section_summary` but no `next_section_summary`.
- The `section_summary` of the first document matches the `prev_section_summary` of the second document.
- The `next_section_summary` of the first document matches the `section_summary` of the second document.

<a id="_notes_5"></a>

#### Notes

- The `SummaryMetadataEnricher` requires a functioning `ChatModel` to generate summaries.
- The enricher can handle document lists of any size, properly handling edge cases for the first and last documents.
- This enricher is particularly useful for creating context-aware summaries, allowing for better understanding of document relationships in a sequence.
- The `MetadataMode` parameter allows control over how existing metadata is incorporated into the summary generation process.

<a id="_writers"></a>

## Writers

<a id="_file"></a>

### File

The `FileDocumentWriter` is a `DocumentWriter` implementation that writes the content of a list of `Document` objects into a file.

<a id="_usage_4"></a>

#### Usage

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

#### Constructors

The `FileDocumentWriter` provides three constructors:

1. `FileDocumentWriter(String fileName)`
2. `FileDocumentWriter(String fileName, boolean withDocumentMarkers)`
3. `FileDocumentWriter(String fileName, boolean withDocumentMarkers, MetadataMode metadataMode, boolean append)`

<a id="_parameters_6"></a>

#### Parameters

- `fileName`: The name of the file to write the documents to.
- `withDocumentMarkers`: Whether to include document markers in the output (default: false).
- `metadataMode`: Specifies what document content to be written to the file (default: MetadataMode.NONE).
- `append`: If true, data will be written to the end of the file rather than the beginning (default: false).

<a id="_behavior_7"></a>

#### Behavior

The `FileDocumentWriter` processes documents as follows:

1. It opens a FileWriter for the specified file name.
2. For each document in the input list:

   1. If `withDocumentMarkers` is true, it writes a document marker including the document index and page numbers.
   2. It writes the formatted content of the document based on the specified `metadataMode`.
3. The file is closed after all documents have been written.

<a id="_document_markers"></a>