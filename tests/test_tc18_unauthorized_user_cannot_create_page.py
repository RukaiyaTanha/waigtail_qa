
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


BASE_URL = "http://127.0.0.1:8000"
CREATE_PAGE_URL = (
    f"{BASE_URL}/admin/pages/add/base/gallerypage/60/"
)


def test_tc18_unauthorized_user_cannot_create_page(admin_driver):

    driver = admin_driver
    wait = WebDriverWait(driver, 20)

    # --------------------------------------------------
    # Step 1: Remove the authenticated admin session
    # --------------------------------------------------

    driver.delete_all_cookies()

    # --------------------------------------------------
    # Step 2: Attempt to access Gallery page creation
    # without logging in
    # --------------------------------------------------

    driver.get(CREATE_PAGE_URL)

    # --------------------------------------------------
    # Step 3: Verify Wagtail redirects to login
    # --------------------------------------------------

    wait.until(
        EC.url_contains("/admin/login/")
    )

    current_url = driver.current_url

    print("\nTC18: Attempted unauthorized page creation.")
    print("Redirected URL:", current_url)

    assert "/admin/login/" in current_url, (
        "Unauthorized user was not redirected to the login page."
    )

    # --------------------------------------------------
    # Step 4: Verify login form is displayed
    # --------------------------------------------------

    password_field = wait.until(
        EC.visibility_of_element_located((
            By.CSS_SELECTOR,
            "input[type='password']"
        ))
    )

    assert password_field.is_displayed(), (
        "Admin login form was not displayed."
    )

    print("TC18 PASSED")
    print("Unauthenticated user cannot access page creation.")
