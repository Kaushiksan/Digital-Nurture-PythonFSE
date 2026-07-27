# ==========================================================
# Hands-On 5
# Selenium Locators & Explicit Waits
# ==========================================================

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def main():
    driver = webdriver.Chrome()

    try:
        # Open Selenium website
        driver.get("https://www.selenium.dev")

        # Maximize browser
        driver.maximize_window()

        # Wait until navigation bar is visible
        wait = WebDriverWait(driver, 10)

        downloads = wait.until(
            EC.element_to_be_clickable(
                (By.LINK_TEXT, "Downloads")
            )
        )

        # Click Downloads
        downloads.click()

        # Verify page title
        wait.until(
            EC.title_contains("Downloads")
        )

        print("Current Title:")
        print(driver.title)

        assert "Downloads" in driver.title

        print("\nTitle verification PASSED")

        # Locate heading
        heading = wait.until(
            EC.visibility_of_element_located(
                (By.TAG_NAME, "h1")
            )
        )

        print("\nHeading:")
        print(heading.text)

        # Print current URL
        print("\nURL:")
        print(driver.current_url)

    except Exception as e:
        print("\nError:")
        print(e)

    finally:
        driver.quit()
        print("\nBrowser Closed Successfully")


if __name__ == "__main__":
    main()
