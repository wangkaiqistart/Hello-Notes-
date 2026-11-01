## Example Usage

To compute the embeddings for a vector database, you need to pick an embedding model that matches the higher-level AI model being used.

For example, with OpenAI’s ChatGPT, we use the `OpenAiEmbeddingModel` and a model named `text-embedding-ada-002`.

The Spring Boot starter’s auto-configuration for OpenAI makes an implementation of `EmbeddingModel` available in the Spring application context for dependency injection.

<a id="_writing_to_a_vector_store"></a>

### Writing to a Vector Store

The general usage of loading data into a vector store is something you would do in a batch-like job, by first loading data into Spring AI’s `Document` class and then calling the `add` method on the `VectorStore` interface.

Given a `String` reference to a source file that represents a JSON file with data we want to load into the vector database, we use Spring AI’s `JsonReader` to load specific fields in the JSON, which splits them up into small pieces and then passes those small pieces to the vector store implementation. The `VectorStore` implementation computes the embeddings and stores the JSON and the embedding in the vector database:

```java
@Autowired
VectorStore vectorStore;

void load(String sourceFile) {
    JsonReader jsonReader = new JsonReader(new FileSystemResource(sourceFile),
            "price", "name", "shortDescription", "description", "tags");
    List<Document> documents = jsonReader.get();
    this.vectorStore.add(documents);
}
```

<a id="_reading_from_a_vector_store"></a>

### Reading from a Vector Store

Later, when a user question is passed into the AI model, a similarity search is done to retrieve similar documents, which are then "stuffed" into the prompt as context for the user’s question.

For read-only operations, you can use either the `VectorStore` interface or the more focused `VectorStoreRetriever` interface:

```java
@Autowired
VectorStoreRetriever retriever; // Could also use VectorStore here

String question = "<question from user>";
List<Document> similarDocuments = retriever.similaritySearch(question);

// Or with more specific search parameters
SearchRequest request = SearchRequest.builder()
    .query(question)
    .topK(5)                       // Return top 5 results
    .similarityThreshold(0.7)      // Only return results with similarity score >= 0.7
    .build();

List<Document> filteredDocuments = retriever.similaritySearch(request);
```

Additional options can be passed into the `similaritySearch` method to define how many documents to retrieve and a threshold of the similarity search.

<a id="_separation_of_read_and_write_operations"></a>

### Separation of Read and Write Operations

Using the separate interfaces allows you to clearly define which components need write access and which only need read access:

```java
// Write operations in a service that needs full access
@Service
class DocumentIndexer {
    private final VectorStore vectorStore;

    DocumentIndexer(VectorStore vectorStore) {
        this.vectorStore = vectorStore;
    }

    public void indexDocuments(List<Document> documents) {
        vectorStore.add(documents);
    }
}

// Read-only operations in a service that only needs retrieval
@Service
class DocumentRetriever {
    private final VectorStoreRetriever retriever;

    DocumentRetriever(VectorStoreRetriever retriever) {
        this.retriever = retriever;
    }

    public List<Document> findSimilar(String query) {
        return retriever.similaritySearch(query);
    }
}
```

This separation of concerns helps create more maintainable and secure applications by limiting access to mutation operations only to components that truly need them.

<a id="_retrieval_operations_with_vectorstoreretriever"></a>

## Retrieval Operations with VectorStoreRetriever

The `VectorStoreRetriever` interface provides a read-only view of a vector store, exposing only the similarity search functionality. This follows the principle of least privilege and is particularly useful in RAG (Retrieval-Augmented Generation) applications where you only need to retrieve documents without modifying the underlying data.

<a id="_benefits_of_using_vectorstoreretriever"></a>

### Benefits of Using VectorStoreRetriever

- **Separation of Concerns**: Clearly separates read operations from write operations.
 
- **Interface Segregation**: Clients that only need retrieval functionality aren’t exposed to mutation methods.
 
- **Functional Interface**: Can be implemented with lambda expressions or method references for simple use cases.
 
- **Reduced Dependencies**: Components that only need to perform searches don’t need to depend on the full `VectorStore` interface.
     

<a id="_example_usage_2"></a>

### Example Usage

You can use `VectorStoreRetriever` directly when you only need to perform similarity searches:

```java
@Service
public class DocumentRetrievalService {

    private final VectorStoreRetriever retriever;

    public DocumentRetrievalService(VectorStoreRetriever retriever) {
        this.retriever = retriever;
    }

    public List<Document> findSimilarDocuments(String query) {
        return retriever.similaritySearch(query);
    }

    public List<Document> findSimilarDocumentsWithFilters(String query, String country) {
        SearchRequest request = SearchRequest.builder()
            .query(query)
            .topK(5)
            .filterExpression("country == '" + country + "'")
            .build();

        return retriever.similaritySearch(request);
    }
}
```

In this example, the service only depends on the `VectorStoreRetriever` interface, making it clear that it only performs retrieval operations and doesn’t modify the vector store.

