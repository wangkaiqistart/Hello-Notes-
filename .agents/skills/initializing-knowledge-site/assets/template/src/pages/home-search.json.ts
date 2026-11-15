import { getCollection } from 'astro:content';
export async function GET() {
  const docs = await getCollection('docs', ({ data }) => !data.draft);
  return Response.json(
    docs.map((doc) => ({
      title: doc.data.title,
      description: doc.data.description ?? '',
      url: '/' + doc.id.replace(/\/index$/, '') + '/',
    })),
  );
}
