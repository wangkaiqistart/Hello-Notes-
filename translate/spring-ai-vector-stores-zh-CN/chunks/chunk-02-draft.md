## 使用示例

向量入库前，需要配置合适的 Embedding 模型。文档向量与查询向量必须处于兼容的向量空间；Embedding 模型不必与生成回答的模型来自同一提供方。

例如，使用 OpenAI 的 ChatGPT 生成回答时，可以用 `OpenAiEmbeddingModel` 和 `text-embedding-ada-002` 生成向量。这里的模型名沿用原示例，实际接入时应选择提供方当前支持的模型。

OpenAI 的 Spring Boot starter 会自动配置 `EmbeddingModel`，供应用通过依赖注入使用。模型职责与向量空间要求见 [Embedding 模型](/frameworks/spring-ai/models/embedding-model/)。

<a id="_writing_to_a_vector_store"></a>

### 写入向量存储

文档入库通常放在批量导入任务中：先读取资料并生成 Spring AI 的 `Document`，再调用 `VectorStore.add()`。

下面通过 `JsonReader` 从 JSON 文件读取指定字段并生成文档，再交给向量存储实现调用 Embedding 模型，保存文档与向量。`sourceFile` 是源文件路径。若文档过长，还需要显式进行文本切分；读取字段不等于已经按 Token 限制分块。读取与切分见 [ETL 管道](/frameworks/spring-ai/rag/document-ingestion/)。

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

### 查询向量存储

用户提问时，先执行相似度检索，找出相关文档，再把文档内容补充到提示词中，作为模型回答问题的上下文。

只需要查询时，可以使用 `VectorStore`，也可以依赖职责更明确的 `VectorStoreRetriever`：

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

通过 `SearchRequest` 为 `similaritySearch()` 指定返回数量和相似度阈值。上例最多返回 5 个结果，并要求相似度达到 `0.7`。

<a id="_separation_of_read_and_write_operations"></a>

### 分离读写职责

分别依赖两个接口，可以明确哪些组件需要写入能力，哪些组件只负责检索：

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

这种职责划分把修改数据的方法限制在确实需要它的组件中，有助于维护应用。这里限制的是 Java 接口暴露的能力；数据库权限与数据隔离仍需单独配置。

<a id="_retrieval_operations_with_vectorstoreretriever"></a>

## 使用 VectorStoreRetriever 检索

`VectorStoreRetriever` 提供向量存储的只读视图，只暴露相似度检索功能。RAG 的在线问答链路通常只需要读取资料，可以依赖这一接口，避免耦合写入和删除方法。

<a id="_benefits_of_using_vectorstoreretriever"></a>

### 为什么使用只读接口

- **职责分离**：明确区分读取与写入。
 
- **接口隔离**：只负责检索的调用方无需接触数据修改方法。
 
- **函数式接口**：简单场景下可用 Lambda 表达式或方法引用实现。
 
- **减少依赖**：只做查询的组件无需依赖完整的 `VectorStore`。
     

<a id="_example_usage_2"></a>

### 使用示例

只做相似度检索时，直接注入 `VectorStoreRetriever`：

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

这个服务只依赖 `VectorStoreRetriever`，因此从接口上就能看出它只检索文档，不修改向量存储。

<a id="_integration_with_rag_applications"></a>

### 集成到 RAG 应用

在 RAG 应用中，用检索器找出相关文档，再将文档文本作为上下文交给聊天模型：

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

这样可以将检索组件与生成组件分开。需要接入 Advisor 时，见 [RAG 的检索与生成](/frameworks/spring-ai/rag/retrieval-and-generation/)。

<a id="metadata-filters"></a>

## 元数据过滤

除了向量相似度，还可以按 `Document` 的元数据限定检索范围。以下两种写法最终都生成过滤表达式。

<a id="_filter_string"></a>

### 字符串表达式

通过 `SearchRequest.filterExpression(String)` 传入类似 SQL 条件的字符串，再交给 `similaritySearch()`。

例如：

- `"country == 'BG'"`
 
- `"genre == 'drama' && year >= 2020"`
 
- `"genre in ['comedy', 'documentary', 'drama']"`
     

<a id="_filter_expression"></a>

### Filter.Expression

`FilterExpressionBuilder` 提供链式 API，用于构建 `Filter.Expression`：

```java
FilterExpressionBuilder b = new FilterExpressionBuilder();
Expression expression = this.b.eq("country", "BG").build();
```

比较与数值符号包括：

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

使用以下逻辑运算符组合表达式：

