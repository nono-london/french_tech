from playwright.sync_api import Locator
from urllib.parse import urljoin

from french_tech.scrap_data.ecosystem_webpages.scrap_helpers.company_class import Company


def scrap_company_info(web_element: Locator, base_url: str) -> Company:
    """Scrap content of a row element representing company info and return it as a Company Class

        Return: Company Class
    """
    company = Company()

    # get company name & url
    name_element = web_element.locator(
        selector="xpath=// div[@class='entity-name__info'] // a[@class='entity-name__name-text']", )
    company.name = name_element.text_content().strip()
    company.company_dr_url = urljoin(base_url, name_element.get_attribute(name="href"))

    # get other data
    dr_signal_element = web_element.locator(
        selector="xpath=// div[@class='table-list-columns'] // p[@class='ranking-bar-legend']", )

    company.dealroom_signal = int(dr_signal_element.text_content().strip())

    print(company)

    return company
