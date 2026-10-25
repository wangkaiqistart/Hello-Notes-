# 翻译上下文

目标：简体中文。读者：熟悉 Java / Spring Boot 的开发者。风格：精确简明、自然中文、少注释、不写翻译过程旁白。

# 内容分析

## 范围与风格

来源为 Spring AI 2.0.2 参考文档，面向开发者。沿用项目简体中文、精翻、简明技术文档风格。保留 API 名称、提示词字符串、配置键、代码与原图关系。

## 术语

- Structured Output → 结构化输出
- Provider-Native Structured Output → 提供方原生结构化输出
- Output Converter → 输出转换器
- JSON Schema → 保留名称，描述结构约束
- fallback → 回退；best effort → 尽力而为

## 重点与难点

原生路径通过 API 传递 Schema；StructuredOutputChatOptions 不支持时静默回退；支持模型清单以文档版本为界，不写成所有后续型号一概支持。保留默认关闭理由、Ollama 推理文本问题、OpenAI 顶层数组限制、全局与逐次开关、提供方 JSON 模式。区分有效 JSON 与符合具体 Schema，不把原生约束写成无条件可靠。

准确覆盖全部段落与代码。先保存初稿，再逐段对照来源审校。合并进现有结构化输出篇时复用已有示例与解释，以正文锚点承接重复内容；保留来源与审校证据。图片保留原有节点、连线和配色，仅中文化说明及校正明确的旧 API 标签。
