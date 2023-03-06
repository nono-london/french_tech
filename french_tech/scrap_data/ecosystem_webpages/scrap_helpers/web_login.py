from random import randint

from playwright.sync_api import Page
from playwright.sync_api import TimeoutError as pw_TimeoutError

from french_tech.app_config_secret import ECOSYSTEM_USERNAME, ECOSYSTEM_PWD
from french_tech.scrap_data.ecosystem_webpages.scrap_helpers.cookie_popup import handle_cookie_popup


def dealroom_login(web_page: Page, timeout: int = 10_000) -> bool:
    """Handle the login process
        web_page: the playwright Page already created and active
        timeout: how long the program should wait for the popup before triggering a timeout error
        Return: True or False whether the login has been successful
    """

    # handle cookie if need be:
    handle_cookie_popup(web_page=web_page, timeout=timeout)

    # find login popup
    try:
        web_page.locator(selector="xpath=// button[@id='login']", ).click(timeout=timeout)
    except pw_TimeoutError as ex:
        print(f'Error while login\n'
              f'Error: {ex}')
        return False

    # login to website
    # username
    web_page.locator(selector="xpath=// input[@id='username']", ).type(text=ECOSYSTEM_USERNAME, )
    # simulate user pause between login steps
    web_page.wait_for_timeout(timeout=randint(2000, 5000))
    # password
    web_page.locator(selector="xpath=// input[@id='password']", ).type(text=ECOSYSTEM_PWD, )
    # simulate user pause between login steps
    web_page.wait_for_timeout(timeout=randint(2000, 5000))
    # click login/continue button
    web_page.get_by_text(text="Continue", exact=True).click(timeout=timeout)

    # handle_new_user(web_page=web_page, timeout=timeout)
    return True


def handle_new_user(web_page: Page, timeout: int = 10_000):
    # fill up New user form:
    # Full Name
    web_page.locator(selector="xpath=// input[@id='name']", ).type(text="John Smith", )
    # simulate user pause between login steps
    web_page.wait_for_timeout(timeout=randint(2000, 5000))
    web_page.locator(selector="xpath=// input[@id='userType']", ).click(timeout=timeout)
    web_page.locator(selector="xpath=// input[@id='react-select-2-input']", ).click(timeout=timeout)

    # click login/continue button
    web_page.get_by_text(text="Start exploring Dealroom.co", exact=True).click(timeout=timeout)
