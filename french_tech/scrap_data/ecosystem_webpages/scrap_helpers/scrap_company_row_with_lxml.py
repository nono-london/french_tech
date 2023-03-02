import logging
from urllib.parse import urljoin

from bs4 import BeautifulSoup as bs
from lxml import html
from playwright.sync_api import Locator

from french_tech.scrap_data.ecosystem_webpages.scrap_helpers.company_class import Company


# https://docs.python.org/3/howto/logging.html
# logger = logging.getLogger(__name__)


def scrap_company_info(web_element: Locator, base_url: str) -> Company:
    """Scrap content of a row element representing company info and return it as a Company Class

        Return: Company Class
    """
    company = Company()

    tree = html.fromstring(web_element.inner_html())

    # get company name & url
    name_elements = tree.xpath("// div[@class='entity-name__info'] // a[@class='entity-name__name-text']")
    company.name = name_elements[0].text.strip()
    company.company_dr_url = urljoin(base_url, name_elements[0].attrib["href"].strip())

    # get other data
    def shared_xpath(class_column_name: str):
        return f"// div[@class='table-list-columns'] / div[contains(@class,'table-list-column {class_column_name}')] "

    elements_to_find: list = tree.xpath(
        shared_xpath(class_column_name="startupRankingRating") + "// p[@class='ranking-bar-legend']", )
    company.dealroom_signal = int(elements_to_find[0].text_content().strip())

    elements_to_find = tree.xpath(shared_xpath(
        class_column_name="companyMarket") + " // div[@class='markets-column'] / ul[@class='item-list-column'] /li/a", )
    company.market = [element.text.strip() for element in elements_to_find]

    elements_to_find = tree.xpath(shared_xpath(
        class_column_name="type") + " // div[@class='business-type-column'] / ul[@class='item-list-column'] /li/a", )
    company.type = [element.text.strip() for element in elements_to_find]
    try:
        elements_to_find = tree.xpath(shared_xpath(
            class_column_name="companyEmployees") + " // div[@class='growth-line-chart'] // div[contains(@class,'growth-line-chart__content')] // span[contains(@class,'growth-line-chart__value')]", )
        company.growth = elements_to_find[0].text_content().strip()
    except IndexError as ex:
        web_soup = bs(web_element.inner_html(), "lxml")
        print(ex)
        # logging.exception()

    try:
        elements_to_find = tree.xpath(shared_xpath(
            class_column_name="companyEmployees") + " // div[@class='growth-line-chart'] // div[contains(@class,'growth-line-chart__hover-content')] // span[contains(@class,'growth-line-chart__value')]", )
        company.number_of_employees = elements_to_find[0].text_content().strip()
    except IndexError as ex:
        web_soup = bs(web_element.inner_html(), "lxml")
        print(ex)
        # logging.exception(ex)

    elements_to_find = tree.xpath(shared_xpath(class_column_name="launchDate") + " / time", )
    company.launch_date = elements_to_find[0].attrib["datetime"].strip().split("T")[0]

    try:
        # needs a try as will not retrieve element if valuation is None
        elements_to_find = tree.xpath(
            shared_xpath(class_column_name="valuation") + " // span[@class='valuation__value']", )
        company.valuation = elements_to_find[0].text_content().strip()
    except IndexError:
        pass

    elements_to_find = tree.xpath(shared_xpath(class_column_name="totalFunding"), )
    company.funding = elements_to_find[0].text_content().strip()

    elements_to_find = tree.xpath(shared_xpath(class_column_name="hqLocations"), )
    company.location = elements_to_find[0].text_content().strip()

    elements_to_find = tree.xpath(shared_xpath(class_column_name="lastFundingEnhanced"), )
    company.last_round = elements_to_find[0].text_content().strip()

    elements_to_find = tree.xpath(shared_xpath(class_column_name="totalJobsAvailable"), )
    company.number_job_opening = elements_to_find[0].text_content().strip()

    elements_to_find = tree.xpath(shared_xpath(class_column_name="jobRoles"), )
    company.job_board = elements_to_find[0].text_content().strip()

    elements_to_find = tree.xpath(shared_xpath(class_column_name="revenue"), )
    company.revenue = elements_to_find[0].text_content().strip()
    if company.revenue == "-":
        company.revenue = None

    elements_to_find = tree.xpath(shared_xpath(class_column_name="companyStatus"), )
    company.status = elements_to_find[0].text_content().strip()

    elements_to_find = tree.xpath(shared_xpath(class_column_name="growthStage") + "/span/span", )
    company.status = elements_to_find[0].text_content().strip()

    try:
        elements_to_find = tree.xpath(shared_xpath(
            class_column_name="companyWebVisitsRank") + "// span[contains(@class,'delta')]", )
        company.web_visits_chg_1Y = int(elements_to_find[0].text_content().strip())
    except (IndexError, ValueError):
        pass

    try:
        elements_to_find = tree.xpath(shared_xpath(
            class_column_name="companyEmployeesRank") + "// span[contains(@class,'delta')]", )
        company.web_employees_chg_1Y = int(elements_to_find[0].text_content().strip())
    except (IndexError, ValueError):
        pass

    try:
        elements_to_find = tree.xpath(
            shared_xpath(class_column_name="kpiMarketFirm") + "// span[@class='valuation__value']", )
        company.enterprise_value = elements_to_find[0].text_content().strip()
    except IndexError:
        pass
    if company.enterprise_value == '-':
        company.enterprise_value = None

    print(company)

    return company
