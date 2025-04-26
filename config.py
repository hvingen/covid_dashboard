from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.resolve()

SRC_DIR = PROJECT_ROOT / "src"
NOTEBOOKS_DIR = PROJECT_ROOT / 'notebooks'
SHAPEFILES_DIR = PROJECT_ROOT / 'data' / 'shapefiles'
CSV_DIR = PROJECT_ROOT / 'data' / 'csv'
EXPORTS_DIR = PROJECT_ROOT / 'notebooks' / 'exports'

GPKG_FILE = SHAPEFILES_DIR / "wijkenbuurten_2024_v1.gpkg"
LOG_FILE = EXPORTS_DIR / "export_log.csv"