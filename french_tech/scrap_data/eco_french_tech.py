from playwright.sync_api import sync_playwright

BASE_URL: str = """https://ecosystem.lafrenchtech.com/companies.startups/f/employees_max/anyof_100/launch_year_min/anyof_2019/locations/allof_France/startup_ranking_rating_min/anyof_1/total_funding_max/anyof_1000000?sort=startup_ranking_runners_up_rank"""
DEFAULT_TIMEOUT: int = 10_000  # milliseconds

with sync_playwright() as p:
    browser = p.firefox.launch(timeout=30_000, headless=False)
    page = browser.new_page()
    page.goto(url=BASE_URL, wait_until="domcontentloaded", timeout=DEFAULT_TIMEOUT)
    print(f"Page title is: {page.title}")

    # close cookies pop up window
    page.locator(selector="xpath=// button[@id='cw-yes']", ).click(timeout=DEFAULT_TIMEOUT)

    # select all table rows
    # page.wait_for_timeout(1_000)
    # https://playwright.dev/python/docs/locators#lists
    company_names = page.locator("xpath=// div[@class='table-list-item']").all()
    print(f'Company names size: {len(company_names)}')
    print(f'Company names: {company_names}')
    page.wait_for_timeout(1000)
    browser.close()
