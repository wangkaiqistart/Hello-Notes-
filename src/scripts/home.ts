import { iconMarkup } from '../components/home/icon-markup';

interface SearchDocument {
  title: string;
  description: string;
  url: string;
}
interface Pagefind {
  search: (query: string) => Promise<{
    results: { data: () => Promise<{ url: string; meta: { title: string }; excerpt: string }> }[];
  }>;
}

const tabs = [...document.querySelectorAll<HTMLButtonElement>('[data-path]')];
const panels = [...document.querySelectorAll<HTMLElement>('[data-path-panel]')];
function selectPath(key: string, focus = false) {
  tabs.forEach((tab) => {
    const active = tab.dataset.path === key;
    tab.setAttribute('aria-selected', String(active));
    tab.tabIndex = active ? 0 : -1;
    if (active && focus) tab.focus();
  });
  panels.forEach((panel) => (panel.hidden = panel.dataset.pathPanel !== key));
}
tabs.forEach((tab, index) => {
  tab.disabled = false;
  tab.addEventListener('click', () => selectPath(tab.dataset.path!));
  tab.addEventListener('keydown', (event) => {
    const offset = (
      { ArrowRight: 1, ArrowDown: 1, ArrowLeft: -1, ArrowUp: -1 } as Record<string, number>
    )[event.key];
    const next = offset
      ? (index + offset + tabs.length) % tabs.length
      : event.key === 'Home'
        ? 0
        : event.key === 'End'
          ? tabs.length - 1
          : null;
    if (next !== null) {
      event.preventDefault();
      selectPath(tabs[next].dataset.path!, true);
    }
  });
});

const menuButton = document.querySelector<HTMLButtonElement>('.menu-toggle')!;
const mobileNav = document.querySelector<HTMLElement>('#mobile-nav')!;
function closeMenu() {
  mobileNav.hidden = true;
  menuButton.setAttribute('aria-expanded', 'false');
  menuButton.setAttribute('aria-label', '展开导航');
}
menuButton.disabled = false;
menuButton.addEventListener('click', () => {
  const expanded = menuButton.getAttribute('aria-expanded') === 'true';
  menuButton.setAttribute('aria-expanded', String(!expanded));
  menuButton.setAttribute('aria-label', expanded ? '展开导航' : '收起导航');
  mobileNav.hidden = expanded;
});
mobileNav.querySelectorAll('a').forEach((link) => link.addEventListener('click', closeMenu));
matchMedia('(min-width: 821px)').addEventListener('change', (event) => {
  if (event.matches) closeMenu();
});

const dialog = document.querySelector<HTMLDialogElement>('#search-dialog')!;
const input = document.querySelector<HTMLInputElement>('#search-input')!;
const results = document.querySelector<HTMLElement>('#search-results')!;
const count = document.querySelector<HTMLElement>('#search-count')!;
const triggers = [...document.querySelectorAll<HTMLButtonElement>('.search-trigger')];
const preferredPaths = [
  '/frameworks/spring-ai/',
  '/frameworks/spring-ai/core/chat-client/',
  '/frameworks/deepagents/',
  '/rag/fundamentals/what-is-rag/',
  '/agent/context-engineering/',
  '/agent/harness/',
];
let documentsPromise: Promise<SearchDocument[]> | undefined;
let pagefindPromise: Promise<Pagefind> | undefined;
let version = 0;
let selectedIndex = 0;
let debounce: ReturnType<typeof setTimeout> | undefined;

function getDocuments() {
  return (documentsPromise ??= fetch(`${import.meta.env.BASE_URL}home-search.json`)
    .then(async (response) => {
      if (!response.ok) throw new Error('Search index unavailable');
      return (await response.json()) as SearchDocument[];
    })
    .catch((error) => {
      documentsPromise = undefined;
      throw error;
    }));
}

function getPagefind(): Promise<Pagefind> {
  const url = `${import.meta.env.BASE_URL}pagefind/pagefind.js`;
  return (pagefindPromise ??= import(/* @vite-ignore */ url).catch((error) => {
    pagefindPromise = undefined;
    throw error;
  }));
}

function selectResult(index: number) {
  const links = [...results.querySelectorAll<HTMLAnchorElement>('a')];
  selectedIndex = links.length ? (index + links.length) % links.length : 0;
  links.forEach((link, i) => link.setAttribute('aria-current', String(i === selectedIndex)));
  links[selectedIndex]?.scrollIntoView({ block: 'nearest' });
}

function renderResults(documents: SearchDocument[], status: string) {
  results.replaceChildren();
  for (const [index, documentData] of documents.entries()) {
    const url = new URL(documentData.url, location.origin);
    if (url.origin !== location.origin) continue;
    const link = document.createElement('a');
    link.className = 'search-result';
    link.href = url.pathname + url.hash;
    link.id = `search-result-${index}`;
    const glyph = document.createElement('span');
    glyph.className = 'search-result-icon';
    glyph.innerHTML = iconMarkup('book');
    const text = document.createElement('span');
    text.textContent = documentData.title;
    const description = document.createElement('small');
    description.textContent = documentData.description;
    text.append(description);
    const arrow = document.createElement('span');
    arrow.innerHTML = iconMarkup('arrow-up-right');
    arrow.className = 'result-arrow';
    link.append(glyph, text, arrow);
    results.append(link);
  }
  if (!documents.length) {
    const empty = document.createElement('div');
    empty.className = 'search-empty';
    empty.textContent = '没有找到相关文档，试试其他关键词。';
    results.append(empty);
  }
  count.textContent = status;
  results.setAttribute('aria-busy', 'false');
  selectResult(0);
}

