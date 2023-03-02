from random import randint

from playwright.sync_api import sync_playwright

from french_tech.scrap_data.ecosystem_webpages.scrap_helpers.cookie_popup import handle_cookie_popup
from french_tech.scrap_data.ecosystem_webpages.scrap_helpers.scrap_company_row_with_lxml import \
    scrap_company_info as scrap_company_info_lxml
from french_tech.scrap_data.ecosystem_webpages.scrap_helpers.web_login import dealroom_login

LOGIN_URL: str = """https://app.dealroom.co/login?"""
DATA_URL: str = """https://ecosystem.lafrenchtech.com/companies.startups/f/employees_max/anyof_100/launch_year_min/anyof_2019/locations/allof_France/startup_ranking_rating_min/anyof_1/total_funding_max/anyof_1000000?sort=startup_ranking_runners_up_rank"""
DEFAULT_TIMEOUT: int = 10_000  # milliseconds

with sync_playwright() as p:
    browser = p.firefox.launch(timeout=30_000, headless=False)
    page = browser.new_page()

    # Go to login page
    page.goto(url=LOGIN_URL, wait_until="domcontentloaded", timeout=DEFAULT_TIMEOUT)
    dealroom_login(web_page=page, timeout=DEFAULT_TIMEOUT)

    # Wait to simulate user input
    page.wait_for_timeout(randint(5_000, 8_000))

    # Go to data page
    page.goto(url=DATA_URL, wait_until="domcontentloaded", timeout=DEFAULT_TIMEOUT * 2)
    print(f"Page title is: {page.title}")

    # close cookies pop up window
    handle_cookie_popup(web_page=page, timeout=DEFAULT_TIMEOUT)
    # wait to load content
    page.wait_for_load_state(state="domcontentloaded", timeout=DEFAULT_TIMEOUT)

    # find out how many companies to retrieve

    max_tries: int = 5
    while max_tries > 0:
        try:
            company_number_text: str = page.locator("xpath=// div[@class='table-info-bar__left']").text_content(
                timeout=DEFAULT_TIMEOUT)
            company_number: int = int(company_number_text.split("Showing")[-1].strip().split("startups")[0].strip())
        except ValueError:
            print(f'Not finding total number of companies available\n'
                  f'Attempt left: {max_tries}')
            page.wait_for_timeout(5_000)
            max_tries += -1
        break

    # select all table rows

    # get first 25 rows
    company_elements = page.locator("xpath=// div[@class='table-list-item']").all()
    print(f'Company names size: {len(company_elements)}')
    # print(f'Company names: {company_elements}')

    for index, company_element in enumerate(company_elements, start=1):
        print("-" * 50, f"Number: {index}", "-" * 50)

        scrap_company_info_lxml(web_element=company_element, base_url=DATA_URL)

    page.wait_for_timeout(10_000)
    browser.close()
