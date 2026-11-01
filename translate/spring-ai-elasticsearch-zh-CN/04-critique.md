# 审校记录

1. 保留Boot<3.3/elasticsearch-java8.13.3两段代码，明确历史定位与原文文字“>8.13.3”和示例不一致；不是当前Spring AI2.0.2配套建议。
2. Rest5Client的HttpHost使用Apache HttpComponents5构造顺序(scheme,host,port)，按Boot4.1.2 RestClientConfigurations核对，修正手动片段。
3. SimilarityFunction枚举为小写cosine，源COSINE无定义；改为SimilarityFunction.cosine。Options维度默认1536，不从模型推断；OpenAI改builder().build()。
4. 自动配置内部new Options并映射properties，不注入单独Options Bean；改为明确手动传入.options(options)。已有索引时直接返回，不验证/迁移mapping，正文说明维度/度量需自行对齐。
5. Spring Boot4.1.2属性类仍保留restclient.sniffer和ssl前缀，不臆改为rest5client。socketKeepAlive默认true而非来源false；保留来源值说明并按实际默认校正。sniffer默认enabled=false，间隔参数不自动启用探测。
6. Filters.g4允许QuotedIdentifier，源'article_type'字段引用合法，不作为语法错误修订。转换器IN输出field:("a" OR "b")，修正原文将第二项移出字段作用域的Lucene结果。
7. dot_product以实际向量单位归一化为前提，不能用品牌保证；保留dense_vector上游说明。
8. 全部6源章节、15代码块、15配置项保留；BOM/仓库、Embedding、元数据过滤复用站内；ES客户端/dense_vector/部署与版本来源保留外链。
