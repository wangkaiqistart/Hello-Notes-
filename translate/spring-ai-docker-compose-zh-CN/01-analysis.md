# 内容分析

原文为 Spring AI 2.0.2 的开发服务接入页，正文约 300 个英文词，低于分块阈值。包含 Maven/Gradle 两个依赖片段、一个服务连接小节和 9 条镜像匹配规则，没有图片。

| 术语                      | 用语                   |
| ------------------------- | ---------------------- |
| Development-time Services | 开发阶段使用的外部服务 |
| Service Connection        | 服务连接               |
| Connection Details        | 连接信息               |
| Matched on                | 按镜像名称匹配         |

使用项目 zh-CN / refined / technical 配置，简明解释操作和职责。完整保留九个连接类型、十一种镜像名与两个依赖片段。原文的 containers named 实际按镜像匹配，不解释为 container_name。

补充 PGvector 场景时，只依据 Boot 4.1.2 开发服务文档与 PostgreSQL 连接工厂源码，明确补充内容和原文清单的范围；避免宣称自动连接会创建模型、表或索引。
