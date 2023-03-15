import pandas as pd
import streamlit as st

from french_tech.data_analysis.keyword_filter_datasets import create_keywords_datasets
from french_tech.data_readers.read_saved_data import (amalgamate_french_startups,
                                                      read_markets,
                                                      read_types)


# create_keywords_datasets

# gather data from web and local copies
@st.cache_data
def init_streamlit_datasets():
    dataset = amalgamate_french_startups(save_locally=True)
    create_keywords_datasets()
    return dataset


DATA_DF = init_streamlit_datasets()

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
