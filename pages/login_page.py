
import os
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

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

        print("\n========== JENKINS LOGIN DEBUG ==========")

        print("Admin URL:", ADMIN_URL)
        print("Username configured:", bool(ADMIN_USERNAME))
        print("Password configured:", bool(ADMIN_PASSWORD))

        self.open_url(ADMIN_URL)

        self.enter_text(self.USERNAME, ADMIN_USERNAME)
        self.enter_text(self.PASSWORD, ADMIN_PASSWORD)

        self.click(self.LOGIN_BUTTON)

        try:
            self.wait.until(
                lambda driver: "/login/" not in driver.current_url
            )

            print("Login successful.")
            print("Current URL:", self.driver.current_url)

        except TimeoutException:

            print("\nLOGIN FAILED OR REDIRECT DID NOT COMPLETE")
            print("Current URL:", self.driver.current_url)
            print("Page title:", self.driver.title)

            print("\nPage content:")
            print(self.driver.find_element(
                By.TAG_NAME, "body"
            ).text)

            os.makedirs("screenshots", exist_ok=True)

            self.driver.save_screenshot(
                "screenshots/jenkins_login_failure.png"
            )

            print("\nScreenshot saved:")
            print("screenshots/jenkins_login_failure.png")

            raise RuntimeError(
                "Wagtail login did not complete. "
                "Check the login error message and screenshot."
            )

        return self.driver.current_url