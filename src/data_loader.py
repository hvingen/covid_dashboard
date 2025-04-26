from config import CSV_DIR, SHAPEFILES_DIR, GPKG_FILE
import pandas as pd
import geopandas as gpd

class Dataframes:
    def __init__(self):
        file1 = CSV_DIR / 'COVID-19_aantallen_gemeente_per_dag.csv'
        file2 = CSV_DIR / 'COVID-19_aantallen_gemeente_per_dag_tm_03102021.csv'
        file3 = CSV_DIR / 'COVID-19_ziekenhuisopnames.csv'
        file4 = CSV_DIR / 'COVID-19_ziekenhuisopnames_tm_03102021.csv'

        try:
            self.aantallen_gemeente_df1 = pd.read_csv(file1, sep=';')
            self.aantallen_gemeente_df2 = pd.read_csv(file2, sep=';')
            self.ziekenhuisopnames_df1 = pd.read_csv(file3, sep=';')
            self.ziekenhuisopnames_df2 = pd.read_csv(file4, sep=';')
        except Exception:
            self.aantallen_gemeente_df1 = None

        self.merged_clean_dataset = self.prepare_merged_dataset()

    def prepare_merged_dataset(self) -> pd.DataFrame:
        try:
            if self.aantallen_gemeente_df1 is None:
                raise ValueError("aantallen_gemeente_df1 is niet beschikbaar.")
            return self.aantallen_gemeente_df1.copy()
        except Exception:
            return None

    def set_merged_and_clean_dataset(self, df: pd.DataFrame):
        self.merged_clean_dataset = df

    def get_merged_and_clean_dataset(self) -> pd.DataFrame:
        return self.merged_clean_dataset


def load_province_shapefile():
    shapefile_path = SHAPEFILES_DIR / "B1_Provinciegrenzen_van_NederlandPolygon.shp"
    return gpd.read_file(shapefile_path)

def load_municipality_shapefile():
    gdf = gpd.read_file(GPKG_FILE, layer="gemeenten")
    return gdf
