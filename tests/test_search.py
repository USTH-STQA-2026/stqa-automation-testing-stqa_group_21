"""
Search & Filter Tests — Library Book Borrowing System

Students must complete ALL 4 test cases in this file.

Hints:
    - After logging in, use flutter_fill() to type into the search box
    - Search box aria-label: "Tìm kiếm theo tên sách hoặc tác giả..."
    - Category filter aria-label: "Lọc theo thể loại (VD: Công nghệ, Kinh tế...)"
    - Each book card has role="group" and an aria-label containing book info
    - Use the login() helper from conftest.py to log in before testing
"""
import os
from conftest import enable_flutter_semantics, flutter_fill, login, SCREENSHOT_DIR


def test_search_book_by_name(page, test_config):
    """TC-04: Search book by name – results found

    Description: Log in → search for "Flutter" → verify the results contain a Flutter book.
    """
    # Arrange: Log in
    login(page, test_config)

    # Act: Type the keyword "Flutter" into the search box
    flutter_fill(page, "Tìm kiếm theo tên sách hoặc tác giả...", "Flutter")

    # Smart Wait: Wait for the search results to appear
    page.locator('flt-semantics[aria-label*="Flutter"]').first.wait_for(state="attached", timeout=10000)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "search_book_by_name.png"))

    # Assert: Verify there is at least one book containing "Flutter" in the results
    results = page.locator('flt-semantics[aria-label*="Flutter"]')
    assert results.count() > 0, "No book containing 'Flutter' was found in the search results"


def test_search_book_no_result(page, test_config):
    """TC-05: Search book – no results

    Description: Log in → search for a non-existent keyword → verify no book is shown.
    """
    # Arrange: Log in
    login(page, test_config)

    # Act: Type a non-existent keyword
    flutter_fill(page, "Tìm kiếm theo tên sách hoặc tác giả...", "xyz_khong_ton_tai_12345")

    # Smart Wait: Wait for the semantics to update after typing
    page.wait_for_timeout(2000)
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "search_book_no_result.png"))

    # Assert: No book is shown
    book_cards = page.locator('flt-semantics[role="group"][aria-label*="Mã: BOOK"]')
    assert book_cards.count() == 0, \
        f"Expected 0 books but found {book_cards.count()} books for a non-existent keyword"


def test_filter_by_category(page, test_config):
    """TC-06: Filter books by category 'Công nghệ'

    Description: Log in → type "Công nghệ" into the category filter → verify all
    displayed books belong to the Công nghệ (Technology) category.
    """
    # Arrange: Log in
    login(page, test_config)

    # Act: Type "Công nghệ" into the category filter
    flutter_fill(page, "Lọc theo thể loại (VD: Công nghệ, Kinh tế...)", "Công nghệ")

    # Smart Wait: Wait for the filter results
    page.wait_for_timeout(2000)
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "filter_by_category.png"))

    # Assert: All displayed books belong to the "Công nghệ" category
    book_cards = page.locator('flt-semantics[role="group"][aria-label*="Mã: BOOK"]')
    count = book_cards.count()
    assert count > 0, "No book found when filtering by the 'Công nghệ' category"

    for i in range(count):
        label = book_cards.nth(i).get_attribute("aria-label")
        assert "Công nghệ" in label, \
            f"Book does not belong to the 'Công nghệ' category: {label}"


def test_search_by_author(page, test_config):
    """TC-07: Search book by author name

    Description: Log in → search for the author "Nguyễn Minh Đức" → verify results exist.
    """
    # Arrange: Log in
    login(page, test_config)

    # Act: Type the author name into the search box
    flutter_fill(page, "Tìm kiếm theo tên sách hoặc tác giả...", "Nguyễn Minh Đức")

    # Smart Wait: Wait for the search results to appear
    page.locator('flt-semantics[aria-label*="Nguyễn Minh Đức"]').first.wait_for(state="attached", timeout=10000)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "search_by_author.png"))

    # Assert: Verify there are books by the author "Nguyễn Minh Đức"
    results = page.locator('flt-semantics[aria-label*="Nguyễn Minh Đức"]')
    assert results.count() > 0, "No book by author 'Nguyễn Minh Đức' was found"
