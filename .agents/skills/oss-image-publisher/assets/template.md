# 链接返回模板

从 OSS 上传返回链接时，使用下面这些格式。

## 纯链接

```text
https://cdn.example.com/images/2026/08/04/example-a1b2c3d4e5f6.png
```

## Markdown

```md
![示例图片](https://cdn.example.com/images/2026/08/04/example-a1b2c3d4e5f6.png)
```

## JSON

```json
{
  "成功": true,
  "上传结果": [
    {
      "源文件": "/absolute/path/example.png",
      "存储桶": "example-bucket",
      "访问域名": "oss-cn-hangzhou.aliyuncs.com",
      "对象路径": "images/2026/08/04/example-a1b2c3d4e5f6.png",
      "链接": "https://cdn.example.com/images/2026/08/04/example-a1b2c3d4e5f6.png",
      "内容类型": "image/png",
      "大小": 12345,
      "是否演练": false
    }
  ]
}
```
