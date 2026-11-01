# RAG 全目录引用优化

本次覆盖 RAG、ETL、向量存储总览及 PGvector、Milvus、Redis、S3 Vector Store、Elasticsearch，共 8 篇。正文中的站内文档引用仅使用 `/frameworks/spring-ai/` 下的内容；本篇锚点与静态图片地址不受此路径限制。

## 调整结果

- 已复查 8 篇，实际修改向量存储总览及五篇后端文档，共 20 处引用相关段落。RAG 与 ETL 已在上一轮达到该标准，本轮复核通过。
- 总览的 5 处模块外 Embedding／Chroma 引用改为 Spring AI 核心概念、Embedding 模型及 Redis 距离度量。Redis 章节只作为后端度量和分数换算的实例，未宣称覆盖完整数学推导。
- 五篇后端补齐 ETL 资料准备、SearchRequest、RAG Advisor 与动态过滤的对应入口；PGvector 补齐向量空间一致性说明，Redis 补齐统一接口和 Advisor 处理链入口，S3 补齐删除参考。
- Milvus 的回答质量评估入口与召回率、延迟测量明确区分，避免把模型评估器当作检索性能评测。
- 原始外链均保留。部署、原生查询、版本迁移、源码证据、未翻译后端与完整数学背景没有等价模块内容时，不用局部笔记替换。

## 逐页检查

| 页面                                                                                                   | 本轮修改段落 | 站内文档引用次数 | 代码块 | 原始锚点 | 图片 |
| ------------------------------------------------------------------------------------------------------ | -----------: | ---------------: | -----: | -------: | ---: |
| [ETL 管道](../../src/content/docs/frameworks/spring-ai/rag/document-ingestion.mdx)                     |            0 |               10 |     41 |       83 |    3 |
| [检索增强生成（RAG）](../../src/content/docs/frameworks/spring-ai/rag/retrieval-and-generation.mdx)    |            0 |               13 |     21 |       26 |    0 |
| [Elasticsearch（ES）](../../src/content/docs/frameworks/spring-ai/rag/vector-stores/elasticsearch.mdx) |            2 |                9 |     15 |        6 |    0 |
| [向量存储总览](../../src/content/docs/frameworks/spring-ai/rag/vector-stores/index.mdx)                |            4 |               38 |     32 |       34 |    0 |
| [Milvus](../../src/content/docs/frameworks/spring-ai/rag/vector-stores/milvus.mdx)                     |            3 |               13 |     15 |       10 |    0 |
| [PGvector](../../src/content/docs/frameworks/spring-ai/rag/vector-stores/pgvector.mdx)                 |            3 |               14 |     14 |        7 |    0 |
| [Redis](../../src/content/docs/frameworks/spring-ai/rag/vector-stores/redis.mdx)                       |            5 |               13 |     33 |       24 |    0 |
| [S3 Vector Store](../../src/content/docs/frameworks/spring-ai/rag/vector-stores/s3-vector-store.mdx)   |            3 |               12 |     13 |        7 |    0 |

合计保留 184 个代码块、197 个原始锚点与 3 张图片；修改前后的代码块、标题层级、原始锚点和图片组逐一相等。修订、定稿与站点正文同步，覆盖记录的页面哈希已刷新。

## 保留的外链

共有 82 个去重的外部文档／产品／源码地址，另有 2 个本地服务示例地址。原因与所在页面已[逐项列出](external-links.md)，机器可读结果见 [audit.json](audit.json)。没有使用主题或范围不确定的站内替代。

重点保留：未翻译的 16 种后端接入、Docker Compose／Testcontainers 开发服务、版本升级、OpenAI 专有配置与限制、Milvus／Redis／ES 原生语法和部署、AWS S3 Vectors 资源与 SDK、pgvector 索引限制、数学推导、论文、jinfer 重排序、Tika 格式表，以及各篇来源链接。

## 验证

- `npm run check`：0 错误、0 警告、0 提示。
- `npm run build`：通过，92 页。
- 桌面 1440×1000、手机 390×844，共 16 次页面检查通过。
- 245 个站内页面、锚点与静态资源目标通过，正文中模块外站内文档引用为 0；无页面横向溢出、图片加载失败或运行时错误。
- 日志见 [check.log](check.log)、[build.log](build.log)，页面详情见 [browser.json](browser.json)。

此次实时验证范围为站内引用及页面。外部地址按语义核对后保留，没有重新验证全部外部网站的可用性。Java 示例未编译或执行，未调用真实模型、数据库或云服务。未提交或推送代码。

## 后续更新：Docker Compose 已收录

Spring AI 的 Docker Compose 开发服务说明已翻译并补充 PGvector 示例。PGvector 页面原来的 Spring AI Docker Compose 链接和 Boot Docker Compose 服务连接说明，已改为本模块新页及运行流程锚点。Testcontainers 和 Boot 高级规则仍保留官网入口。

本文件前面的链接列表与检查数字记录全目录复核时的快照，这两处引用的当前状态以[后续记录](../spring-ai-docker-compose-zh-CN/coverage-audit.json)为准。
