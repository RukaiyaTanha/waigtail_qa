from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


BASE_URL = "http://127.0.0.1:8000"
PARENT_URL = f"{BASE_URL}/admin/pages/60/"
PAGE_ID = "114"


def test_tc23_cancel_page_deletion(admin_driver):

    driver = admin_driver
    wait = WebDriverWait(driver, 20)

    # Step 1: Open the parent page listing
    driver.get(PARENT_URL)

    # Step 2: Open the delete confirmation page
    driver.get(
        f"{BASE_URL}/admin/pages/{PAGE_ID}/delete/"
        f"?next=%2Fadmin%2Fpages%2F60%2F"
    )

    # Step 3: Verify delete confirmation page
    wait.until(
        EC.url_contains(f"/admin/pages/{PAGE_ID}/delete/")
    )

    cancel_button = wait.until(
        EC.element_to_be_clickable((
            By.XPATH,
            "//a[@href='/admin/pages/60/' "
            "and contains(text(), \"No, don't delete it\")]"
        ))
    )

    # Step 4: Cancel deletion
    cancel_button.click()

    # Step 5: Verify return to parent listing
    wait.until(
        EC.url_contains("/admin/pages/60/")
    )

    assert driver.current_url.rstrip("/") == PARENT_URL.rstrip("/"), (
        f"Unexpected URL after cancelling deletion: {driver.current_url}"
    )

    # Step 6: Verify the original page still exists
    driver.get(
        f"{BASE_URL}/admin/pages/{PAGE_ID}/edit/"
    )

    wait.until(
        EC.url_contains(f"/admin/pages/{PAGE_ID}/edit/")
    )

    assert f"/admin/pages/{PAGE_ID}/edit/" in driver.current_url, (
        "Original page was not accessible after cancelling deletion."
    )

    print("\nTC23 PASSED")
    print("Deletion was cancelled.")
    print("Original draft page remains accessible.")