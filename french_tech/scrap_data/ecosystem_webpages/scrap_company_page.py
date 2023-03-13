"""Scrap data that can be found on the website dedicated company page
    targeted info are:
        company website
        Twitter acct
        Linkedin acct
"""
from playwright.sync_api import sync_playwright
from typing import Union
from pathlib import Path
from french_tech.app_config import get_project_download_path

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


def get_company_info():
    with sync_playwright() as p:
        browser = p.firefox.launch(timeout=30_000, headless=False)
        page = browser.new_page()

        # Go to login page
        page.goto(url=DATA_URL, wait_until="domcontentloaded", timeout=DEFAULT_TIMEOUT)
        locator = page.locator(selector="xpath=// div[@class='item-details-info__website'] / a")
        print(locator.get_attribute("href"))
        locators = page.locator(selector="xpath=// div[@class='item-details-info__website'] / div[contains(@class,'resource-urls')] / a").all()
        for locator in locators:
            print(locator.get_attribute("href"))

if __name__ == '__main__':
    get_company_info()
