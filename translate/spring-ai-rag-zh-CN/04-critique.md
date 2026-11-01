# 审校记录

## 准确性

- 保留全部 26 个小节锚点和 21 段代码；初稿代码与源 HTML 对应代码一致。
- `StPromptTemplate` 是来源中的旧称；2.0.2 的 `PromptTemplate` 实际默认使用 `StTemplateRenderer`，修正正文。
- 来源说 `userTextAdvise()` 已弃用，但 2.0.2 Builder 已无该方法；改为说明旧版入口与当前 `.promptTemplate()` 的关系。
- 已核实 `VectorStoreChatMemoryAdvisor` 仍在 2.0.2 的 vector-store-advisor 模块中，可保留依赖说明。
- 动态过滤示例声明局部 `chatClient` 后误用 `this.chatClient`；统一局部变量。
- `ConcatenationDocumentJoiner` 按 Document ID 去重、保留先遇到的文档，再按原始分数降序排列；补全来源省略的实际排序语义。
- 默认空上下文只改变提示词，不停止模型调用；保持初稿准确表述。
- 请求级条件覆盖检索器条件；补充不自动 AND，以及租户条件必须来自可信上下文的工程说明。

## 中文表达

- 一级内容标为“RAG Advisor（重点掌握）”与“模块参考（按需深入）”。保留所有原层级，不缩略内容。
- 先说明两种 Advisor 的适用场景、ETL 前置条件、调用链与阅读路线，避免把进阶模块当作必须配置。
- 模块表用于定位职责，避免初学者混淆查询改写与检索文档填充。

## 说明与边界

- 增补内容标为学习路线、选型或工程判断；不承诺自动引用来源、绝对拒答或数据授权。
- 示例的阈值与 Top-K 保留，说明它们是示例值。
- API 依据为 spring-projects/spring-ai 的 v2.0.2 标签源码；仅静态对照，不宣称编译或模型实测。

## 定稿补充

- 保留 26 个源小节锚点；增加构建器模块入口定位，不额外引入示例代码块。
- 查询转换的 temperature 建议限定为提供方支持时使用，默认值不作统一假定。
