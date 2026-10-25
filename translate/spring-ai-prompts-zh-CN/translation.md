---
title: Spring AI：提示词
description: 理解 Prompt、消息角色与 PromptTemplate，掌握模板变量、自定义分隔符、资源加载和 Token 边界。
sidebar:
  label: 提示词
  order: 5
---

提示词（Prompt）是引导模型生成结果的输入，其内容、结构和措辞都会影响回答质量。在 Spring AI 中，提示词可以包含多条不同角色的消息，以及本次请求的模型选项。

提示词模板类似 Spring MVC 的视图模板：先定义包含占位符的文本，再用用户请求或应用数据填入变量。也可以类比带占位符的 SQL。

如果借用数据库访问 API 作类比，`ChatModel` 类似底层 JDBC，`ChatClient` 类似构建在其上的 `JdbcClient`。`ChatClient` 还可通过 `Advisor` 引入历史对话、参考文档和智能体行为。

早期提示词通常只是字符串，之后逐步发展为带有角色标记的文本，再到按系统、用户、助手等角色组织的消息列表。

## API 概览

### Prompt：消息与请求选项的容器

`ChatModel.call(Prompt)` 接收一个 `Prompt`，返回 `ChatResponse`。`Prompt` 将有序的 `Message` 列表与本次请求的 `ChatOptions` 放在一起。下面省略了构造器和辅助方法：

```java
public class Prompt implements ModelRequest<List<Message>> {

    private final List<Message> messages;

    private ChatOptions chatOptions;
}
```

按角色访问消息时，要注意“第一条”和“最后一条”的区别：

| 方法                                 | 返回内容                                           |
| ------------------------------------ | -------------------------------------------------- |
| `getUserMessage()`                   | 最后一条用户消息；不存在时返回空的 `UserMessage`。 |
| `getSystemMessage()`                 | 第一条系统消息；不存在时返回空的 `SystemMessage`。 |
| `getLastUserOrToolResponseMessage()` | 最后一条用户消息或工具响应消息，便于衔接对话。     |
| `getUserMessages()`                  | 按原顺序返回全部用户消息。                         |
| `getSystemMessages()`                | 按原顺序返回全部系统消息。                         |

这些方法适合多轮对话，或按角色分别处理消息的场景。

### Message：文本、元数据与角色

`Message` 通过 `Content` 提供文本和元数据，通过 `MessageType` 标识消息角色。以下为简化接口：

```java
public interface Content {

	String getText();

	Map<String, Object> getMetadata();
}

public interface Message extends Content {

	MessageType getMessageType();
}
```

多模态消息还实现 `MediaContent`，提供图片、音频等 `Media` 对象：

```java
public interface MediaContent extends Content {

	Collection<Media> getMedia();

}
```

消息的角色决定模型如何理解这段内容：

| 角色              | 职责                                                         |
| ----------------- | ------------------------------------------------------------ |
| System（系统）    | 设定行为规则、身份和回答风格，提供对话的总体指令。           |
| User（用户）      | 承载用户的问题、命令或陈述。                                 |
| Assistant（助手） | 保存模型回复，帮助后续交互延续上下文；也可包含工具调用请求。 |
| Tool（工具）      | 回传工具执行结果，回应助手发出的工具调用请求。               |

对应的枚举定义如下：

```java
public enum MessageType {

	USER("user"),

	ASSISTANT("assistant"),

	SYSTEM("system"),

	TOOL("tool");

    ...
}
```

下图将文本、元数据、多模态内容和具体消息类型放在一起，重点看 `Message` 与 `MediaContent` 的关系，以及底部各消息类携带的数据。

<figure style={{ margin: '1.5rem 0' }}>
  <a href="/images/frameworks/spring-ai/spring-ai-message-api-zh.svg">
    <img
      src="/images/frameworks/spring-ai/spring-ai-message-api-zh.svg"
      alt="Spring AI 消息 API 类图：Message 和 MediaContent 扩展 Content，AbstractMessage 实现 Message；系统、用户、助手和工具响应消息分别携带角色、媒体或工具数据"
      width="1760"
      height="1435"
      style={{ width: '100%', height: 'auto' }}
    />
  </a>
  <figcaption style={{ fontSize: '0.875rem', color: 'var(--sl-color-gray-2)' }}>
    消息角色描述用途，媒体和工具数据描述内容；点击图片可放大查看。
  </figcaption>
</figure>

