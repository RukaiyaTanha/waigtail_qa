
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.mark.ui
@pytest.mark.cms
@pytest.mark.regression
def test_tc06_verify_draft_status_and_preview(admin_driver):

    wait = WebDriverWait(admin_driver, 10)

    # Step 1: Open parent page explorer
    admin_driver.get(
        "http://127.0.0.1:8000/admin/pages/60/"
    )

    # Step 2: Open existing Gallery page
    gallery_link = wait.until(
        EC.element_to_be_clickable((
            By.XPATH,
            "//a[contains(normalize-space(), 'QA Gallery TC04 Updated Title')]"
        ))
    )
    gallery_link.click()

    # Step 3: Verify Draft status
    wait.until(
        EC.presence_of_element_located((
            By.ID, "status-sidebar-draft"
        ))
    )

    assert "Draft" in admin_driver.page_source

    # Step 4: Click View history
    history_link = wait.until(
        EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            "a[href*='/history/']"
        ))
    )
    history_link.click()

    # Step 5: Click Actions dots on the revision row
    revision_actions = wait.until(
        EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            "button.w-dropdown__toggle[aria-label='Actions']"
        ))
    )
    revision_actions.click()

    # Step 6: Click Preview
    preview_link = wait.until(
        EC.element_to_be_clickable((
            By.XPATH,
            "//a[contains(@href, '/revisions/') and "
            "contains(@href, '/view/') and "
            "normalize-space()='Preview']"
        ))
    )

    preview_url = preview_link.get_attribute("href")
    preview_link.click()

    # Step 7: Verify preview page opened
    wait.until(EC.url_to_be(preview_url))

    assert "/revisions/" in admin_driver.current_url
    assert "/view/" in admin_driver.current_url

    print("\nTC06 PASSED: Draft status verified.")
    print("Revision history opened successfully.")
    print("Preview page opened successfully.")
    print(f"Preview URL: {admin_driver.current_url}")
