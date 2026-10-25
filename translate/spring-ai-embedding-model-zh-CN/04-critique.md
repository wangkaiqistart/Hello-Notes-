# Embedding 模型审校

## 准确性

已对照来源与 2.0.2 EmbeddingModel Javadoc，确认 float[]、List<float[]>、embedForResponse、getEmbeddingContent 和 dimensions。来源接口中的数组.size()错误未传播到译文，补充示例用 vector.length。

dimensions 默认会请求远端，不一定是本地属性；向量维度、嵌入空间兼容性和重建索引分别说明，不把同维度等同于同一空间。Document 元数据参与方式受具体实现与配置影响。

## 精选范围

省略全部实现源码、继承图与逐家配置，保留方法表和三段最小片段。RAG 分工与索引一致性明确为工程说明。三个片段分开使用，不能直接拼成同一方法。

## 中文表达

将“一定免费”改为“不会一定仅在本地执行”，避免假设本地或远端的计费情况。保留必要输入限制和查询入口。
