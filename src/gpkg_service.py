
import geopandas as gpd
from config import SHAPEFILES_DIR
from pathlib import Path
import fiona

def list_gpkg_files():
    return sorted([f.name for f in SHAPEFILES_DIR.glob("*.gpkg")])

def list_gpkg_layers(gpkg_name):
    gpkg_path = SHAPEFILES_DIR / gpkg_name
    with fiona.Env():
        return fiona.listlayers(gpkg_path)

def load_gpkg_layer(gpkg_name, layer_name):
    gpkg_path = SHAPEFILES_DIR / gpkg_name
    return gpd.read_file(gpkg_path, layer=layer_name)
