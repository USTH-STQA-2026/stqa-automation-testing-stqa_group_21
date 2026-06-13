"""
Logout & Language Tests — Library Book Borrowing System

Students must complete ALL 2 test cases in this file.

Hints:
    - Use the login() helper to log in
    - Logout button: 'flt-semantics[role="button"]:has-text("Đăng xuất")'
    - Language switch EN button: 'flt-semantics[role="button"]:has-text("EN")'
    - After logout: the page returns to login (has a "Đăng nhập" button and an "Email" input)
    - After switching to EN: the text "Logout", "Borrow", "Search", "Library" may appear
"""
import os
from conftest import enable_flutter_semantics, login, SCREENSHOT_DIR


def test_logout(page, test_config):
    """TC-11: Logout success

    Description: Log in → click Logout → verify we return to the login page.
    """
    # Arrange: Log in
    login(page, test_config)

    # Act: Click the "Đăng xuất" button
    logout_btn = page.locator('flt-semantics[role="button"]:has-text("Đăng xuất")').first
    logout_btn.click()

    # Smart Wait: Wait to return to the login page
    page.wait_for_timeout(3000)
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "logout.png"))

    # Assert: Verify we returned to the login page (has a "Đăng nhập" button or an Email field)
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    has_login_page = "Đăng nhập" in sem_text or "Email" in sem_text or "Login" in sem_text
    has_email_input = page.locator('input[aria-label="Email"]').count() > 0
    assert has_login_page or has_email_input, \
        f"Did not return to the login page after logging out. Sem text: {sem_text[:300]}"


def test_switch_language_to_english(page, test_config):
    """TC-12: Switch language to English

    Description: Log in → click the "EN" button → verify the UI switches to English.
    """
    # Arrange: Log in
    login(page, test_config)

    # Act: Click the "EN" button to switch language
    en_btn = page.locator('flt-semantics[role="button"]:has-text("EN")').first
    en_btn.click()

    # Smart Wait: Wait for the UI to switch language
    page.wait_for_timeout(2000)
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "switch_language_en.png"))

    # Assert: Verify the UI is displayed in English
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    has_english = "Logout" in sem_text or "Borrow" in sem_text or "Library" in sem_text or "Search" in sem_text
    assert has_english, \
        f"The UI did not switch to English after clicking 'EN'. Sem text: {sem_text[:300]}"