```text
AND: 'AND' | 'and' | '&&';
OR: 'OR' | 'or' | '||';
```

例如，选择类型为 `drama` 且年份不早于 2020 的文档：

```java
Expression exp = b.and(b.eq("genre", "drama"), b.gte("year", 2020)).build();
```

还支持以下运算符：

```text
IN: 'IN' | 'in';
NIN: 'NIN' | 'nin';
NOT: 'NOT' | 'not';
```

例如：

```java
Expression exp = b.and(b.in("genre", "drama", "documentary"), b.not(b.lt("year", 2020))).build();
```

还支持以下运算符：

```text
IS: 'IS' | 'is';
NULL: 'NULL' | 'null';
NOT NULL: 'NOT NULL' | 'not null';
```

例如：

```java
Expression exp = b.and(b.isNull("year")).build();
Expression exp = b.and(b.isNotNull("year")).build();
```

> 并非所有向量存储都支持 `IS NULL` 和 `IS NOT NULL`，使用前应核对对应实现。

<a id="_partitioning_a_shared_index"></a>

### 在共享索引中划分文档组

一个向量索引可能同时存放多个客户、项目或知识库的资料。`VectorStore` 面向整个索引执行操作；需要通过过滤条件限定本次搜索或删除所属的文档组。

写入时，为每个文档添加分组元数据；查询和删除时，使用匹配的过滤条件：

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

保持分组清晰，需要同时做到：

- 每个文档写入时都带上分组标识，确保后续有字段可供过滤。
 
- 查询和删除都一致地添加分组过滤，避免操作落到其他组。
       

<a id="_deleting_documents_from_vector_store"></a>

## 删除向量存储中的文档

`VectorStore` 提供按文档 ID 和按元数据过滤条件删除的方法。

<a id="_delete_by_document_ids"></a>

### 按文档 ID 删除

已知文档 ID 时，直接传入 ID 列表：

```java
void delete(List<String> idList);
```

该方法删除 ID 与列表匹配的文档；列表中不存在的 ID 会被忽略。

   使用示例：  

```java
// Create and add document
Document document = new Document("The World is Big",
    Map.of("country", "Netherlands"));
vectorStore.add(List.of(document));

// Delete document by ID
vectorStore.delete(List.of(document.getId()));
```

<a id="_delete_by_filter_expression"></a>

### 按 Filter.Expression 删除

需要按多个条件删除时，使用过滤表达式：

```java
void delete(Filter.Expression filterExpression);
```

`Filter.Expression` 定义待删除文档的条件，适合按元数据属性批量删除。

   使用示例：  

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

### 按字符串表达式删除

也可以直接传入字符串过滤条件：

```java
void delete(String filterExpression);
```

该方法会在内部将字符串转换为 `Filter.Expression`，适合过滤条件本身就是字符串的场景。

   使用示例：  

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

### 处理删除异常

删除方法遇到错误时可能抛出异常。

可使用 `try-catch` 捕获并处理删除失败：

   使用示例：  

```java
try {
    vectorStore.delete("country == 'Bulgaria'");
}
catch (Exception  e) {
    logger.error("Invalid filter expression", e);
}
```

<a id="_document_versioning_use_case"></a>

### 文档版本管理

更新文档时，常常需要删除旧版本，再写入新版本。可以通过业务文档标识与版本元数据定位旧数据：

   使用示例：  

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

同样的操作也可以用字符串表达式完成：

   使用示例：  

```java
// Delete old version using string filter
vectorStore.delete("docId == 'AIML-001' AND version == '1.0'");

// Add new version
vectorStore.add(List.of(documentV2));
```

<a id="_performance_considerations_while_deleting_documents"></a>

### 删除操作的性能取舍

- 已知具体文档 ID 时，按 ID 列表删除通常更直接、速度更快。
 
- 按过滤条件删除可能需要扫描索引以找到匹配文档，具体代价取决于向量存储的实现。
 
- 大量删除应分批执行，避免一次操作给系统造成过大压力。
 
- 按文档属性清理数据时，可直接使用过滤表达式，无需先搜集全部 ID。
       

<a id="_understanding_vectors"></a>

## 理解向量

基础概念可先看本站的 [Embedding 基础](/basics/embedding/embedding-basics/)与 [Chroma：相似度怎么理解](/rag/vector-db/chroma-vector-store/#相似度怎么理解)。Chroma 笔记使用 Python 示例，这里只引用其原理说明；需要向量几何和距离推导时，再查 [Understanding Vectors](https://docs.spring.io/spring-ai/reference/api/vectordbs/understand-vectordbs.html)。