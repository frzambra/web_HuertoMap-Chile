"""Build the map preview assets from HuertoMap-Chile outputs (read-only source).

Writes, inside this repo only:
  public/tiles/{prediccion,catastro}-{huerto,especies}/{z}/{x}/{y}.png
  src/assets/mapa-especies.png           native-resolution render for the hero
  src/data/mapa.json                     crop bounds (lon/lat) for MapLibre

The catastro (Maule 2024 polygons) is rasterized on the same 10 m grid as the
prediction so both sides of the comparison look alike.

Needs rasterio, pyproj, Pillow, geopandas + pyarrow, and GDAL's gdal2tiles.py:
  conda run -n huertos python scripts/tiles.py
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

import geopandas as gpd
import numpy as np
import rasterio
from PIL import Image
from pyproj import Transformer
from rasterio.features import rasterize
from rasterio.windows import from_bounds

FUENTE = Path("/home/francisco/Documentos/Proyectos/clasificacion_huertos")
SRC = FUENTE / (
    "data/predictions/map_Maule_2024_s2s1_top60_OHiggins2021-Coquimbo2021-Araucania2021-"
    "Maule2022_to_OHiggins-Maule-Coquimbo-Araucania_cap_clean.tif"
)
CATASTRO = FUENTE / "data/interim/catastro_all.parquet"
CATASTRO_REGION, CATASTRO_ANIO = "Maule", 2024

# Curicó–Molina, Maule (EPSG:32719). ~30 % orchard, all 16 classes present.
BOX = (282000, 6104000, 306000, 6136000)
# Hero render: a 12 x 8 km window at native 10 m resolution.
HERO = (288000, 6114000, 300000, 6122000)
ZOOM = "9-14"

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from paleta import ESPECIES, HUERTO  # noqa: E402

CODIGO = {c: i for i, (c, _, _) in enumerate(ESPECIES, start=1)}


def hex_rgb(h):
    h = h.lstrip("#")
    return [int(h[i:i + 2], 16) for i in (0, 2, 4)]


def rgba(orchard, species, capa):
    """orchard: 0/1 array; species: 1-based class code (0 = none)."""
    out = np.zeros((4, *orchard.shape), np.uint8)
    on = orchard == 1
    if capa == "huerto":
        for b, v in enumerate(hex_rgb(HUERTO)):
            out[b][on] = v
        out[3][on] = 255
    else:
        for code, (_, _, color) in enumerate(ESPECIES, start=1):
            m = on & (species == code)
            for b, v in enumerate(hex_rgb(color)):
                out[b][m] = v
            out[3][m] = 255
    return out


def teselar(img, profile, nombre, tmp):
    tif = tmp / f"{nombre}.tif"
    with rasterio.open(tif, "w", **profile) as dst:
        dst.write(img)
    out = ROOT / "public" / "tiles" / nombre
    shutil.rmtree(out, ignore_errors=True)
    out.mkdir(parents=True)
    subprocess.run(["gdal2tiles.py", "--xyz", "-z", ZOOM, "-r", "near", "-w", "none",
                    "--processes", "4", "-q", str(tif), str(out)], check=True)
    for extra in out.glob("*.xml"):
        extra.unlink()
    rellenar(out)


def rango_teselas(z):
    """XYZ tile range covering BOX at zoom z."""
    import math
    tr = Transformer.from_crs(32719, 4326, always_xy=True)
    w, s = tr.transform(BOX[0], BOX[1])
    e, n = tr.transform(BOX[2], BOX[3])

    def xy(lon, lat):
        k = 2 ** z
        x = int((lon + 180) / 360 * k)
        y = int((1 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2 * k)
        return x, y

    (x0, y0), (x1, y1) = xy(w, n), xy(e, s)
    return range(x0, x1 + 1), range(y0, y1 + 1)


def rellenar(out):
    """gdal2tiles skips fully transparent tiles; write a blank one so the map gets no 404s."""
    vacia = None
    lo, hi = (int(v) for v in ZOOM.split("-"))
    for z in range(lo, hi + 1):
        xs, ys = rango_teselas(z)
        for x in xs:
            for y in ys:
                p = out / str(z) / str(x) / f"{y}.png"
                if p.exists():
                    continue
                if vacia is None:
                    vacia = out.parent / "_vacia.png"
                    Image.new("RGBA", (256, 256), (0, 0, 0, 0)).save(vacia, optimize=True)
                p.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(vacia, p)


def catastro_raster(shape, transform):
    g = gpd.read_parquet(CATASTRO, columns=["region", "survey_year", "clase", "geometry"])
    g = g[(g.region == CATASTRO_REGION) & (g.survey_year == CATASTRO_ANIO)]
    g = g.cx[BOX[0]:BOX[2], BOX[1]:BOX[3]]
    codes = g.clase.map(CODIGO).fillna(CODIGO["OTRO"]).astype(int)
    species = rasterize(zip(g.geometry, codes), out_shape=shape, transform=transform,
                        fill=0, dtype="uint8")
    print(f"catastro: {len(g)} polígonos en el recorte")
    return (species > 0).astype(np.uint8), species


def main():
    # Clear the previous single-source layout.
    for viejo in ("huerto", "especies"):
        shutil.rmtree(ROOT / "public" / "tiles" / viejo, ignore_errors=True)
    tmp = ROOT / "scripts" / ".tmp"
    tmp.mkdir(exist_ok=True)
    with rasterio.open(SRC) as src:
        win = from_bounds(*BOX, src.transform)
        orchard = src.read(5, window=win)
        species = src.read(2, window=win)
        transform = src.window_transform(win)
        profile = dict(driver="GTiff", width=orchard.shape[1], height=orchard.shape[0], count=4,
                       dtype="uint8", crs=src.crs, transform=transform, compress="deflate")
        hw = from_bounds(*HERO, src.transform)
        hero = rgba(src.read(5, window=hw), src.read(2, window=hw), "especies")

    cat_orchard, cat_species = catastro_raster(orchard.shape, transform)
    for capa in ("huerto", "especies"):
        teselar(rgba(orchard, species, capa), profile, f"prediccion-{capa}", tmp)
        teselar(rgba(cat_orchard, cat_species, capa), profile, f"catastro-{capa}", tmp)
    shutil.rmtree(tmp)
    (ROOT / "public" / "tiles" / "_vacia.png").unlink(missing_ok=True)

    print(f"superficie huerto, mapa / catastro: {(orchard == 1).sum() / cat_orchard.sum():.2f}")

    (ROOT / "src" / "assets").mkdir(parents=True, exist_ok=True)
    Image.fromarray(np.moveaxis(hero, 0, -1), "RGBA").save(
        ROOT / "src" / "assets" / "mapa-especies.png", optimize=True)

    tr = Transformer.from_crs(32719, 4326, always_xy=True)
    w, s = tr.transform(BOX[0], BOX[1])
    e, n = tr.transform(BOX[2], BOX[3])
    (ROOT / "src" / "data").mkdir(parents=True, exist_ok=True)
    with open(ROOT / "src" / "data" / "mapa.json", "w") as f:
        json.dump({"bounds": [round(w, 5), round(s, 5), round(e, 5), round(n, 5)],
                   "minzoom": int(ZOOM.split("-")[0]), "maxzoom": int(ZOOM.split("-")[1]),
                   "region": "Maule", "temporada": "2023/24",
                   "catastro": f"{CATASTRO_REGION} {CATASTRO_ANIO}"}, f, indent=2)


if __name__ == "__main__":
    main()
