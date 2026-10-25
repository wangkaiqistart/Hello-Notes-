# 图像模型审校

## 准确性

六个来源类结构的职责均已覆盖，保留 ImageModel 接口定义原文；两段调用示例按 ImagePrompt 构造器、Image.getUrl / getB64Json 和 ImageResponse API 整理。原文没有示例图片，页面不虚构生成结果。

2.0.2 ImageOptions 包含 getStyle，按现行 API 增补；URL / Base64 可为空，不保证同时返回。ImageMessage 权重、尺寸和张数等参数均以具体模型支持为前提。保留三家来源实现入口。

## 中文与范围

用职责表替代重复的完整类定义，缩短翻译腔。初稿对局部片段和空结果边界说明足够，定稿不再扩展提供方配置。图片编辑范围由提供方决定，不将其误写成所有 ImageModel 必备方法。
