// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import site from './site.config.json' with { type: 'json' };

export default defineConfig({
  site: site.site,
  output: 'static',
  trailingSlash: 'always',
  integrations: [
    starlight({
      title: site.title,
      description: site.description,
      locales: { root: { label: '简体中文', lang: 'zh-CN' } },
      favicon: '/favicon.svg',
      customCss: ['./src/styles/docs.css'],
      sidebar: [
        { label: '返回首页', link: '/' },
        { slug: 'start' },
        ...site.topics.map((topic) => ({
          label: topic.label,
          items: [{ autogenerate: { directory: topic.id } }],
        })),
      ],
    }),
  ],
});
