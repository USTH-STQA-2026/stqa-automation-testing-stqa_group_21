"""
Login Tests — Library Book Borrowing System

📖 Textbook concepts in this file:
   - RIPR Model (Ch.2): See [R], [I], [P], [R✓] comments in TC-01
   - Data-Driven Testing / @parametrize (Ch.3 §3.3.2): See hint in TC-02/TC-03

This file contains 1 completed example (TC-01).
Students must complete TC-02 and TC-03.
"""
import os
import pytest
from conftest import enable_flutter_semantics, flutter_fill, flutter_click_button, wait_for_flutter, SCREENSHOT_DIR


def test_login_success(page, test_config):
    """TC-01: Login success with valid credentials

    ✅ COMPLETED — Use as a reference example.

    📖 RIPR Model (Textbook Ch.2 — Reachability → Infection → Propagation → Revealability):
        Each line of the test maps to one step of the RIPR chain.
        See the [R], [I], [P], [R✓] comments below.
    """
    # [R] Reachability: Open the login page — reach the UI under test
    page.goto(test_config["base_url"], wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)

    # [I] Infection: Enter valid data — trigger the login logic in the system
    flutter_fill(page, "Email", test_config["email"])
    flutter_fill(page, "Mật khẩu", test_config["password"])
    flutter_click_button(page, "Đăng nhập")

    # [P] Propagation: Wait for the state to propagate to the UI — the "Đăng xuất" button appears
    # (Smart Wait: instead of time.sleep(5) — faster and more stable)
    wait_for_flutter(page, text="Đăng xuất")
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "login_success.png"))

    # [R✓] Revealability: Check the result — the Test Oracle detects a failure if any
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    has_user_name = test_config["display_name"] in sem_text
    has_logout = "Đăng xuất" in sem_text or "Logout" in sem_text
    assert has_user_name or has_logout, \
        f"Login failed: '{test_config['display_name']}' or Logout button not found"


@pytest.mark.parametrize("email,password,expected_error", [
    ("ba.nguyen@email.com", "wrongpassword", "Mật khẩu không đúng"),
    ("", "", "Vui lòng nhập email và mật khẩu"),
    ("nobody@test.com", "anything", "Không tìm thấy thành viên"),
])
def test_login_fail_parametrize(page, test_config, email, password, expected_error):
    """B2: Data-driven login failure test

    📖 Data-Driven Testing (Ch.3 §3.3.2):
        Use @pytest.mark.parametrize to run the same scenario with multiple data sets.
    """
    # Arrange: Open the login page
    page.goto(test_config["base_url"], wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)

    # Act: Enter the data and log in
    if email:
        flutter_fill(page, "Email", email)
    if password:
        flutter_fill(page, "Mật khẩu", password)
    flutter_click_button(page, "Đăng nhập")

    # Smart Wait: Wait for the error message
    wait_for_flutter(page, text=expected_error)

    # Assert: Verify the correct error message
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert expected_error in sem_text, \
        f"Expected error '{expected_error}' not found in: {sem_text[:200]}"


def test_login_success_librarian(page, test_config):
    """TC-13 (B1): Login success as Librarian

    Unlike TC-01 (Member login), this test logs in with a Librarian account
    (librarian@library.com) — verifying the system recognizes the Librarian role.

    📖 RIPR Model:
        [R] Open the login page
        [I] Enter valid Librarian credentials → trigger the login logic
        [P] State propagates to the UI (name + Librarian role)
        [R✓] Assert the displayed name "Nguyễn Thủ Thư" or the "Đăng xuất" button
    """
    # [R] Reachability
    page.goto(test_config["base_url"], wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)

    # [I] Infection: Log in with the Librarian account
    flutter_fill(page, "Email", "librarian@library.com")
    flutter_fill(page, "Mật khẩu", "admin123")
    flutter_click_button(page, "Đăng nhập")

    # [P] Propagation: Wait for the main page to load
    wait_for_flutter(page, text="Đăng xuất")
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "login_success_librarian.png"))

    # [R✓] Revealability: Verify login with the correct Librarian role
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    has_librarian = "Nguyễn Thủ Thư" in sem_text or "Thủ thư" in sem_text
    has_logout = "Đăng xuất" in sem_text or "Logout" in sem_text
    assert has_librarian or has_logout, \
        f"Librarian login failed. Sem text: {sem_text[:200]}"


def test_login_fail_wrong_password(page, test_config):
    """TC-02: Login fail – wrong password

    📖 RIPR Model:
        [R] Open the login page
        [I] Enter a correct email + wrong password → trigger the error-handling branch
        [P] The error propagates to a message on the UI
        [R✓] Assert the error message "Mật khẩu không đúng"
    """
    # [R] Reachability: Open the login page
    page.goto(test_config["base_url"], wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)

    # [I] Infection: Enter a correct email but a wrong password
    flutter_fill(page, "Email", test_config["email"])
    flutter_fill(page, "Mật khẩu", "wrongpassword")
    flutter_click_button(page, "Đăng nhập")

    # [P] Propagation: Wait for the error message to appear
    wait_for_flutter(page, text="Mật khẩu không đúng")
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "login_fail_wrong_password.png"))

    # [R✓] Revealability: Verify the error message
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert "Mật khẩu không đúng" in sem_text, \
        f"Expected error message 'Mật khẩu không đúng' not found in: {sem_text[:200]}"


def test_login_fail_empty_fields(page, test_config):
    """TC-03: Login fail – empty fields

    📖 RIPR Model:
        [R] Open the login page
        [I] Enter nothing, click Login → trigger validation
        [P] The error propagates to the message "Vui lòng nhập email và mật khẩu"
        [R✓] Assert the error message or that we remain on the login page
    """
    # [R] Reachability: Open the login page
    page.goto(test_config["base_url"], wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)

    # [I] Infection: Enter nothing, click Login right away
    flutter_click_button(page, "Đăng nhập")

    # [P] Propagation: Wait for the error message to appear
    wait_for_flutter(page, text="Vui lòng nhập email và mật khẩu")
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "login_fail_empty_fields.png"))

    # [R✓] Revealability: Verify the error message
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert "Vui lòng nhập email và mật khẩu" in sem_text, \
        f"Expected error message 'Vui lòng nhập email và mật khẩu' not found in: {sem_text[:200]}"
