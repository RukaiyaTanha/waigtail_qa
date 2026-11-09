
import re

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def test_tc11_approve_moderated_page(admin_driver):

    wait = WebDriverWait(admin_driver, 15)

    # Open the parent page
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

    # Find a Gallery page currently in moderation
    for page_url in page_urls:

        admin_driver.get(page_url)

        wait.until(
            EC.presence_of_element_located((By.ID, "id_title"))
        )

        if admin_driver.find_elements(
            By.ID, "status-sidebar-in-moderation"
        ):
            selected_page_url = page_url
            break

    assert selected_page_url, (
        "TC11 failed: No Gallery page in moderation was found."
    )

    print("\nSelected page:", selected_page_url)

    # Open the workflow dropdown
    dropdown = wait.until(
        EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            "button.w-dropdown__toggle.button"
        ))
    )
    dropdown.click()

    # Click Approve and Publish
    approve_button = wait.until(
        EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            "button[data-workflow-action-name='approve']"
            ":not([data-workflow-action-modal-url])"
        ))
    )

    print("Button:", approve_button.text)

    approve_button.click()
    
    # Wait for Wagtail to process approval
    wait.until(EC.staleness_of(approve_button))

    print("\n========== AFTER APPROVAL ==========")
    print("Current URL:", admin_driver.current_url)

    body_text = admin_driver.find_element(
        By.TAG_NAME, "body"
    ).text

    print("\nPage content:")
    print(body_text)

    print("\n========== STATUS ELEMENTS ==========")

    status_elements = admin_driver.find_elements(
        By.CSS_SELECTOR,
        "[id*='status-sidebar'], .w-status"
    )

    for element in status_elements:
        if element.is_displayed():
            print(
                "ID:", element.get_attribute("id"),
                "| TEXT:", element.text,
                "| HTML:", element.get_attribute("outerHTML")
            )

    print("\n========== END DIAGNOSTIC ==========")
