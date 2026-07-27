from pages.input_form_page import InputFormPage


def test_input_form(driver, base_url):

    page = InputFormPage(driver)

    page.navigate_to(base_url + "input-form-demo")

    page.fill_form(
        "Kaushik A",
        "kaushik@example.com",
        "9876543210",
        "No.24 Gandhi Street, Anna Nagar, Chennai"
    )

    page.submit_form()
