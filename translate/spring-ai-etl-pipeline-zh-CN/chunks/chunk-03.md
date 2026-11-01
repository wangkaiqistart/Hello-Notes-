#### Document Markers

When `withDocumentMarkers` is set to true, the writer includes markers for each document in the following format:

```
### Doc: [index], pages:[start_page_number,end_page_number]
```

<a id="_metadata_handling"></a>

#### Metadata Handling

The writer uses two specific metadata keys:

- `page_number`: Represents the starting page number of the document.
- `end_page_number`: Represents the ending page number of the document.

These are used when writing document markers.

<a id="_example_12"></a>

#### Example

```java
List<Document> documents = // initialize your documents
FileDocumentWriter writer = new FileDocumentWriter("output.txt", true, MetadataMode.ALL, true);
writer.accept(documents);
```

This will write all documents to "output.txt", including document markers, using all available metadata, and appending to the file if it already exists.

<a id="_notes_6"></a>

#### Notes

- The writer uses `FileWriter`, so it writes text files with the default character encoding of the operating system.
- If an error occurs during writing, a `RuntimeException` is thrown with the original exception as its cause.
- The `metadataMode` parameter allows control over how existing metadata is incorporated into the written content.
- This writer is particularly useful for debugging or creating human-readable outputs of document collections.

<a id="_vectorstore"></a>

### VectorStore

Provides integration with various vector stores.
See [Vector DB Documentation](https://docs.spring.io/spring-ai/reference/api/vectordbs.html) for a full listing.