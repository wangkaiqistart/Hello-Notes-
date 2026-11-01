# 翻译上下文

目标：将英文 Spring AI 2.0.2 文档完整改写成自然、简明的简体中文开发者文档。

## 背景

说明 Document 数据载体、Reader/Transformer/Writer 三类函数式接口，JSON、文本、HTML、Markdown、PDF、Tika 读取器，切分与元数据增强，以及文件与向量存储写入。

## 术语

| English                                        | 中文约定                                                  |
| ---------------------------------------------- | --------------------------------------------------------- |
| Retrieval Augmented Generation                 | 检索增强生成（RAG）                                       |
| Query / Query Transformation / Query Expansion | 查询 / 查询转换 / 查询扩展                                |
| Query Augmentation                             | 查询增强（把检索结果补入查询）                            |
| Pre-Retrieval / Post-Retrieval                 | 检索前处理 / 检索后处理                                   |
| Document / metadata                            | 文档 / 元数据；Java 类型名保留                            |
| Embedding                                      | 嵌入（Embedding），内容的向量表示；生成向量的过程称向量化 |
| chunk / TextSplitter                           | 文本块 / 文本切分器                                       |
| ETL Pipeline                                   | ETL 管道（抽取、转换、加载）                              |
| Reader / Transformer / Writer                  | 读取器 / 转换器 / 写入器                                  |
| reranking / similarity threshold               | 重排序 / 相似度阈值                                       |
| top-k                                          | Top-K（最多返回的结果数）                                 |
| Token                                          | 词元（Token）；后文保留 Token                             |
| Advisor / ChatClient / VectorStore             | 保留 API 名称                                             |
| Supplier / Function / Consumer                 | 保留 Java 接口名，不译为普通业务角色                      |

## 约束与难点

不要把普通 FileDocumentWriter 说成向量存储。区分 get/read、apply/transform、accept/write 别名及各自返回值。图片沿用原图、绝不重画或加官方水印；图片用途需先由正文解释。保留 JSON Pointer 示例、参数、默认值、安全警告和元数据字段。Tokenizer 默认编码与实际模型编码需要核对；保留未验证代码行为到审校核验。

保持原有结构及所有 <a id="..."> 锚点，保留代码块数量及顺序。代码内容原样保留（包括注释和字符串），仅翻译代码前后的说明。不得替换 API 名称、URL、路径、参数名、属性名或默认值。链接可保留绝对来源 URL。图片引用先保留来源 URL，后续由主代理本地化路径。译文不出现“本次翻译、原文说、翻译说明”等写作旁白。原文尚无答案的内容不擅自添加承诺。疑似错误保留到审校，不在初稿默改。

长句可拆为短句，译文精简表达但保留全部事实、条件、异常分支、警告与参数参考。只写正文，不加 frontmatter 或额外总结。
