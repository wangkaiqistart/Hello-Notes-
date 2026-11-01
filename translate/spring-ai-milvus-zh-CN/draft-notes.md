# 初稿待审校问题

1. 原 YAML 示例用 Tab 缩进，不能直接作为合法 YAML 粘贴；可在修订稿改为空格并添加 initialize-schema: true（仅本地首建时）。初稿逐字保留源代码。
2. 手动配置中的 milvusContainer 未声明，是测试上下文；withAuthorization 使用 minioadmin，与前文 Milvus root/milvus 默认凭据不一致，需源码与 SDK 核对后修订为可配置参数。
3. 原文把 nprobe=1、空结果和提升参数的效果讲得过于绝对；应说明依赖 SDK/服务版本、索引类型和 nlist，不应将128视为通用最优值。
4. client.idle-timeout-ms 属性名与默认值24h并不统一，需核对对应版本属性类的真实类型和赋值，保留原文表格值并说明时需避免猜测。
5. “localhost:19530”是Milvus服务端点，不应声称是浏览器管理界面；9001/minioadmin是配套MinIO管理信息，不能当作Milvus认证信息。
6. docker-compose down; rm -Rf ./volumes 会删除本地持久化数据；docker system prune --all --force --volumes 清理范围更大。保留原文作为参考但应明确影响，不能作为常规首选排查步骤。未执行这些命令。
7. Metadata Gson数值Long/Double行为可能是较新提交，需按当前版本源码核对再确定是否作为v2.0.2保证。
8. 本初稿未编译Java示例，未运行数据库或模型。原生接口、配置默认值、索引行为需主代理统一源码审校。