:::note[版本说明]
来源页的接口片段和类图仍写作 `getContent()`；本文按 [Spring AI 2.0.2 Content API](https://docs.spring.io/spring-ai/docs/2.0.2/api/org/springframework/ai/content/Content.html) 修正为 `getText()`。类图用于说明关系，完整签名以对应版本的 API 为准。
:::

### PromptTemplate：将模板转换为提示词

`PromptTemplate` 用于构造待发送给模型的提示词：

```java
public class PromptTemplate implements PromptTemplateActions, PromptTemplateMessageActions {

    // 其他方法见下文
}
```

它通过 `TemplateRenderer` 渲染模板。默认实现 `StTemplateRenderer` 基于 Terence Parr 开发的 [StringTemplate](https://www.stringtemplate.org/) 引擎，使用 `{变量名}` 标识占位符，也支持自定义分隔符。

```java
public interface TemplateRenderer extends BiFunction<String, Map<String, Object>, String> {

	@Override
	String apply(String template, Map<String, Object> variables);

}
```

需要自定义替换逻辑时，可以实现 `TemplateRenderer`；文本已完整、不需要模板处理时，可以使用 `NoOpTemplateRenderer`。

例如，将变量分隔符设为 `<` 和 `>`：

```java
PromptTemplate promptTemplate = PromptTemplate.builder()
    .renderer(StTemplateRenderer.builder().startDelimiterToken('<').endDelimiterToken('>').build())
    .template("""
            Tell me the names of 5 movies whose soundtrack was composed by <composer>.
            """)
    .build();

String prompt = promptTemplate.render(Map.of("composer", "John Williams"));
```

`PromptTemplate` 相关接口分别生成字符串、消息和完整的 `Prompt`。日常开发通常直接使用 `PromptTemplate`，理解这些返回类型即可。

#### 生成字符串：render

```java
public interface PromptTemplateStringActions {

	String render();

	String render(Map<String, Object> model);

}
```

- `render()`：不额外传入变量，直接渲染模板。
- `render(Map<String, Object>)`：用 Map 的键匹配占位符，将值填入模板，返回字符串。

#### 生成消息：createMessage

```java
public interface PromptTemplateMessageActions {

	Message createMessage();

    Message createMessage(List<Media> mediaList);

	Message createMessage(Map<String, Object> model);

}
```

| 重载                                 | 用途                       |
| ------------------------------------ | -------------------------- |
| `createMessage()`                    | 不额外传入变量，创建消息。 |
| `createMessage(List<Media>)`         | 创建包含文本与媒体的消息。 |
| `createMessage(Map<String, Object>)` | 填入变量后创建消息。       |

#### 生成完整请求：create

```java
public interface PromptTemplateActions extends PromptTemplateStringActions {

	Prompt create();

	Prompt create(ChatOptions modelOptions);

	Prompt create(Map<String, Object> model);

	Prompt create(Map<String, Object> model, ChatOptions modelOptions);

}
```

| 重载                                       | 用途                                      |
| ------------------------------------------ | ----------------------------------------- |
| `create()`                                 | 不额外传入变量，生成 `Prompt`。           |
| `create(ChatOptions)`                      | 生成 `Prompt`，并指定本次聊天请求的选项。 |
| `create(Map<String, Object>)`              | 填入变量后生成 `Prompt`。                 |
| `create(Map<String, Object>, ChatOptions)` | 同时设置模板变量和请求选项。              |

## 使用示例

### 填入模板变量

下面的示例来自 [PromptTemplates Workshop](https://github.com/Azure-Samples/spring-ai-azure-workshop/blob/main/2-README-prompt-templating.md)，把形容词和话题填入模板，再调用模型：

```java
PromptTemplate promptTemplate = new PromptTemplate("Tell me a {adjective} joke about {topic}");

Prompt prompt = promptTemplate.create(Map.of("adjective", adjective, "topic", topic));

return chatModel.call(prompt).getResult();
```

### 组合系统消息与用户消息

[Roles Workshop](https://github.com/Azure-Samples/spring-ai-azure-workshop/blob/main/3-README-prompt-roles.md) 展示了两类消息的分工：用户消息提出问题，系统消息通过 `{name}` 和 `{voice}` 设置身份与风格。

```java
String userText = """
    Tell me about three famous pirates from the Golden Age of Piracy and why they did.
    Write at least a sentence for each pirate.
    """;

Message userMessage = new UserMessage(userText);

String systemText = """
  You are a helpful AI assistant that helps people find information.
  Your name is {name}
  You should reply to the user's request with your name and also in the style of a {voice}.
  """;

SystemPromptTemplate systemPromptTemplate = new SystemPromptTemplate(systemText);
Message systemMessage = systemPromptTemplate.createMessage(Map.of("name", name, "voice", voice));

Prompt prompt = new Prompt(List.of(userMessage, systemMessage));

List<Generation> response = chatModel.call(prompt).getResults();
```

`SystemPromptTemplate` 生成系统角色的 `Message`，再与 `UserMessage` 一起组成 `Prompt`。通过 `getResults()` 获取生成结果列表。

### 自定义模板渲染器

可以实现自己的 `TemplateRenderer` 并传给 `PromptTemplate`，也可以只调整默认 `StTemplateRenderer` 的配置。

当提示词本身包含 JSON 时，JSON 的花括号可能与默认模板语法冲突。改用 `<变量名>`，可区分模板变量和 JSON 结构：

```java
PromptTemplate promptTemplate = PromptTemplate.builder()
    .renderer(StTemplateRenderer.builder().startDelimiterToken('<').endDelimiterToken('>').build())
    .template("""
            Tell me the names of 5 movies whose soundtrack was composed by <composer>.
            """)
    .build();

String prompt = promptTemplate.render(Map.of("composer", "John Williams"));
```

### 从资源文件加载模板

Spring AI 支持 `org.springframework.core.io.Resource`，可以把提示词放入文件，避免在 Java 中维护长字符串。例如，在 Spring 管理的组件中注入资源：

```java
@Value("classpath:/prompts/system-message.st")
private Resource systemResource;
```

再直接传给 `SystemPromptTemplate`：

```java
SystemPromptTemplate systemPromptTemplate = new SystemPromptTemplate(systemResource);
```

## 提示词工程

提示词的质量与结构会影响生成结果。设计提示词需要结合实际任务反复比较；社区中的分享、讨论和相关研究可以提供参考。

来源页援引研究，使用“深呼吸，逐步解决这个问题”这样的引导语改善了特定任务的表现。这类结果依赖模型和任务，不能据此保证某句话普遍有效。

### 一条有效提示词包含什么

| 要素                           | 作用                           |
| ------------------------------ | ------------------------------ |
| 指令（Instructions）           | 清楚、直接地说明要完成什么。   |
| 外部上下文（External Context） | 提供背景、参考资料或具体指导。 |
| 用户输入（User Input）         | 放入用户真正的问题或请求。     |
| 输出要求（Output Indicator）   | 指定期望的格式，如 JSON。      |

要求 JSON 不代表一定得到合法 JSON：模型可能在前面加上“这是你的 JSON”，也可能生成格式错误的数据。提供预期的问答示例，可以帮助模型理解结构与任务意图。

### 基础技巧

- [文本摘要](https://www.promptingguide.ai/introduction/examples.en#text-summarization)：保留要点，压缩长文本。
- [问答](https://www.promptingguide.ai/introduction/examples.en#question-answering)：根据给定资料回答具体问题。
- [文本分类](https://www.promptingguide.ai/introduction/examples.en#text-classification)：将文本分配到预设类别。
- [对话](https://www.promptingguide.ai/introduction/examples.en#conversation)：组织连续交互，维持对话上下文。
- [代码生成](https://www.promptingguide.ai/introduction/examples.en#code-generation)：根据自然语言要求生成代码。

### 进阶技巧

- [零样本（Zero-shot）](https://www.promptingguide.ai/techniques/zeroshot)：不提供任务示例，直接给出指令。
- [少样本（Few-shot）](https://www.promptingguide.ai/techniques/fewshot)：给出少量示例，帮助模型识别任务模式和输出格式。
- [思维链（Chain-of-Thought，CoT）](https://www.promptingguide.ai/techniques/cot)：通过中间推理步骤处理复杂任务。
- [ReAct（Reason + Act）](https://www.promptingguide.ai/techniques/react)：交替进行推理与行动，结合外部信息继续处理任务。

**概念澄清：**原文将 CoT 描述为串联多条回答以维持对话；这里按其链接中的定义表述为中间推理步骤，与多轮对话记忆区分。

### Microsoft Guidance

[Guidance](https://github.com/microsoft/guidance) 提供创建和优化提示词的工具，可用于更有结构地控制模型交互。

## Token：长度、费用与上下文

模型将输入文本切分为词元（Token），按 Token 处理并生成输出，随后将输出还原为文本。这个切分过程称为 Tokenization（分词）。**Token 不等于单词，也不等于汉字。**

原文用“一个 Token 约等于 3/4 个英文单词”作粗略估算：约 90 万英文单词的莎士比亚作品，可能对应约 120 万 Token。这只是英文估算，实际数量取决于分词器和文本，不能直接套用于中文。

可以使用 [OpenAI Tokenizer](https://platform.openai.com/tokenizer) 查看具体文本的切分结果。

| 关注点     | 工程含义                                                                     |
| ---------- | ---------------------------------------------------------------------------- |
| 费用       | 模型服务常按输入和输出 Token 计费；精简无关上下文有助于控制成本。            |
| 模型限制   | 上下文窗口限制一次请求可容纳的信息量，输出长度也可能有独立上限。             |
| 上下文取舍 | 超出上限时需要减少内容；例如询问《哈姆雷特》，通常不必附上莎士比亚全部作品。 |
| 响应元数据 | 关注响应中的 Token 用量信息，用于统计与成本管理。                            |

原文列举了早期模型的 Token 容量，这些数字不作为当前规格保留；具体上下文窗口与输出上限，应查询所选模型的版本说明。

接下来阅读[聊天响应元数据](/frameworks/spring-ai/core/chat-response-metadata/)，学习读取 Token 用量、限流与缓存指标。

来源：[Spring AI Prompts](https://docs.spring.io/spring-ai/reference/api/prompt.html)。文档版本：2.0.2；核验日期：2026-10-25。
