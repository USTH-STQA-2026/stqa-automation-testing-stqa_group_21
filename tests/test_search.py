"""
Search & Filter Tests (*Kiểm thử Tìm kiếm & Lọc sách*) — Library Book Borrowing System (*Hệ thống Mượn sách thư viện*)

Students must complete ALL 4 test cases in this file.
(*Sinh viên cần hoàn thành TẤT CẢ 4 test case trong file này.*)

Hints (*Gợi ý*):
    - After logging in, use flutter_fill() to type into the search box
      (*Sau khi đăng nhập, dùng flutter_fill() để nhập vào ô tìm kiếm*)
    - Search box aria-label: "Tìm kiếm theo tên sách hoặc tác giả..."
    - Category filter aria-label: "Lọc theo thể loại (VD: Công nghệ, Kinh tế...)"
    - Each book card has role="group" and aria-label containing book info
      (*Mỗi card sách có role="group" và aria-label chứa thông tin sách*)
    - Use login() helper from conftest.py to log in before testing
      (*Dùng login() helper từ conftest.py để đăng nhập trước khi test*)
"""
import os
from conftest import enable_flutter_semantics, flutter_fill, login, SCREENSHOT_DIR


def test_search_book_by_name(page, test_config):
    """TC-04: Search book by name – results found (*Tìm kiếm sách theo tên — tìm thấy kết quả*)

    Mô tả: Đăng nhập → tìm kiếm từ khóa "Flutter" → kiểm tra có sách Flutter trong kết quả.
    """
    # Arrange: Đăng nhập
    login(page, test_config)

    # Act: Nhập từ khóa "Flutter" vào ô tìm kiếm
    flutter_fill(page, "Tìm kiếm theo tên sách hoặc tác giả...", "Flutter")

    # Smart Wait: Chờ kết quả tìm kiếm xuất hiện
    page.locator('flt-semantics[aria-label*="Flutter"]').first.wait_for(state="attached", timeout=10000)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "search_book_by_name.png"))

    # Assert: Kiểm tra có sách chứa "Flutter" trong kết quả
    results = page.locator('flt-semantics[aria-label*="Flutter"]')
    assert results.count() > 0, "Không tìm thấy sách nào chứa 'Flutter' trong kết quả tìm kiếm"


def test_search_book_no_result(page, test_config):
    """TC-05: Search book – no results (*Tìm kiếm sách — không có kết quả*)

    Mô tả: Đăng nhập → tìm kiếm từ khóa không tồn tại → kiểm tra không có sách nào hiển thị.
    """
    # Arrange: Đăng nhập
    login(page, test_config)

    # Act: Nhập từ khóa không tồn tại
    flutter_fill(page, "Tìm kiếm theo tên sách hoặc tác giả...", "xyz_khong_ton_tai_12345")

    # Smart Wait: Chờ semantics cập nhật sau khi nhập
    page.wait_for_timeout(2000)
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "search_book_no_result.png"))

    # Assert: Không có sách nào hiển thị
    book_cards = page.locator('flt-semantics[role="group"][aria-label*="Mã: BOOK"]')
    assert book_cards.count() == 0, \
        f"Expected 0 books but found {book_cards.count()} books for non-existent keyword"


def test_filter_by_category(page, test_config):
    """TC-06: Filter books by category 'Công nghệ' (*Lọc sách theo thể loại 'Công nghệ'*)

    Mô tả: Đăng nhập → nhập "Công nghệ" vào ô lọc thể loại → kiểm tra tất cả sách
    hiển thị đều thuộc thể loại Công nghệ.
    """
    # Arrange: Đăng nhập
    login(page, test_config)

    # Act: Nhập "Công nghệ" vào ô lọc thể loại
    flutter_fill(page, "Lọc theo thể loại (VD: Công nghệ, Kinh tế...)", "Công nghệ")

    # Smart Wait: Chờ kết quả lọc
    page.wait_for_timeout(2000)
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "filter_by_category.png"))

    # Assert: Tất cả sách hiển thị đều thuộc thể loại "Công nghệ"
    book_cards = page.locator('flt-semantics[role="group"][aria-label*="Mã: BOOK"]')
    count = book_cards.count()
    assert count > 0, "Không tìm thấy sách nào khi lọc theo thể loại 'Công nghệ'"

    for i in range(count):
        label = book_cards.nth(i).get_attribute("aria-label")
        assert "Công nghệ" in label, \
            f"Sách không thuộc thể loại 'Công nghệ': {label}"


def test_search_by_author(page, test_config):
    """TC-07: Search book by author name (*Tìm kiếm sách theo tên tác giả*)

    Mô tả: Đăng nhập → tìm kiếm tên tác giả "Nguyễn Minh Đức" → kiểm tra có kết quả.
    """
    # Arrange: Đăng nhập
    login(page, test_config)

    # Act: Nhập tên tác giả vào ô tìm kiếm
    flutter_fill(page, "Tìm kiếm theo tên sách hoặc tác giả...", "Nguyễn Minh Đức")

    # Smart Wait: Chờ kết quả tìm kiếm xuất hiện
    page.locator('flt-semantics[aria-label*="Nguyễn Minh Đức"]').first.wait_for(state="attached", timeout=10000)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "search_by_author.png"))

    # Assert: Kiểm tra có sách của tác giả "Nguyễn Minh Đức"
    results = page.locator('flt-semantics[aria-label*="Nguyễn Minh Đức"]')
    assert results.count() > 0, "Không tìm thấy sách nào của tác giả 'Nguyễn Minh Đức'"
