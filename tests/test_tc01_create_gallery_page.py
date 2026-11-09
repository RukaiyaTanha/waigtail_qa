
import pytest
from datetime import datetime

from pages.page_management_page import PageManagementPage


@pytest.mark.ui
@pytest.mark.smoke
@pytest.mark.cms

def test_tc01_create_gallery_page(admin_driver):

    page = PageManagementPage(admin_driver)

    # Generate a unique title for each execution
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    page_title = f"QA Gallery TC01 {timestamp}"

    introduction = "Gallery created for SQA testing"

    # Step 1: Open parent page
    page.navigate_to_parent_page()

    # Step 2: Open Actions menu
    page.open_actions_menu()

    # Step 3: Add child page
    page.click_add_child_page()

    # Step 4: Select Gallery page
    page.select_gallery_page()

    # Step 5: Enter valid information
    page.create_gallery_page(
        page_title,
        introduction
    )

    # Step 6: Save as draft
    page.save_draft()

    # Step 7: Verify saved page title
    assert page.verify_page_title(page_title), (
        "TC01 FAILED: Gallery page title was not saved correctly."
    )

    print("\nTC01 PASSED: Gallery page created successfully.")
    print(f"Created page: {page_title}")
