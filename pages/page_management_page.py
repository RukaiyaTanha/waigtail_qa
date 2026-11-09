from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException

from pages.base_page import BasePage
from config.settings import BASE_URL, PARENT_PAGE_ID


class PageManagementPage(BasePage):

    # Parent page
    ACTIONS_BUTTON = (
        By.CSS_SELECTOR,
        "button[aria-label='Actions']"
    )

    ADD_CHILD_PAGE = (
        By.CSS_SELECTOR,
        f"a[href='/admin/pages/{PARENT_PAGE_ID}/add_subpage/']"
    )

    # Gallery page selection
    GALLERY_PAGE = (
        By.CSS_SELECTOR,
        f"a[href='/admin/pages/add/base/gallerypage/{PARENT_PAGE_ID}/']"
    )

    # Gallery form fields
    PAGE_TITLE = (By.ID, "id_title")

    INTRODUCTION = (
        By.ID,
        "id_introduction"
    )

    COLLECTION = (
        By.ID,
        "id_collection"
    )

    SAVE_DRAFT = (
        By.CSS_SELECTOR,
        "button.action-save"
    )

    def navigate_to_parent_page(self):

        self.open_url(
            f"{BASE_URL}/admin/pages/{PARENT_PAGE_ID}/edit/"
        )

    def open_actions_menu(self):

        self.click(self.ACTIONS_BUTTON)

    def click_add_child_page(self):

        self.click(self.ADD_CHILD_PAGE)

    def select_gallery_page(self):

        self.click(self.GALLERY_PAGE)

    def create_gallery_page(self, title, introduction):

        self.enter_text(self.PAGE_TITLE, title)

        self.enter_text(
            self.INTRODUCTION,
            introduction
        )

        self.select_by_visible_text(
            self.COLLECTION,
            "Bakeries"
        )

    def save_draft(self):

        save_button = self.wait.until(
            EC.presence_of_element_located(self.SAVE_DRAFT)
        )

        self.scroll_to(save_button)

        save_button = self.wait.until(
            EC.element_to_be_clickable(self.SAVE_DRAFT)
        )

        try:
            save_button.click()
        except ElementClickInterceptedException:
            self.driver.execute_script(
                "arguments[0].click();", save_button
            )

        # Wait until Wagtail replaces the old editor button
        self.wait.until(
            EC.staleness_of(save_button)
        )

        # Wait for the refreshed title field
        self.wait.until(
            EC.visibility_of_element_located(self.PAGE_TITLE)
        )

    def verify_page_title(self, expected_title):

        actual_title = self.get_attribute(
            self.PAGE_TITLE,
            "value"
        )

        return actual_title == expected_title