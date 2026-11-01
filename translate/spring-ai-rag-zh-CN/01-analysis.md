# 内容分析

来源：Spring AI 2.0.2，2026-11-01 获取。

## 内容概述

说明两种 RAG Advisor、顺序式基础/进阶流程，以及检索前、检索、检索后、生成四阶段模块。

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

默认空上下文仅通过提示词要求模型不回答，不是 Java 层硬性拒绝。请求级过滤覆盖检索器过滤，不自动合并；租户过滤不可据此当作授权。区分 QueryTransformer 与上下文增强、ChatClient 模板与 Advisor 模板。来源 StPromptTemplate 名称可能与实际 StTemplateRenderer 不一致，暂按来源保留并在审校核验。

保留所有源锚点、代码块、代码字符串、链接和表格信息；正文可分层与加少量工程说明，必须与原译文可区分。不把示例阈值写为推荐默认值。
