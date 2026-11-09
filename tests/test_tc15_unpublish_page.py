import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

def test_tc15_unpublish_page(admin_driver):

    wait = WebDriverWait(admin_driver, 15)

    timestamp = time.strftime("%Y%m%d_%H%M%S")
    page_title = f"QA TC15 Unpublish {timestamp}"

    # Step 1: Open the Gallery page creation form
    admin_driver.get(
        "http://127.0.0.1:8000/admin/pages/add/base/gallerypage/60/"
    )

    wait.until(
        EC.visibility_of_element_located((By.ID, "id_title"))
    ).send_keys(page_title)

    admin_driver.find_element(
        By.ID, "id_introduction"
    ).send_keys(
        "Gallery page created automatically for TC15 unpublish testing."
    )

    Select(
        admin_driver.find_element(By.ID, "id_collection")
    ).select_by_value("2")

    # Save the page
    save_button = wait.until(
        EC.element_to_be_clickable((
            By.CSS_SELECTOR, "button.action-save"
        ))
    )

    save_button.click()

# Wait for successful redirect to the page editor
    try:
        WebDriverWait(admin_driver, 15).until(
            lambda d: "/edit/" in d.current_url
        )

    except Exception:
        print("\nPAGE SAVE FAILED")
        print("Current URL:", admin_driver.current_url)

        print("\nPage content:")
        print(admin_driver.find_element(By.TAG_NAME, "body").text)

        raise AssertionError(
            "Page was not saved. Check the validation messages above."
        )

    page_url = admin_driver.current_url

    print("\nPage saved successfully.")
    print("Editor URL:", page_url)
    

    # Step 4: Open the page editor
    admin_driver.get(page_url)

    wait.until(
        EC.presence_of_element_located((By.ID, "id_title"))
    )

    # Step 5: Publish the page using the dropdown beside Save draft
    dropdown = wait.until(
        EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            "button.w-dropdown__toggle.button"
        ))
    )
    dropdown.click()

    publish_button = wait.until(
        EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            ".w-dropdown__content button[name='action-publish']"
        ))
    )
    publish_button.click()

    # Step 6: Wait for Wagtail to return to the parent page listing
    wait.until(
        EC.url_contains("/admin/pages/60/")
    )

    # Step 7: Reopen the newly published page
    admin_driver.get(page_url)

    wait.until(
        EC.presence_of_element_located(
            (By.ID, "status-sidebar-live")
        )
    )

    print("Page published successfully.")

    # Step 8: Open the dropdown and locate Unpublish
    dropdown = wait.until(
        EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            "button.w-dropdown__toggle.button"
        ))
    )
    dropdown.click()

    unpublish_link = wait.until(
        EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            "a.button[href*='/unpublish/']"
        ))
    )

    print("Unpublish action found:", unpublish_link.get_attribute("href"))

    # Step 9: Click Unpublish
    unpublish_link.click()

    # Step 10: Inspect the confirmation page before confirming
    wait.until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

    print("\nUnpublish confirmation URL:", admin_driver.current_url)
    print("Confirmation page text:")
    print(admin_driver.find_element(By.TAG_NAME, "body").text)

    # Stop here until the actual confirmation control is verified.
    assert "/unpublish/" in admin_driver.current_url
