"""Read data from download folder and convert columns to their relevant types"""

import math
from ast import literal_eval  # use to convert csv string list into type list
from pathlib import Path
from typing import Union, List, Optional

import pandas as pd

from french_tech.app_config import get_project_download_path

pd.set_option('display.max_columns', None)


def read_types() -> Union[List, None]:
    file_path = Path(get_project_download_path(), "column_filter_type.csv")
    if not file_path.exists():
        print(f"File column_filter_type.csv not found")
        return None
    type_df = pd.read_csv(filepath_or_buffer=file_path)
    return type_df["type"].values.tolist()


def read_markets() -> Union[List, None]:
    file_path = Path(get_project_download_path(), "column_filter_market.csv")
    if not file_path.exists():
        print(f"File column_filter_market.csv not found")
        return None
    type_df = pd.read_csv(filepath_or_buffer=file_path)
    return type_df["market"].values.tolist()


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


def check_company_info_exists(deal_room_url: str, company_info_file_path: Optional[str] = None) -> False:
    """ Return True if company urls are already stored"""
    if company_info_file_path is None:
        company_info_file_path = "company_urls_info.csv"
    file_path = Path(get_project_download_path(), company_info_file_path)

    # if local file doesn't exist return False
    if not file_path.exists():
        return False

    company_df: pd.datFrame = pd.read_csv(filepath_or_buffer=file_path, sep=',')
    row_df = company_df.loc[company_df["company_dr_url"] == deal_room_url]
    if len(row_df) == 0:
        return False
    else:
        if row_df.iloc[0]["company_url"] == "" or row_df.iloc[0]["company_url"] is None or math.isnan(
                row_df.iloc[0]["company_url"]):
            return False
        else:

            return True


if __name__ == '__main__':
    print(check_company_info_exists(deal_room_url="https://ecosystem.lafrenchtech.com/companies/tim_tek"))

    print(read_types())
    print(read_markets())

    FILE_NAME: str = "2023-03-12_french_startups.csv"
    print(dataset_reader(file_name=FILE_NAME))
