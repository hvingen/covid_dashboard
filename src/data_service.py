"""
TODO: Add module-level description here.
"""

import pandas as pd
import data_loader
import dataframe_cleaner
import dataframe_combiner
from data_loader import load_province_shapefile

from data_loader import load_municipality_shapefile
# from data_service import get_prepared_covid_dataset

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


def get_province_heatmap_data(year):
    """TODO: Beschrijf deze functie."""
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
    """TODO: Beschrijf deze functie."""
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


def get_metric_mapping():
    """TODO: Beschrijf deze functie."""
    return {
    'Total reported': 'Total_reported',
    'Hospital admission': 'Hospital_admission',
    'Deceased': 'Deceased'
    }


def get_available_years(df):
    """TODO: Beschrijf deze functie."""
    return df['Year'].dropna().sort_values().unique().tolist()