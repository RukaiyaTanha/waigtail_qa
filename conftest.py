
import os
import pytest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from pages.login_page import LoginPage


@pytest.fixture
def driver(request):

    options = Options()

    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")

    if os.getenv("HEADLESS", "false").lower() == "true":
        options.add_argument("--headless=new")

    browser = webdriver.Chrome(options=options)

    yield browser

    report = getattr(request.node, "rep_call", None)

    if report and report.failed:

        os.makedirs("screenshots", exist_ok=True)

        browser.save_screenshot(
            f"screenshots/{request.node.name}.png"
        )

        print("\nFailure screenshot captured.")

    browser.quit()


@pytest.fixture
def admin_driver(driver):

    login_page = LoginPage(driver)

    login_page.login()

    return driver


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):

    outcome = yield
    report = outcome.get_result()

    setattr(item, f"rep_{report.when}", report)
