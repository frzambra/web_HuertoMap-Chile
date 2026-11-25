"""Build the map preview assets from a HuertoMap-Chile map (read-only source).

Writes, inside this repo only:
  public/tiles/huerto/{z}/{x}/{y}.png    orchard / non-orchard layer
  public/tiles/especies/{z}/{x}/{y}.png  species layer (only where orchard)
  src/assets/mapa-especies.png           native-resolution render for the hero
  src/data/mapa.json                     crop bounds (lon/lat) for MapLibre

Run with a Python that has rasterio + pyproj + Pillow, and GDAL's gdal2tiles.py on PATH:
  python3 scripts/tiles.py
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
import rasterio
from PIL import Image
from pyproj import Transformer
from rasterio.windows import from_bounds

SRC = Path(
    "/home/francisco/Documentos/Proyectos/clasificacion_huertos/data/predictions/"
    "map_Maule_2024_s2s1_top60_OHiggins2021-Coquimbo2021-Araucania2021-Maule2022_to_"
    "OHiggins-Maule-Coquimbo-Araucania_cap_clean.tif"
)
# Curicó–Molina, Maule (EPSG:32719). ~30 % orchard, all 16 classes present.
BOX = (282000, 6104000, 306000, 6136000)
# Hero render: a 12 x 8 km window at native 10 m resolution.
HERO = (288000, 6114000, 300000, 6122000)
ZOOM = "9-14"

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from paleta import ESPECIES, HUERTO  # noqa: E402


def hex_rgb(h):
    h = h.lstrip("#")
    return [int(h[i:i + 2], 16) for i in (0, 2, 4)]


def rgba(orchard, species, layer):
    out = np.zeros((4, *orchard.shape), np.uint8)
    on = orchard == 1
    if layer == "huerto":
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


def main():
    tmp = ROOT / "scripts" / ".tmp"
    tmp.mkdir(exist_ok=True)
    with rasterio.open(SRC) as src:
        win = from_bounds(*BOX, src.transform)
        orchard = src.read(5, window=win)
        species = src.read(2, window=win)
        profile = dict(driver="GTiff", width=orchard.shape[1], height=orchard.shape[0], count=4,
                       dtype="uint8", crs=src.crs, transform=src.window_transform(win),
                       compress="deflate")

        for layer in ("huerto", "especies"):
            tif = tmp / f"{layer}.tif"
            with rasterio.open(tif, "w", **profile) as dst:
                dst.write(rgba(orchard, species, layer))
            out = ROOT / "public" / "tiles" / layer
            shutil.rmtree(out, ignore_errors=True)
            out.mkdir(parents=True)
            subprocess.run(["gdal2tiles.py", "--xyz", "-z", ZOOM, "-r", "near", "-w", "none",
                            "--processes", "4", "-q", str(tif), str(out)], check=True)
            for extra in out.glob("*.xml"):
                extra.unlink()

        hw = from_bounds(*HERO, src.transform)
        img = rgba(src.read(5, window=hw), src.read(2, window=hw), "especies")

    (ROOT / "src" / "assets").mkdir(parents=True, exist_ok=True)
    Image.fromarray(np.moveaxis(img, 0, -1), "RGBA").save(
        ROOT / "src" / "assets" / "mapa-especies.png", optimize=True)

    tr = Transformer.from_crs(32719, 4326, always_xy=True)
    w, s = tr.transform(BOX[0], BOX[1])
    e, n = tr.transform(BOX[2], BOX[3])
    (ROOT / "src" / "data").mkdir(parents=True, exist_ok=True)
    with open(ROOT / "src" / "data" / "mapa.json", "w") as f:
        json.dump({"bounds": [round(w, 5), round(s, 5), round(e, 5), round(n, 5)],
                   "minzoom": int(ZOOM.split("-")[0]), "maxzoom": int(ZOOM.split("-")[1]),
                   "region": "Maule", "temporada": "2023/24"}, f, indent=2)
    shutil.rmtree(tmp)


if __name__ == "__main__":
    main()
