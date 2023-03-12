from urllib.parse import urljoin

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

    # get company name
    try:
        name_elements = tree.xpath("// div[@class='entity-name__info'] // a[@class='entity-name__name-text']")
        company.name = name_elements[0].text.strip()
    except IndexError:
        print(f'Company name not found')
        return company

    print(f'### Getting data for company: {company.name} ###')

    # company URL
    try:
        company.company_dr_url = urljoin(base_url, name_elements[0].attrib["href"].strip())
    except Exception as ex:
        print(f'Error while getting company url:\nError: {ex}')

    # get other data
    def shared_xpath(class_column_name: str):
        return f"// div[@class='table-list-columns'] / div[contains(@class,'table-list-column {class_column_name}')] "

    # startupRankingRating
    try:
        elements_to_find: list = tree.xpath(
            shared_xpath(class_column_name="startupRankingRating") + "// p[@class='ranking-bar-legend']", )
        company.dealroom_signal = int(elements_to_find[0].text_content().strip())
    except IndexError as ex:
        print(f'startup RankingRating not found.\nError:{ex}')

    # companyMarket
    try:
        elements_to_find = tree.xpath(shared_xpath(
            class_column_name="companyMarket") + " // div[@class='markets-column'] / ul[@class='item-list-column'] /li/a", )
        company.market = [element.text.strip() for element in elements_to_find]
    except IndexError as ex:
        print(f'company market not found.\nError:{ex}')

    # business-type
    try:
        elements_to_find = tree.xpath(shared_xpath(
            class_column_name="type") + " // div[@class='business-type-column'] / ul[@class='item-list-column'] /li/a", )
        company.type = [element.text.strip() for element in elements_to_find]
    except IndexError as ex:
        print(f'company business-type not found.\nError:{ex}')
    # companyEmployees
    try:
        elements_to_find = tree.xpath(shared_xpath(
            class_column_name="companyEmployees") + " // div[@class='growth-line-chart'] // div[contains(@class,'growth-line-chart__content')] // span[contains(@class,'growth-line-chart__value')]", )
        company.growth = elements_to_find[0].text_content().strip()
    except IndexError as ex:
        print(f'company employees not found.\nError:{ex}')

    # companyEmployees
    try:
        elements_to_find = tree.xpath(shared_xpath(
            class_column_name="companyEmployees") + " // div[@class='growth-line-chart'] // div[contains(@class,'growth-line-chart__hover-content')] // span[contains(@class,'growth-line-chart__value')]", )
        company.number_of_employees = elements_to_find[0].text_content().strip()
    except IndexError as ex:
        print(f'companyEmployees not found, using default: 1900-01-01\nError is: {ex}')

    # get launch date
    try:
        elements_to_find = tree.xpath(shared_xpath(class_column_name="launchDate") + " / time", )
        company.launch_date = elements_to_find[0].attrib["datetime"].strip().split("T")[0]
    except IndexError as ex:
        print(f'Launch date not found, using default: 1900-01-01\nError is: {ex}')
        company.launch_date = "1900-01-01"

    # valuation
    try:
        # needs a try as will not retrieve element if valuation is None
        elements_to_find = tree.xpath(
            shared_xpath(class_column_name="valuation") + " // span[@class='valuation__value']", )
        company.valuation = elements_to_find[0].text_content().strip()
    except IndexError as ex:
        print(f'valuation not found.\nError:{ex}')

    # totalFunding
    try:
        elements_to_find = tree.xpath(shared_xpath(class_column_name="totalFunding"), )
        company.funding = elements_to_find[0].text_content().strip()
    except IndexError as ex:
        print(f'total funding not found.\nError:{ex}')

    # hqLocations
    try:
        elements_to_find = tree.xpath(shared_xpath(class_column_name="hqLocations"), )
        company.location = elements_to_find[0].text_content().strip()
    except IndexError as ex:
        print(f'HQ Locations not found.\nError:{ex}')

    # lastFundingEnhanced
    try:
        elements_to_find = tree.xpath(shared_xpath(class_column_name="lastFundingEnhanced"), )
        company.last_round = elements_to_find[0].text_content().strip()
    except IndexError as ex:
        print(f'last funding enhanced not found.\nError:{ex}')

    # totalJobsAvailable
    try:
        elements_to_find = tree.xpath(shared_xpath(class_column_name="totalJobsAvailable"), )
        company.number_job_opening = elements_to_find[0].text_content().strip()
    except IndexError as ex:
        print(f'total jobs available not found.\nError:{ex}')

    # job roles
    try:
        elements_to_find = tree.xpath(shared_xpath(class_column_name="jobRoles"), )
        company.job_board = elements_to_find[0].text_content().strip()
    except IndexError as ex:
        print(f'Job roles not found.\nError:{ex}')

    # revenues
    try:
        elements_to_find = tree.xpath(shared_xpath(class_column_name="revenue"), )
        company.revenue = elements_to_find[0].text_content().strip()
        if company.revenue == "-":
            company.revenue = None
    except IndexError as ex:
        print(f'Company revenues not found.\nError:{ex}')

    # Company status
    try:
        elements_to_find = tree.xpath(shared_xpath(class_column_name="companyStatus"), )
        company.status = elements_to_find[0].text_content().strip()
    except IndexError as ex:
        print(f'Company status not found.\nError:{ex}')

    # growth_stage
    try:
        elements_to_find = tree.xpath(shared_xpath(class_column_name="growthStage") + "/span/span", )
        company.status = elements_to_find[0].text_content().strip()
    except IndexError as ex:
        print(f'Growth Stage not found.\nError:{ex}')

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
