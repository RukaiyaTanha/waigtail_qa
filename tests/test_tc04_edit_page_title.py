
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.mark.ui
@pytest.mark.cms
@pytest.mark.regression
def test_tc04_edit_existing_page_title(admin_driver):

    wait = WebDriverWait(admin_driver, 10)

    # Open parent page explorer
    admin_driver.get(
        "http://127.0.0.1:8000/admin/pages/60/"
    )

    # Find the Gallery page created in TC01
    gallery_link = wait.until(
        EC.element_to_be_clickable((
            By.XPATH,
            "//a[contains(normalize-space(), 'QA Gallery TC01')]"
        ))
    )

    gallery_link.click()

    # Wait for the Gallery page editor to open
    title_field = wait.until(
        EC.visibility_of_element_located(
            (By.ID, "id_title")
        )
    )

    # Change the existing title
    new_title = "QA Gallery TC04 Updated Title"

    title_field.clear()
    title_field.send_keys(new_title)

    # Save the updated page
    save_button = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "button.action-save")
        )
    )

    save_button.click()

    # Verify updated title after saving
    wait.until(
        EC.url_contains("/admin/pages/")
    )

    admin_driver.get(
        "http://127.0.0.1:8000/admin/pages/60/"
    )

    updated_title = wait.until(
        EC.visibility_of_element_located((
            By.XPATH,
            f"//a[contains(normalize-space(), '{new_title}')]"
        ))
    )

    assert updated_title.is_displayed(), (
        "TC04 FAILED: Updated Gallery page title was not found."
    )

    print("\nTC04 PASSED: Existing Gallery page title updated successfully.")
    print(f"Updated title: {new_title}")
