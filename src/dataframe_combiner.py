"""
TODO: Add module-level description here.
"""

import pandas as pd

def combine_dataframes(dataframes: object) -> pd.DataFrame:
    """
    Different dataframes are merged to a new dataframe. The new created dataframe that is merged from the dataframes and
    that is cleaned, will be returned
    :param: dataframes, an instance of the Class DataFrames that contains multiple pandas dataframes
    :return: a pandas dataframe: merged_clean_dataset
    """
    # create a new dataframe based on aantal_gemeente dataframe and ziekenhuisopnames dataframe
    new_aantallen_gemeente_df = pd.concat([dataframes.aantallen_gemeente_df1, dataframes.aantallen_gemeente_df2.iloc[1:, :]],
                                          ignore_index=True, axis=0)
    new_ziekenhuisopnames_df = pd.concat([dataframes.ziekenhuisopnames_df1, dataframes.ziekenhuisopnames_df2.iloc[1:, :]], ignore_index=True,
                                         axis=0)

    # add new column Province in two steps to the dataframe of ziekenhuisopnames because it is missing.
    # To do this we first group the dataframe aantallen gemeente on two columns: Province and Municipality_code
    # and assign this new data group to a variable province_df.
    province_df = new_aantallen_gemeente_df.groupby(['Province', 'Municipality_code', 'Municipality_name'], as_index=False, sort=False).agg({'Version': 'count'})

    # Then we join this new dataframe with the ziekenhuisopnames dataframe on the shared column Municipality_code
    # the new dataframe  merged_ziekenhuisopnames_df contains as well a column Province
    merged_ziekenhuisopnames_df = new_ziekenhuisopnames_df.merge(province_df, left_on=['Municipality_code'], right_on=['Municipality_code'], how='inner')

    # create new column 'join_column' in both dataframes for joining the dataframes and to avoid to join on empty columns which give wrong results
    new_aantallen_gemeente_df['join_column'] = new_aantallen_gemeente_df['Date_of_publication'] + new_aantallen_gemeente_df['Municipality_code'].fillna(new_aantallen_gemeente_df.Province).fillna('leeg')
    merged_ziekenhuisopnames_df['join_column'] = merged_ziekenhuisopnames_df['Date_of_statistics'] + merged_ziekenhuisopnames_df['Municipality_code'].fillna('leeg')

    # Join the two datasets on the just created column 'join_column' with an outer join
    merged_clean_dataset = new_aantallen_gemeente_df.merge(merged_ziekenhuisopnames_df, left_on=['join_column'], right_on=['join_column'], how='outer')

    return merged_clean_dataset