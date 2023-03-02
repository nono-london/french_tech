from playwright.sync_api import Page
from playwright.sync_api import TimeoutError as pw_TimeoutError


def handle_cookie_popup(web_page: Page, timeout: int = 10_000) -> bool:
    """Close the cookie popup to allow access to the page
        web_page: the playwright Page already created and active
        timeout: how long the program should wait for the popup before triggering a timeout error
        Return: True or False whether the popup has been found
    """
    # close cookies pop up window
    try:
        web_page.locator(selector="xpath=// button[@id='cw-yes']", ).click(timeout=timeout)
        return True
    except pw_TimeoutError as ex:
        print(f"Cookie popup not found\n"
              f"Error: {ex}")
        return False
