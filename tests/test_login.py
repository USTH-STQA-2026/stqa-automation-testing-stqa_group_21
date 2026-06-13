"""
Login Tests (*Kiểm thử Đăng nhập*) — Library Book Borrowing System (*Hệ thống Mượn sách thư viện*)

📖 Textbook concepts in this file:
   - RIPR Model (Ch.2): See [R], [I], [P], [R✓] comments in TC-01
   - Data-Driven Testing / @parametrize (Ch.3 §3.3.2): See hint in TC-02/TC-03

This file contains 1 completed example (TC-01).
Students must complete TC-02 and TC-03.

(*File này chứa 1 ví dụ mẫu (TC-01) đã hoàn chỉnh.
Sinh viên cần hoàn thành TC-02 và TC-03.*)
"""
import os
import pytest
from conftest import enable_flutter_semantics, flutter_fill, flutter_click_button, wait_for_flutter, SCREENSHOT_DIR


def test_login_success(page, test_config):
    """TC-01: Login success with valid credentials (*Đăng nhập thành công với thông tin hợp lệ*)

    ✅ COMPLETED — Use as a reference example.
    (*ĐÃ HOÀN THÀNH — Dùng làm ví dụ tham khảo.*)

    📖 RIPR Model (Textbook Ch.2 — Reachability → Infection → Propagation → Revealability):
        Mỗi dòng code trong test tương ứng với 1 bước trong chuỗi RIPR.
        Xem comment [R], [I], [P], [R✓] bên dưới.
    """
    # [R] Reachability: Truy cập trang đăng nhập — chạm tới UI cần test
    page.goto(test_config["base_url"], wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)

    # [I] Infection: Nhập dữ liệu hợp lệ — kích hoạt logic đăng nhập trong hệ thống
    flutter_fill(page, "Email", test_config["email"])
    flutter_fill(page, "Mật khẩu", test_config["password"])
    flutter_click_button(page, "Đăng nhập")

    # [P] Propagation: Chờ trạng thái lan truyền ra UI — nút "Đăng xuất" xuất hiện
    # (Smart Wait: thay vì time.sleep(5) — nhanh hơn và ổn định hơn)
    wait_for_flutter(page, text="Đăng xuất")
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "login_success.png"))

    # [R✓] Revealability: Kiểm tra kết quả — Test Oracle phát hiện lỗi nếu có
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    has_user_name = test_config["display_name"] in sem_text
    has_logout = "Đăng xuất" in sem_text or "Logout" in sem_text
    assert has_user_name or has_logout, \
        f"Login failed: '{test_config['display_name']}' or Logout button not found " \
        f"(Đăng nhập không thành công: không tìm thấy tên hoặc nút Đăng xuất)"


@pytest.mark.parametrize("email,password,expected_error", [
    ("ba.nguyen@email.com", "wrongpassword", "Mật khẩu không đúng"),
    ("", "", "Vui lòng nhập email và mật khẩu"),
    ("nobody@test.com", "anything", "Không tìm thấy thành viên"),
])
def test_login_fail_parametrize(page, test_config, email, password, expected_error):
    """B2: Data-driven login failure test (*Kiểm thử đăng nhập thất bại — nhiều bộ dữ liệu*)

    📖 Data-Driven Testing (Ch.3 §3.3.2):
        Dùng @pytest.mark.parametrize để chạy cùng kịch bản với nhiều bộ dữ liệu khác nhau.
    """
    # Arrange: Truy cập trang đăng nhập
    page.goto(test_config["base_url"], wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)

    # Act: Nhập dữ liệu và đăng nhập
    if email:
        flutter_fill(page, "Email", email)
    if password:
        flutter_fill(page, "Mật khẩu", password)
    flutter_click_button(page, "Đăng nhập")

    # Smart Wait: Chờ thông báo lỗi
    wait_for_flutter(page, text=expected_error)

    # Assert: Kiểm tra thông báo lỗi đúng
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert expected_error in sem_text, \
        f"Expected error '{expected_error}' not found in: {sem_text[:200]}"


