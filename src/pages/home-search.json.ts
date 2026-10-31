import { getCollection } from 'astro:content';
import type { APIRoute } from 'astro';

export const GET: APIRoute = async () => {
  const documents = await getCollection('docs', ({ data }) => !data.draft);
  const index = documents
    .filter(({ id }) => !['index', '404'].includes(id))
    .map(({ id, data }) => ({
      title: data.title,
      description: data.description || '',
      url: `/${id.replace(/\/index$/, '')}/`,
    }))
    .sort((a, b) => a.title.localeCompare(b.title, 'zh-CN'));

  return new Response(JSON.stringify(index), {
    headers: { 'Content-Type': 'application/json; charset=utf-8' },
  });
};
