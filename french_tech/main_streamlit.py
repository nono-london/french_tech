import streamlit as st
from french_tech.data_readers.read_saved_data import dataset_reader

data_df=dataset_reader("2023-03-12_french_startups.csv")
st.dataframe(data_df)
st.text("this is teh page")