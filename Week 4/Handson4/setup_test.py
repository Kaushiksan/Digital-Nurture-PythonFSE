"""
===========================================================
Hands-On 4
Selenium WebDriver Setup, Browser Drivers & Basic Commands
===========================================================

Task 24 - Selenium Architecture

1. WebDriver
   WebDriver is the main Selenium component that communicates
   directly with the browser through browser-specific drivers.

2. Selenium Grid
   Selenium Grid allows execution of tests on multiple
   browsers and machines simultaneously.

3. Selenium IDE
   Selenium IDE is a browser extension used to record,
   playback and generate Selenium automation scripts.

Task 26

Implicit Wait

driver.implicitly_wait(10)

Implicit waits apply globally to all element searches.
Explicit waits are preferred because they wait only for
specific elements under specific conditions.
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def create_driver(headless=False):
    """Create Chrome WebDriver."""

    options = webdriver.ChromeOptions()

    if headless:
        options.add_argument("--headless=new")

    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(
        service=Service(
            ChromeDriverManager().install()
        ),
        options=options
    )

    driver.implicitly_wait(10)

    return driver


def main():

    driver = create_driver(headless=False)

    try:

        driver.get(
            "https://www.lambdatest.com/selenium-playground/"
        )

        print("=" * 60)
        print("LambdaTest Selenium Playground Opened")
        print("=" * 60)

        print("\nPage Title:")
        print(driver.title)

        print("\nCurrent URL:")
        print(driver.current_url)

    finally:

        driver.quit()

        print("\nBrowser Closed Successfully")


if __name__ == "__main__":
    main()
