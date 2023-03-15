"""Read data from download folder and convert columns to their relevant types"""

from ast import literal_eval  # use to convert csv string list into type list
from pathlib import Path
from typing import Union, List, Optional

import pandas as pd

from french_tech.app_config import (g_sheet_company_info_url,
                                    g_sheet_companies)
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
        if isinstance(row_df.iloc[0]["company_url"], str):
            return True
        else:
            return False


def amalgamate_french_startups(save_locally: bool = True) -> pd.DataFrame:
    file_paths: List[Path] = list(Path(get_project_download_path()).glob("*french_startups.csv"))
    print(file_paths)
    # get local copies
    french_startups_dfs: List[pd.DataFrame] = [pd.read_csv(filepath_or_buffer=path) for path in file_paths]
    # get g_sheet copy
    gsheet_df = pd.read_csv(filepath_or_buffer=g_sheet_companies())
    # merge datasets
    result_df = pd.concat(objs=[gsheet_df] + french_startups_dfs, ignore_index=True)

    result_df.sort_values(by=["company_dr_url"], inplace=True)

    result_df.drop_duplicates(subset=["company_dr_url"], inplace=True)
    if save_locally:
        local_file_name: Path = Path(get_project_download_path(), "1900-01-01_all_french_startups.csv")
        result_df.to_csv(path_or_buf=local_file_name,
                         sep=",",
                         index=False)
    result_df.reset_index(drop=True, inplace=True)
    result_df["market"] = result_df["market"].apply(eval)
    result_df["type"] = result_df["type"].apply(eval)
    return result_df


def amalgamate_company_info(save_locally: bool = True) -> pd.DataFrame:
    file_paths: List[Path] = list(Path(get_project_download_path()).glob("*company_urls_info.csv"))
    print(file_paths)
    # get local copies
    company_info_dfs: List[pd.DataFrame] = [pd.read_csv(filepath_or_buffer=path) for path in file_paths]
    # get g_sheet copy
    gsheet_df = pd.read_csv(filepath_or_buffer=g_sheet_company_info_url())
    # merge datasets
    result_df = pd.concat(objs=[gsheet_df] + company_info_dfs, ignore_index=True)

    result_df.sort_values(by=list(result_df.columns), inplace=True)

    result_df.drop_duplicates(subset=["company_dr_url"], inplace=True, keep='last')
    if save_locally:
        local_file_name: Path = Path(get_project_download_path(), "1900-01-01_company_urls_info.csv")
        result_df.to_csv(path_or_buf=local_file_name,
                         sep=",",
                         index=False)
    result_df.reset_index(drop=True, inplace=True)
    return result_df


if __name__ == '__main__':
    print(amalgamate_french_startups(save_locally=True))

    print(amalgamate_company_info(save_locally=True))
    exit(0)

    print(check_company_info_exists(deal_room_url="https://ecosystem.lafrenchtech.com/companies/tim_tek"))
    exit(0)
    print(read_types())
    print(read_markets())

    FILE_NAME: str = "2023-03-12_french_startups.csv"
    print(dataset_reader(file_name=FILE_NAME))
