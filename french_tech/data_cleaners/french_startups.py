""" Clean data from euro sign and add columns with min max revenue
"""

from ast import literal_eval  # use to convert csv string list into type list
from pathlib import Path

import pandas as pd

from french_tech.app_config import get_project_download_path

pd.set_option('display.max_columns', None)

# variables
FILE_NAME: str = "2023-03-02_french_startups.csv"
COLUMNS_TO_FILTER: list = ['market', 'type']  # columns with list to be filtered on reduced to none duplicate

# check if file exists:
FILE_FULL_PATH: Path = Path(get_project_download_path(), FILE_NAME)
if not FILE_FULL_PATH.exists():
    exit(f"File not found\nFile Name: {FILE_FULL_PATH}")

# read/load previously saved scraped file
# TODO: need to take off the currency and nominal denominator first:ex: € , m
data_df: pd.DataFrame = pd.read_csv(filepath_or_buffer=FILE_FULL_PATH,
                                    converters={column_to_filter: literal_eval for column_to_filter in
                                                COLUMNS_TO_FILTER})
data_df[['EV_min', 'EV_max']] = data_df['enterprise_value'].str.split('—', expand=True)

print(data_df)

# split EV into min max columns


print(data_df)
print(data_df.dtypes)
