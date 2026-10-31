export interface LearningPath {
  badge: string;
  title: string;
  description: string;
  steps: [string, string, string][];
}

export const learningPaths: Record<string, LearningPath> = {
  java: {
    badge: '从熟悉到可能',
    title: '把 Spring 经验，变成 AI 能力。',
    description: '从第一个模型调用开始，逐步加入记忆、检索与工具。',
    steps: [
      ['接入第一个模型', '配置与快速开始', '/frameworks/spring-ai/getting-started/quickstart/'],
      ['掌握 ChatClient', '提示词与流式响应', '/frameworks/spring-ai/core/chat-client/'],
      ['让对话有记忆', '上下文与会话管理', '/frameworks/spring-ai/core/chat-memory/'],
      ['赋予工具能力', '让模型执行行动', '/frameworks/spring-ai/tools/tool-calling/'],
    ],
  },
  python: {
    badge: '从脚本到应用',
    title: '从 Python 出发，构建你的 AI 应用。',
    description: '理解模型调用，学习框架编排，再把知识连接到应用中。',
    steps: [
      ['理解大模型', '能力与使用边界', '/basics/llm-theory/what-is-llm/'],
      ['入门 LangChain', '模型与应用编排', '/frameworks/langchain/langchain-basics/'],
      ['理解 RAG', '让回答有据可依', '/rag/fundamentals/what-is-rag/'],
      ['探索 LangGraph', '有状态的工作流', '/frameworks/langgraph/'],
    ],
  },
  agent: {
    badge: '从调用到构建',
    title: '不止会回答，更要能解决问题。',
    description: '从工程结构理解智能体，连接上下文、规划与外部工具。',
    steps: [
      ['理解 Harness', '模型之外的工程', '/agent/harness/'],
      ['组织上下文', '为决策准备信息', '/agent/context-engineering/'],
      ['构建 Deep Agent', '规划与协作执行', '/frameworks/deepagents/'],
      ['连接 MCP', '开放的工具生态', '/frameworks/spring-ai/mcp/overview/'],
    ],
  },
};
