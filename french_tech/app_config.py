import sys
from json import loads
from pathlib import Path
from typing import Union
from urllib.error import URLError
from urllib.request import Request, urlopen

import pandas as pd

COMPANY_INFO_FILE_NAME: str = "company_urls_info.csv"


def init_datasets():
    # company urls info
    company_urls_path: Path = Path(get_project_download_path(), COMPANY_INFO_FILE_NAME)
    if not company_urls_path.exists():
        company_urls_df: pd.DataFrame = pd.read_csv(filepath_or_buffer=g_sheet_company_info_url())
        company_urls_df.to_csv(path_or_buf=company_urls_path,
                               sep=',',
                               index=False
                               )
    # french tech companies

    companies_path: Path = Path(get_project_download_path(), "1900-01-01_all_french_startups.csv")
    if not companies_path.exists():
        company_urls_df: pd.DataFrame = pd.read_csv(filepath_or_buffer=g_sheet_companies())
        company_urls_df.to_csv(path_or_buf=companies_path,
                               sep=',',
                               index=False
                               )


def get_external_ip_address() -> Union[str, None]:
    """get external ip address"""

    url: str = 'https://jsonip.com/'

    req = Request(url)
    try:
        response = urlopen(req)
    except URLError as e:
        if hasattr(e, 'reason'):
            print('We failed to reach a server.')
            print('Reason: ', e.reason)
        elif hasattr(e, 'code'):
            print("The server couldn't fulfill the request.")
            print('Error code: ', e.code)
        return None

    # read JSOn data
    # https://stackoverflow.com/questions/32795460/loading-json-object-in-python-using-urllib-request-and-json-modules
    encoding = response.info().get_content_charset('utf-8')
    data = response.read()
    json_data = loads(data.decode(encoding))
    return json_data['ip']


def get_project_root_path() -> str:
    # https://stackoverflow.com/questions/5137497/find-the-current-directory-and-files-directory
    root_dir = Path(__file__).resolve().parent.parent
    return str(root_dir)


def get_project_download_path() -> str:
    # https://stackoverflow.com/questions/25389095/python-get-path-of-root-project-structure/40227116
    download_folder_path = Path(get_project_root_path(), "french_tech", "downloads")
    if not download_folder_path.exists():
        download_folder_path.mkdir(parents=True)
    return str(download_folder_path)


def pack_python_libs_in_path():
    """Adding manually libs that ae needed for the app to work"""

    python_app_folder_path: Path = Path(get_project_root_path())
    if str(python_app_folder_path) not in sys.path:
        print(f'Syspath, adding: {str(python_app_folder_path)}')
        sys.path.insert(1, str(python_app_folder_path))

    python_app_folder_path: Path = Path(get_project_root_path()).parent
    # mysql_helpers_folder_path: Path = Path(python_app_folder_path, 'mysql_helpers')
    # print(mysql_helpers_folder_path)
    #
    # # insert path in 2nd position, first position is reserved
    # if mysql_helpers_folder_path not in sys.path:
    #     sys.path.insert(1, str(mysql_helpers_folder_path))
    #
    # postgres_folder_path: Path = Path(python_app_folder_path, 'postgresql_helpers')
    # # insert path in 2nd position, first position is reserved
    # if postgres_folder_path not in sys.path:
    #     sys.path.insert(1, str(postgres_folder_path))
    #
    # proxy_helpers_folder_path: Path = Path(python_app_folder_path, 'proxy_helpers')
    # # insert path in 2nd position, first position is reserved
    # if proxy_helpers_folder_path not in sys.path:
    #     sys.path.insert(1, str(proxy_helpers_folder_path))
    #
    # selenium_folder_path: Path = Path(python_app_folder_path, 'selenium_helpers')
    # # insert path in 2nd position, first position is reserved
    # if selenium_folder_path not in sys.path:
    #     sys.path.insert(1, str(selenium_folder_path))


def g_sheet_company_info_url() -> str:
    """Return the csv version of the PUBLISHED GSheet as a csv.
        See File->Share-Publish to web on the GSheet
    """
    g_sheet_url = """https://docs.google.com/spreadsheets/d/e/2PACX-1vS2DmGW-VLUYEST5DD2G2Z8faRZWo3ghv4Vfd_i39wWZfQQRPwqZLlK920JIjkcrGtOkkM62wjy4VIF/pub?gid=149087946&single=true&output=csv"""
    return g_sheet_url


def g_sheet_companies() -> str:
    """Return the csv version of the PUBLISHED GSheet as a csv.
        See File->Share-Publish to web on the GSheet
    """
    g_sheet_url = """https://docs.google.com/spreadsheets/d/e/2PACX-1vS2DmGW-VLUYEST5DD2G2Z8faRZWo3ghv4Vfd_i39wWZfQQRPwqZLlK920JIjkcrGtOkkM62wjy4VIF/pub?gid=1957905855&single=true&output=csv"""
    return g_sheet_url


if __name__ == '__main__':
    init_datasets()
    pack_python_libs_in_path()
    print(sys.path)
