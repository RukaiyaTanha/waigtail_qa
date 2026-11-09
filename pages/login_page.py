
from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from config.settings import ADMIN_URL, ADMIN_USERNAME, ADMIN_PASSWORD


class LoginPage(BasePage):

    USERNAME = (By.NAME, "username")
    PASSWORD = (By.NAME, "password")

    LOGIN_BUTTON = (
        By.CSS_SELECTOR,
        "button[type='submit']"
    )

    def login(self):

        self.open_url(ADMIN_URL)

        self.enter_text(self.USERNAME, ADMIN_USERNAME)
        self.enter_text(self.PASSWORD, ADMIN_PASSWORD)

        self.click(self.LOGIN_BUTTON)

        self.wait.until(
            lambda driver: "/login/" not in driver.current_url
        )

        return self.driver.current_url
