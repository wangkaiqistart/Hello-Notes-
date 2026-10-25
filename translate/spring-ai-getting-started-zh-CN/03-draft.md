---
title: Spring AI：快速入门
description: 配置 Spring AI 的版本、Maven 与 Gradle 仓库、BOM 和组件依赖。
sidebar:
  label: 快速入门
  order: 3
---

import { TabItem, Tabs } from '@astrojs/starlight/components';

使用 Spring AI 时，先确认 Spring Boot 版本，再配置依赖仓库、导入 BOM，并添加所需组件。

**Spring AI 2.0.x 支持 Spring Boot 4.0.x 和 4.1.x。**

## 创建项目

打开 [Spring Initializr](https://start.spring.io/)，选择新应用需要使用的 AI 模型和向量存储，创建项目。

## 配置依赖仓库

### 正式版：使用 Maven Central

Spring AI 的正式版依赖已发布到 Maven Central，不需要额外添加 Spring 仓库。Maven 默认包含 Maven Central；Gradle 需要在构建文件中启用 `mavenCentral()`。

<Tabs>
  <TabItem label="Maven">

```xml
<!-- Maven 默认包含 Maven Central，通常不需要显式配置。 -->
<repositories>
    <repository>
        <id>central</id>
        <url>https://repo.maven.apache.org/maven2</url>
    </repository>
</repositories>
```

  </TabItem>
  <TabItem label="Gradle">

```groovy
repositories {
    mavenCentral()
}
```

  </TabItem>
</Tabs>

### 快照版：添加 SNAPSHOT 仓库

使用开发中的快照版本，例如原文中的 `2.0.0-SNAPSHOT`，需要在构建文件中添加快照仓库：

<Tabs>
  <TabItem label="Maven">

```xml
<repositories>
  <repository>
    <id>spring-snapshots</id>
    <name>Spring Snapshots</name>
    <url>https://repo.spring.io/snapshot</url>
    <releases>
      <enabled>false</enabled>
    </releases>
  </repository>
  <repository>
    <name>Central Portal Snapshots</name>
    <id>central-portal-snapshots</id>
    <url>https://central.sonatype.com/repository/maven-snapshots/</url>
    <releases>
      <enabled>false</enabled>
    </releases>
    <snapshots>
      <enabled>true</enabled>
    </snapshots>
  </repository>
</repositories>
```

  </TabItem>
  <TabItem label="Gradle">

```groovy
repositories {
  mavenCentral()
  maven { url 'https://repo.spring.io/milestone' }
  maven { url 'https://repo.spring.io/snapshot' }
  maven {
    name = 'Central Portal Snapshots'
    url = 'https://central.sonatype.com/repository/maven-snapshots/'
  }
}
```

  </TabItem>
</Tabs>

### Maven 镜像配置

使用快照版时，需要注意 `settings.xml` 中的镜像配置。下面的 `*` 会将全部仓库请求转发到镜像：

```xml
<mirror>
    <id>my-mirror</id>
    <mirrorOf>*</mirrorOf>
    <url>https://my-company-repository.com/maven</url>
</mirror>
```

若要让两个快照仓库绕过镜像，使用以下 `mirrorOf` 配置：

```xml
<mirror>
    <id>my-mirror</id>
    <mirrorOf>*,!spring-snapshots,!central-portal-snapshots</mirrorOf>
    <url>https://my-company-repository.com/maven</url>
</mirror>
```

这里的排除项必须与仓库定义中的 `id` 一致。这样可以直接访问快照仓库，其他依赖仍通过镜像下载。

## 使用 BOM 管理版本

Spring AI 的依赖版本清单（Bill of Materials，BOM）声明了某个发行版推荐使用的依赖版本。

BOM 只提供依赖管理，不声明插件，也不直接引入 Spring 或 Spring Boot。Spring Boot 的版本仍通过 Spring Boot 父 POM，或 `spring-boot-dependencies` BOM 管理。

以下示例保留原文中的 BOM 版本 `2.0.0`；本页对应的文档版本为 `2.0.2`。实际使用时，将 BOM 版本改为项目选定的 Spring AI 版本。

<Tabs>
  <TabItem label="Maven">

```xml
<dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>org.springframework.ai</groupId>
            <artifactId>spring-ai-bom</artifactId>
            <version>2.0.0</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>
    </dependencies>
</dependencyManagement>
```

  </TabItem>
  <TabItem label="Gradle">

```groovy
dependencies {
  implementation platform("org.springframework.ai:spring-ai-bom:2.0.0")
  // 按需替换为具体模块，例如 spring-ai-openai，
  // 或 Starter，例如 spring-ai-starter-model-openai
  implementation 'org.springframework.ai:spring-ai-openai'
}
```

  </TabItem>
</Tabs>

Gradle 的 `platform(...)` 用于导入 Maven BOM，将其中的依赖版本约束应用到当前项目。

## 添加具体组件依赖

导入 BOM 后，还需要添加实际使用的组件依赖。各章节分别说明所需模块和配置：

- [聊天模型](https://docs.spring.io/spring-ai/reference/api/chatmodel.html)
- [嵌入模型](https://docs.spring.io/spring-ai/reference/api/embeddings.html)
- [图像生成模型](https://docs.spring.io/spring-ai/reference/api/imageclient.html)
- [语音转写模型](https://docs.spring.io/spring-ai/reference/api/audio/transcriptions.html)
- [语音合成（TTS）模型](https://docs.spring.io/spring-ai/reference/api/audio/speech.html)
- [向量数据库](https://docs.spring.io/spring-ai/reference/api/vectordbs.html)

## 示例与学习资源

[Awesome Spring AI](https://github.com/spring-ai-community/awesome-spring-ai) 汇总了 Spring AI 相关资源和示例，可按需要查阅。

来源：[Spring AI Getting Started](https://docs.spring.io/spring-ai/reference/getting-started.html)。文档版本：2.0.2；核验日期：2026-10-25。
