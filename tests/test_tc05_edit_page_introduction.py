
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.mark.ui
@pytest.mark.cms
@pytest.mark.regression
def test_tc05_edit_page_introduction(admin_driver):

    wait = WebDriverWait(admin_driver, 15)

    # Open parent page explorer
    admin_driver.get(
        "http://127.0.0.1:8000/admin/pages/60/"
    )

    # Find the Gallery page updated in TC04
    gallery_link = wait.until(
        EC.presence_of_element_located((
            By.XPATH,
            "//a[contains(normalize-space(), 'QA Gallery TC04 Updated Title')]"
        ))
    )

    # Save the editor URL for later verification
    editor_url = gallery_link.get_attribute("href")

    assert editor_url, "TC05 FAILED: Gallery page editor URL not found."

    # Open the Gallery page editor directly
    admin_driver.get(editor_url)

    # Wait for the introduction field
    introduction_field = wait.until(
        EC.visibility_of_element_located(
            (By.ID, "id_introduction")
        )
    )

    # Update the introduction
    new_introduction = (
        "Introduction updated successfully through "
        "Selenium automation for TC05."
    )

    introduction_field.clear()
    introduction_field.send_keys(new_introduction)

    # Save changes
    save_button = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "button.action-save")
        )
    )

    save_button.click()

    # Wait for Wagtail to finish saving and refresh the editor
    wait.until(
        EC.staleness_of(save_button)
    )

    wait.until(
        EC.visibility_of_element_located(
            (By.ID, "id_title")
        )
    )

    # Reopen the same editor URL
    admin_driver.get(editor_url)

    # Verify the saved introduction
    saved_introduction = wait.until(
        EC.visibility_of_element_located(
            (By.ID, "id_introduction")
        )
    )

    actual_introduction = (
        saved_introduction.get_attribute("value") or ""
    )

    assert actual_introduction == new_introduction, (
        "TC05 FAILED: Introduction was not updated correctly. "
        f"Expected: {new_introduction}, "
        f"Actual: {actual_introduction}"
    )

    print("\nTC05 PASSED: Gallery page introduction updated successfully.")
    print(f"Updated introduction: {actual_introduction}")
