"""Scrap data that can be found on the website dedicated company page
    targeted info are:
        company website
        Twitter acct
        LinkedIn acct
"""
from pathlib import Path
from typing import Union, List, Dict

import pandas as pd
from playwright.sync_api import (sync_playwright, Page,
                                 TimeoutError, Error)
from tqdm import tqdm

from french_tech.app_config import get_project_download_path
from french_tech.scrap_data.ecosystem_webpages.scrap_helpers.company_class import Company

DEFAULT_TIMEOUT: int = 10_000  # milliseconds

DATA_URL: str = "https://ecosystem.lafrenchtech.com/companies/edtake"
COMPANY_INFO_FILE_NAME: str = "company_urls_info.csv"


def _get_latest_dataset_path(only_select_all: bool) -> Union[Path, None]:
    """Get the latest web scraped dataset by date
        only_select_all: if True
    """
    # get all data files that match pattern
    if only_select_all:
        files: list[Path] = sorted(Path(get_project_download_path()).glob("*all_french_startups.csv"))
    else:
        files: list[Path] = sorted(Path(get_project_download_path()).glob("*_french_startups.csv"))
    if files is None or len(files) == 0:
        return None
    else:
        return files[-1]


def save_company_info(new_company_info_df: pd.DataFrame) -> pd.DataFrame:
    """Save company info data, and keep first saved in case of duplicate
     keeps previously saved data
     Returns the amalgamated DataFrame
    """
    # check and read current saved file
    file_path: Path = Path(get_project_download_path(), COMPANY_INFO_FILE_NAME)
    if file_path.exists():
        temp_df: pd.DataFrame = pd.read_csv(filepath_or_buffer=file_path,
                                            sep=',')

        new_company_info_df = pd.concat([temp_df, new_company_info_df],
                                        ignore_index=True,
                                        )
    # merge new df with old df
    new_company_info_df.drop_duplicates(subset=["company_dr_url"],
                                        inplace=True,
                                        keep='first',
                                        ignore_index=True)
    new_company_info_df.to_csv(path_or_buf=file_path,
                               sep=",",
                               index=False)
    return new_company_info_df


def scrap_company_info(page: Page) -> Company:
    company = Company()
    try:
        locator = page.locator(selector="xpath=// div[@class='item-details-info__website'] / a")
        company.company_url = locator.get_attribute("href")
    except Exception:
        return company

    try:
        locators = page.locator(
            selector="xpath=// div[@class='item-details-info__website'] / div[contains(@class,'resource-urls')] / a").all()
    except TimeoutError:
        return company
    except Exception:
        return company
    for locator in locators:
        try:
            url = locator.get_attribute("href").lower()
        except Exception:
            continue

        if "twitter" in url:
            company.twitter_url = url
        elif "linkedin" in url:
            company.linkedin_url = url
        elif "facebook" in url:
            company.facebook_url = url
        elif "apple" in url:
            company.apple_url = url
        elif "google" in url:
            company.google_url = url
        elif "instagram" in url:
            company.instagram_url = url
        else:
            print(f"New url type found: {url}")
    return company


def get_company_info(headless: bool = True,
                     select_all_dataset: bool = True):
    # load dataset
    companies_df: pd.DataFrame = pd.read_csv(
        filepath_or_buffer=_get_latest_dataset_path(only_select_all=select_all_dataset),
    )
    # scrap data
    companies: List[Dict] = []
    with sync_playwright() as p:
        browser = p.firefox.launch(timeout=30_000, headless=headless)
        page = browser.new_page()

        for index, row in tqdm(companies_df.iterrows(), total=len(companies_df)):
            # Go to deal room company page
            try:
                page.goto(url=row["company_dr_url"], wait_until="domcontentloaded", timeout=DEFAULT_TIMEOUT)
            except Error:
                print(f"Error while getting info for company url: {row['company_dr_url']}")

            except Exception as ex:
                print(f"Error while getting info for company url: {row['company_dr_url']}\n"
                      f"Error: {ex}")

            # scrap data
            company = scrap_company_info(page=page)
            companies.append({"company_dr_url": row["company_dr_url"],
                              "company_url": company.company_url,
                              "twitter_url": company.twitter_url,
                              "linkedin_url": company.linkedin_url,
                              "facebook_url": company.facebook_url,
                              "apple_url": company.apple_url,
                              "google_url": company.google_url,
                              "instagram_url": company.instagram_url,
                              })
            # save every 100 results
            if len(companies) % 100 == 0:
                companies_df = pd.DataFrame(companies)
                save_company_info(new_company_info_df=companies_df)

    companies_df = pd.DataFrame(companies)
    save_company_info(new_company_info_df=companies_df)


if __name__ == '__main__':
    get_company_info()
