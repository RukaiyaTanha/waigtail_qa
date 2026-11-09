
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait


def test_tc16_delete_draft_page(admin_driver):

    wait = WebDriverWait(admin_driver, 20)

    timestamp = f"{time.strftime('%Y%m%d_%H%M%S')}_{int(time.time() * 1000)}"
    page_title = f"QA TC16 Delete Draft {timestamp}"

    # Step 1: Open Gallery page creation form
    admin_driver.get(
        "http://127.0.0.1:8000/admin/pages/add/base/gallerypage/60/"
    )

    wait.until(
        EC.visibility_of_element_located((By.ID, "id_title"))
    ).send_keys(page_title)

    admin_driver.find_element(
        By.ID, "id_introduction"
    ).send_keys(
        "Draft page created for TC16 deletion testing."
    )

    Select(
        admin_driver.find_element(By.ID, "id_collection")
    ).select_by_value("2")

    # Step 2: Save the new draft
    save_button = wait.until(
        EC.element_to_be_clickable((
            By.CSS_SELECTOR, "button.action-save"
        ))
    )

    save_button.click()

    print("\nDraft saved:", page_title)

    # Step 3: Open the parent listing directly
    time.sleep(2)

    print("URL after saving:", admin_driver.current_url)
    print("Page title after saving:", admin_driver.title)

    admin_driver.get(
        "http://127.0.0.1:8000/admin/pages/60/"
    )

    wait.until(
        EC.presence_of_element_located((
            By.CSS_SELECTOR,
            "button[aria-label^='More options for']"
        ))
    )

    print("Parent listing opened:", admin_driver.current_url)

    # Step 4: Find the exact page-specific Actions button
    def find_created_page_actions(driver):

        buttons = driver.find_elements(
            By.CSS_SELECTOR,
            "button[aria-label^='More options for']"
        )

        expected_label = f"More options for '{page_title}'"

        for button in buttons:
            if (
                button.get_attribute("aria-label") == expected_label
                and button.is_displayed()
            ):
                return button

        return False

    options_button = wait.until(find_created_page_actions)

    print("Found newly created page in parent listing.")

    # Step 5: Open that page's three-dot menu
    options_button.click()

    # Step 6: Click its Delete option
    delete_link = wait.until(
        EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            "a[href*='/delete/?next=']"
        ))
    )

    delete_url = delete_link.get_attribute("href")

    print("Delete URL:", delete_url)

    delete_link.click()

    # Step 7: Confirm deletion
    confirm_button = wait.until(
        EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            "input[type='submit'][value='Yes, delete it']"
        ))
    )

    confirm_button.click()

    # Step 8: Return to the parent listing
    wait.until(
        EC.url_contains("/admin/pages/60/")
    )

    admin_driver.get(
        "http://127.0.0.1:8000/admin/pages/60/"
    )

    # Step 9: Verify that this exact page no longer exists
    remaining_page = admin_driver.find_elements(
        By.XPATH,
        f"//*[normalize-space()='{page_title}']"
    )

    print("\n========== TC16 VERIFICATION ==========")
    print("Created page:", page_title)
    print("Deleted successfully:", not bool(remaining_page))

    assert not remaining_page, (
        f"TC16 failed: {page_title} still exists in the parent listing."
    )

    print("TC16 verification passed.")
    print("=======================================")
