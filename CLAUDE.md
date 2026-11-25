# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Landing page for **HuertoMap-Chile**, a remote sensing product that maps fruit orchards in Chile from Sentinel-2 and Sentinel-1 imagery. The page presents the product. It is not where the science happens: the pipeline, models and methods book live in the source project at `/home/francisco/Documentos/Proyectos/clasificacion_huertos/` (read its `CLAUDE.md` and `book/index.qmd` before writing product copy). Treat that repo as **read-only** from here.

Design brief: sophisticated, modern, minimalist and professional. It should look like a serious geospatial/earth-observation product page (think Planet, Sentinel Hub, Vizzuality), not an academic poster and not a generic SaaS template.

## Product facts (source of truth for copy)

Pull numbers from the source repo, never invent them. As of 2026-11-23 (`clasificacion_huertos/book/index.qmd`):

- Two products: **orchard / non-orchard** map, and **species** map with 15 classes + `OTRO` (cerezo, vid de mesa, arándano, palto, nogal, manzano, duraznero/nectarino, cítricos, avellano, rubus, olivo, ciruelo, kiwi, peral, almendro). A dedicated **cherry** model on top.
- 10 m resolution. Inputs: Sentinel-2 L2A (Cloud Score+ masked) and monthly Sentinel-1 VV/VH, processed in Google Earth Engine; LightGBM models.
- Key capability: predicts an **agricultural season the model has never seen, without retraining** (leave-one-season-out validation).
- Within season, four pilot regions: orchard F1 0.96, species macro-F1 0.87, cherry per-orchard F1 0.92.
- Unseen season: orchard F1 0.93–0.97, 95–99 % of catastro orchards detected; cherry per-orchard F1 0.72–0.90; species per-orchard macro-F1 0.58–0.75.
- Wall-to-wall maps (Maule, O'Higgins 2024, unseen season) after post-processing: 1.01× and 1.06× the catastro area; cherry area 1.00–1.02×.
- Regions: pilots Coquimbo, O'Higgins, Maule, Araucanía; extension Ñuble, Biobío; Hito 3 maps for 2025/26 in Valparaíso, Metropolitana, O'Higgins, Maule, Ñuble.
- Reference labels: CIREN catastro frutícola (~294k polygons).
- Limitations to state honestly where metrics appear: metrics are against the catastro (which omits wine vineyards); independent probabilistic validation is planned for 2027; orchard model is weaker in Coquimbo.

If a number here disagrees with the source book, the book wins; update this section.

## Stack (defaults, change only with the user's agreement)

- **Astro** (static output) + **Tailwind CSS**, TypeScript. Minimal client JS; islands only where interaction earns it.
- **MapLibre GL JS** for an interactive map section (basemap + sample orchard/species tiles or a static COG-derived PNG/PMTiles overlay). Keep map data small; never commit large rasters.
- Fonts self-hosted (e.g. Inter / Inter Tight or Geist for UI, a mono for figures). No icon font; inline SVG.
- Deploy target: static hosting (GitHub Pages or Netlify/Vercel). No backend.
- Node 20 is installed (`node -v` → v20.19.5).

Commands once scaffolded:

```bash
npm install
npm run dev       # local dev server
npm run build     # static build to dist/
npm run preview   # serve the build
```

## Content and language

- The site is **Spanish only** (Chilean Spanish; audience: Chilean agriculture sector, ODEPA/CIREN, researchers, exporters). Set `<html lang="es-CL">`, use Spanish for all visible text, alt text, metadata and URLs/slugs, and format numbers the Chilean way (decimal comma, thousands point: 0,96; 293.736). No English locale or language switcher. Code, comments and commit messages stay in English.
- Suggested sections: hero (map visual + one-line value proposition) → what it maps → how it works (imagery → features → model → map, a clean diagram) → accuracy (few headline numbers, with the limitations note) → coverage (regions + seasons timeline) → interactive map preview → use cases (planning, export forecasting, water management, catastro updates) → team/institution and contact.
- Copy is short, concrete and numeric. No hype words ("revolutionary", "AI-powered" as a headline), no stock photos.

## Design rules

- Restrained palette: near-black/off-white neutrals plus one agricultural accent (deep green) and per-species colors only inside map legends. Define colors as CSS variables; support light and dark mode.
- Generous whitespace, strong typographic hierarchy, 12-column grid, max content width ~1200 px.
- Imagery is the visual identity: satellite crops, NDVI/phenology curves, map tiles. Reuse/re-render figures from `clasificacion_huertos/book/figuras/` and `reports/presentacion/figs/`, restyled to match the site (do not ship matplotlib defaults). Copy assets into `public/` or `src/assets/`; never symlink into the source repo.
- Motion is subtle (fade/translate on scroll, map fly-to). Respect `prefers-reduced-motion`.
- Mobile-first; no horizontal scroll at 360 px.
- Accessibility: WCAG 2.2 AA contrast, semantic landmarks, alt text on every figure, keyboard-usable map controls.
- Performance budget: Lighthouse ≥ 95 on all four categories; optimized images (AVIF/WebP via Astro `<Image>`), lazy-load the map.

## Constraints

- Do not read or copy credentials from the source project or its baseline folder (`.env`, `secrets/`).
- Do not expose Earth Engine project IDs, asset paths or internal file paths on the public page.
- Raw data on `/media/francisco/Respaldo_frzambra/` is off-limits for this repo.
- The project is registered in Earth Engine for noncommercial use; do not describe it as a commercial service or add pricing without the user's confirmation.
