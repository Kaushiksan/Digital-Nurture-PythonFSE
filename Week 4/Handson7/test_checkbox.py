from pages.checkbox_page import CheckboxPage


def test_checkbox(driver, base_url):

    page = CheckboxPage(driver)

    page.navigate_to(base_url + "checkbox-demo")

    page.check_option()

    assert page.is_option_checked()

    page.uncheck_option()

    assert not page.is_option_checked()
