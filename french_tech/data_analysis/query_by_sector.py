from pathlib import Path

import pandas as pd

from french_tech.app_config import get_project_download_path

pd.set_option('display.max_columns', None)

FILE_NAME: str = "2023-03-02_french_startups.csv"
FILE_FULL_PATH: Path = Path(get_project_download_path(), FILE_NAME)

data_df: pd.DataFrame = pd.read_csv(filepath_or_buffer=FILE_FULL_PATH)
print(data_df)
