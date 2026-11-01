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
List<Document> documents = // initialize your documents
FileDocumentWriter writer = new FileDocumentWriter("output.txt", true, MetadataMode.ALL, true);
writer.accept(documents);
```

该示例将所有文档写入 `output.txt`，包含文档标记及全部可用元数据。如果文件已经存在，则追加写入。

<a id="_notes_6"></a>

#### 注意事项

- 写入器使用 `FileWriter`，按操作系统的默认字符编码写入文本文件。
- 写入出错时，抛出 `RuntimeException`，并将原始异常作为其原因。
- `metadataMode` 决定如何将已有元数据纳入写入内容。
- 该写入器适合调试，或将一组文档输出为便于阅读的文本。

<a id="_vectorstore"></a>

### VectorStore

集成多种向量存储。完整列表见[向量数据库文档](https://docs.spring.io/spring-ai/reference/api/vectordbs.html)。
