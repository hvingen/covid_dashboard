"""
TODO: Add module-level description here.
"""

import pandas as pd

# 📂 Paden instellen + modules laden
import os, sys
from pathlib import Path

project_root = Path.cwd()
while not (project_root / 'config.py').exists() and project_root != project_root.parent:
    project_root = project_root.parent
sys.path.insert(0, project_root.as_posix())

from config import SRC_DIR, CSV_DIR
if SRC_DIR.as_posix() not in sys.path:
    sys.path.insert(0, SRC_DIR.as_posix())

print('Werkdirectory ingesteld op:', os.getcwd())

#from config import SRC_DIR, CSV_FOLDER
import data_loader
import dataframe_cleaner
import dataframe_combiner

from data_loader import load_province_shapefile

from data_loader import load_municipality_shapefile
#from data_service import get_prepared_covid_dataset


write_dataset_to_csv_file = False
remove_non_required_data = True


def get_prepared_covid_dataset() -> pd.DataFrame:
    """
    Creates data set to be used in order to be able to create covid dashboard
    The data service will call the functions to:
    - Read data to be used for dashboards and create data frames
    - Clean the data in the data frames
    - Combine the dataframes to new dataframe
    - Conditionally removes the not required columns
    - Conditionally writes the data of the dataframe to a csv file
    :param :
    :return: a pandas dataframe with cleaned and merged data
    """
    # read the data from RIVM and create dataframes in a class instance
    dfs = data_loader.Dataframes()

    #clean the data set for aantal gemeenten
    dataframe_cleaner.clean_dataframe_aantallen_gemeente(dfs)

    #clean the dataset for ziekenhuisopnamen
    dataframe_cleaner.clean_dataframe_ziekenhuisopnames(dfs)

    #create a new dataset by joining the cleaned dataset aantal gemeenten with the cleaned dataset ziekenhuisopnamen
    clean_dataset = dataframe_combiner.combine_dataframes(dfs)

    #update the class variable with the new created dataset
    dfs.set_merged_and_clean_dataset(clean_dataset)

    #add extra columns to dataset to enable better grouping of data for the dashboard
    dataframe_cleaner.add_columns_clean_merged_dataframe(dfs)

    if remove_non_required_data:
        # remove data that is not required in order to get a better performance
        clean_small_dataset = dataframe_cleaner.remove_non_required_columns(clean_dataset)
    else:
        clean_small_dataset = clean_dataset

    # update the class variable with the new created dataset
    dfs.set_merged_and_clean_dataset(clean_small_dataset)

    if write_dataset_to_csv_file:
        # write to csv to validate the merged data for testing purposes and validation
        dfs.merged_clean_dataset.to_csv('merged_clean_data.csv', index=False)

    return dfs.merged_clean_dataset

def get_prepared_riool_dataset() -> pd.DataFrame:
    """
    Creates data set to be used in order to be able to create riool dashboard
    The data service will call the functions to:
    - Read data to be used for dashboards and create data frames
    - Clean the data in the data frames
    - Combine the dataframes to new dataframe
    - Conditionally removes the not required columns
    - Conditionally writes the data of the dataframe to a csv file
    :param :
    :return: a pandas dataframe with cleaned and merged data
    """
    dfs_riool = data_loader.Riool()

    dfs_riool.aantallen_riool['Year'] = dfs_riool.aantallen_riool['Date_measurement'].dt.to_period('Y').astype(str)  # format YYYY
    dfs_riool.aantallen_riool['Month'] = dfs_riool.aantallen_riool['Date_measurement'].dt.month.astype(int)
    dfs_riool.aantallen_riool['Month_name'] = dfs_riool.aantallen_riool['Date_measurement'].dt.month_name().astype(str)

    return dfs_riool

def get_province_heatmap_data(year):
    """
    Combineer provinciegrenzen met COVID-data per provincie voor een gegeven jaar.
    """
    df = get_prepared_covid_dataset()
    df_year = df[df['Year'] == year]
    gdf = load_province_shapefile()
    df_grouped = df_year.groupby('Province_merged')[['Total_reported', 'Hospital_admission', 'Deceased']].sum().reset_index() 
    gdf = gdf.rename(columns={'PROV_NAAM': 'Province_merged'})   
    merged = gdf.merge(df_grouped, on='Province_merged', how='left')
    return merged

def get_municipality_heatmap_data(year):
    """
    Combineert gemeentegrenzen met COVID-data voor een gegeven jaar.
    """
    gdf = load_municipality_shapefile()
    df = get_prepared_covid_dataset()
    df_year = df[df['Year'] == year]
    df_grouped = df_year.groupby('Municipality_name_merged')[['Total_reported', 'Hospital_admission', 'Deceased']].sum().reset_index()
    gdf = gdf.rename(columns={'gemeentenaam': 'Municipality_name_merged'})
    merged = gdf.merge(df_grouped, on='Municipality_name_merged', how='left')
    return merged
    
    # Laad de COVID-data
    df = get_prepared_covid_dataset()
    
    # Filter op het geselecteerde jaar
    df_year = df[df['Year'] == year]
    
    # Groepeer en sommeer de data per gemeente
    df_grouped = df_year.groupby('gemeenten').sum().reset_index()
    
    # Merge de COVID-data met de gemeentegrenzen
    gdf = gdf.rename(columns={'gemeenten': 'Municipality_name_merged'})
    merged = gdf.merge(df_grouped, on='gemeenten', how='left')
    
    return merged
    
def get_province_heatmap_riool_data(year):
    """
    Combineer provinciegrenzen met COVID-data per provincie voor een gegeven jaar.
    """
    df = get_prepared_riool_dataset()
    df_year = df.aantallen_riool[df.aantallen_riool['Year'] == year]
    df_year = df_year.rename(columns={'RWZI_AWZI_name': 'Gemeentenaam'})
    df_prov = df.gemeenten_per_provincie
    merged_df = pd.merge(df_year, df_prov, on='Gemeentenaam', how='inner')
    
    gdf = load_province_shapefile()
    df_grouped = merged_df.groupby('Provincie')[['RNA_flow_per_100000']].sum().reset_index()
    gdf = gdf.rename(columns={'PROV_NAAM': 'Provincie'})   
    merged = gdf.merge(df_grouped, on='Provincie', how='left')
    return merged

def get_municipality_heatmap_riool_data(year):
    """
    Combineert gemeentegrenzen met COVID-data voor een gegeven jaar.
    """
    gdf = load_municipality_shapefile()
    df = get_prepared_riool_dataset()
    df_year = df.aantallen_riool[df.aantallen_riool['Year'] == year]
    df_grouped = df_year.groupby('RWZI_AWZI_name')[['RNA_flow_per_100000']].sum().reset_index()
    gdf = gdf.rename(columns={'gemeentenaam': 'RWZI_AWZI_name'})
    merged = gdf.merge(df_grouped, on='RWZI_AWZI_name', how='left')
    return merged
    

def get_metric_mapping():
    return {
    'Total reported': 'Total_reported',
    'Hospital admission': 'Hospital_admission',
    'Deceased': 'Deceased'
    }


def get_available_years(df):
    return df['Year'].dropna().sort_values().unique().tolist()