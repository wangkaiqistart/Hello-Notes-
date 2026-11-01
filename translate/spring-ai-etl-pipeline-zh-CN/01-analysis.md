# 内容分析

来源：Spring AI 2.0.2，2026-11-01 获取。

## 内容概述

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

## 风格

面向熟悉 Java 与 Spring Boot 的开发者；简体中文，精翻，简明技术文档风格。保留完整参考内容，不缩写成摘要。

## 翻译难点

不要把普通 FileDocumentWriter 说成向量存储。区分 get/read、apply/transform、accept/write 别名及各自返回值。图片沿用原图、绝不重画或加官方水印；图片用途需先由正文解释。保留 JSON Pointer 示例、参数、默认值、安全警告和元数据字段。Tokenizer 默认编码与实际模型编码需要核对；保留未验证代码行为到审校核验。

保留所有源锚点、代码块、代码字符串、链接和表格信息；正文可分层与加少量工程说明，必须与原译文可区分。不把示例阈值写为推荐默认值。
