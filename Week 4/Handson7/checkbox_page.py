from selenium.webdriver.common.by import By
from .base_page import BasePage


class CheckboxPage(BasePage):

    CHECKBOX = (By.ID, "isAgeSelected")

    def check_option(self):
        self.wait_for_element(self.CHECKBOX).click()

    def uncheck_option(self):
        self.wait_for_element(self.CHECKBOX).click()

    def is_option_checked(self):
        return self.wait_for_element(self.CHECKBOX).is_selected()
