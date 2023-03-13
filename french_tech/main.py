"""Launch the webscraper"""
from app_config import pack_python_libs_in_path

# pack libs in python sys path
pack_python_libs_in_path()

from french_tech.data_analysis.keyword_filter_datasets import create_keywords_datasets
from french_tech.scrap_data.ecosystem_webpages.eco_french_tech import get_french_startups_data

if __name__ == '__main__':
    print(f"Getting UNFILTERED DATA: expect about 10k+ companies")
    get_french_startups_data(headless=True,
                             all_data=True,
                             print_errors=False)

    create_keywords_datasets()
    exit(0)

    print(f"Getting filtered data: expect about 500 companies")
    get_french_startups_data(headless=True,
                             all_data=False,
                             print_errors=False)
    create_keywords_datasets()

    exit(0)
