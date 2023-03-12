"""Launch the webscraper"""
from app_config import pack_python_libs_in_path

# pack libs in python sys path
pack_python_libs_in_path()

from french_tech.data_analysis.keyword_filter_datasets import create_keywords_datasets
from french_tech.scrap_data.ecosystem_webpages.eco_french_tech import get_french_startups_data

if __name__ == '__main__':
    get_french_startups_data(headless=True,
                             all_data=False)
    create_keywords_datasets()
