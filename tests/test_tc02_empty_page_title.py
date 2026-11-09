
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.page_management_page import PageManagementPage


@pytest.mark.ui
@pytest.mark.cms
@pytest.mark.regression
def test_tc02_create_gallery_with_empty_title(admin_driver):

    page = PageManagementPage(admin_driver)

    wait = WebDriverWait(admin_driver, 15)

    # Step 1: Open parent page
    page.navigate_to_parent_page()

    # Step 2: Open Actions menu
    page.open_actions_menu()

    # Step 3: Add child page
    page.click_add_child_page()

    # Step 4: Select Gallery page
    page.select_gallery_page()

    # Step 5: Leave title empty
    page.enter_text(
        page.INTRODUCTION,
        "Testing mandatory title validation"
    )

    page.select_by_visible_text(
        page.COLLECTION,
        "Bakeries"
    )

    # Step 6: Locate title field before saving
    title_field = wait.until(
        EC.visibility_of_element_located(page.PAGE_TITLE)
    )

    # Verify title is mandatory
    assert title_field.get_attribute("required") is not None, (
        "TC02 FAILED: Title field does not have the required attribute."
    )

    # Verify the empty title fails HTML validation
    is_valid = admin_driver.execute_script(
        "return arguments[0].checkValidity();",
        title_field
    )

    assert not is_valid, (
        "TC02 FAILED: Empty page title passed browser validation."
    )

    # Step 7: Click Save draft
    save_button = wait.until(
        EC.element_to_be_clickable(page.SAVE_DRAFT)
    )

    save_button.click()

    # Step 8: Verify the editor remains open because title is empty
    wait.until(
        EC.visibility_of_element_located(page.PAGE_TITLE)
    )

    assert "/admin/pages/add/base/gallerypage/" in admin_driver.current_url, (
        "TC02 FAILED: Wagtail unexpectedly left the creation form."
    )

    print(
        "\nTC02 PASSED: Wagtail prevents saving a Gallery page "
        "without a title."
    )
