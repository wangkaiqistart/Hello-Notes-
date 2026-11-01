# 审校记录

1. YAML Tab改为两空格，统一 kebab-case 属性，加入本地首建开关。
2. 手动客户端示例引用未定义milvusContainer且误用MinIO用户名密码；改为注入Milvus host/port/username/password，SDK方法由自动配置源码确认。
3. Gson LONG_OR_DOUBLE策略、分区作用范围、原生表达式优先级均由同版本源码确认。
4. nprobe=1是来源对未指定时的说明，Spring AI此处仅透传JSON，不保证每个SDK/服务端一致；128不是通用最优值，调节需兼顾nlist、召回与延迟。
5. idle-timeout-ms 是long毫秒，默认24小时等于86400000；表中修正单位，全部30行配置保留。
6. 19530是Milvus服务端点，9001/minioadmin属于配套MinIO管理，不混淆身份。
7. 保留原文全部启动、清理、排查命令，但说明rm删除本地卷数据、system prune影响全局Docker环境，不把后者当常规首选；没有执行任何命令。
8. BOM/仓库、统一过滤与Embedding复用站内，部署/专用索引/原生表达式保留原文。
