"""
General UI tests - logout and bilingual behaviour.

This file intentionally separates two bilingual checks:
- TC-12 verifies that the main UI chrome switches to English.
- TC-16 verifies full category localization and is marked xfail because
  Manual TC-33 / BUG-08 proves the current system still shows Vietnamese
  category names after switching to English.
"""
import os

import pytest
from playwright.sync_api import Error as PlaywrightError

from conftest import enable_flutter_semantics, login, wait_for_flutter, SCREENSHOT_DIR


def _safe_screenshot(page, filename):
    """Capture evidence without letting a transient CanvasKit screenshot timeout fail the oracle."""
    try:
        page.screenshot(path=os.path.join(SCREENSHOT_DIR, filename), timeout=10000)
    except PlaywrightError:
        pass


def _switch_to_english(page, test_config):
    """Log in, switch the application language to English, and return semantics text."""
    login(page, test_config)

    en_btn = page.locator('flt-semantics[role="button"]:has-text("EN")').first
    en_btn.wait_for(state="attached", timeout=10000)
    en_btn.click()

    english_terms = ("Logout", "Borrow", "Return", "Library", "Search", "Books")
    sem_text = ""
    for _ in range(20):
        page.wait_for_timeout(300)
        enable_flutter_semantics(page)
        sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
        if any(term in sem_text for term in english_terms):
            return sem_text

    return sem_text


def test_logout(page, test_config):
    """TC-11: Logout success.

    Log in, click Logout, and verify the login form is visible again.
    """
    # Arrange
    login(page, test_config)

    # Act
    logout_btn = page.locator('flt-semantics[role="button"]:has-text("Đăng xuất")').first
    logout_btn.wait_for(state="attached", timeout=10000)
    logout_btn.click()

    # Assert
    wait_for_flutter(page, text="Đăng nhập")
    enable_flutter_semantics(page)
    _safe_screenshot(page, "logout.png")

    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    has_login_button = "Đăng nhập" in sem_text or "Login" in sem_text
    has_email_input = page.locator('input[aria-label="Email"]').count() > 0
    assert has_login_button and has_email_input, (
        "Did not return to the login page after logout. "
        f"Sem text: {sem_text[:300]}"
    )


def test_switch_language_to_english(page, test_config):
    """TC-12: Switch language to English.

    This required A2 test checks that the main navigation/UI chrome changes to
    English. Manual TC-33 separately checks full category localization.
    """
    sem_text = _switch_to_english(page, test_config)
    _safe_screenshot(page, "switch_language_en.png")

    english_terms = ("Logout", "Borrow", "Return", "Library", "Search")
    assert any(term in sem_text for term in english_terms), (
        "The main UI did not switch to English after clicking EN. "
        f"Sem text: {sem_text[:300]}"
    )


@pytest.mark.xfail(
    reason="Known defect BUG-08 from Manual TC-33: category names remain Vietnamese after switching to English.",
    strict=True,
)
def test_english_category_localization_bug08(page, test_config):
    """TC-16 (Manual TC-33 alignment): category names should also localize.

    Expected behaviour from SRS section 5: after switching to English, visible
    book category names in Search/Filter should not remain Vietnamese.
    Current behaviour: categories such as "Công nghệ", "Quản trị", and
    "Kinh tế" remain visible, so this test is an expected failure until BUG-08
    is fixed.
    """
    sem_text = _switch_to_english(page, test_config)
    _safe_screenshot(page, "switch_language_category_bug08.png")

    vietnamese_categories = (
        "Công nghệ",
        "Quản trị",
        "Kinh tế",
        "Kỹ năng mềm",
        "Giáo dục",
        "Văn học",
    )
    leaked_categories = [category for category in vietnamese_categories if category in sem_text]

    assert not leaked_categories, (
        "Vietnamese category names are still visible after switching to English: "
        f"{', '.join(leaked_categories)}"
    )
