import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


BASE_URL = "http://127.0.0.1:8000"
PARENT_URL = f"{BASE_URL}/admin/pages/60/"


def test_tc20_search_existing_page(admin_driver):

    driver = admin_driver
    wait = WebDriverWait(driver, 20)

    # Step 1: Open parent page listing
    driver.get(PARENT_URL)

    # Step 2: Locate search field
    search_field = wait.until(
        EC.visibility_of_element_located((By.ID, "id_q"))
    )

    # Step 3: Enter an existing page title
    search_title = "QA TC19 Slug Verification"

    search_field.clear()
    search_field.send_keys(search_title)

    # Step 4: Submit search
    search_field.submit()

    # Step 5: Wait for search results
    wait.until(
        lambda d: search_title.lower() in d.page_source.lower()
    )

    # Step 6: Verify the matching page appears
    matching_pages = driver.find_elements(
        By.XPATH,
        "//a[contains(@href, '/admin/pages/') and contains(@href, '/edit/')]"
    )

    matching_titles = [
        element.text.strip()
        for element in matching_pages
        if search_title.lower() in element.text.lower()
    ]

    print("\nSearch keyword:", search_title)
    print("Matching pages:", matching_titles)

    assert matching_titles, (
        f"No page found for search keyword: {search_title}"
    )

    print("\nTC20 PASSED")
    print("Existing page search verified.")