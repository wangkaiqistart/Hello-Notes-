// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

// https://astro.build/config
export default defineConfig({
	site: 'https://notes.wwkq.top',
	redirects: {
		'/frameworks/spring-ai/core/advisors-recursive/': '/frameworks/spring-ai/core/advisors/#递归-advisors',
	},
	integrations: [
		starlight({
			title: 'Hi, Agent!',
			locales: { root: { label: '简体中文', lang: 'zh-CN' } },
			favicon: '/favicon.png?v=20261101',
			head: [
				{ tag: 'link', attrs: { rel: 'apple-touch-icon', sizes: '180x180', href: '/apple-touch-icon.png?v=20261101' } },
			],
			customCss: ['./src/styles/site-theme.css', './src/styles/docs.css'],
			components: {
				SiteTitle: './src/components/SiteBrand.astro',
				ThemeSelect: './src/components/ThemeSelect.astro',
				Sidebar: './src/components/Sidebar.astro',
			},
			logo: {
				src: './src/assets/logo.png',
			},
			social: [
				{ icon: 'github', label: 'GitHub', href: 'https://github.com/wangkaiqistart/Hello-Notes-' },
			],
			sidebar: [
				{
					label: '基础入门',
					collapsed: true,
					items: [
						{ label: '大模型理论', collapsed: true, items: [{ autogenerate: { directory: 'basics/llm-theory', collapsed: true } }] },
						{ label: '提示词工程', collapsed: true, items: [{ autogenerate: { directory: 'basics/prompt-engineering', collapsed: true } }] },
						{ label: '模型接入', collapsed: true, items: [{ autogenerate: { directory: 'basics/model-access', collapsed: true } }] },
						{ label: 'Embedding', collapsed: true, items: [{ autogenerate: { directory: 'basics/embedding', collapsed: true } }] },
						{ label: 'Python 工程基础', collapsed: true, items: [{ autogenerate: { directory: 'basics/python-foundation', collapsed: true } }] },
					],
				},
				{
					label: '开发框架',
					collapsed: true,
					items: [
						{
							label: 'Spring AI',
							collapsed: true,
							items: [
								'frameworks/spring-ai',
								'frameworks/spring-ai/concepts',
								'frameworks/spring-ai/getting-started/quickstart',
								'frameworks/spring-ai/core/chat-client',
								'frameworks/spring-ai/core/advisors',
								'frameworks/spring-ai/core/prompts',
								'frameworks/spring-ai/core/chat-response-metadata',
								'frameworks/spring-ai/core/structured-output',
								'frameworks/spring-ai/core/multimodality',
								{
									label: '模型',
									collapsed: true,
									items: [
										'frameworks/spring-ai/models',
										'frameworks/spring-ai/models/chat-model',
										'frameworks/spring-ai/models/embedding-model',
										'frameworks/spring-ai/models/image-model',
										'frameworks/spring-ai/models/audio-model',
										'frameworks/spring-ai/models/moderation-model',
									],
								},
								'frameworks/spring-ai/core/chat-memory',
								{
									label: '工具调用',
									collapsed: true,
									items: [
										'frameworks/spring-ai/tools/tool-calling',
										'frameworks/spring-ai/tools/tool-calling-advisor',
										'frameworks/spring-ai/tools/tool-search-tool',
										'frameworks/spring-ai/tools/chatmodel-tool-calling',
									],
								},
								{
									label: 'MCP',
									collapsed: true,
									items: [
										'frameworks/spring-ai/mcp/overview',
										'frameworks/spring-ai/mcp/client',
										'frameworks/spring-ai/mcp/server',
									],
								},
								{
									label: 'RAG',
									collapsed: true,
									items: [
										'frameworks/spring-ai/rag/retrieval-and-generation',
										'frameworks/spring-ai/rag/document-ingestion',
										{
											label: '向量存储',
											collapsed: true,
											items: [
												'frameworks/spring-ai/rag/vector-stores',
												'frameworks/spring-ai/rag/vector-stores/pgvector',
												'frameworks/spring-ai/rag/vector-stores/milvus',
												'frameworks/spring-ai/rag/vector-stores/redis',
												'frameworks/spring-ai/rag/vector-stores/s3-vector-store',
												'frameworks/spring-ai/rag/vector-stores/elasticsearch',
											],
										},
									],
								},
								{
									label: '工程实践',
									collapsed: true,
									items: [
										'frameworks/spring-ai/engineering/evaluation',
										'frameworks/spring-ai/engineering/docker-compose',
									],
								},
							],
						},
						{ label: 'LangChain', collapsed: true, items: [{ autogenerate: { directory: 'frameworks/langchain', collapsed: true } }] },
						{
							label: 'Deep Agents',
							collapsed: true,
							items: [
								'frameworks/deepagents',
								{
									label: '入门',
									collapsed: true,
									items: [
										'frameworks/deepagents/getting-started/quickstart',
										'frameworks/deepagents/getting-started/customization',
										'frameworks/deepagents/getting-started/models',
									],
								},
								{
									label: '部署',
									collapsed: true,
									items: ['frameworks/deepagents/deployment/going-to-production'],
								},
							],
						},
					],
				},
				{
					label: 'RAG 知识库',
					collapsed: true,
					items: [
						{ label: '基础架构', collapsed: true, items: [{ autogenerate: { directory: 'rag/fundamentals', collapsed: true } }] },
						{ label: '文档解析', collapsed: true, items: [{ autogenerate: { directory: 'rag/document-parsing', collapsed: true } }] },
						{ label: '向量数据库', collapsed: true, items: [{ autogenerate: { directory: 'rag/vector-db', collapsed: true } }] },
					],
				},
				{
					label: '智能体开发',
					collapsed: true,
					items: [
						{ label: 'Agent 基础', collapsed: true, items: [{ autogenerate: { directory: 'agent/fundamentals', collapsed: true } }] },
						{ label: 'Agent 实战进阶', collapsed: true, items: [{ autogenerate: { directory: 'agent/agent-practice', collapsed: true } }] },
						{ label: '开发范式', collapsed: true, items: [{ autogenerate: { directory: 'agent/development-patterns', collapsed: true } }] },
						{ label: 'Loop Engineering', collapsed: true, items: [{ autogenerate: { directory: 'agent/loop-engineering', collapsed: true } }] },
						{ label: 'Hermes', collapsed: true, items: [{ autogenerate: { directory: 'agent/hermes', collapsed: true } }] },
						{ label: 'Skills 架构', collapsed: true, items: [{ autogenerate: { directory: 'agent/skills', collapsed: true } }] },
						{ label: '记忆系统', collapsed: true, items: [{ autogenerate: { directory: 'agent/memory', collapsed: true } }] },
						{ label: 'Harness', collapsed: true, items: [{ autogenerate: { directory: 'agent/harness', collapsed: true } }] },
					],
				},
				{
					label: 'AI 编程',
					collapsed: true,
					items: [
						'ai-programming',
						{
							label: '认知篇',
							collapsed: true,
							items: [
								'ai-programming/cognition/essence-and-value',
								'ai-programming/cognition/tool-landscape',
								'ai-programming/cognition/human-ai-workflow',
								'ai-programming/cognition/trend-snapshot-2026',
							],
						},
						{
							label: '方法论',
							collapsed: true,
							items: [
								'ai-programming/methodology/sdd-and-harness',
								'ai-programming/methodology/spec-kit-and-openspec',
								'ai-programming/methodology/skills-and-superpowers',
							],
						},
					],
				},

				{
					label: '实战项目',
					collapsed: true,
					items: [{ autogenerate: { directory: 'projects', collapsed: true } }],
				},
			],
		}),
	],
});
