
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.mark.ui
@pytest.mark.cms
@pytest.mark.regression
def test_tc07_publish_draft_page(admin_driver):

    wait = WebDriverWait(admin_driver, 10)

    # Step 1: Open parent page explorer
    admin_driver.get(
        "http://127.0.0.1:8000/admin/pages/60/"
    )

    # Step 2: Find an existing Gallery page dynamically
    draft_link = wait.until(
        EC.element_to_be_clickable((
            By.XPATH,
            "//a[contains(@href, '/admin/pages/') "
            "and contains(normalize-space(), 'QA Gallery')]"
        ))
    )

    draft_link.click()

    # Step 3: Verify Draft status
    wait.until(
        EC.presence_of_element_located((
            By.ID, "status-sidebar-draft"
        ))
    )

    assert "Draft" in admin_driver.page_source

    # Open the Save draft dropdown
    dropdown_button = wait.until(
        EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            "button.w-dropdown__toggle.button[data-w-dropdown-target='toggle']"
        ))
    )
    dropdown_button.click()

    # Click Publish
    publish_button = wait.until(
        EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            "button[name='action-publish'][value='action-publish']"
        ))
    )
    publish_button.click()

    # Step 6: Verify Live status
    wait.until(
        EC.presence_of_element_located((
            By.ID, "status-sidebar-live"
        ))
    )

    assert "Live" in admin_driver.page_source

    print("\nTC07 PASSED: Existing draft page published successfully.")
