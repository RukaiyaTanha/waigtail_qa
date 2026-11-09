
import re

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def test_tc08_edit_published_gallery_page(admin_driver):

    wait = WebDriverWait(admin_driver, 15)

    # Open the parent page explorer
    admin_driver.get("http://127.0.0.1:8000/admin/pages/60/")

    # Collect child page editor links dynamically
    page_links = admin_driver.find_elements(
        By.CSS_SELECTOR,
        "a[href*='/admin/pages/'][href*='/edit/']"
    )

    page_urls = list(dict.fromkeys([
        link.get_attribute("href")
        for link in page_links
        if link.is_displayed()
        and re.search(
            r"/admin/pages/\d+/edit/",
            link.get_attribute("href") or ""
        )
    ]))

    selected_page_url = None

    # Find a published Gallery page
    for page_url in page_urls:

        admin_driver.get(page_url)

        try:
            wait.until(
                EC.presence_of_element_located((By.ID, "id_title"))
            )

            page_source = admin_driver.find_element(
                By.TAG_NAME, "body"
            ).text

            is_gallery = "Gallery page" in page_source

            is_live = len(
                admin_driver.find_elements(
                    By.ID, "status-sidebar-live"
                )
            ) > 0

            if is_gallery and is_live:
                selected_page_url = page_url
                break

        except TimeoutException:
            continue

    assert selected_page_url, (
        "No published Gallery page was found."
    )

    # Read the existing introduction
    introduction = wait.until(
        EC.presence_of_element_located((By.ID, "id_introduction"))
    )

    original_text = introduction.get_attribute("value") or ""

    updated_text = (
        original_text + " Updated by TC08 automated test."
    )

    # Update introduction
    introduction.clear()
    introduction.send_keys(updated_text)

    # Open the Save draft dropdown
    dropdown_button = wait.until(
        EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            "button.w-dropdown__toggle.button"
        ))
    )
    dropdown_button.click()

    # Publish the updated page
    publish_button = wait.until(
        EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            "button[name='action-publish']"
        ))
    )
    publish_button.click()

    # Wait for Wagtail to redirect to the parent explorer
    wait.until(
        EC.url_contains("/admin/pages/60/")
    )

    # Confirm the publish success message
    wait.until(
        EC.text_to_be_present_in_element(
            (By.TAG_NAME, "body"),
            "has been published."
        )
    )

    # Reopen the same page editor
    admin_driver.get(selected_page_url)

    # Verify the page remains published
    wait.until(
        EC.presence_of_element_located(
            (By.ID, "status-sidebar-live")
        )
    )

    # Verify the updated introduction was saved
    saved_introduction = wait.until(
        EC.visibility_of_element_located(
            (By.ID, "id_introduction")
        )
    )

    actual_text = saved_introduction.get_attribute("value") or ""

    assert actual_text == updated_text, (
        "TC08 FAILED: Updated introduction was not saved correctly."
    )

    print(
        "TC08 PASSED: Published Gallery page introduction "
        "updated and verified successfully."
    )
