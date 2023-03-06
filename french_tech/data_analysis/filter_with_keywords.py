from ast import literal_eval  # use to convert csv string list into type list
from pathlib import Path

import pandas as pd

from french_tech.app_config import get_project_download_path

pd.set_option('display.max_columns', None)

# variables
FILE_NAME: str = "2023-03-02_french_startups.csv"
COLUMN_TO_FILTER: str = 'market'
KEYWORDS_TO_USE: list = ['travel', 'telecom']

# check if file exists:
FILE_FULL_PATH: Path = Path(get_project_download_path(), FILE_NAME)
if not FILE_FULL_PATH.exists():
    exit(f"File not found\nFile Name: {FILE_FULL_PATH}")

# read previously saved scraped file
data_df: pd.DataFrame = pd.read_csv(filepath_or_buffer=FILE_FULL_PATH,
                                    converters={COLUMN_TO_FILTER: literal_eval})


# function to apply to filter rows
def find_keyword(column_name):
    for keyword in KEYWORDS_TO_USE:
        if keyword in column_name:
            return True
    return False


# select rows that contain either of the keywords
result_df = data_df[data_df[COLUMN_TO_FILTER].apply(lambda x: find_keyword(x))]
# sort data
result_df = result_df.sort_values(by=['name'], ascending=True, inplace=False)

if len(result_df) == 0:
    exit(f'Did not find any data for keywords:\n{KEYWORDS_TO_USE}')
else:
    print(f'Found {len(result_df)} companies for given keywords: {KEYWORDS_TO_USE}')

# create file name with max first 4 keywords (in order to avoid too long file names)
file_name = 'data_' + '_'.join([keyword[:4] for keyword in KEYWORDS_TO_USE[:4]]) + ".csv"
full_path_name = Path(get_project_download_path(), file_name)

# save dataset
result_df.to_csv(path_or_buf=full_path_name,
                 sep=',',
                 index=False)
print(f'Dataset save in download folder with file name:\n   {file_name}')
