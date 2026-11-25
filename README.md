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

`scripts/tiles.py` recorta un mapa del proyecto de clasificación (solo lectura) y genera las teselas en
`public/tiles/`, la imagen de portada `src/assets/mapa-especies.png` y los límites en `src/data/mapa.json`.
Requiere Python con rasterio, pyproj y Pillow, y `gdal2tiles.py`. La paleta está en `scripts/paleta.py`
y debe coincidir con `src/data/especies.ts`.

## Publicación

GitHub Actions (`.github/workflows/deploy.yml`) construye y publica en GitHub Pages en cada push a `main`.
En el repositorio: Settings → Pages → Source: GitHub Actions.

## Pendiente

- Institución, equipo y correo de contacto (`TODO(usuario)` en `src/data/textos.ts`).
