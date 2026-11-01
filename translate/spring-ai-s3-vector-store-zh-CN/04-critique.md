# 审校记录

1. 使用AWS S3 Vectors专用向量桶/索引，普通S3对象接口不可替代。源文套用“hashes/JSON”概述，按SDK向量记录+metadata说明。
2. S3VectorStoreProperties两个字段均Nullable且无默认，自动配置构造器要求非null；原表spring-ai-index/my-vector-bucket-on-aws是示例，不是实际默认资源。保留示例并明确必填。
3. afterPropertiesSet无建索引逻辑；必须先准备向量桶和索引，保证区域、维度、距离类型与模型一致，不能沿用其他实现initialize-schema开关。
4. 源手动构造引用未定义properties/yourConverter；改为@Value注入真实配置，显式保留默认转换器/扩展点，补S3VectorsClient Bean（区域读AWS_REGION，凭据交SDK默认链），OpenAI改builder。
5. 核对过滤转换为AWS SDK Document；过滤删除maxResults500，本地判定后按500键分批删除，不是服务端原子过滤删除。
6. 重要适配边界：doAdd写入向量键、data、metadata，没有文档原文；toDocument把vector.key放进text，未恢复原id或score，距离放入SPRING_AI_S3_DISTANCE；doSimilaritySearch未使用similarityThreshold，基类亦不追加阈值过滤。正文添加清楚的版本限定说明，不能把它当作原文已完整回填的RAG后端。
7. 全部7源章节、13代码块、2配置参数与来源引用保留；BOM/仓库、Embedding、统一过滤使用站内链接，无等价的AWS资源/SDK文档保留外链。