<a id="_integration_with_rag_applications"></a>

### Integration with RAG Applications

The `VectorStoreRetriever` interface is particularly useful in RAG applications, where you need to retrieve relevant documents to provide context for an AI model:

```java
@Service
public class RagService {

    private final VectorStoreRetriever retriever;
    private final ChatModel chatModel;

    public RagService(VectorStoreRetriever retriever, ChatModel chatModel) {
        this.retriever = retriever;
        this.chatModel = chatModel;
    }

    public String generateResponse(String userQuery) {
        // Retrieve relevant documents
        List<Document> relevantDocs = retriever.similaritySearch(userQuery);

        // Extract content from documents to use as context
        String context = relevantDocs.stream()
            .map(Document::getContent)
            .collect(Collectors.joining("\n\n"));

        // Generate response using the retrieved context
        String prompt = "Context information:\n" + context + "\n\nUser query: " + userQuery;
        return chatModel.generate(prompt);
    }
}
```

This pattern allows for a clean separation between the retrieval component and the generation component in RAG applications.

<a id="metadata-filters"></a>

## Metadata Filters

This section describes various filters that you can use against the results of a query.

<a id="_filter_string"></a>

### Filter String

You can pass in an SQL-like filter expressions as a `String` to one of the `similaritySearch` overloads.

Consider the following examples:

- `"country == 'BG'"`
 
- `"genre == 'drama' && year >= 2020"`
 
- `"genre in ['comedy', 'documentary', 'drama']"`
     

<a id="_filter_expression"></a>

### Filter.Expression

You can create an instance of `Filter.Expression` with a `FilterExpressionBuilder` that exposes a fluent API. A simple example is as follows:

```java
FilterExpressionBuilder b = new FilterExpressionBuilder();
Expression expression = this.b.eq("country", "BG").build();
```

You can build up sophisticated expressions by using the following operators:

```text
EQUALS: '=='
MINUS : '-'
PLUS: '+'
GT: '>'
GE: '>='
LT: '<'
LE: '<='
NE: '!='
```

You can combine expressions by using the following operators:

```text
AND: 'AND' | 'and' | '&&';
OR: 'OR' | 'or' | '||';
```

Considering the following example:

```java
Expression exp = b.and(b.eq("genre", "drama"), b.gte("year", 2020)).build();
```

You can also use the following operators:

```text
IN: 'IN' | 'in';
NIN: 'NIN' | 'nin';
NOT: 'NOT' | 'not';
```

Consider the following example:

```java
Expression exp = b.and(b.in("genre", "drama", "documentary"), b.not(b.lt("year", 2020))).build();
```

You can also use the following operators:

```text
IS: 'IS' | 'is';
NULL: 'NULL' | 'null';
NOT NULL: 'NOT NULL' | 'not null';
```

Consider the following example:

```java
Expression exp = b.and(b.isNull("year")).build();
Expression exp = b.and(b.isNotNull("year")).build();
```

> `IS NULL` and `IS NOT NULL` have not been implemented in all vector stores yet.

<a id="_partitioning_a_shared_index"></a>

### Partitioning a Shared Index

A single vector store is often shared by many logical groups of documents — for example one index holding content for several customers, projects, or knowledge bases. A `VectorStore` operates over the whole index and returns or removes documents based on similarity and the filter you provide, so a filter expression is what selects the group you want to work with.

The approach is to tag each document with metadata that identifies its group when it is written, and then apply a matching filter on searches and deletes:

```java
// When writing, record the group the document belongs to.
Document document = new Document(content, Map.of("group", groupId));
vectorStore.add(List.of(document));

// When searching, select documents from that group.
List<Document> results = vectorStore.similaritySearch(SearchRequest.builder()
    .query(query)
    .filterExpression("group == '" + groupId + "'")
    .build());

// When deleting by filter, target the same group.
Filter.Expression scoped = new FilterExpressionBuilder().eq("group", groupId).build();
vectorStore.delete(scoped);
```

A couple of practices keep the groups cleanly separated:

- Add the identifying metadata to every document at write time, so it is always available to filter on later.
 
- Apply the corresponding filter consistently on searches and deletes so an operation only affects the intended group.
       

<a id="_deleting_documents_from_vector_store"></a>

## Deleting Documents from Vector Store

The Vector Store interface provides multiple methods for deleting documents, allowing you to remove data either by specific document IDs or using filter expressions.

<a id="_delete_by_document_ids"></a>

### Delete by Document IDs

The simplest way to delete documents is by providing a list of document IDs:

```java
void delete(List<String> idList);
```

This method removes all documents whose IDs match those in the provided list. If any ID in the list doesn’t exist in the store, it will be ignored.

   Example usage  

```java
// Create and add document
Document document = new Document("The World is Big",
    Map.of("country", "Netherlands"));
vectorStore.add(List.of(document));

// Delete document by ID
vectorStore.delete(List.of(document.getId()));
```

<a id="_delete_by_filter_expression"></a>

