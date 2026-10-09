// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

// https://astro.build/config
export default defineConfig({
	site: 'https://notes.wwkq.top',
	integrations: [
		starlight({
			title: 'Hi, Agent!',
			logo: {
				src: './src/assets/logo.png',
			},
			social: [
				{ icon: 'github', label: 'GitHub', href: 'https://github.com/wangkaiqistart/Hello-Notes-' },
			],
			sidebar: [
				{
					label: '基础入门',
					items: [
						{ label: '大模型理论', items: [{ autogenerate: { directory: 'basics/llm-theory' } }] },
						{ label: '提示词工程', items: [{ autogenerate: { directory: 'basics/prompt-engineering' } }] },
						{ label: '模型接入', items: [{ autogenerate: { directory: 'basics/model-access' } }] },
						{ label: 'Embedding', items: [{ autogenerate: { directory: 'basics/embedding' } }] },
						{ label: 'Python 工程基础', items: [{ autogenerate: { directory: 'basics/python-foundation' } }] },
					],
				},
				{
					label: '开发框架',
					items: [
						{ label: 'LangChain', items: [{ autogenerate: { directory: 'frameworks/langchain' } }] },
						{ label: 'LangGraph', items: [{ autogenerate: { directory: 'frameworks/langgraph' } }] },
						{ label: 'LlamaIndex', items: [{ autogenerate: { directory: 'frameworks/llamaindex' } }] },
						{ label: 'MCP', items: [{ autogenerate: { directory: 'frameworks/mcp' } }] },
						{
							label: 'Deep Agents',
							items: [
								'frameworks/deepagents',
								{
									label: '入门',
									items: [
										'frameworks/deepagents/getting-started/quickstart',
										'frameworks/deepagents/getting-started/customization',
										'frameworks/deepagents/getting-started/models',
									],
								},
								{
									label: '部署',
									items: [
										'frameworks/deepagents/deployment/managed-deep-agents',
										{
											label: '生产化',
											items: [
												'frameworks/deepagents/deployment/going-to-production/fault-tolerance',
											],
										},
									],
								},
								{
									label: '执行环境',
									items: [
										'frameworks/deepagents/execution-environment/tools',
										'frameworks/deepagents/execution-environment/backends',
										'frameworks/deepagents/execution-environment/permissions',
										'frameworks/deepagents/execution-environment/multimodality',
										'frameworks/deepagents/execution-environment/sandboxes',
										{ slug: 'frameworks/deepagents/execution-environment/interpreters', badge: 'Beta' },
										{ slug: 'frameworks/deepagents/execution-environment/event-streaming', badge: 'Beta' },
										'frameworks/deepagents/execution-environment/streaming',
									],
								},
								{
									label: '上下文管理',
									items: [
										'frameworks/deepagents/context-management/skills',
										'frameworks/deepagents/context-management/memory',
										'frameworks/deepagents/context-management/retrieval',
										'frameworks/deepagents/context-management/context-engineering',
										{ slug: 'frameworks/deepagents/context-management/profiles', badge: 'Beta' },
										'frameworks/deepagents/context-management/openwiki',
									],
								},
								{
									label: '委派',
									items: [
										'frameworks/deepagents/delegation/subagents',
										{ slug: 'frameworks/deepagents/delegation/dynamic-subagents', badge: 'Beta' },
										'frameworks/deepagents/delegation/async-subagents',
									],
								},
								{
									label: 'Steering',
									items: [
										'frameworks/deepagents/steering/human-in-the-loop',
										{ slug: 'frameworks/deepagents/steering/grading-rubrics', badge: 'Beta' },
									],
								},
								{
									label: 'Middleware',
									items: [
										'frameworks/deepagents/middleware/prebuilt',
										'frameworks/deepagents/middleware/custom',
									],
								},
								{
									label: 'Frontend',
									items: [
										{
											label: 'Patterns',
											items: [
												'frameworks/deepagents/frontend/patterns/subagent-streaming',
												'frameworks/deepagents/frontend/patterns/todo-list',
												'frameworks/deepagents/frontend/patterns/sandbox',
											],
										},
									],
								},
								{
									label: 'Protocols',
									items: [
										'frameworks/deepagents/protocols/acp',
										'frameworks/deepagents/protocols/mcp-with-langchain',
										'frameworks/deepagents/protocols/a2a-with-langsmith',
										'frameworks/deepagents/protocols/ag-ui',
									],
								},
							],
						},
					],
				},
				{
					label: 'RAG 知识库',
					items: [
						{ label: '基础架构', items: [{ autogenerate: { directory: 'rag/fundamentals' } }] },
						{ label: '文档解析', items: [{ autogenerate: { directory: 'rag/document-parsing' } }] },
						{ label: '向量数据库', items: [{ autogenerate: { directory: 'rag/vector-db' } }] },
						{ label: '进阶优化', items: [{ autogenerate: { directory: 'rag/advanced' } }] },
					],
				},
				{
					label: '智能体开发',
					items: [
						{ label: 'Agent 基础', items: [{ autogenerate: { directory: 'agent/fundamentals' } }] },
						{ label: 'OpenWiki', items: [{ autogenerate: { directory: 'agent/openwiki' } }] },
						{ label: 'Agent 实战进阶', items: [{ autogenerate: { directory: 'agent/agent-practice' } }] },
						{ label: '开发范式', items: [{ autogenerate: { directory: 'agent/development-patterns' } }] },
						{ label: 'Loop Engineering', items: [{ autogenerate: { directory: 'agent/loop-engineering' } }] },
						{ label: 'Hermes', items: [{ autogenerate: { directory: 'agent/hermes' } }] },
						{ label: 'Skills 架构', items: [{ autogenerate: { directory: 'agent/skills' } }] },
						{ label: '记忆系统', items: [{ autogenerate: { directory: 'agent/memory' } }] },
						{ label: '上下文工程', items: [{ autogenerate: { directory: 'agent/context-engineering' } }] },
						{ label: 'Harness', items: [{ autogenerate: { directory: 'agent/harness' } }] },
					],
				},
				{
					label: 'AI 编程',
					items: [
						'ai-programming',
						{
							label: '认知篇',
							items: [
								'ai-programming/cognition/essence-and-value',
								'ai-programming/cognition/tool-landscape',
								'ai-programming/cognition/human-ai-workflow',
								'ai-programming/cognition/trend-snapshot-2026',
							],
						},
						{
							label: '方法论',
							items: [
								'ai-programming/methodology/sdd-and-harness',
								'ai-programming/methodology/spec-kit-and-openspec',
								'ai-programming/methodology/skills-and-superpowers',
							],
						},
					],
				},
				{
					label: '部署与微调',
					items: [
						{ label: '接口设计', items: [{ autogenerate: { directory: 'deployment/api-design' } }] },
						{ label: '容器化', items: [{ autogenerate: { directory: 'deployment/containerization' } }] },
						{ label: '微调与私有化', items: [{ autogenerate: { directory: 'deployment/fine-tuning' } }] },
					],
				},
				{
					label: '工具指南',
					items: [
						{ label: 'Codex', items: [{ autogenerate: { directory: 'tools/codex' } }] },
					],
				},
				{
					label: '实战项目',
					items: [{ autogenerate: { directory: 'projects' } }],
				},
			],
		}),
	],
});
