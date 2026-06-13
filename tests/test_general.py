"""
Logout & Language Tests (*Kiểm thử Đăng xuất & Chuyển ngôn ngữ*) — Library Book Borrowing System (*Hệ thống Mượn sách thư viện*)

Students must complete ALL 2 test cases in this file.
(*Sinh viên cần hoàn thành TẤT CẢ 2 test case trong file này.*)

Hints (*Gợi ý*):
    - Use login() helper to log in (*Dùng login() helper để đăng nhập*)
    - Logout button: 'flt-semantics[role="button"]:has-text("Đăng xuất")'
      (*Nút Đăng xuất*)
    - Language switch EN button: 'flt-semantics[role="button"]:has-text("EN")'
      (*Nút chuyển ngôn ngữ EN*)
    - After logout: page returns to login (has "Đăng nhập" button and "Email" input)
      (*Sau đăng xuất: trang quay về login*)
    - After switching to EN: text "Logout", "Borrow", "Search", "Library" may appear
      (*Sau chuyển EN: text tiếng Anh có thể xuất hiện*)
"""
import os
from conftest import enable_flutter_semantics, login, SCREENSHOT_DIR


def test_logout(page, test_config):
    """TC-11: Logout success (*Đăng xuất thành công*)

    Mô tả: Đăng nhập → click Đăng xuất → kiểm tra quay về trang đăng nhập.
    """
    # Arrange: Đăng nhập
    login(page, test_config)

    # Act: Click nút "Đăng xuất"
    logout_btn = page.locator('flt-semantics[role="button"]:has-text("Đăng xuất")').first
    logout_btn.click()

    # Smart Wait: Chờ quay về trang đăng nhập
    page.wait_for_timeout(3000)
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "logout.png"))

    # Assert: Kiểm tra đã quay về trang đăng nhập (có nút "Đăng nhập" hoặc ô Email)
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    has_login_page = "Đăng nhập" in sem_text or "Email" in sem_text or "Login" in sem_text
    has_email_input = page.locator('input[aria-label="Email"]').count() > 0
    assert has_login_page or has_email_input, \
        f"Không quay về trang đăng nhập sau khi đăng xuất. Sem text: {sem_text[:300]}"


def test_switch_language_to_english(page, test_config):
    """TC-12: Switch language to English (*Chuyển ngôn ngữ sang tiếng Anh*)

    Mô tả: Đăng nhập → click nút "EN" → kiểm tra giao diện chuyển sang tiếng Anh.
    """
    # Arrange: Đăng nhập
    login(page, test_config)

    # Act: Click nút "EN" để chuyển ngôn ngữ
    en_btn = page.locator('flt-semantics[role="button"]:has-text("EN")').first
    en_btn.click()

    # Smart Wait: Chờ giao diện chuyển ngôn ngữ
    page.wait_for_timeout(2000)
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "switch_language_en.png"))

    # Assert: Kiểm tra giao diện hiển thị tiếng Anh
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    has_english = "Logout" in sem_text or "Borrow" in sem_text or "Library" in sem_text or "Search" in sem_text
    assert has_english, \
        f"Giao diện không chuyển sang tiếng Anh sau khi click 'EN'. Sem text: {sem_text[:300]}"
