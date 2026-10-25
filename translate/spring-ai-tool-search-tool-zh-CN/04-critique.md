# 工具搜索审校

## 准确性

- maxResults是模型未给值时的回退，不是强制上限；双方均未给值时Regex/Lucene/Vector默认10，工具描述提示5仅为提示。配置表同步澄清。
- RegexToolIndex将自然语言查询分词、移除停用词、转义后组成不区分大小写的OR模式，匹配名称与summary，名称匹配权重2倍。不可把get_*当glob使用。
- 索引会在工具集合指纹变化时重建，不应绝对声称会话只建立一次。
- tenantId为索引分组键，不能自动实现用户鉴权或逐会话隔离。
- 快速开始混排@Bean方法和局部构建代码，提示toolIndex指已注入的Bean。
- 55,000+Token与34–64%降幅是特定案例/基准，保留来源引用不当普遍保证。

## 表达与格式

保留17段代码、1张来源图、完整属性表和策略；图片放步骤说明之后，保留来源字节。

## 证据

../spring-ai-tool-calling-zh-CN/api/ 的ToolSearchTool、RegexToolIndex、LuceneToolIndex、VectorToolIndex、ToolSearchAdvisorProperties及ToolSearchAdvisorAutoConfiguration。

## 渲染复核

来源 Gradle 代码标为 gradle，但当前站点高亮器不支持该语言名；改为 groovy，仅调整两个代码围栏标记，代码内容不变。
