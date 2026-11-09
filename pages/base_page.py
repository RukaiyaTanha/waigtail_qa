
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

from config.settings import TIMEOUT


class BasePage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, TIMEOUT)

    def open_url(self, url):
        self.driver.get(url)

    def click(self, locator):
        element = self.wait.until(
            EC.element_to_be_clickable(locator)
        )
        element.click()

    def enter_text(self, locator, value):
        element = self.wait.until(
            EC.visibility_of_element_located(locator)
        )
        element.clear()
        element.send_keys(value)

    def select_by_visible_text(self, locator, value):
        element = self.wait.until(
            EC.element_to_be_clickable(locator)
        )
        Select(element).select_by_visible_text(value)

    def get_attribute(self, locator, attribute):
        element = self.wait.until(
            EC.visibility_of_element_located(locator)
        )
        return element.get_attribute(attribute)

    def get_text(self, locator):
        element = self.wait.until(
            EC.visibility_of_element_located(locator)
        )
        return element.text
