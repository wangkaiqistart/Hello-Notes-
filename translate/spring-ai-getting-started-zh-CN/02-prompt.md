# 翻译上下文

源语言：英文。目标语言：简体中文。模式：refined。读者：熟悉 Java 与 Spring Boot 的开发者，每周 10–15 小时学习 Spring AI。风格：简明技术文档。

## 内容背景

本文是 Spring AI 2.0.2 Getting Started，重点是版本、依赖仓库与 BOM。整篇翻译，不分块，不扩写成完整应用教程。

## 术语

Artifact Repositories → 依赖仓库；Releases → 正式版；Snapshots → 快照版（SNAPSHOT）；Mirror → 镜像仓库；Bill of Materials → 依赖版本清单（BOM）；Dependency Management → 依赖管理；Vector Store → 向量存储；Embedding Model → 嵌入模型；Starter 保留英文。

## 翻译约束

保留全部 8 个代码块、URL、坐标、镜像匹配表达式及全部 6 类组件入口。XML 和 Groovy 注释可以翻译，代码结构不变。保留 BOM 2.0.0 并注明它是来源示例，与文档版本 2.0.2 分开。不要凭记忆增加 JDK 版本、模型 API Key、Controller 或声称示例已执行。原文无图，不增加装饰示意图。使用 Maven / Gradle 标签页，页面路径沿 README 规划的 getting-started/quickstart.mdx。

## 原则

先保证事实、版本与代码准确，再改写为自然简洁的中文。长句按用途拆分；保留必要条件。来源链接放正文末尾，不添加宣传和写作过程旁白。记录初稿、审校、修订与最终稿。
