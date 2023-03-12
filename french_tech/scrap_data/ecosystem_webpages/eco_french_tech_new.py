from datetime import datetime
from pathlib import Path
from random import randint

import pandas as pd
import tqdm
from playwright.sync_api import sync_playwright

from french_tech.app_config import get_project_download_path
from french_tech.scrap_data.ecosystem_webpages.scrap_helpers.company_class import Company
from french_tech.scrap_data.ecosystem_webpages.scrap_helpers.cookie_popup import handle_cookie_popup
from french_tech.scrap_data.ecosystem_webpages.scrap_helpers.scrap_company_row_with_lxml import \
    scrap_company_info as scrap_company_info_lxml
from french_tech.scrap_data.ecosystem_webpages.scrap_helpers.web_login import dealroom_login

LOGIN_URL: str = """https://app.dealroom.co/login?"""
DEFAULT_TIMEOUT: int = 10_000  # milliseconds


def get_french_startups_data(headless: bool = True, all_data: bool = False):
    """scrap datat from French tech website
        headless: show or not the web browser
        all_data: will scrap all data which have an HQ in France, Otherwise use default website filters
    """
    if all_data:
        data_url: str = """https://ecosystem.lafrenchtech.com/companies.startups/f/locations/allof_France/startup_ranking_rating_min/anyof_1?sort=startup_ranking_runners_up_rank"""
        file_name: str = "all_french_startups.csv"
    else:
        data_url: str = """https://ecosystem.lafrenchtech.com/companies.startups/f/employees_max/anyof_100/launch_year_min/anyof_2019/locations/allof_France/startup_ranking_rating_min/anyof_1/total_funding_max/anyof_1000000?sort=startup_ranking_runners_up_rank"""
        file_name: str = "french_startups.csv"

    with sync_playwright() as p:
        browser = p.firefox.launch(timeout=30_000, headless=headless)
        page = browser.new_page()

        # Go to login page
        page.goto(url=LOGIN_URL, wait_until="domcontentloaded", timeout=DEFAULT_TIMEOUT)
        dealroom_login(web_page=page, timeout=DEFAULT_TIMEOUT)

        # Wait to simulate user input
        page.wait_for_timeout(randint(5_000, 8_000))

        # Go to data page
        page.goto(url=data_url, wait_until="domcontentloaded", timeout=DEFAULT_TIMEOUT * 2)

        # close cookies pop up window
        handle_cookie_popup(web_page=page, timeout=DEFAULT_TIMEOUT)
        # wait to load content
        page.wait_for_load_state(state="domcontentloaded", timeout=DEFAULT_TIMEOUT)

        # find out how many companies to retrieve

        max_tries: int = 5
        company_number: int = -1
        while max_tries > 0:
            try:
                company_number_text: str = page.locator("xpath=// div[@class='table-info-bar__left']").text_content(
                    timeout=DEFAULT_TIMEOUT)
                company_number_text = company_number_text.split("Showing")[-1].strip().split("startups")[0].strip()
                company_number_text = company_number_text.replace(".", "").replace(",", "")
                company_number: int = int(company_number_text)
                print(f'Found a total of {company_number} companies to retrieve info from')
                break
            except ValueError:
                print(f'Not finding total number of companies available\n'
                      f'Attempt left: {max_tries}')
                page.wait_for_timeout(5_000)
                max_tries -= 1

        if company_number == -1 or company_number is None:
            print(f'Problem while getting number of companies to retrieve')
            exit(0)
        # select all table rows
        companies_set: set = set()

        company_elements = page.locator("xpath=// div[@class='table-list-item']").all()

        # get first available rows (usually 25)
        for index, company_element in enumerate(company_elements, start=1):
            print("-" * 50, f"Number: {index}", "-" * 50)

            company: Company = scrap_company_info_lxml(web_element=company_element, base_url=data_url)
            companies_set.add(company)

        # scroll down to get last results
        bar = tqdm.tqdm(total=company_number)
        temp_company_number: int = len(companies_set)
        max_tries: int = 10
        while max_tries > 0:
            # print("-" * 50, f"Total companies found: {len(companies_set)} ", "-" * 50)
            # Update the tqdm bar with the amount of new data
            new_data: int = len(companies_set) - temp_company_number
            bar.update(new_data)
            # reset new_data
            temp_company_number = len(companies_set)

            page.mouse.wheel(0, 1000)
            page.wait_for_load_state(state="domcontentloaded", timeout=DEFAULT_TIMEOUT * 4)

            # close cookies pop up window
            handle_cookie_popup(web_page=page, timeout=DEFAULT_TIMEOUT)

            company_elements = page.locator("xpath=// div[@class='table-list-item']").all()

            # get first available rows (usually 25)
            for index, company_element in enumerate(company_elements, start=1):
                company: Company = scrap_company_info_lxml(web_element=company_element, base_url=data_url)
                companies_set.add(company)

            # get out of the loop
            if temp_company_number == len(companies_set):  # means that no new data were found
                max_tries -= 1

        result_df = pd.DataFrame([vars(company) for company in companies_set])
        save_full_path = Path(get_project_download_path(), f"{datetime.utcnow().strftime('%Y-%m-%d')}_{file_name}")
        result_df.to_csv(save_full_path, sep=',', index=False)
        page.wait_for_timeout(10_000)
        browser.close()


if __name__ == '__main__':
    get_french_startups_data(headless=False,
                             all_data=False)
