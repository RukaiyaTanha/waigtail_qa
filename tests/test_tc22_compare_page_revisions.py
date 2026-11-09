from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


BASE_URL = "http://127.0.0.1:8000"
PAGE_ID = "106"


def test_tc22_compare_page_revisions(admin_driver):

    driver = admin_driver
    wait = WebDriverWait(driver, 20)

    # Step 1: Open page history
    driver.get(f"{BASE_URL}/admin/pages/{PAGE_ID}/history/")

    # Step 2: Locate the second revision row
    revision_rows = wait.until(
        EC.presence_of_all_elements_located((
            By.CSS_SELECTOR,
            "table tbody tr"
        ))
    )

    assert len(revision_rows) >= 2, (
        "History does not contain at least two revision rows."
    )

    second_row = revision_rows[1]

    # Step 3: Open the second row's Actions dropdown
    actions_button = second_row.find_element(
        By.CSS_SELECTOR,
        "button[aria-label='Actions']"
    )

    actions_button.click()

    # Step 4: Click Compare with current version
    compare_link = wait.until(
        EC.element_to_be_clickable((
            By.XPATH,
            "//a[contains(@href, '/revisions/compare/') "
            "and contains(text(), 'Compare with current version')]"
        ))
    )

    compare_link.click()

    # Step 5: Verify comparison page URL
    wait.until(
        EC.url_contains("/revisions/compare/")
    )

    expected_url_part = (
        f"/admin/pages/{PAGE_ID}/revisions/compare/"
    )

    assert expected_url_part in driver.current_url, (
        f"Unexpected comparison URL: {driver.current_url}"
    )

    # Step 6: Verify comparison page loaded
    assert driver.find_element(By.TAG_NAME, "body").is_displayed()

    print("\nTC22 PASSED")
    print("Second revision row selected.")
    print("Comparison URL:", driver.current_url)