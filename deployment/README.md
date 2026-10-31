# OSS 页面发布

推送到 `main` 后，工作流构建站点并运行 `scripts/deploy_oss.py --apply`。

- 先上传本次构建，再逐个删除已退役的 HTML，最后更新 `.deployment/pages.json`。
- 旧页来自上次成功发布清单及 `retired-pages.json`；本次构建中仍存在的页面会保留。
- `retired-pages.json` 记录 2026-11-01 清理的 56 个页面，用于兼容尚无发布清单的旧站点。
- 只删除明确列出的 `.html` 文件，不递归删除目录，也不清理图片等其他资产。
- 清单读取、上传或删除失败会停止发布；只有 `NoSuchKey`（对象不存在）允许跳过。
- 工作流串行执行，避免多个版本交叉更新清单。

本地验证清理逻辑：

```bash
python3 -m unittest discover -s scripts -p 'test_*.py'
```

已配置 OSS CLI 和 `OSS_BUCKET` 时，可只读取远端清单并预览删除范围：

```bash
npm run build
python3 scripts/deploy_oss.py
```
