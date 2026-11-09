import time
import re

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


BASE_URL = "http://127.0.0.1:8000"
PARENT_URL = f"{BASE_URL}/admin/pages/60/"


def test_tc19_auto_generate_page_slug(admin_driver):

    driver = admin_driver
    wait = WebDriverWait(driver, 20)

    timestamp = time.strftime("%Y%m%d_%H%M%S")
    page_title = f"QA TC19 Slug Verification {timestamp}"

    expected_slug = page_title.lower().replace(" ", "-")

    # Step 1: Open Gallery page creation form
    driver.get(
        f"{BASE_URL}/admin/pages/add/base/gallerypage/60/"
    )

    # Step 2: Enter page title
    title_field = wait.until(
        EC.visibility_of_element_located((By.ID, "id_title"))
    )

    title_field.clear()
    title_field.send_keys(page_title)

# Step 3: Select Collection
    Select(
        driver.find_element(By.ID, "id_collection")
    ).select_by_value("2")

# Step 4: Open Promote tab
    promote_tab = wait.until(
        EC.element_to_be_clickable((By.ID, "tab-label-promote"))
    )
    promote_tab.click()

# Step 5: Verify automatically generated slug
    slug_field = wait.until(
        EC.visibility_of_element_located((By.ID, "id_slug"))
    )

    wait.until(
        lambda d: d.find_element(
            By.ID, "id_slug"
        ).get_attribute("value").strip() != ""
    )

    actual_slug = slug_field.get_attribute("value")

    print("\nExpected slug:", expected_slug)
    print("Actual slug:", actual_slug)

    assert actual_slug == expected_slug, (
        f"Slug mismatch. Expected: {expected_slug}, "
        f"Actual: {actual_slug}"
    )

    # Save the page
    save_button = wait.until(
        EC.element_to_be_clickable((
            By.CSS_SELECTOR, "button.action-save"
        ))
    )

    save_button.click()

# Wait for successful redirect to the page editor
    try:
        WebDriverWait(driver, 15).until(
            lambda d: "/edit/" in d.current_url
        )

    except Exception:
        print("\nPAGE SAVE FAILED")
        print("Current URL:", driver.current_url)

        print("\nPage content:")
        print(driver.find_element(By.TAG_NAME, "body").text)

        raise AssertionError(
            "Page was not saved. Check the validation messages above."
        )

    page_url = driver.current_url

    print("\nPage saved successfully.")
    print("Editor URL:", page_url)
    
    # Step 8: Reopen Promote tab and verify saved slug
    driver.get(page_url)

    wait.until(
        EC.element_to_be_clickable((By.ID, "tab-label-promote"))
    ).click()

    saved_slug = wait.until(
        EC.visibility_of_element_located((By.ID, "id_slug"))
    ).get_attribute("value")

    assert saved_slug == expected_slug

    print("\nTC19 PASSED")
    print("Automatic slug generation verified.")
    print("Saved slug:", saved_slug)
    print("Page URL:", page_url)