def test_login_success_librarian(page, test_config):
    """TC-13 (B1): Login success as Librarian (*Đăng nhập thành công với vai trò Thủ thư*)

    Khác với TC-01 (đăng nhập Thành viên), TC này kiểm tra đăng nhập bằng tài khoản
    Thủ thư (librarian@library.com) — xác minh hệ thống nhận đúng vai trò Thủ thư.

    📖 RIPR Model:
        [R] Truy cập trang đăng nhập
        [I] Nhập credentials Thủ thư hợp lệ → kích hoạt logic đăng nhập
        [P] Trạng thái lan truyền ra UI (tên + vai trò Thủ thư)
        [R✓] Assert tên hiển thị "Nguyễn Thủ Thư" hoặc nút "Đăng xuất"
    """
    # [R] Reachability
    page.goto(test_config["base_url"], wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)

    # [I] Infection: Đăng nhập bằng tài khoản Thủ thư
    flutter_fill(page, "Email", "librarian@library.com")
    flutter_fill(page, "Mật khẩu", "admin123")
    flutter_click_button(page, "Đăng nhập")

    # [P] Propagation: Chờ trang chính load
    wait_for_flutter(page, text="Đăng xuất")
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "login_success_librarian.png"))

    # [R✓] Revealability: Kiểm tra đăng nhập đúng vai trò Thủ thư
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    has_librarian = "Nguyễn Thủ Thư" in sem_text or "Thủ thư" in sem_text
    has_logout = "Đăng xuất" in sem_text or "Logout" in sem_text
    assert has_librarian or has_logout, \
        f"Đăng nhập Thủ thư không thành công. Sem text: {sem_text[:200]}"


def test_login_fail_wrong_password(page, test_config):
    """TC-02: Login fail – wrong password (*Đăng nhập thất bại – sai mật khẩu*)

    📖 RIPR Model:
        [R] Truy cập trang đăng nhập
        [I] Nhập email đúng + mật khẩu sai → kích hoạt nhánh xử lý lỗi
        [P] Lỗi lan truyền ra thông báo trên UI
        [R✓] Assert kiểm tra thông báo lỗi "Mật khẩu không đúng"
    """
    # [R] Reachability: Truy cập trang đăng nhập
    page.goto(test_config["base_url"], wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)

    # [I] Infection: Nhập email đúng nhưng mật khẩu sai
    flutter_fill(page, "Email", test_config["email"])
    flutter_fill(page, "Mật khẩu", "wrongpassword")
    flutter_click_button(page, "Đăng nhập")

    # [P] Propagation: Chờ thông báo lỗi xuất hiện
    wait_for_flutter(page, text="Mật khẩu không đúng")
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "login_fail_wrong_password.png"))

    # [R✓] Revealability: Kiểm tra thông báo lỗi
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert "Mật khẩu không đúng" in sem_text, \
        f"Expected error message 'Mật khẩu không đúng' not found in: {sem_text[:200]}"


def test_login_fail_empty_fields(page, test_config):
    """TC-03: Login fail – empty fields (*Đăng nhập thất bại – để trống các trường*)

    📖 RIPR Model:
        [R] Truy cập trang đăng nhập
        [I] Không nhập gì, click Đăng nhập → kích hoạt validation
        [P] Lỗi lan truyền ra thông báo "Vui lòng nhập email và mật khẩu"
        [R✓] Assert kiểm tra thông báo lỗi hoặc vẫn ở trang đăng nhập
    """
    # [R] Reachability: Truy cập trang đăng nhập
    page.goto(test_config["base_url"], wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)

    # [I] Infection: Không nhập gì, click Đăng nhập ngay
    flutter_click_button(page, "Đăng nhập")

    # [P] Propagation: Chờ thông báo lỗi xuất hiện
    wait_for_flutter(page, text="Vui lòng nhập email và mật khẩu")
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "login_fail_empty_fields.png"))

    # [R✓] Revealability: Kiểm tra thông báo lỗi
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert "Vui lòng nhập email và mật khẩu" in sem_text, \
        f"Expected error message 'Vui lòng nhập email và mật khẩu' not found in: {sem_text[:200]}"
