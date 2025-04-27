"""
TODO: Add module-level description here.
"""

import pandas as pd
from config import SRC_DIR, CSV_DIR

date_pattern1 = r'(?:^\d{2}-0[1-9]|1[0-2])-\d{4}$'  # DD-MM-YYYY pattern
date_pattern2 = r'(?:^\d{4}-0[1-9]|1[0-2])-\d{2}$'  # YYYY-MM-DD pattern
date_pattern3 = r'(?:^\d{2}/0[1-9]|1[0-2])/\d{4}$'  # DD/MM/YYYY pattern
date_pattern4 = r'(?:^\d{4}/0[1-9]|1[0-2])/\d{2}$'  # YYYY/MM/DD pattern


def determine_date_format_date_of_publication(dataframes: object) -> str:
    """
    This function determines in which date format the data in the column 'Date_of_publication' is stored
    Four date formats are checked. If any column contains that format then that format can be used to read the data as a date
    :param an instance of the Class DataFrames : dataframes
    :return: string
    """
    if dataframes.aantallen_gemeente_df1['Date_of_publication'].str.contains(date_pattern1).any():
        date_format = '%d-%m-%Y'
    elif dataframes.aantallen_gemeente_df1['Date_of_publication'].str.contains(date_pattern2).any():
        date_format = '%Y-%m-%d'
    elif dataframes.aantallen_gemeente_df1['Date_of_publication'].str.contains(date_pattern3).any():
        date_format = '%d/%m/%Y'
    elif dataframes.aantallen_gemeente_df1['Date_of_publication'].str.contains(date_pattern4).any():
        date_format = '%Y/%m/%d'
    return date_format


def determine_date_format_date_of_statistics(dataframes: object) -> str:
    """
    This function determines in which date format the data in the column ''Date_of_statistics'' is stored
    Four date formats are checked. If any column contains that format then that format can be used to read the data as a date
    :param an instance of the Class DataFrames : dataframes
    :return: string
    """
    if dataframes.ziekenhuisopnames_df1['Date_of_statistics'].str.contains(date_pattern1).any():
        date_format = '%d-%m-%Y'
    elif dataframes.ziekenhuisopnames_df1['Date_of_statistics'].str.contains(date_pattern2).any():
        date_format = '%Y-%m-%d'
    elif dataframes.ziekenhuisopnames_df1['Date_of_statistics'].str.contains(date_pattern3).any():
        date_format = '%d/%m/%Y'
    elif dataframes.ziekenhuisopnames_df1['Date_of_statistics'].str.contains(date_pattern4).any():
        date_format = '%Y/%m/%d'
    return date_format


def clean_dataframe_aantallen_gemeente(dataframes: object):
    """
    This function cleans the dataframe for aantallen_gemeente
    - adds mew column in a date types using a previously determined date format
    - replaces the 9999 values for the column deceased with 0 for all rows with a date after 1-1-12023
    :param an instance of the Class DataFrames : dataframes
    """
    date_format = determine_date_format_date_of_publication(dataframes)
    # make a new column of type date to be able later to easier get the year and month from the 'Date_of_publication'
    # and to replace the value for the deceased records with 9999 after the date 01-01-2023 with the value 0
    dataframes.aantallen_gemeente_df1['Publication_date'] = pd.to_datetime(
        dataframes.aantallen_gemeente_df1['Date_of_publication'], format=date_format, errors='coerce')
    dataframes.aantallen_gemeente_df2['Publication_date'] = pd.to_datetime(
        dataframes.aantallen_gemeente_df2['Date_of_publication'], format=date_format, errors='coerce')

    # set the value of deceased to 0 in case it has the value 9999 after the date 01-01-2023
    dataframes.aantallen_gemeente_df1['Deceased'] = dataframes.aantallen_gemeente_df1.apply(
        lambda row: 0 if row['Deceased'] == 9999 and row['Publication_date'] >= pd.Timestamp(2023, 1, 1) else row['Deceased'], axis=1)


def clean_dataframe_ziekenhuisopnames(dataframes: object):
    """
    Adds mew column in both dataframes ziekenhuisopnames in a date type using a previously determined date format
    :param an instance of the Class DataFrames : dataframes
    """
    date_format = determine_date_format_date_of_statistics(dataframes)
    # make a new column of type date to be able later to easier get the year and month from the 'Date_of_statistics'
    dataframes.ziekenhuisopnames_df1['Statistics_date'] = pd.to_datetime(dataframes.ziekenhuisopnames_df1['Date_of_statistics'],
        format=date_format, errors='coerce')
    dataframes.ziekenhuisopnames_df2['Statistics_date'] = pd.to_datetime(dataframes.ziekenhuisopnames_df2['Date_of_statistics'],
        format=date_format, errors='coerce')


def add_columns_clean_merged_dataframe(dataframes: object):
    """
    This method ads new columns to the merged_clean_dataset in order to enable better grouping of data for the covid dashboard
    :param an instance of the Class Riool : dataframes
    """
    #create new columns for grouping the data on less columns and to ensure that the columns always have a value from one of the two original dataframes
    dataframes.merged_clean_dataset['Municipality_name_merged'] = dataframes.merged_clean_dataset['Municipality_name'].fillna(dataframes.merged_clean_dataset['Municipality_name_x'])
    dataframes.merged_clean_dataset['Province_merged'] = dataframes.merged_clean_dataset['Province_x'].fillna(dataframes.merged_clean_dataset['Province_y'])

    dataframes.merged_clean_dataset['Year'] = dataframes.merged_clean_dataset['Publication_date'].fillna(dataframes.merged_clean_dataset['Statistics_date']).dt.to_period('Y').astype(str)  # format YYYY
    dataframes.merged_clean_dataset['Month'] = dataframes.merged_clean_dataset['Publication_date'].fillna(dataframes.merged_clean_dataset['Statistics_date']).dt.month.astype(int)
    dataframes.merged_clean_dataset['Month_name'] = dataframes.merged_clean_dataset['Publication_date'].fillna(dataframes.merged_clean_dataset['Statistics_date']).dt.month_name().astype(str)


def remove_non_required_columns(clean_merged_dataset: object) -> object:
    """
    This method removes all columns that are not required to group and show data in the covid dashboard.
    This should lead to a better performance
    :param clean_merged_dataset:
    :return:
    """
    selected_cols = ['Total_reported', 'Deceased', 'Hospital_admission', 'Municipality_name_merged', 'Province_merged', 'Year', 'Month', 'Month_name']
    clean_small_merged_dataset = clean_merged_dataset[selected_cols]
    return clean_small_merged_dataset

