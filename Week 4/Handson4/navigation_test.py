"""
===========================================================
Hands-On 4
Task 28–31
WebDriver Navigation & Window Commands
===========================================================

Task 28
- Open Selenium Playground
- Navigate to Simple Form Demo
- Verify URL
- Navigate Back

Task 29
- Open Google in a new tab
- List all window handles
- Switch to the new tab
- Print Google title

Task 30
- Switch back
- Take screenshot

Task 31
- Get window size
- Set new window size
- Print updated window size

Why consistent window size?

A fixed browser window size ensures consistent rendering of
web pages across different machines. This helps avoid failures
caused by responsive layouts changing element positions.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install())
)

driver.implicitly_wait(10)

try:

    # Task 28
    driver.get("https://www.lambdatest.com/selenium-playground/")

    print("=" * 60)
    print("Task 28")
    print("=" * 60)

    driver.find_element(By.LINK_TEXT, "Simple Form Demo").click()

    assert "simple-form-demo" in driver.current_url

    print("URL Verified")
    print(driver.current_url)

    driver.back()

    print("Returned to Homepage")

    # Task 29
    print("\n" + "=" * 60)
    print("Task 29")
    print("=" * 60)

    driver.execute_script(
        'window.open("https://www.google.com");'
    )

    print("\nWindow Handles:")

    for handle in driver.window_handles:
        print(handle)

    driver.switch_to.window(driver.window_handles[1])

    print("\nGoogle Title:")
    print(driver.title)

    # Task 30
    print("\n" + "=" * 60)
    print("Task 30")
    print("=" * 60)

    driver.switch_to.window(driver.window_handles[0])

    driver.save_screenshot("playground_screenshot.png")

    print("Screenshot Saved")

    # Task 31
    print("\n" + "=" * 60)
    print("Task 31")
    print("=" * 60)

    print("Current Window Size:")

    print(driver.get_window_size())

    driver.set_window_size(1280, 800)

    print("\nUpdated Window Size:")

    print(driver.get_window_size())

finally:

    driver.quit()

    print("\nBrowser Closed Successfully")
