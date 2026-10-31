import { iconPaths } from './icons';

/** Icons are authored locally; document titles and excerpts are rendered as text. */
export function iconMarkup(name: string) {
  return `<svg class="icon" viewBox="0 0 24 24" aria-hidden="true">${iconPaths[name] || iconPaths['arrow-right']}</svg>`;
}
