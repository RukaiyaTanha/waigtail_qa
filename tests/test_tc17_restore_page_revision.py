
import time
import re

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


BASE_URL = "http://127.0.0.1:8000"
PARENT_URL = f"{BASE_URL}/admin/pages/60/"


def open_page_history(driver, wait, page_title):

    driver.get(PARENT_URL)

    def find_page_menu(d):
        buttons = d.find_elements(
            By.CSS_SELECTOR,
            "button[aria-label^='More options for']"
        )

        for button in buttons:
            if button.get_attribute("aria-label") == (
                f"More options for '{page_title}'"
            ):
                return button

        return False

    wait.until(find_page_menu).click()

    def find_visible_edit_link(d):
        links = d.find_elements(
            By.CSS_SELECTOR,
            "a[href*='/admin/pages/'][href$='/edit/']"
        )

        for link in links:
            if link.is_displayed():
                return link

        return False

    edit_url = wait.until(find_visible_edit_link).get_attribute("href")

    match = re.search(r"/admin/pages/(\d+)/edit/", edit_url)
    assert match, f"Could not extract page ID from: {edit_url}"

    page_id = match.group(1)

    assert page_id != "60", "Incorrectly selected Home page."

    history_link = wait.until(
        EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            f"a[href='/admin/pages/{page_id}/history/']"
        ))
    )

    history_link.click()

    wait.until(
        EC.url_contains(f"/admin/pages/{page_id}/history/")
    )

    return page_id


def test_tc17_restore_page_revision(admin_driver):

    driver = admin_driver
    wait = WebDriverWait(driver, 20)

    timestamp = time.strftime("%Y%m%d_%H%M%S")
    unique_id = str(time.time_ns())[-6:]

    original_title = f"QA TC17 Original {timestamp}_{unique_id}"
    updated_title = f"QA TC17 Updated {timestamp}_{unique_id}"

    original_intro = "Original introduction for TC17 revision testing."
    updated_intro = "Updated introduction for TC17 revision testing."

    # --------------------------------------------------
    # Step 1: Create a new Gallery draft
    # --------------------------------------------------

    driver.get(
        f"{BASE_URL}/admin/pages/add/base/gallerypage/60/"
    )

    wait.until(
        EC.visibility_of_element_located((By.ID, "id_title"))
    ).send_keys(original_title)

    driver.find_element(
        By.ID, "id_introduction"
    ).send_keys(original_intro)

    Select(
        driver.find_element(By.ID, "id_collection")
    ).select_by_value("2")

    wait.until(
        EC.element_to_be_clickable((
            By.CSS_SELECTOR, "button.action-save"
        ))
    ).click()

    time.sleep(3)

    print("\nTC17: Gallery draft created:", original_title)

    # --------------------------------------------------
    # Step 2: Open its History
    # --------------------------------------------------

    page_id = open_page_history(
        driver, wait, original_title
    )

    print("TC17: Page ID:", page_id)

    # --------------------------------------------------
    # Step 3: Edit the page to create a second revision
    # --------------------------------------------------

    driver.get(
        f"{BASE_URL}/admin/pages/{page_id}/edit/"
    )

    title_field = wait.until(
        EC.visibility_of_element_located((By.ID, "id_title"))
    )

    title_field.clear()
    title_field.send_keys(updated_title)

    intro_field = wait.until(
        EC.visibility_of_element_located((By.ID, "id_introduction"))
    )

    intro_field.clear()
    intro_field.send_keys(updated_intro)

    wait.until(
        EC.element_to_be_clickable((
            By.CSS_SELECTOR, "button.action-save"
        ))
    ).click()

    time.sleep(3)

    print("TC17: Updated revision saved:", updated_title)

    # --------------------------------------------------
    # Step 4: Open History again
    # --------------------------------------------------

    second_page_id = open_page_history(
        driver, wait, updated_title
    )

    assert second_page_id == page_id

    # --------------------------------------------------
    # Step 5: Click the SECOND revision row's dropdown
    # --------------------------------------------------

    def get_revision_rows(d):

        rows = d.find_elements(
            By.CSS_SELECTOR,
            "tr"
        )

        matching_rows = []

        for row in rows:
            if row.is_displayed() and row.find_elements(
                By.CSS_SELECTOR,
                "button.w-dropdown__toggle"
            ):
                matching_rows.append(row)

        return matching_rows if len(matching_rows) >= 2 else False

    revision_rows = wait.until(get_revision_rows)

    print(
        "TC17: Revision rows found:",
        len(revision_rows)
    )

    # The second row contains the previous revision
    second_revision_row = revision_rows[1]

    second_revision_menu = second_revision_row.find_element(
        By.CSS_SELECTOR,
        "button.w-dropdown__toggle"
    )

    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center'});",
        second_revision_menu
    )

    second_revision_menu.click()

    # --------------------------------------------------
    # Step 6: Find Review this version in the opened menu
    # --------------------------------------------------

    review_link = wait.until(
        EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            f"a[href^='/admin/pages/{page_id}/revisions/'][href$='/revert/']"
        ))
    )

    review_url = review_link.get_attribute("href")

    print("TC17: Review this version found:", review_url)

    review_link.click()

    # --------------------------------------------------
    # Step 7: Replace current draft
    # --------------------------------------------------

    replace_button = wait.until(
        EC.element_to_be_clickable((
            By.XPATH,
            "//button[contains(@class, 'action-save') "
            "and .//em[normalize-space()='Replace current draft']]"
        ))
    )

    print("TC17: Clicking Replace current draft.")

    replace_button.click()

    time.sleep(3)

    # --------------------------------------------------
    # Step 8: Verify original revision was restored
    # --------------------------------------------------

    driver.get(
        f"{BASE_URL}/admin/pages/{page_id}/edit/"
    )

    restored_title = wait.until(
        EC.visibility_of_element_located((By.ID, "id_title"))
    ).get_attribute("value")

    restored_intro = wait.until(
        EC.visibility_of_element_located((By.ID, "id_introduction"))
    ).get_attribute("value")

    assert restored_title == original_title, (
        f"Title was not restored.\n"
        f"Expected: {original_title}\n"
        f"Actual: {restored_title}"
    )

    assert restored_intro == original_intro, (
        f"Introduction was not restored.\n"
        f"Expected: {original_intro}\n"
        f"Actual: {restored_intro}"
    )

    print("\nTC17 PASSED")
    print("Restored title:", restored_title)
    print("Restored introduction:", restored_intro)
