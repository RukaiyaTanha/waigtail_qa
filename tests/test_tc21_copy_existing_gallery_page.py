import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


BASE_URL = "http://127.0.0.1:8000"
PARENT_URL = f"{BASE_URL}/admin/pages/60/"


def test_tc21_copy_existing_gallery_page(admin_driver):

    driver = admin_driver
    wait = WebDriverWait(driver, 20)

    timestamp = time.strftime("%Y%m%d_%H%M%S")

    original_title = "QA TC19 Slug Verification"
    copied_title = f"QA TC21 Copied Gallery {timestamp}"
    copied_slug = f"qa-tc21-copied-gallery-{timestamp}"

    # Step 1: Open the parent page listing
    driver.get(PARENT_URL)

    # Step 2: Find the original Gallery page
    original_page = wait.until(
        EC.presence_of_element_located((
            By.XPATH,
            "//a[contains(@href, '/admin/pages/118/edit/') "
            "and contains(., 'QA TC19 Slug Verification')]"
        ))
    )

    assert original_page.is_displayed(), (
        "Original Gallery page was not found."
    )

    # Step 3: Open the Copy form
    driver.get(f"{BASE_URL}/admin/pages/118/copy/")

    # Step 4: Enter a new page title
    title_field = wait.until(
        EC.visibility_of_element_located((By.ID, "id_new_title"))
    )
    title_field.clear()
    title_field.send_keys(copied_title)

    # Step 5: Enter a unique slug
    slug_field = driver.find_element(By.ID, "id_new_slug")
    slug_field.clear()
    slug_field.send_keys(copied_slug)

    # Step 6: Submit the copy form
    copy_button = wait.until(
        EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            "input[type='submit'][value='Copy this page']"
        ))
    )
    copy_button.click()

    # Step 7: Wait for the copied page to appear in the listing
    wait.until(
        lambda d: copied_title.lower() in d.page_source.lower()
    )

    # Step 8: Verify the copied page exists
    copied_page = wait.until(
        EC.presence_of_element_located((
            By.XPATH,
            f"//a[contains(@href, '/admin/pages/') "
            f"and contains(@href, '/edit/') "
            f"and contains(., '{copied_title}')]"
        ))
    )

    assert copied_page.is_displayed(), (
        "Copied Gallery page was not found."
    )

    # Step 9: Verify the original page still exists
    driver.get(PARENT_URL)

    original_page_after_copy = wait.until(
        EC.presence_of_element_located((
            By.XPATH,
            "//a[contains(@href, '/admin/pages/118/edit/') "
            "and contains(., 'QA TC19 Slug Verification')]"
        ))
    )

    assert original_page_after_copy.is_displayed(), (
        "Original Gallery page was changed or removed."
    )

    print("\nTC21 PASSED")
    print("Original page:", original_title)
    print("Copied page:", copied_title)
    print("Copied slug:", copied_slug)