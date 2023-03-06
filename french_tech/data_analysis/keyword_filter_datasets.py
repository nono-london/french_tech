""" Create files with datasets of unique keywords in columns ['market', 'type']
    files are named: column_filter_market.csv and column_filter_type.csv
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

# read previously saved scraped file
data_df: pd.DataFrame = pd.read_csv(filepath_or_buffer=FILE_FULL_PATH,
                                    converters={column_to_filter: literal_eval for column_to_filter in
                                                COLUMNS_TO_FILTER})


def create_keywords_datasets():
    # create dataset of non-duplicate choices in column to filter
    def create_sector_set(types_column: list):
        for sector_type in types_column:
            filter_keywords.add(sector_type)

    # loop through columns and create all dataset of keywords
    for column_to_filter in COLUMNS_TO_FILTER:
        filter_keywords: set = set()

        # filter all keywords
        data_df[column_to_filter].apply(lambda x: create_sector_set(x))

        # sort keywords
        sorted(filter_keywords, reverse=False)

        # save available choices
        column_choices_df: pd.DataFrame = pd.DataFrame(data=list(filter_keywords), columns=[column_to_filter])
        save_path = Path(get_project_download_path(), f'column_filter_{column_to_filter}.csv')
        column_choices_df.to_csv(path_or_buf=save_path,
                                 sep=',',
                                 index=False)

        print(f'Found {len(filter_keywords)} unique keywords for column: "{column_to_filter}"')


if __name__ == '__main__':
    create_keywords_datasets()
