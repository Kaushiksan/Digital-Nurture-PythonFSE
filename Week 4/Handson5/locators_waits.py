"""
===========================================================
Hands-On 5
Task 36–39
Explicit Waits & FluentWait
===========================================================

Task 36
- Bootstrap Alerts
- Explicit Wait
- Assert Success Message

Task 37
- Compare time.sleep() vs Explicit Wait

Task 38
- element_to_be_clickable()
- visibility_of_element_located()

Task 39
- FluentWait
"""

import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager


driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install())
)

driver.maximize_window()

wait = WebDriverWait(driver, 10)

try:

    driver.get(
        "https://www.lambdatest.com/selenium-playground/bootstrap-alert-messages-demo"
    )

    print("=" * 60)
    print("Task 36")
    print("=" * 60)

    success_btn = wait.until(
        EC.element_to_be_clickable(
            (By.ID, "autoclosable-btn-success")
        )
    )

    success_btn.click()

    success_alert = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, ".alert-success")
        )
    )

    assert "successfully" in success_alert.text.lower()

    print("Success Alert Verified")

    print("\nAlert Text:")
    print(success_alert.text)

    print("\n" + "=" * 60)
    print("Task 37")
    print("=" * 60)

    start = time.time()

    time.sleep(3)

    sleep_time = time.time() - start

    print(f"time.sleep() took {sleep_time:.2f} seconds")

    start = time.time()

    wait.until(
        EC.visibility_of(success_alert)
    )

    explicit_time = time.time() - start

    print(f"Explicit Wait took {explicit_time:.2f} seconds")

    print("\nExplicit Wait is usually faster and more reliable.")

    print("\n" + "=" * 60)
    print("Task 38")
    print("=" * 60)

    clickable = wait.until(
        EC.element_to_be_clickable(
            (By.ID, "autoclosable-btn-success")
        )
    )

    print("Element is Clickable")

    visible = wait.until(
        EC.visibility_of_element_located(
            (By.ID, "autoclosable-btn-success")
        )
    )

    print("Element is Visible")

    print("""
Difference:

visibility_of_element_located
→ Element is present and visible.

element_to_be_clickable
→ Element is visible AND enabled,
   so Selenium can click it safely.
""")

    print("=" * 60)
    print("Task 39")
    print("=" * 60)

    fluent_wait = WebDriverWait(
        driver,
        timeout=10,
        poll_frequency=0.5,
        ignored_exceptions=[NoSuchElementException]
    )

    button = fluent_wait.until(
        EC.presence_of_element_located(
            (By.ID, "autoclosable-btn-success")
        )
    )

    print("FluentWait Successful")
    print(button.tag_name)

finally:

    driver.quit()

    print("\nBrowser Closed Successfully")
