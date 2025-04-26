from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.resolve()
SRC_DIR = PROJECT_ROOT / "src"
SHAPEFILES_DIR = PROJECT_ROOT / "data" / "shapefiles"

# Aangepast CSV_FOLDER naar CSV_DIR
CSV_DIR = PROJECT_ROOT / "data" / "csv"
EXPORT_FOLDER = PROJECT_ROOT / "notebooks" / "exports"
