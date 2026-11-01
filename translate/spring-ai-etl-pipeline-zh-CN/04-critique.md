# 审校记录

## 准确性

- 初稿保留来源全部 41 个代码块、全部 83 个小节锚点和 3 张图片；代码未改动，正式计数见验证清单。
- Document 旧图与正文过时：2.0.2 的 Document 不继承 Content/MediaContent；text 与单个 Media 必须二选一，正文用 getText()、getMedia()。保留原图并明确其仅用于结构示意。
- JSON Pointer 示例、文本切分示例错误引用 this.jsonReader/this.documents；改为已声明的局部变量。
- JSON 示例数组与 /store/books/0 不是同一结构，需明确二者独立，数组可用 /0。
- JsonReader 先 readTree() 完整载入再用 Java Stream 遍历；来源的“大文件流式读取”说法不成立。正文区分遍历方式与流式解析，并补充字段名加值及回退到完整对象的实际行为。
- TextReader 的 source 优先为文件名，无文件名时还会依次回退到 URI、URL 或资源描述。
- Markdown 读取器保留内容、代码文本和部分元数据，但不保留 Markdown 原始排版；includeCodeBlock/includeBlockquote=false 表示分离而非丢弃。标题元数据按实际 visitor 解释。
- TokenTextSplitter 流程不应固定写 CL100K_BASE，改为“所配置的编码，默认 CL100K_BASE”。minChunkLengthToEmbed 比较的是 Java String.length()；maxNumChunks 达到后还有剩余文本块，不能宣称严格上限或保证不超过模型容量。
- TokenTextSplitter 示例的 getContent() 改为 2.0.2 的 getText()。
- KeywordMetadataEnricher 两处示例在同一作用域重复声明 enricher：保留两种配置，第二种使用 customEnricher 名称；用途说明为二选一。
- 关键词示例的 this.doc/this.enrichedDocs/this.enrichedDoc 与摘要示例的 this.doc1/this.doc2 均改为局部变量；未初始化的 ChatModel 占位改为假定上下文已注入该对象。
- 关键词默认模板源码无反斜杠，去掉源文档展示中的转义符；按文本而非 Java 程序高亮。
- FileWriter 使用 JVM 默认字符集，现代 JDK 一般为 UTF-8，不能简单写成操作系统决定；append=false 是覆盖而非“从开头追加”。

## 中文表达

- 统一“构造器”“处理流程”“注意事项”，避免分块译名不一致。
- 增加阅读路线与 Reader 选型表；完整参数、行为、示例不删减。
- Maven 与 Gradle 的标签分别放到对应代码前，不保留来源 tabs 扁平化产生的无意义列表。

## 图片与边界

- 3 张 JPG 保留来源字节和比例，不重画；提供准确中文替代文本、用途说明、简短图注与原尺寸链接。
- Document API 图过时，图前明确当前实现，避免把旧关系看作当前 API。
- 页面示例仍为 API 片段，需要已配置的 VectorStore、模型及 Resource。只做源码静态核验和页面验证，不冒称端到端 RAG 实测。

## 定稿补充

- 所有 83 个源小节锚点保留。TokenTextSplitter 参数表对标点阈值与主循环次数补充精确语义。
- Prettier 将 HTML 示例中的空元素改为自闭合写法，语义不变；列入代码对照，不记为 API 修正。
- 关键词、摘要与文件写入示例仍依赖已注入对象，是 API 片段而非完整独立程序。
