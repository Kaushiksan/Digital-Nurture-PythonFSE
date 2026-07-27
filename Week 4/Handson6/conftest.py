# ==========================================================
# Hands-On 6
# Pytest Fixture
# ==========================================================

import pytest
from selenium import webdriver


@pytest.fixture
def driver():

    driver = webdriver.Chrome()

    driver.maximize_window()

    yield driver

    driver.quit()
