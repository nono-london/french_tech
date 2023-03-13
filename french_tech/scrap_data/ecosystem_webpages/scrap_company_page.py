"""Scrap data that can be found on the website dedicated company page
    targeted info are:
        company website
        Twitter acct
        Linkedin acct
"""
from pathlib import Path
from typing import Union, List, Dict

import pandas as pd
from playwright.sync_api import sync_playwright, Page
from tqdm import tqdm

from french_tech.app_config import get_project_download_path
from french_tech.scrap_data.ecosystem_webpages.scrap_helpers.company_class import Company

DEFAULT_TIMEOUT: int = 10_000  # milliseconds

DATA_URL: str = "https://ecosystem.lafrenchtech.com/companies/edtake"


def _get_latest_dataset_path(only_select_all: bool) -> Union[Path, None]:
    """Get latest webscraped dataset by date
        only_select_all: if True
    """
    # get all data files that match pattern
    if only_select_all:
        files: list[Path] = sorted(Path(get_project_download_path()).glob("*_french_startups.csv"))
    else:
        files: list[Path] = sorted(Path(get_project_download_path()).glob("*_french_startups.csv"))
    if files is None or len(files) == 0:
        return None
    else:
        return files[-1]


def scrap_company_info(page: Page) -> Company:
    company = Company()
    locator = page.locator(selector="xpath=// div[@class='item-details-info__website'] / a")
    company.company_url = locator.get_attribute("href")

    locators = page.locator(
        selector="xpath=// div[@class='item-details-info__website'] / div[contains(@class,'resource-urls')] / a").all()
    for locator in locators:
        url = locator.get_attribute("href")
        if "twitter" in url:
            company.twitter_url = url
        elif "linkedin" in url:
            company.linkedin_url = url
        elif "facebook" in url:
            company.facebook_url = url
        else:
            print(f"New url type found: {url}")
    return company


def get_company_info(headless: bool = True):
    companies_df: pd.DataFrame = pd.read_csv(filepath_or_buffer=_get_latest_dataset_path(only_select_all=False),
                                             )

    companies: List[Dict] = []
    with sync_playwright() as p:
        browser = p.firefox.launch(timeout=30_000, headless=headless)
        page = browser.new_page()

        for index, row in tqdm(companies_df.iterrows(), total=len(companies_df)):
            # Go to deal room company page
            page.goto(url=row["company_dr_url"], wait_until="domcontentloaded", timeout=DEFAULT_TIMEOUT)

            # scrap data
            company = scrap_company_info(page=page)
            companies.append({"company_url": company.company_url,
                              "twitter_url": company.twitter_url,
                              "linkedin_url": company.linkedin_url,
                              "facebook_url": company.facebook_url,
                              })

    # save data
    save_path = Path(get_project_download_path(), "company_url_info.csv")

    companies_df = pd.DataFrame(companies)
    companies_df.to_csv(path_or_buf=save_path,
                        sep=",",
                        index=False)


if __name__ == '__main__':
    get_company_info()
