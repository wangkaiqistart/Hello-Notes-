interface SearchDocument {
  title: string;
  description: string;
  url: string;
}
interface PagefindResult {
  data: () => Promise<{
    url: string;
    meta: { title: string };
    excerpt: string;
  }>;
}
interface Pagefind {
  search: (query: string) => Promise<{ results: PagefindResult[] }>;
}
const form = document.querySelector<HTMLFormElement>('.search');
const input = document.querySelector<HTMLInputElement>('#query');
const results = document.querySelector<HTMLUListElement>('#results');
const status = document.querySelector<HTMLElement>('#search-status');
let version = 0;
let timer: ReturnType<typeof setTimeout>;
let documents: Promise<SearchDocument[]> | undefined;
let pagefind: Promise<Pagefind> | undefined;

async function search(query: string) {
  const ticket = ++version;
  if (!input || !results || !status) return;
  results.replaceChildren();
  results.hidden = true;
  if (!query) {
    status.textContent = '输入关键词，发现相关笔记';
    return;
  }
  status.textContent = '正在搜索';
  try {
    let matches: SearchDocument[];
    let fallback = import.meta.env.DEV;
    try {
      if (fallback) throw new Error('Development metadata index');
      const url = '/pagefind/pagefind.js';
      const engine = await (pagefind ??= import(/* @vite-ignore */ url).catch(
        (error) => {
          pagefind = undefined;
          throw error;
        },
      ));
      const response: Awaited<ReturnType<Pagefind['search']>> =
        await engine.search(query);
      matches = await Promise.all(
        response.results.slice(0, 8).map(async (result) => {
          const data = await result.data();
          const text =
            new DOMParser().parseFromString(data.excerpt, 'text/html').body
              .textContent ?? '';
          return { title: data.meta.title, description: text, url: data.url };
        }),
      );
    } catch {
      fallback = true;
      const docs = await (documents ??= fetch('/home-search.json')
        .then(async (response) => {
          if (!response.ok) throw new Error('Index unavailable');
          return (await response.json()) as SearchDocument[];
        })
        .catch((error) => {
          documents = undefined;
          throw error;
        }));
      const words = query.toLocaleLowerCase().split(/\s+/);
      matches = docs
        .filter((doc) =>
          words.every((word) =>
            `${doc.title} ${doc.description}`
              .toLocaleLowerCase()
              .includes(word),
          ),
        )
        .slice(0, 8);
    }
    if (ticket !== version) return;
    for (const match of matches) {
      const destination = new URL(match.url, location.origin);
      if (destination.origin !== location.origin) continue;
      const li = document.createElement('li');
      const a = document.createElement('a');
      const title = document.createElement('strong');
      const description = document.createElement('p');
      a.href = destination.pathname + destination.hash;
      title.textContent = match.title;
      description.textContent = match.description;
      a.append(title, description);
      li.append(a);
      results.append(li);
    }
    results.hidden = results.children.length === 0;
    status.textContent = results.hidden
      ? '没有找到相关笔记，可以浏览知识目录'
      : `找到 ${results.children.length} 篇相关笔记${fallback ? '（标题与简介）' : ''}`;
  } catch {
    if (ticket === version)
      status.textContent = '暂时无法搜索，可以直接浏览知识目录';
  }
}
input?.addEventListener('input', () => {
  ++version;
  clearTimeout(timer);
  timer = setTimeout(() => search(input.value.trim()), 180);
});
input?.addEventListener('keydown', (event) => {
  if (event.key === 'Escape') {
    input.value = '';
    void search('');
  }
  if (event.key === 'ArrowDown') {
    event.preventDefault();
    results?.querySelector('a')?.focus();
  }
});
form?.addEventListener('submit', (event) => {
  event.preventDefault();
  clearTimeout(timer);
  void search(input?.value.trim() ?? '');
});
