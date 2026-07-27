"""
===========================================================
Hands-On 5
Task 32–35
Locator Strategies
===========================================================

Task 32
Locate the message input using:
- ID
- Name
- Class Name
- Tag Name
- Absolute XPath
- Relative XPath

Task 33
Locate the same element using CSS Selectors.

Task 34
Locate checkbox labels using XPath text() and contains().

Task 35
Preferred Locator Ranking

1. ID
2. Name
3. CSS Selector
4. Relative XPath
5. Class Name
6. Absolute XPath

Absolute XPath is least preferred because it breaks whenever
the page structure changes.
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

    driver.get(
        "https://www.lambdatest.com/selenium-playground/simple-form-demo"
    )

    print("=" * 60)
    print("Task 32 - Locator Strategies")
    print("=" * 60)

    # ID
    element = driver.find_element(By.ID, "user-message")
    print("Located using ID")

    # Name
    element = driver.find_element(By.NAME, "message")
    print("Located using Name")

    # Class Name
    element = driver.find_element(By.CLASS_NAME, "form-control")
    print("Located using Class Name")

    # Tag Name
    element = driver.find_element(By.TAG_NAME, "input")
    print("Located using Tag Name")

    # Relative XPath
    element = driver.find_element(
        By.XPATH,
        "//input[@id='user-message']"
    )
    print("Located using Relative XPath")

    # Absolute XPath
    try:
        element = driver.find_element(
            By.XPATH,
            "/html/body/div/div[3]/div/div/div[1]/div/input"
        )
        print("Located using Absolute XPath")
    except Exception:
        print("Absolute XPath may vary depending on page updates.")

    print("\nTask 33 - CSS Selectors")

    driver.find_element(By.CSS_SELECTOR, "#user-message")
    print("CSS by ID")

    driver.find_element(
        By.CSS_SELECTOR,
        "input[name='message']"
    )
    print("CSS by Attribute")

    driver.find_element(
        By.CSS_SELECTOR,
        "div.w-6 > input"
    )
    print("CSS Parent > Child")

    print("\nTask 34 - Checkbox Demo")

    driver.get(
        "https://www.lambdatest.com/selenium-playground/checkbox-demo"
    )

    label = driver.find_element(
        By.XPATH,
        "//label[text()='Option 1']"
    )

    print(label.text)

    labels = driver.find_elements(
        By.XPATH,
        "//label[contains(text(),'Option')]"
    )

    print(f"Labels Found: {len(labels)}")

    print("\nTask 35 - Locator Ranking Completed")

finally:

    driver.quit()
