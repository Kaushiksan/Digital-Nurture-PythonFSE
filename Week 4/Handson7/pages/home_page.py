# ==========================================================
# Hands-On 7
# Page Object Model
# ==========================================================

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class HomePage:

    URL = "https://www.selenium.dev"

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self):
        self.driver.get(self.URL)

    def get_title(self):
        return self.driver.title

    def get_heading(self):
        heading = self.wait.until(
            EC.visibility_of_element_located(
                (By.TAG_NAME, "h1")
            )
        )
        return heading.text

    def click_downloads(self):
        button = self.wait.until(
            EC.element_to_be_clickable(
                (By.LINK_TEXT, "Downloads")
            )
        )
        button.click()

    def current_url(self):
        return self.driver.current_url
