# 内容分析

来源：Spring AI Getting Started，文档版本 2.0.2，2026-10-25 获取。来源正文与 8 个代码块已保存；正文约 547 个空白分隔词，低于分块阈值，直接完成整篇精翻。

## 内容与范围

面向已有 Java / Spring Boot 基础的开发者，介绍版本兼容、Spring Initializr、正式版和快照仓库、Maven 镜像、BOM 和各组件依赖入口。原文没有插图，也没有完整的模型调用应用。本篇保留全部 8 个 Maven / Gradle 配置块，不扩写代码教程。

## 术语

| 原文                    | 译法                          |
| ----------------------- | ----------------------------- |
| Artifact Repositories   | 依赖仓库                      |
| Releases                | 正式版                        |
| Snapshots               | 快照版（SNAPSHOT）            |
| Mirror                  | 镜像仓库                      |
| Bill of Materials (BOM) | 依赖版本清单（BOM）           |
| Dependency Management   | 依赖管理                      |
| Vector Store            | 向量存储                      |
| Embedding Model         | 嵌入模型                      |
| Starter                 | Starter，保留 Spring 常用名称 |

## 风格与难点

- 延续已有页面：简明中文，直接说明用途与配置位置，避免翻译腔和额外宣传。
- 精确保留兼容关系：Spring AI 2.0.x 支持 Spring Boot 4.0.x / 4.1.x。
- 来源正文版本 2.0.2，但两个 BOM 示例都写 2.0.0。保留示例并以简短说明明确差异，不能静默替换版本或将 2.0.0 写成当前最新。
- 快照示例的 2.0.0-SNAPSHOT 只是原文示例，不表述为核验日最新开发版本。
- BOM 只声明推荐依赖版本，不声明插件，也不直接引入 Spring / Spring Boot；仍需添加实际组件依赖。
- Maven mirrorOf 使用仓库 ID 排除规则；原文的两个排除 ID 必须与仓库定义一致。
- 原文同时有 Maven 和 Gradle，使用 Starlight Tabs 保留两套配置，减少纵向重复。
- 不添加“官方”字样到页面。组件标签保留英文，中文标题与说明保持一致。
