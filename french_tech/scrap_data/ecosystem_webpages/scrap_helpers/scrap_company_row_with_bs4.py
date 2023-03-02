from urllib.parse import urljoin

from bs4 import BeautifulSoup as bs
from playwright.sync_api import Locator
from playwright.sync_api import TimeoutError as pw_TimeoutError

from french_tech.scrap_data.ecosystem_webpages.scrap_helpers.company_class import Company


def scrap_company_info(web_element: Locator, base_url: str) -> Company:
    """Scrap content of a row element representing company info and return it as a Company Class

        Return: Company Class
    """
    company = Company()
    print("-" * 150)

    web_soup = bs(web_element.inner_html(), 'lxml')
    print(web_soup.prettify())

    # get company name & url
    name_element = web_element.locator(
        selector="xpath=// div[@class='entity-name__info'] // a[@class='entity-name__name-text']", )
    company.name = name_element.text_content().strip()
    company.company_dr_url = urljoin(base_url, name_element.get_attribute(name="href"))

    # get other data
    def shared_xpath(class_column_name: str):
        return f"xpath=// div[@class='table-list-columns'] / div[contains(@class,'table-list-column {class_column_name}')] "

    element_to_find = web_element.locator(
        selector=shared_xpath(class_column_name="startupRankingRating") + "// p[@class='ranking-bar-legend']", )
    company.dealroom_signal = int(element_to_find.text_content().strip())

    element_to_find = web_element.locator(
        selector=shared_xpath(
            class_column_name="companyMarket") + " // div[@class='markets-column'] / ul[@class='item-list-column'] /li/a", ).all()
    company.market = [element.text_content().strip() for element in element_to_find]

    element_to_find = web_element.locator(
        selector=shared_xpath(
            class_column_name="type") + " // div[@class='business-type-column'] / ul[@class='item-list-column'] /li/a", ).all()
    company.type = [element.text_content().strip() for element in element_to_find]

    element_to_find = web_element.locator(
        selector=shared_xpath(
            class_column_name="companyEmployees") + " // div[@class='growth-line-chart'] // div[@class='growth-line-chart__content hbox'] // span", )
    company.growth = element_to_find.first.text_content().strip()

    element_to_find = web_element.locator(
        selector=shared_xpath(
            class_column_name="companyEmployees") + " // div[@class='growth-line-chart'] // div[@class='growth-line-chart__hover-content vbox'] // span", )
    company.number_of_employees = element_to_find.first.text_content().strip()

    element_to_find = web_element.locator(
        selector=shared_xpath(class_column_name="launchDate") + " / time", )
    company.launch_date = element_to_find.get_attribute(name="datetime").strip().split("T")[0]
    try:
        # needs a try as will not retrieve element if valuation is None
        element_to_find = web_element.locator(
            selector=shared_xpath(class_column_name="valuation") + " // span[@class='valuation__value']", )
        company.valuation = element_to_find.text_content().strip()
    except pw_TimeoutError:
        pass

    element_to_find = web_element.locator(
        selector=shared_xpath(class_column_name="totalFunding"), )
    company.funding = element_to_find.text_content().strip()

    element_to_find = web_element.locator(
        selector=shared_xpath(class_column_name="hqLocations"), )
    company.location = element_to_find.text_content().strip()

    element_to_find = web_element.locator(
        selector=shared_xpath(class_column_name="lastFundingEnhanced"), )
    company.last_round = element_to_find.text_content().strip()

    element_to_find = web_element.locator(
        selector=shared_xpath(class_column_name="totalJobsAvailable"), )
    company.number_job_opening = element_to_find.text_content().strip()

    element_to_find = web_element.locator(
        selector=shared_xpath(class_column_name="jobRoles"), )
    company.job_board = element_to_find.text_content().strip()

    element_to_find = web_element.locator(
        selector=shared_xpath(class_column_name="revenue"), )
    company.revenue = element_to_find.text_content().strip()
    if company.revenue == "-":
        company.revenue = None

    element_to_find = web_element.locator(
        selector=shared_xpath(class_column_name="companyStatus"), )
    company.status = element_to_find.text_content().strip()

    element_to_find = web_element.locator(
        selector=shared_xpath(class_column_name="growthStage") + "/span/span", ).first
    company.status = element_to_find.text_content().strip()

    try:
        element_to_find = web_element.locator(
            selector=shared_xpath(
                class_column_name="companyWebVisitsRank") + "// span[contains(@class,'delta')]", ).first
        company.web_visits_chg_1Y = int(element_to_find.text_content().strip())
    except (pw_TimeoutError, ValueError):
        pass

    try:
        element_to_find = web_element.locator(
            selector=shared_xpath(
                class_column_name="companyEmployeesRank") + "// span[contains(@class,'delta')]", ).first
        company.web_employees_chg_1Y = int(element_to_find.text_content().strip())
    except (pw_TimeoutError, ValueError):
        pass

    try:
        element_to_find = web_element.locator(
            selector=shared_xpath(class_column_name="kpiMarketFirm") + "// span[@class='valuation__value']", ).first
        company.enterprise_value = element_to_find.text_content().strip()
    except pw_TimeoutError:
        pass
    if company.enterprise_value == '-':
        company.enterprise_value = None

    print(company)

    return company
