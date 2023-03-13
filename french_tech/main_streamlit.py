import streamlit as st

from french_tech.data_readers.read_saved_data import (dataset_reader,
                                                      read_markets,
                                                      read_types)

st.title("Company Search")


left_col_row1, right_column_row1 = st.columns(2)
with left_col_row1:
    selected_markets = st.multiselect(label="Company Markets",
                                  options=read_markets())
with right_column_row1:
    selected_types = st.multiselect(label="Company Types",
                                options=read_types())

print(selected_markets)
print(selected_types)
data_df = dataset_reader("2023-03-12_french_startups.csv")
st.dataframe(data_df)
