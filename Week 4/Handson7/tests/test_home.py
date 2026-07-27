from pages.home_page import HomePage


def test_home_page(driver):

    home = HomePage(driver)

    home.open()

    assert "Selenium" in home.get_title()

    print("\nTitle Verified")

    print(home.get_heading())

    home.click_downloads()

    assert "downloads" in home.current_url().lower()

    print("\nDownloads page opened successfully")
