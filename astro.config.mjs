// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

// https://astro.build/config
export default defineConfig({
	site: 'https://notes.wwkq.top',
	integrations: [
		starlight({
			title: 'Hello, Notes!',
			social: [
				{ icon: 'github', label: 'GitHub', href: 'https://github.com/wangkaiqistart/Hello-Notes-' },
			],
			editLink: {
				baseUrl: 'https://github.com/wangkaiqistart/Hello-Notes-/edit/main/',
			},
			sidebar: [
				{
					label: 'Guides',
					items: [
						{ label: 'Example Guide', slug: 'guides/example' },
					],
				},
				{
					label: 'Reference',
					items: [{ autogenerate: { directory: 'reference' } }],
				},
			],
		}),
	],
});