### Delete by Filter Expression

For more complex deletion criteria, you can use filter expressions:

```java
void delete(Filter.Expression filterExpression);
```

This method accepts a `Filter.Expression` object that defines the criteria for which documents should be deleted. It’s particularly useful when you need to delete documents based on their metadata properties.

   Example usage  

```java
// Create test documents with different metadata
Document bgDocument = new Document("The World is Big",
    Map.of("country", "Bulgaria"));
Document nlDocument = new Document("The World is Big",
    Map.of("country", "Netherlands"));

// Add documents to the store
vectorStore.add(List.of(bgDocument, nlDocument));

// Delete documents from Bulgaria using filter expression
Filter.Expression filterExpression = new Filter.Expression(
    Filter.ExpressionType.EQ,
    new Filter.Key("country"),
    new Filter.Value("Bulgaria")
);
vectorStore.delete(filterExpression);

// Verify deletion with search
SearchRequest request = SearchRequest.builder()
    .query("World")
    .filterExpression("country == 'Bulgaria'")
    .build();
List<Document> results = vectorStore.similaritySearch(request);
// results will be empty as Bulgarian document was deleted
```

<a id="_delete_by_string_filter_expression"></a>

### Delete by String Filter Expression

For convenience, you can also delete documents using a string-based filter expression:

```java
void delete(String filterExpression);
```

This method converts the provided string filter into a `Filter.Expression` object internally. It’s useful when you have filter criteria in string format.

   Example usage  

```java
// Create and add documents
Document bgDocument = new Document("The World is Big",
    Map.of("country", "Bulgaria"));
Document nlDocument = new Document("The World is Big",
    Map.of("country", "Netherlands"));
vectorStore.add(List.of(bgDocument, nlDocument));

// Delete Bulgarian documents using string filter
vectorStore.delete("country == 'Bulgaria'");

// Verify remaining documents
SearchRequest request = SearchRequest.builder()
    .query("World")
    .topK(5)
    .build();
List<Document> results = vectorStore.similaritySearch(request);
// results will only contain the Netherlands document
```

<a id="_error_handling_when_calling_the_delete_api"></a>

### Error Handling When Calling the Delete API

All deletion methods may throw exceptions in case of errors:

The best practice is to wrap delete operations in try-catch blocks:

   Example usage  

```java
try {
    vectorStore.delete("country == 'Bulgaria'");
}
catch (Exception  e) {
    logger.error("Invalid filter expression", e);
}
```

<a id="_document_versioning_use_case"></a>

### Document Versioning Use Case

A common scenario is managing document versions where you need to upload a new version of a document while removing the old version. Here’s how to handle this using filter expressions:

   Example usage  

```java
// Create initial document (v1) with version metadata
Document documentV1 = new Document(
    "AI and Machine Learning Best Practices",
    Map.of(
        "docId", "AIML-001",
        "version", "1.0",
        "lastUpdated", "2024-01-01"
    )
);

// Add v1 to the vector store
vectorStore.add(List.of(documentV1));

// Create updated version (v2) of the same document
Document documentV2 = new Document(
    "AI and Machine Learning Best Practices - Updated",
    Map.of(
        "docId", "AIML-001",
        "version", "2.0",
        "lastUpdated", "2024-02-01"
    )
);

// First, delete the old version using filter expression
Filter.Expression deleteOldVersion = new Filter.Expression(
    Filter.ExpressionType.AND,
    new Filter.Expression(
        Filter.ExpressionType.EQ,
        new Filter.Key("docId"),
        new Filter.Value("AIML-001")
    ),
    new Filter.Expression(
        Filter.ExpressionType.EQ,
        new Filter.Key("version"),
        new Filter.Value("1.0")
    )
);
vectorStore.delete(deleteOldVersion);

// Add the new version
vectorStore.add(List.of(documentV2));

// Verify only v2 exists
SearchRequest request = SearchRequest.builder()
    .query("AI and Machine Learning")
    .filterExpression("docId == 'AIML-001'")
    .build();
List<Document> results = vectorStore.similaritySearch(request);
// results will contain only v2 of the document
```

You can also accomplish the same using the string filter expression:

   Example usage  

```java
// Delete old version using string filter
vectorStore.delete("docId == 'AIML-001' AND version == '1.0'");

// Add new version
vectorStore.add(List.of(documentV2));
```

<a id="_performance_considerations_while_deleting_documents"></a>

### Performance Considerations While Deleting Documents

- Deleting by ID list is generally faster when you know exactly which documents to remove.
 
- Filter-based deletion may require scanning the index to find matching documents; however, this is vector store implementation-specific.
 
- Large deletion operations should be batched to avoid overwhelming the system.
 
- Consider using filter expressions when deleting based on document properties rather than collecting IDs first.
       

<a id="_understanding_vectors"></a>

## Understanding Vectors

[Understanding Vectors](https://docs.spring.io/spring-ai/reference/api/vectordbs/understand-vectordbs.html)