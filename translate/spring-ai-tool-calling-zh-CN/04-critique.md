# 工具调用审校

## 准确性

- 快速开始的日期获取是给服务器本地时间附上用户时区，不能得到用户时区的真实当前时间；改 ZonedDateTime.now(zone)。闹钟仅打印，明确非真实调度。
- 手动 ChatClient 示例 .options 需要 Builder，改 chatOptions.mutate()；补 returnDirect 分支并构建工具结果响应，避免把直接返回结果再次发给模型。
- ToolAdvisor 校验实际是至多一个，显式禁用自动注册时允许零个；不能绝对称恰好一个。
- 参数描述注解的 Jackson 属性是 value，JsonClassDescription 是类级描述；方法参数优先级为 ToolParam → JsonPropertyDescription → Schema。
- Schema(required=false) 在该版本默认 requiredMode=AUTO 下仍可能判为必填，需 NOT_REQUIRED。
- 结果转换器不在 ToolMetadata 上，使用 @Tool.resultConverter 或回调构建器 toolCallResultConverter。
- 默认异常处理遇 checked/Error 会重新抛 ToolExecutionException 包装，并非原样抛 cause；部分授权运行时异常也会直接重抛。
- 参数扩充中的推理字段只是模型生成的调用理由，不保证代表其真实内部推理；不改变底层工具签名。

## 表达与格式

保留38段代码、6张原图、完整主题与配置。分块衔接连续。重建源转换器摊平的步骤，图片放在说明后。保留来源锚点，链接改站内以便连读。原图英文标签保留，alt中文。

## 证据

api-review-notes.md 及 api/ 中的2.0.2源码。示例仍是片段，不声称编译或实际执行。
