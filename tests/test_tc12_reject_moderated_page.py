import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait


def scroll_and_click(driver, wait, locator):
    """Scroll the element into view, then click it."""
    element = wait.until(EC.presence_of_element_located(locator))
    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center'});", element
    )
    element = wait.until(EC.element_to_be_clickable(locator))
    element.click()
    return element


def test_tc12_reject_moderated_page(admin_driver):

    wait = WebDriverWait(admin_driver, 15)

    timestamp = time.strftime("%Y%m%d_%H%M%S")
    page_title = f"QA TC12 Request Changes {timestamp}"

    # Step 1: Open the Gallery page creation form
    admin_driver.get(
        "http://127.0.0.1:8000/admin/pages/add/base/gallerypage/60/"
    )

    title_field = wait.until(
        EC.visibility_of_element_located((By.ID, "id_title"))
    )

    # Step 2: Fill the required Gallery page fields
    title_field.send_keys(page_title)

    introduction_field = admin_driver.find_element(
        By.ID, "id_introduction"
    )
    introduction_field.send_keys(
        "Gallery page created automatically for TC12 moderation testing."
    )

    collection_field = Select(
        admin_driver.find_element(By.ID, "id_collection")
    )
    collection_field.select_by_value("2")

    # Step 3: Save the page as a draft
    scroll_and_click(
        admin_driver,
        wait,
        (By.CSS_SELECTOR, "button.action-save")
    )

    # Step 4: Wait for Wagtail to redirect to the new page's editor
    wait.until(
        EC.url_matches(r"/admin/pages/\d+/edit/")
    )

    selected_page_url = admin_driver.current_url

    print("\nCreated page:", page_title)
    print("Editor URL:", selected_page_url)

    # Step 5: Make sure the editor has loaded
    wait.until(
        EC.presence_of_element_located((By.ID, "id_title"))
    )

    # Step 6: Open the dropdown beside Save draft
    scroll_and_click(
        admin_driver,
        wait,
        (By.CSS_SELECTOR, "button.w-dropdown__toggle.button")
    )

    # Step 7: Submit the draft for moderation
    submit_button = wait.until(
        EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            ".w-dropdown__content button[name='action-submit']"
            "[value='Submit to Moderators approval']"
        ))
    )

    submit_button.click()

    # Wagtail redirects to the parent page after submission
    wait.until(
        EC.url_contains("/admin/pages/60/")
    )

    print("Page submitted for moderation.")

    # Step 8: Reopen the same page
    admin_driver.get(selected_page_url)

    wait.until(
        EC.presence_of_element_located(
            (By.ID, "status-sidebar-in-moderation")
        )
    )

    # Step 9: Open the workflow actions dropdown
    scroll_and_click(
        admin_driver,
        wait,
        (By.CSS_SELECTOR, "button.w-dropdown__toggle.button")
    )

    # Step 10: Select Request changes
    request_changes_button = wait.until(
        EC.element_to_be_clickable((
            By.XPATH,
            "//div[contains(@class, 'w-dropdown__content')]"
            "//button[normalize-space()='Request changes']"
        ))
    )

    request_changes_button.click()

    # Step 11: Enter the workflow comment
    comment_field = wait.until(
        EC.visibility_of_element_located((By.ID, "id_comment"))
    )

    comment_field.send_keys(
        "QA TC12: Requesting changes for moderation testing."
    )

    # Step 12: Submit Request changes in the modal
    confirm_button = wait.until(
        EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            "div.modal.fade.in button[type='submit'].button-longrunning"
        ))
    )

    assert "Request changes" in confirm_button.text

    confirm_button.click()

    wait.until(
        EC.staleness_of(confirm_button)
    )

    # Step 13: Reopen the same page and verify the workflow action
    admin_driver.get(selected_page_url)

    wait.until(
        EC.presence_of_element_located((By.ID, "id_title"))
    )

    scroll_and_click(
        admin_driver,
        wait,
        (By.CSS_SELECTOR, "button.w-dropdown__toggle.button")
    )

    resubmit_button = wait.until(
        EC.visibility_of_element_located((
            By.CSS_SELECTOR,
            ".w-dropdown__content button[name='action-submit']"
            "[value='Resubmit to Moderators approval']"
        ))
    )

    print("\n========== TC12 VERIFICATION ==========")
    print("Created page:", page_title)
    print("Submitted for moderation: Yes")
    print("Request changes submitted: Yes")
    print(
        "Available next action:",
        resubmit_button.text.strip()
    )
    print("TC12 verification passed.")
    print("=======================================")

    assert resubmit_button.is_displayed()