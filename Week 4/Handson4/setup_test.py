# ==========================================================
# Hands-On 4
# Selenium WebDriver Setup
# ==========================================================

from selenium import webdriver
from selenium.webdriver.common.by import By


def main():
    # Selenium Manager automatically manages ChromeDriver
    driver = webdriver.Chrome()

    try:
        # Open website
        driver.get("https://www.selenium.dev")

        # Maximize browser
        driver.maximize_window()

        # Print title
        print("Page Title:")
        print(driver.title)

        # Print current URL
        print("\nCurrent URL:")
        print(driver.current_url)

        # Verify title
        assert "Selenium" in driver.title

        print("\nTitle verification PASSED.")

        # Find page heading
        heading = driver.find_element(By.TAG_NAME, "h1")
        print("\nHeading:")
        print(heading.text)

    finally:
        # Close browser
        driver.quit()
        print("\nBrowser closed successfully.")


if __name__ == "__main__":
    main()