async function search(currentVersion: number) {
  const query = input.value.trim();
  results.setAttribute('aria-busy', 'true');
  count.textContent = query ? '正在搜索…' : '正在准备搜索…';
  const stillCurrent = () => currentVersion === version && dialog.open;
  try {
    const documents = await getDocuments();
    if (!stillCurrent()) return;
    if (!query) {
      const featured = preferredPaths.flatMap(
        (path) => documents.find((doc) => doc.url === path) || [],
      );
      renderResults(featured, `搜索 ${documents.length} 篇文档`);
      return;
    }
    let matches: SearchDocument[];
    let total: number;
    try {
      // Pagefind is generated by Starlight during the production build.
      if (import.meta.env.DEV) throw new Error('Use collection metadata in development');
      const engine = await getPagefind();
      if (!stillCurrent()) return;
      const response = await engine.search(query);
      total = response.results.length;
      const found = await Promise.all(response.results.slice(0, 8).map((result) => result.data()));
      matches = found.map((data) => {
        const excerpt = document.createElement('template');
        excerpt.innerHTML = data.excerpt;
        const description =
          documents.find((doc) => doc.url === new URL(data.url, location.origin).pathname)
            ?.description ||
          excerpt.content.textContent ||
          '';
        return {
          title: data.meta.title,
          url: data.url,
          description: description.replace(/\s+/g, ' ').trim().slice(0, 160),
        };
      });
    } catch {
      // Real title/description search also works in dev and when the full-text index cannot load.
      const words = query.toLocaleLowerCase().split(/\s+/);
      const found = documents.filter((doc) =>
        words.every((word) =>
          `${doc.title} ${doc.description} ${doc.url}`.toLocaleLowerCase().includes(word),
        ),
      );
      total = found.length;
      matches = found.slice(0, 8);
    }
    if (!stillCurrent()) return;
    renderResults(matches, `${total} 条匹配结果${total > 8 ? ' · 显示前 8 条' : ''}`);
  } catch {
    if (!stillCurrent()) return;
    results.replaceChildren();
    const message = document.createElement('div');
    message.className = 'search-empty';
    message.append('搜索暂时不可用，请检查网络后 ');
    const retry = document.createElement('button');
    retry.className = 'search-retry';
    retry.textContent = '重试';
    retry.addEventListener('click', () => void search(++version));
    message.append(retry);
    results.append(message);
    count.textContent = '搜索未能完成';
    results.setAttribute('aria-busy', 'false');
  }
}

function closeSearch() {
  clearTimeout(debounce);
  version++;
  if (dialog.open) dialog.close();
}
function openSearch() {
  if (dialog.open) return;
  closeMenu();
  dialog.showModal();
  input.value = '';
  input.focus();
  void search(++version);
}
triggers.forEach((trigger) => {
  trigger.disabled = false;
  trigger.addEventListener('click', openSearch);
  const apple = /Mac|iPhone|iPad/.test(navigator.userAgent);
  trigger.setAttribute('aria-keyshortcuts', apple ? 'Meta+K' : 'Control+K');
  trigger.querySelector('kbd')!.textContent = apple ? '⌘ K' : 'Ctrl K';
});
document.querySelector('#search-close')!.addEventListener('click', closeSearch);
dialog.addEventListener('close', () => {
  // Native close events may arrive after a user has already reopened the dialog.
  if (dialog.open) return;
  clearTimeout(debounce);
  version++;
});
dialog.addEventListener('keydown', (event) => {
  if (event.key === 'Escape' && !event.isComposing) {
    event.preventDefault();
    closeSearch();
  }
});
dialog.addEventListener('click', (event) => {
  if (event.target !== dialog) return;
  const bounds = dialog.getBoundingClientRect();
  if (
    event.clientX < bounds.left ||
    event.clientX > bounds.right ||
    event.clientY < bounds.top ||
    event.clientY > bounds.bottom
  )
    closeSearch();
});
results.addEventListener('click', (event) => {
  if (event.target instanceof Element && event.target.closest('a')) closeSearch();
});
input.addEventListener('input', (event) => {
  clearTimeout(debounce);
  const currentVersion = ++version;
  results.setAttribute('aria-busy', 'true');
  count.textContent = '正在搜索…';
  if (!(event as InputEvent).isComposing)
    debounce = setTimeout(() => void search(currentVersion), 160);
});
input.addEventListener('compositionend', () => {
  clearTimeout(debounce);
  const currentVersion = ++version;
  debounce = setTimeout(() => void search(currentVersion), 160);
});
input.addEventListener('keydown', (event) => {
  if (event.isComposing) return;
  if (event.key === 'ArrowDown' || event.key === 'ArrowUp') {
    event.preventDefault();
    selectResult(selectedIndex + (event.key === 'ArrowDown' ? 1 : -1));
  }
  if (event.key === 'Enter') {
    event.preventDefault();
    if (results.getAttribute('aria-busy') !== 'true')
      results.querySelectorAll<HTMLAnchorElement>('a')[selectedIndex]?.click();
  }
});
document.addEventListener('keydown', (event) => {
  if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === 'k') {
    event.preventDefault();
    if (dialog.open) closeSearch();
    else openSearch();
  }
  if (event.key === 'Escape' && !mobileNav.hidden) {
    closeMenu();
    menuButton.focus();
  }
});

const scene = document.querySelector<HTMLElement>('#knowledge-scene')!;
const motionButton = document.querySelector<HTMLButtonElement>('#motion-toggle')!;
const observer = new IntersectionObserver(
  ([entry]) => {
    if (!entry.isIntersecting) return;
    observer.disconnect();
    void import('./home-graph.js')
      .then(({ initKnowledgeGraph }) => initKnowledgeGraph(scene, motionButton))
      .catch(() => {
        scene.dataset.fallback = 'true';
        motionButton.hidden = true;
      });
  },
  { rootMargin: '160px' },
);
observer.observe(scene);
