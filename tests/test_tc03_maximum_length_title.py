import pytest
from pages.page_management_page import PageManagementPage
from datetime import datetime

@pytest.mark.ui
@pytest.mark.cms
@pytest.mark.regression
def test_tc03_create_gallery_with_maximum_length_title(admin_driver):

    page = PageManagementPage(admin_driver)

    # Generate a unique title with exactly 255 characters
    prefix = f"QA Gallery TC03 {datetime.now():%Y%m%d_%H%M%S} "
    page_title = prefix + ("A" * (255 - len(prefix)))

    introduction = "Testing maximum allowed page title length"

    page.navigate_to_parent_page()
    page.open_actions_menu()
    page.click_add_child_page()
    page.select_gallery_page()

    # Verify the title field's maximum length
    title_field = admin_driver.find_element(*page.PAGE_TITLE)
    max_length = title_field.get_attribute("maxlength")

    assert max_length == "255", (
        f"Expected title maxlength 255, but found {max_length}"
    )

    page.create_gallery_page(page_title, introduction)
    page.save_draft()

    assert page.verify_page_title(page_title), (
        "TC03 FAILED: Maximum-length page title was not saved correctly."
    )

    print("\nTC03 PASSED: Gallery page created with a 255-character title.")
    print(f"Title length: {len(page_title)}")