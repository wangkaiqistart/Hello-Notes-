# Advisors API 审校

## 准确性与代码

- 11 个来源代码块均保留，包括 Re2 模板。源码 HTML 的说明标号 (1)/(2)/(3) 需作为文档标注清除，不能留在 Java 方法体中，初稿已移出并以正文解释。
- 首例局部 chatClient 与 this.chatClient 混用，修订为局部变量；占位初始化保留并说明。
- 末尾流式骨架的两个 map Lambda 缺少返回值，修订时补 return request / return response；这只补全示意数据流，不宣称是可独立运行的应用。
- 来源“实现 Advisor”将 nextCall/nextStream 误写成需要实现的方法。2.0.2 Javadoc 确认应实现 adviseCall/adviseStream，nextCall/nextStream 属于 Chain；译文已更正。
- order 小先请求后响应，同值不保序；不按默认 Advisor 的添加顺序推断执行顺序。
- 聚合器用于完整响应的只读观察，不把汇总回调误写为将响应流改为单个对象。
- 内置 Advisor 全部覆盖，保留实际限制；内容防护不保证绝对安全，Re2 不承诺任意模型效果提升。
- 上下文说明区分当前 record 的 context() 与历史 M3 的 updateContext，不把历史不可变 Map API 当成 2.0.2 当前方法。

## 图与链接

- 保留来源 3 张 JPG，中文版内嵌原图，仅替换图例、步骤及“内部调用”等说明；类型与方法保留英文。
- 顺序对比图旧 Flux<AdvisedResponse> 标签改为 Flux<ChatClientResponse>，流程图裁短的 ChatClientReques 标签修正完整。
- 本地递归工具小节链接在构建后核验锚点；来源页使用的旧锚点不直接照搬。
- 图片在用途解释后引用，提供准确替代文本、短图注和查看大图入口。

## 表达与修订

将重复顺序说明整理为表格，保留核心流程与历史迁移。修订补全示例变量和 map 返回值，添加代码边界说明，最终保留 11 个代码块。
