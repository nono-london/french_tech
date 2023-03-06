"""Launch the webscraper"""
from french_tech.data_analysis.keyword_filter_datasets import create_keywords_datasets
from french_tech.scrap_data.ecosystem_webpages.eco_french_tech import get_french_startups_data

if __name__ == '__main__':
    get_french_startups_data()
    create_keywords_datasets()
