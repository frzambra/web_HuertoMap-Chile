// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import tailwindcss from '@tailwindcss/vite';

// GitHub Pages: SITE_URL and BASE_PATH are set by .github/workflows/deploy.yml.
export default defineConfig({
  site: process.env.SITE_URL ?? 'http://localhost:4321',
  base: process.env.BASE_PATH ?? '/',
  output: 'static',
  integrations: [sitemap()],
  // Cast: @tailwindcss/vite and Astro bundle different Vite type versions.
  vite: { plugins: [/** @type {any} */ (tailwindcss())] },
});
