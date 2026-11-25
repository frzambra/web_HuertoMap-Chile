# HuertoMap-Chile · sitio web

Página de presentación de HuertoMap-Chile, mapas de huertos frutales de Chile a 10 m con Sentinel-2 y Sentinel-1.
Sitio estático con Astro, Tailwind CSS y MapLibre GL. Todo el texto está en `src/data/textos.ts`.

```bash
npm install
npm run dev       # http://localhost:4321
npm run build     # astro check + build a dist/
npm run preview
```

## Mapa de muestra

El mapa compara el Catastro Frutícola 2024 (izquierda) con la predicción (derecha) en Curicó y Molina.
`scripts/tiles.py` recorta el mapa del proyecto de clasificación (solo lectura), rasteriza el catastro
en la misma grilla de 10 m y genera las teselas en `public/tiles/{prediccion,catastro}-{especies,huerto}/`,
la imagen de portada `src/assets/mapa-especies.png` y los límites en `src/data/mapa.json`:

```bash
conda run -n huertos python scripts/tiles.py
```

Requiere `gdal2tiles.py`. La paleta está en `scripts/paleta.py` y debe coincidir con `src/data/especies.ts`.
El script imprime la razón de superficie mapa / catastro del recorte; si cambia, actualice `mapa.nota`
en `src/data/textos.ts`.

## Publicación

GitHub Actions (`.github/workflows/deploy.yml`) construye y publica en GitHub Pages en cada push a `main`.
En el repositorio: Settings → Pages → Source: GitHub Actions.

## Pendiente

- Institución, equipo y correo de contacto (`TODO(usuario)` en `src/data/textos.ts`).
