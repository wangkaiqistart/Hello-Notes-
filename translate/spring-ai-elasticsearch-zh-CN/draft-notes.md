# Elasticsearch 初稿待审校问题

初稿保留6个源章节锚点、15个代码块、全部15项配置参数及来源链接；代码块原样保留，未修改站点或导航。

1. Boot<3.3.0兼容说明与Spring AI 2.0.2当前配套并不一致，已经标明为历史说明；来源称依赖版本>8.13.3而示例使用8.13.3，需保留其历史定位并由主代理核对当前BOM。
2. 手动Rest5Client示例的HttpHost构造器仍是旧客户端参数顺序，需核对Apache HttpComponents 5的HttpHost构造形式。
3. 手动OpenAiEmbeddingModel构造器与options.apiKey形式需按当前版本源码校正，可沿用前篇已核对的builder().build()与凭据准备说明。
4. 字符串过滤表达式将article_type放在单引号中；需要检查通用DSL对字段名称引用的支持，可能应去掉引号。
5. Elasticsearch过滤转换示例(metadata.author:john OR jill)可能丢失第二项的字段限定，应按ElasticsearchFilterExpressionConverter实际输出核对。
6. 配置表restclient.sniffer/ssl字段可能属于旧版客户端，当前Rest5Client与Boot版本的参数前缀需核对。
7. ElasticsearchVectorStoreOptions Bean是否由当前自动配置接收、维度默认与模型推断逻辑是否与表中1536一致需核对源码。
8. 点积要求单位向量不能仅由提供方品牌保证；维度、归一化与已有索引mapping一致性应明确。
9. 未编译Java示例，未连接Elasticsearch或模型；全部判断留主代理源码审校。
