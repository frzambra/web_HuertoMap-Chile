// Prefix a public path with the configured base (GitHub Pages serves under /<repo>/).
export function ruta(p: string): string {
  const base = import.meta.env.BASE_URL.replace(/\/$/, '');
  return `${base}/${p.replace(/^\//, '')}`;
}
