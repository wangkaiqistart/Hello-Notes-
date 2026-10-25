# 工具调用 Advisor 审校

## 准确性

- strictChecker 的 finishReason 属于首个 Generation 的metadata，不是ChatResponseMetadata；增加空结果保护。
- 审计子类缺构造器，final audit未初始化；补父类构造器调用及字段赋值，补空响应判断。Builder复制时需保留子类和audit字段，补newCopy/copy。
- 观察Advisor缺构造器、getName和logger；按Advisor接口补齐。
- 手动流式两处options需传Builder；补returnDirect分支，最终response携带工具生成结果。
- 使用blockLast等待迭代，明确示例阻塞边界；SSE转发由应用实现。
- 单工具约束是至多一个，自动注册关闭时可为零。记忆Advisor仍需调用时显式会话ID。

## 表达与格式

保留全部12段代码、构建器表、5类钩子和全部章节。原文无图。保留英文锚点便于跨页引用，中文标题便于阅读。

## 证据

../spring-ai-tool-calling-zh-CN/api/ 的ToolCallingAdvisor、DefaultChatClient、Advisor、ChatGenerationMetadata、ToolExecutionResult源码。示例未运行。
