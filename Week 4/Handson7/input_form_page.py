from selenium.webdriver.common.by import By
from .base_page import BasePage


class InputFormPage(BasePage):

    NAME = (By.NAME, "name")
    EMAIL = (By.NAME, "email")
    PHONE = (By.NAME, "phone")
    ADDRESS = (By.NAME, "address")
    SUBMIT = (By.XPATH, "//button[@type='submit']")

    def fill_form(self, name, email, phone, address):

        self.wait_for_element(self.NAME).send_keys(name)
        self.wait_for_element(self.EMAIL).send_keys(email)
        self.wait_for_element(self.PHONE).send_keys(phone)
        self.wait_for_element(self.ADDRESS).send_keys(address)

    def submit_form(self):
        self.wait_for_element(self.SUBMIT).click()
