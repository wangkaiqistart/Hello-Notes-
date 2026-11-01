# 审校记录

1. 原文Redis许可证描述不涵盖所有发行版，正文采用中性介绍并保留历史描述边界。
2. 原文配置表与v2.0.2属性类不一致：自动配置index/prefix默认default-index/default:，builder默认spring-ai-index/embedding:；HNSW实际属性hnsw.m/ef-construction/ef-runtime；distanceMetric/vectorAlgorithm/range/textScorer仅builder提供，完整保留来源各参数并标出实际入口。
3. 语义缓存属性类没有host/port，连接由JedisConnectionFactory读取spring.data.redis；修正YAML并逐项说明旧键无效。
4. 手动Embedding示例改为OpenAiEmbeddingModel.builder().build()，依赖OPENAI_API_KEY自动检测；不再使用错误的构造形式。补声明后文category TAG元数据；暴露RedisVectorStore具体类型供扩展方法使用。
5. searchByRange第三参数在v2.0.2直接拼接原生Redis条件，不是通用DSL；改为@category:{AI}。它没有显式分页遍历，不保证返回全部匹配；IP小阈值回退topK1000。searchByText仅对简单等值作特殊处理，不当作完整通用过滤器。
6. 距离归一化以源码公式说明，文本分数无$score时回退0.9；不能将该值当实测相关性或跨算法统一置信度。
7. defaultRangeThreshold构建器默认未设置，来源表0.8只是示例值。支持半径转换但参数含义是归一化相似度阈值，值越高越严格。
8. 默认Langcache模型依赖TransformersEmbeddingModel在类路径，首次准备需要获取模型资源，不是无条件可用。
9. 缓存仅更换indexName仍共享相同key前缀；同时指定独立indexName/prefix，说明并非数据库授权。
10. system prompt哈希不包括历史/权限/模型/工具结果；null上下文不会添加过滤，不保证与带系统提示词缓存分开；正文修正来源过度承诺。缓存命中取决于实际阈值，不能承诺必命中。
11. distanceThreshold(d)按1-d/2换算，similarityThreshold(s)越高越严格。部分set重载查重直接使用存储值，优先用相似度模式，距离代码保留作API参考。
12. TTL重载在RedisVectorStore上调用expire；Advisor默认set上下文重载无TTL，不自动给全部回答过期。clear针对整个索引可见记录，不是当前用户。
13. 保留全部24源章节、33源代码块和16行来源参数，增加校正说明而不删除主题。
