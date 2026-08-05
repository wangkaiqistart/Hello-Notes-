# OSS 图片发布设计说明

## 适用请求示例
- "把这张截图上传到 OSS，返回链接。"
- "将 `/tmp/diagram.png` 发布到阿里云 OSS。"
- "给这几张知识库图片生成可访问 URL。"
- "把这些本地图片上传到 OSS，并返回 Markdown 图片链接。"

## 不适用的相邻请求
- "把这个图片链接放进知识库合适的位置。" 先用这个 skill 返回链接，再交给文档或知识库编辑 skill。
- "整理知识库图片引用。" 这是内容维护，不是上传。
- "创建 OSS bucket / 配置 RAM 权限 / 设置 CDN。" 这个 skill 默认 OSS 基础设施已经存在。
- "生成图片 / 压缩图片 / 改图。" 先使用图片生成或素材处理流程，再上传最终文件。

## 环境变量

真实上传必填：
- `ALIYUN_OSS_ACCESS_KEY_ID`
- `ALIYUN_OSS_ACCESS_KEY_SECRET`
- `ALIYUN_OSS_BUCKET`
- `ALIYUN_OSS_ENDPOINT`

可选：
- `ALIYUN_OSS_SECURITY_TOKEN`：使用临时凭证时填写 STS Token。
- `ALIYUN_OSS_PREFIX`：对象路径前缀，默认 `images`。
- `ALIYUN_OSS_PUBLIC_BASE_URL`：CDN、自定义域名或公开存储桶访问地址。不设置时，链接格式为 `https://<bucket>.<endpoint>/<key>`。
- `ALIYUN_OSS_OBJECT_ACL`：可选对象 ACL，例如 `public-read`。
- `ALIYUN_OSS_FORBID_OVERWRITE`：设为 `true` 时发送 `x-oss-forbid-overwrite: true`。

不要把 AccessKey 写进 skill 文件、Markdown、文档或命令示例。如果密钥曾经被粘贴到聊天或日志里，建议轮换密钥。

## 上传约定

脚本对每张图片执行一次 OSS PutObject 单对象上传，并使用 OSS V1 鉴权头。请求形态遵循阿里云 OSS PutObject 和 V1 签名规则：
- PutObject 每次上传一个对象，单次上传上限为 5 GB。
- V1 签名使用 `Authorization: OSS <AccessKeyId>:<Signature>`，签名内容由请求方法、MD5、内容类型、日期、OSS 头和规范化资源路径计算得到。

## 对象路径规则

默认对象路径格式：

```text
<prefix>/<YYYY>/<MM>/<DD>/<filename-slug>-<sha256-12><extension>
```

这样既方便识别重复上传，也能降低误覆盖风险。只有用户明确需要固定对象路径，并且只上传一张图片时，才使用 `--key`。

## 公开链接规则

返回链接不等于一定能公开访问；如果存储桶是私有的，链接可能无法直接打开。优先用 `ALIYUN_OSS_PUBLIC_BASE_URL` 返回 CDN 或自定义域名链接。如果用户需要公开直链，存储桶策略必须允许访问，或者在权限允许时使用 `--acl public-read`。
