# REPORT - Automated Testing Results

**Group**: Group 21  
**Class**: STQA - USTH  
**Semester**: Semester 2, 2025-2026  
**System**: ABC Library Book Borrowing - https://stqa.rbc.vn  
**Tools**: Python + Playwright + pytest  
**Test run date**: 13/06/2026  

---

## 1. Results Overview

| Metric | Value |
|--------|-------|
| Required A2 test cases | 12 / 12 implemented |
| Bonus B1 tests | 3 additional tests implemented |
| Bonus B2 data-driven checks | 3 parametrized login-failure datasets |
| Manual alignment regression | 1 expected-failure check for Manual TC-33 / BUG-08 |
| Pytest outcome | 18 passed, 1 xfailed, 0 failed |
| Browser | Chromium with `--disable-gpu` |

The suite keeps the A2 scoring checks green while also documenting the known localization defect from the Manual PERFECT submission. The BUG-08 check is marked `xfail(strict=True)`: if the application is fixed later, the test will XPASS and fail the run, forcing the expected-failure marker to be removed.

---

## 2. Test Case Details

### Group 1: Login (`tests/test_login.py`)

#### TC-01: Login success - PASSED

- **Description**: Enter valid member credentials and verify the home page is reached.
- **Oracle**: Semantics Tree contains the configured display name or the Logout button.
- **Evidence**: `screenshots/login_success.png`

#### TC-02: Login failure - wrong password - PASSED

- **Description**: Enter a valid email with an invalid password.
- **Oracle**: Exact error message `Mật khẩu không đúng`.
- **Evidence**: `screenshots/login_fail_wrong_password.png`

#### TC-03: Login failure - empty fields - PASSED

- **Description**: Leave both login fields empty and submit.
- **Oracle**: Exact validation message `Vui lòng nhập email và mật khẩu`.
- **Evidence**: `screenshots/login_fail_empty_fields.png`

#### TC-13: Login success as Librarian - PASSED

- **Description**: Log in with `librarian@library.com` / `admin123`.
- **Oracle**: Semantics Tree contains `Nguyễn Thủ Thư`, `Thủ thư`, or Logout.
- **Evidence**: `screenshots/login_success_librarian.png`

#### B2: Data-driven login failures - ALL PASSED

- **Technique**: `@pytest.mark.parametrize`.
- **Datasets**:
  - Correct email + wrong password.
  - Empty email + empty password.
  - Unknown email.
- **Oracle**: Each dataset checks its exact SRS error message.
- **Evidence**:
  - `screenshots/login_fail_parametrize_wrong_password.png`
  - `screenshots/login_fail_parametrize_empty_fields.png`
  - `screenshots/login_fail_parametrize_unknown_email.png`

---

### Group 2: Search & Filter (`tests/test_search.py`)

#### TC-04: Search book by name - PASSED

- **Description**: Search for `Flutter`.
- **Oracle**: At least one result contains `Flutter`.
- **Evidence**: `screenshots/search_book_by_name.png`

#### TC-05: Search book - no results - PASSED

- **Description**: Search for a keyword that does not exist.
- **Oracle**: No book cards are displayed.
- **Evidence**: `screenshots/search_book_no_result.png`

#### TC-06: Filter by category - PASSED

- **Description**: Filter by `Công nghệ`.
- **Oracle**: Every displayed book card belongs to `Công nghệ`.
- **Evidence**: `screenshots/filter_by_category.png`

#### TC-07: Search by author - PASSED

- **Description**: Search for author `Nguyễn Minh Đức`.
- **Oracle**: At least one result contains that author name.
- **Evidence**: `screenshots/search_by_author.png`

---

### Group 3: Borrow & Return (`tests/test_borrow_return.py`)

#### TC-08: Borrow a book - PASSED

- **Description**: Use an active member, borrow an available book, and confirm the dialog.
- **Oracle**: Success text or borrowed status appears after confirmation.
- **Evidence**: `screenshots/borrow_book_before.png`, `screenshots/borrow_book_dialog.png`, `screenshots/borrow_book.png`

#### TC-09: View borrowed books - PASSED

- **Description**: Open the Borrow/Return tab as a member with an existing borrow record.
- **Oracle**: Borrowed status, Return Book button, or BR001 is visible.
- **Evidence**: `screenshots/view_borrowed_books.png`

#### TC-10: Return a book - PASSED

- **Description**: Return an active borrowed book.
- **Oracle**: Success text, returned status, or available status appears.
- **Evidence**: `screenshots/return_book.png`

#### TC-14: Suspended member borrow rejection - PASSED

- **Description**: Log in as MEM004 and attempt to borrow an available book.
- **Oracle**: Poll for a transient rejection message related to suspended status.
- **Evidence**: `screenshots/borrow_suspended_member.png`

#### TC-15: Expired member borrow rejection - PASSED

- **Description**: Log in as MEM005 and attempt to borrow an available book.
- **Oracle**: Poll for a transient rejection message related to expired status.
- **Evidence**: `screenshots/borrow_expired_member.png`

---

### Group 4: General & Bilingual (`tests/test_general.py`)

#### TC-11: Logout - PASSED

- **Description**: Log in, click Logout, and verify the login page is visible again.
- **Oracle**: Login button and Email input are present.
- **Evidence**: `screenshots/logout.png`

#### TC-12: Switch language to English - PASSED

- **Description**: Switch the UI language to English.
- **Oracle**: Main UI chrome contains English labels such as Logout, Borrow, Library, or Search.
- **Evidence**: `screenshots/switch_language_en.png`

#### TC-16: English category localization - XFAIL, known BUG-08

- **Description**: Switch to English and verify visible book category names are also localized.
- **Manual alignment**: This is the automation counterpart of Manual TC-33 / BUG-08 in the Manual PERFECT submission.
- **Expected oracle**: Vietnamese category names such as `Công nghệ`, `Quản trị`, `Kinh tế`, `Kỹ năng mềm`, `Giáo dục`, and `Văn học` should not remain visible.
- **Current result**: Expected failure until BUG-08 is fixed.
- **Evidence**: `screenshots/switch_language_category_bug08.png`

---

## 3. Quality Notes

- Tests interact with Flutter CanvasKit through the Accessibility Semantics Tree (`flt-semantics`, ARIA labels, roles).
- Smart waits (`wait_for_flutter`, `locator.wait_for`) are used for key transitions instead of raw `time.sleep()`.
- The Chromium browser is launched with `--disable-gpu` to avoid the CanvasKit GPU-process crash observed around borrow confirmation flows.
- Assertions check specific text/state instead of only checking URL changes.
- Screenshots are named by scenario and stored in `screenshots/`.

---

## 4. Bonus Coverage

| Bonus | Evidence |
|-------|----------|
| B1: At least 3 new tests | TC-13, TC-14, TC-15 |
| B2: Data-driven test | `test_login_fail_parametrize` with 3 datasets |
| B3: Detailed assertions | Exact messages, role/name, book/category/status checks |
| B4: Detailed report | This `REPORT.md` |

---

## 5. AI Usage Declaration

The group used an AI tool (Warp Oz Agent) for assistance.

- **Scope of use**: Implementing TC-02 to TC-12, bonus tests TC-13 to TC-15, data-driven login checks, and Flutter CanvasKit stability improvements.
- **Review performed**: The code was reviewed and adjusted for stronger oracles, scenario-specific screenshots, Semantics Tree interaction, and alignment with Manual TC-33 / BUG-08.
- **Verification target**: `pytest` should report `18 passed, 1 xfailed, 0 failed` when run against the current system state.
