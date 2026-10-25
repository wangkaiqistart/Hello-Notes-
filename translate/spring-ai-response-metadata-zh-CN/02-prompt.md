# 精翻上下文

将英文 Chat Response Metadata 全文改写为自然、简明的中文技术文档，面向熟悉 Java / Spring Boot 的开发者。保留 5 个主要章节、2 个示例子节、8 段代码和 8 家提供方的缓存支持表；原文无图片，不添加装饰图。

遵循项目词汇：词元（Token）、提示词、响应元数据、限流信息、用量、原生用量、提示词缓存。ChatResponseMetadata、RateLimit、Usage 及所有 API 标识保持原样。仅翻译代码注释，提示词字符串、输出字符串与配置不变。

重点保留 EmptyRateLimit 零值语义、缓存指标 null、多步调用累计与原生对象不能合并的限制。提供方表说明为当前 Spring AI 实现的支持情况。明确 Usage 接口为节选，getTotalTokens 的默认实现不展开。禁止将返回指标写成框架已自动实施限流，也不把 Token 数直接写成金额。保留 OpenAI 的限流、套餐和响应头参考链接。

审校后接入 Starlight：中文标题、说明与 sidebar label，正文从二级标题开始，来源版本与日期放页尾；关联现有 ChatClient、Prompts 页面。保留分析、初稿、审校、修订和定稿文件。
