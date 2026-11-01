# 审校记录

完整核对来源正文、两块初译及 api/ 中 v2.0.2 源码。初译保留 32 个源代码块与 34 个章节锚点，无源图片。

## 准确性与源码修订

1. 自定义 TokenCountEstimator 示例声明局部 customEstimator，却传入 this.customEstimator：应使用局部变量。
2. 手动 PgVectorStore 构造示例接收 BatchingStrategy，却没有 .batchingStrategy(batchingStrategy)：补齐显式设置。
3. 源文称自定义策略 Bean 会自动用于所有 EmbeddingModel，过度概括。已核对 PgVectorStoreAutoConfiguration 注入策略，PgVectorStore.doAdd 将它传入 EmbeddingModel.embed；手动构建不能依赖仅声明 Bean 生效。
4. VectorStoreRetriever 是接口层面的只读限制，不构成数据库授权和租户隔离；保留初译的准确边界。
5. 不能要求 Embedding 模型“匹配生成模型”：应保证文档与查询向量空间兼容及存储维度一致。初译已修正。
6. JsonReader 提取字段不等于按 Token 切分；初译已修正，保留 ETL 站内引用。
7. RagService 使用旧 Document::getContent 和不存在的 chatModel.generate(String)：改为 getText、call，过滤空文本，并说明简化流程不包含完整拒答/引用逻辑。
8. FilterExpressionBuilder 示例定义局部 b 却用 this.b：改为 b；Expression 加 Filter. 前缀使类型明确。
9. b.and 需要两个 Op；单条件 isNull/isNotNull 示例去掉无效 and 包裹，分别使用不同变量名。
10. country 和 groupId 作为值时用 FilterExpressionBuilder.eq 生成条件，避免手动拼接和引用转义问题；保留字符串 DSL 固定字面量示例。
11. 删除异常可能来自后端而非只有过滤表达式错误，日志消息应描述删除失败；保留异常处理主题。
12. 缺失 ID 通常可忽略，但接口本身不保证所有后端一致。相似度搜索验证例仅限隔离测试数据，不能把空检索当成完整删除证明。
13. 先删旧版再写新版的步骤不具原子性；标明失败后的数据缺口，不把示例当事务保障。
14. 自动截断示例 132900 / 20000 和 5–10 倍建议仅属源文特定情景。预算调整不会改变模型单条/批次上限；正文保留相关内容，明确先切分为常规方案。
15. 默认 TokenCountBatchingStrategy 按 Math.round(max*(1-reserve)) 计算预算；默认 8191 与 10% 是策略默认，不能视为全部模型共同限制。8191*0.9 四舍五入为7372，不复用源码Javadoc中7371的算术错误。

## 中文和结构

- 原文长参考内容完整保留；新增阅读路线标注 API、基本读写、过滤为初读重点，批处理与删除作为进阶参考。
- 介绍中出现的 Word2Vec、GloVe、BERT 保留历史示例定位，不当作当前接入推荐清单。
- 消除源自 HTML 的列表空白和重复“使用示例”缩进，保留注释与所有代码主题。
- 模型名和默认策略参数属于2.0.2文档示例，不伪装成最新提供方承诺。

## 子目录与链接

- 导航列出21个后端子页，正文实现列表有18个后端加 SimpleVectorStore；补充导航中的 Azure Cosmos DB、Amazon Bedrock Knowledge Base、Couchbase 三个入口，并保留外部 Cosmos 模块说明。
- 以原理与 Spring AI 接入区分 Chroma 既有笔记，不拿 Python 页面替换 Java 后端配置。
- 详细翻译顺序：总览本次完成，PGvector下一篇，Chroma备选；其他19个后端按实际使用选择，不批量翻译重复配置。
- Understanding Vectors 的基础内容由站内 Embedding 和相似度笔记承接，数学推导保留来源链接；不会称其为已完整翻译。
- 提供方参数、数学推导、历史模型背景与原始出处无等价站内页面时保留外链，并在 README 记录。
