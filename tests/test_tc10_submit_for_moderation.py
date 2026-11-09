
import re

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def test_tc10_submit_page_for_moderation(admin_driver):

    wait = WebDriverWait(admin_driver, 15)

    # Open the parent page containing Gallery pages
    admin_driver.get("http://127.0.0.1:8000/admin/pages/60/")

    page_links = admin_driver.find_elements(
        By.CSS_SELECTOR,
        "a[href*='/admin/pages/'][href*='/edit/']"
    )

    page_urls = list(dict.fromkeys(
        link.get_attribute("href")
        for link in page_links
        if link.is_displayed()
        and re.search(
            r"/admin/pages/\d+/edit/",
            link.get_attribute("href") or ""
        )
    ))

    selected_page_url = None

    # Find a Gallery page that is still a draft
    for page_url in page_urls:

        admin_driver.get(page_url)

        wait.until(
            EC.presence_of_element_located((By.ID, "id_title"))
        )

        body_text = admin_driver.find_element(
            By.TAG_NAME, "body"
        ).text

        is_gallery = "Gallery page" in body_text
        is_draft = bool(
            admin_driver.find_elements(
                By.ID, "status-sidebar-draft"
            )
        )

        if is_gallery and is_draft:
            selected_page_url = page_url
            break

    assert selected_page_url, (
        "TC10 failed: No draft Gallery page was found."
    )

    print("\nSelected draft page:", selected_page_url)

    # Open the actions dropdown beside Save draft
    dropdown = wait.until(
        EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            "button.w-dropdown__toggle.button"
        ))
    )
    dropdown.click()

    # Click the actual moderation submission button
    submit_button = wait.until(
        EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            "button[name='action-submit']"
            "[value='Submit to Moderators approval']"
        ))
    )

    print("Button:", submit_button.text)

    submit_button.click()

    
    # Wait for the submission response
    wait.until(EC.staleness_of(submit_button))

    print("\n========== AFTER SUBMISSION ==========")
    print("Current URL:", admin_driver.current_url)

    print("\nPage content:")
    print(admin_driver.find_element(By.TAG_NAME, "body").text)

    print("\n========== STATUS ELEMENTS ==========")

    status_elements = admin_driver.find_elements(
        By.CSS_SELECTOR,
        "[id*='status-sidebar']"
    )

    for element in status_elements:
        print(
            "ID:", element.get_attribute("id"),
            "| TEXT:", element.text
        )

    print("\n========== VALIDATION ERRORS ==========")

    errors = admin_driver.find_elements(
        By.CSS_SELECTOR,
        ".error-message, .help-block, .w-field__errors, "
        "[aria-invalid='true']"
    )

    for error in errors:
        if error.is_displayed():
            print("ERROR:", error.text)

    print("\n========== END DIAGNOSTIC ==========")
    
