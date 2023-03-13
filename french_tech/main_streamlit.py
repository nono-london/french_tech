import streamlit as st
import pandas as pd
from french_tech.data_readers.read_saved_data import (dataset_reader,
                                                      read_markets,
                                                      read_types)

DATA_DF = dataset_reader("2023-03-12_french_startups.csv")


st.title("Company Search")

left_col_row1, right_column_row1 = st.columns(2)
with left_col_row1:
    selected_markets:list = st.multiselect(label="Company Markets",
                                  options=read_markets())
with right_column_row1:
    selected_types:list = st.multiselect(label="Company Types",
                                options=read_types())

def filter_dataset(selected_markets:list, selected_types:list)->pd.DataFrame:
    temp_df = DATA_DF[pd.DataFrame(DATA_DF['market'].tolist()).isin(selected_markets).any(1).values]
    temp_df = temp_df[pd.DataFrame(temp_df['type'].tolist()).isin(selected_types).any(1).values]
    return temp_df


print(selected_markets)
print(selected_types)
#data_df = dataset_reader("2023-03-12_french_startups.csv")
st.dataframe(filter_dataset(selected_markets=selected_markets,
                            selected_types=selected_types)
             )
