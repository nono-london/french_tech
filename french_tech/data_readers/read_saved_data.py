"""Read data from download folder and convert columns to their relevant types"""

from ast import literal_eval  # use to convert csv string list into type list
from pathlib import Path

import pandas as pd

from french_tech.app_config import get_project_download_path

pd.set_option('display.max_columns', None)


def dataset_reader(file_name: str):
    # variables
    list_columns: list = ['market', 'type']  # columns with list
    int_columns: list = []  # columns with int
    float_columns: list = ['web_visits_chg_1Y', 'web_employees_chg_1Y', ]  # columns with floats or int that contains NA
    # check if file exists:
    file_full_path: Path = Path(get_project_download_path(), file_name)
    if not file_full_path.exists():
        exit(f"File not found\nFile Name: {file_full_path}")

    converters_list: dict = {column_to_filter: literal_eval for column_to_filter in
                             list_columns}

    data_df: pd.DataFrame = pd.read_csv(filepath_or_buffer=file_full_path,
                                        converters=converters_list,
                                        )

    for column in int_columns:
        data_df[column] = data_df[column].astype(int, errors='ignore')
    for column in float_columns:
        data_df[column] = data_df[column].astype(float, errors='ignore')

    return data_df


if __name__ == '__main__':
    FILE_NAME: str = "2023-03-12_french_startups.csv"
    print(dataset_reader(file_name=FILE_NAME))
