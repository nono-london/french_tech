""" Create files with datasets of unique keywords in columns ['market', 'type']
    files are named: column_filter_market.csv and column_filter_type.csv
"""

from ast import literal_eval  # use to convert csv string list into type list
from pathlib import Path
from typing import Union

import pandas as pd

from french_tech.app_config import get_project_download_path

pd.set_option('display.max_columns', None)

# variables
FILE_NAME: str = "2023-03-02_french_startups.csv"
COLUMNS_TO_FILTER: list = ['market', 'type']  # columns with list to be filtered on reduced to none duplicate


def _get_latest_dataset_path() -> Union[Path, None]:
    """Get latest webscraped dataset by date """
    # get all data files that match pattern
    files: list[Path] = sorted(Path(get_project_download_path()).glob("*_french_startups.csv"))
    if files is None or len(files) == 0:
        return None
    else:
        return files[-1]


def create_keywords_datasets(use_latest_dataset: bool = False):
    """create dataset of non-duplicate choices in column to filter"""

    # build default path:
    if use_latest_dataset:
        file_full_path: Path = _get_latest_dataset_path()
    else:
        file_full_path: Path = Path(get_project_download_path(), FILE_NAME)

    # check that file exists, if not stop process further
    if not file_full_path.exists():
        print(f"File not found\nFile Name: {file_full_path}")
        return
    else:
        print(f'Using dataset in file: {file_full_path.name}')

    # read previously saved scraped file
    data_df: pd.DataFrame = pd.read_csv(filepath_or_buffer=file_full_path,
                                        converters={column_to_filter: literal_eval for column_to_filter in
                                                    COLUMNS_TO_FILTER})

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
