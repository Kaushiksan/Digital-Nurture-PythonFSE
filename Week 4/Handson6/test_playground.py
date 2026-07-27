# ==========================================================
# Hands-On 6
# Selenium + pytest
# ==========================================================

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_selenium_homepage(driver):

    driver.get("https://www.selenium.dev")

    # Verify title
    assert "Selenium" in driver.title

    wait = WebDriverWait(driver, 10)

    heading = wait.until(
        EC.visibility_of_element_located(
            (By.TAG_NAME, "h1")
        )
    )

    print("\nHeading:")
    print(heading.text)

    downloads = wait.until(
        EC.element_to_be_clickable(
            (By.LINK_TEXT, "Downloads")
        )
    )

    assert downloads.is_displayed()

    print("\nDownloads link found.")

    print("\nCurrent URL:")
    print(driver.current_url)
