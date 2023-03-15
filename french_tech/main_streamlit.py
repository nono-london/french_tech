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

row1_col1, row1_col2, row1_col3 = st.columns(3)
with row1_col1:
    selected_markets: list = st.multiselect(label="Company Markets",
                                            options=read_markets())
with row1_col2:
    selected_types: list = st.multiselect(label="Company Types",
                                          options=read_types())
with row1_col3:
    selected_status: list = st.multiselect(label="Company Status",
                                           options=sorted(set(DATA_DF['status'].values.tolist())))

@st.cache_data
def filter_dataset(markets: list, types: list, status:list) -> pd.DataFrame:
    """Returns dataset that have any markets AND any types selected (not OR)"""
    if len(markets) > 0:
        temp_df = DATA_DF[pd.DataFrame(DATA_DF['market'].tolist()).isin(markets).any(1).values]
    else:
        temp_df = DATA_DF
    if len(types) > 0:
        temp_df = temp_df[pd.DataFrame(temp_df['type'].tolist()).isin(types).any(1).values]
    if len(status)>0:
        temp_df = temp_df[pd.DataFrame(temp_df['status'].tolist()).isin(status).any(1).values]
    temp_df.reset_index(drop=True, inplace=True)

    return temp_df


streamlit_df = filter_dataset(markets=selected_markets,
                              types=selected_types,
                              status=selected_status)



st.write(f"Found {len(streamlit_df)} results")
st.dataframe(streamlit_df)
