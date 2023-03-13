import pandas as pd
import streamlit as st

from french_tech.data_readers.read_saved_data import (dataset_reader,
                                                      read_markets,
                                                      read_types)

DATA_DF = dataset_reader("2023-03-12_french_startups.csv")

st.title("Company Search")

left_col_row1, right_column_row1 = st.columns(2)
with left_col_row1:
    selected_markets: list = st.multiselect(label="Company Markets",
                                            options=read_markets())
with right_column_row1:
    selected_types: list = st.multiselect(label="Company Types",
                                          options=read_types())


@st.cache_data
def filter_dataset(markets: list, types: list) -> pd.DataFrame:
    """Returns dataset that have any markets AND any types selected (not OR)"""
    if len(markets) > 0:
        temp_df = DATA_DF[pd.DataFrame(DATA_DF['market'].tolist()).isin(markets).any(1).values]
    else:
        temp_df = DATA_DF
    if len(types) > 0:
        temp_df = temp_df[pd.DataFrame(temp_df['type'].tolist()).isin(types).any(1).values]
    temp_df.reset_index(drop=True, inplace=True)

    return temp_df


st.dataframe(filter_dataset(markets=selected_markets,
                            types=selected_types)
             )
