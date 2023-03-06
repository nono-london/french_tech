from ast import literal_eval
from pathlib import Path

import pandas as pd

from french_tech.app_config import get_project_download_path

pd.set_option('display.max_columns', None)

# variables
FILE_NAME: str = "2023-03-02_french_startups.csv"
COLUMN_TO_FILTER: str = 'market'

# read previously saved scraped file
FILE_FULL_PATH: Path = Path(get_project_download_path(), FILE_NAME)
data_df: pd.DataFrame = pd.read_csv(filepath_or_buffer=FILE_FULL_PATH,
                                    converters={COLUMN_TO_FILTER: literal_eval})

filter_keywords: set = set()


# create dataset of non-duplicate choices in column to filter
def create_sector_set(types_column: list):
    for sector_type in types_column:
        filter_keywords.add(sector_type)


data_df[COLUMN_TO_FILTER].apply(lambda x: create_sector_set(x))

sorted(filter_keywords)

# save available choices
column_choices_df: pd.DataFrame = pd.DataFrame(data=list(filter_keywords), columns=[COLUMN_TO_FILTER])
save_path = Path(get_project_download_path(), f'column_to_filter_{COLUMN_TO_FILTER}.csv')
column_choices_df.to_csv(path_or_buf=save_path,
                         sep=',',
                         index=False)
