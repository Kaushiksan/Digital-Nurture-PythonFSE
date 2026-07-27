import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.mark.parametrize(
    "message",
    [
        "Hello",
        "Selenium Automation",
        "12345"
    ]
)
def test_simple_form_submission(driver, base_url, message):

    driver.get(base_url + "simple-form-demo")

    input_box = driver.find_element(By.ID, "user-message")

    input_box.clear()
    input_box.send_keys(message)

    driver.find_element(By.ID, "showInput").click()

    output = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.ID, "message")
        )
    )

    assert output.text == message


def test_checkbox_demo(driver, base_url):

    driver.get(base_url + "checkbox-demo")

    checkbox = driver.find_element(By.ID, "isAgeSelected")

    checkbox.click()

    assert checkbox.is_selected()

    checkbox.click()

    assert not checkbox.is_selected()


def test_dropdown_selection(driver, base_url):

    driver.get(base_url + "select-dropdown-demo")

    dropdown = Select(
        driver.find_element(By.ID, "select-demo")
    )

    dropdown.select_by_visible_text("Wednesday")

    selected = dropdown.first_selected_option.text

    assert selected == "Wednesday"
