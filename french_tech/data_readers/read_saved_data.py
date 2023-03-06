"""Read data from download folder and convert columns to their relevant types"""

from ast import literal_eval  # use to convert csv string list into type list
from pathlib import Path

import pandas as pd

from french_tech.app_config import get_project_download_path

pd.set_option('display.max_columns', None)


def dataset_reader(file_name: str):
    # variables
    list_columns: list = ['market', 'type']  # columns with list to be filtered on reduced to none duplicate
    int_columns: list = ['dealroom_signal', 'web_visits_chg_1Y', 'web_employees_chg_1Y', ]
    # check if file exists:
    file_full_path: Path = Path(get_project_download_path(), file_name)
    if not file_full_path.exists():
        exit(f"File not found\nFile Name: {file_full_path}")

    converters_list = {column_to_filter: literal_eval for column_to_filter in
                       list_columns}
    converters_int = {column_to_filter: int for column_to_filter in
                      int_columns}

    data_df: pd.DataFrame = pd.read_csv(filepath_or_buffer=file_full_path,
                                        converters={**converters_list, **converters_int})
    return data_df


if __name__ == '__main__':
    FILE_NAME: str = "2023-03-02_french_startups.csv"
    print(dataset_reader(file_name=FILE_NAME))
