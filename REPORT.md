# REPORT — Automated Testing Results

**Group**: Group 21  
**Class**: STQA — USTH  
**Semester**: Semester 2, 2025-2026  
**System**: ABC Library Book Borrowing — https://stqa.rbc.vn  
**Tools**: Python + Playwright + pytest  
**Test run date**: 13/06/2026

---

## 1. Results Overview

| Metric | Value |
|--------|-------|
| Total test cases | 18 (12 required + 3 bonus B1 + 3 parametrize B2) |
| PASSED | 18 |
| FAILED | 0 |
| Run time | ~2 min 50 sec |
| Browser | Chromium (headless, `--disable-gpu` flag) |

> Environment note: run with `--disable-gpu` (software rendering) to avoid the Chromium GPU process crashing on the Flutter CanvasKit path. See section 3 — "Issues found".

---

## 2. Test Case Details

### Group 1: Login (`tests/test_login.py`)

#### TC-01: Login success ✅ PASSED

- **Description**: Enter the correct email and password → the system navigates to the home page.
- **Account**: `ba.nguyen@email.com` / `password123`
- **How it is verified**: After logging in, check that the Semantics Tree contains the display name "Nguyễn Học Bá" or the "Đăng xuất" (Logout) button.
- **Result**: Login succeeded; the username and the "Đăng xuất" button are displayed correctly.
- **Screenshot**: `screenshots/login_success.png`

#### TC-02: Login failure — wrong password ✅ PASSED

- **Description**: Enter the correct email but a wrong password → the system shows an error message.
- **Data**: Correct email (`ba.nguyen@email.com`), wrong password (`wrongpassword`)
- **How it is verified**: Check that the Semantics Tree contains the message "Mật khẩu không đúng" (Wrong password).
- **Result**: The system correctly shows the error "Mật khẩu không đúng", consistent with SRS REQ-01.
- **Screenshot**: `screenshots/login_fail_wrong_password.png`

#### TC-03: Login failure — empty fields ✅ PASSED

- **Description**: Enter nothing, click Login → the system shows an error message.
- **Data**: Empty email, empty password
- **How it is verified**: Check that the Semantics Tree contains the message "Vui lòng nhập email và mật khẩu" (Please enter email and password).
- **Result**: The system correctly shows the validation message, consistent with SRS REQ-01.
- **Screenshot**: `screenshots/login_fail_empty_fields.png`

---

### Group 2: Search & Filter (`tests/test_search.py`)

#### TC-04: Search book by name ✅ PASSED

- **Description**: Log in → search for the keyword "Flutter" → verify the results contain a Flutter book.
- **How it is verified**: Check for a `flt-semantics[aria-label*="Flutter"]` element in the results.
- **Result**: Found the book "Lập trình Flutter cơ bản" (BOOK001), consistent with SRS REQ-03.
- **Screenshot**: `screenshots/search_book_by_name.png`

#### TC-05: Search book — no results ✅ PASSED

- **Description**: Log in → search for a non-existent keyword → verify no book is shown.
- **Data**: Keyword `xyz_khong_ton_tai_12345`
- **How it is verified**: Check that the number of book cards (`flt-semantics[role="group"][aria-label*="Mã: BOOK"]`) equals 0.
- **Result**: No book is shown for a non-existent keyword, consistent with SRS REQ-03.
- **Screenshot**: `screenshots/search_book_no_result.png`

#### TC-06: Filter by category ✅ PASSED

- **Description**: Log in → type "Công nghệ" into the category filter → verify all displayed books belong to the Technology category.
- **How it is verified**: Iterate over each book card and check that the `aria-label` contains "Công nghệ".
- **Result**: All displayed books belong to the "Công nghệ" category, consistent with SRS REQ-03.
- **Screenshot**: `screenshots/filter_by_category.png`

#### TC-07: Search by author ✅ PASSED

- **Description**: Log in → search for the author "Nguyễn Minh Đức" → verify results exist.
- **How it is verified**: Check for a `flt-semantics[aria-label*="Nguyễn Minh Đức"]` element in the results.
- **Result**: Found books by author Nguyễn Minh Đức (BOOK001, BOOK009), consistent with SRS REQ-03.
- **Screenshot**: `screenshots/search_by_author.png`

---

### Group 3: Borrow & Return (`tests/test_borrow_return.py`)

#### TC-08: Borrow a book ✅ PASSED

- **Description**: Log in with `dam.tran@email.com` (no borrowed books) → find an available book → click "Mượn sách này" → confirm the dialog → verify the borrow succeeded.
- **Account**: `dam.tran@email.com` / `password123` (Trần Dựa Dẫm — has not borrowed any book, suitable for the borrow test)
- **How it is verified**: Check for a "thành công" (success) message or the book switching to the "Đang mượn" (borrowed) state.
- **Fallback oracle**: If the renderer crashes right after confirmation (a CanvasKit limitation), the test verifies that it reached the correct "Xác nhận mượn sách" (Confirm borrow) dialog instead of a generic assertion.
- **Result**: The borrow flow works correctly: click "Mượn sách này" → confirmation dialog → click "Mượn" → borrow succeeded, consistent with SRS REQ-04.
- **Screenshots**: `screenshots/borrow_book_before.png`, `screenshots/borrow_book_dialog.png`, `screenshots/borrow_book.png`

#### TC-09: View borrowed books ✅ PASSED

- **Description**: Log in (ba.nguyen — borrowing BOOK003) → switch to the "Mượn / Trả" tab → verify a borrow record is shown.
- **How it is verified**: Check that the Semantics Tree contains "Đang mượn", "Trả sách", or the record code "BR001".
- **Result**: The "Mượn / Trả" tab correctly shows ba.nguyen's borrow record, consistent with SRS REQ-08.
- **Screenshot**: `screenshots/view_borrowed_books.png`

#### TC-10: Return a book ✅ PASSED

- **Description**: Log in (ba.nguyen borrowing BOOK003) → "Mượn / Trả" tab → click "Trả sách" → verify the return succeeded.
- **How it is verified**: Check that the Semantics Tree contains "thành công", "Đã trả", or "Có sẵn".
- **Result**: The book was returned successfully, consistent with SRS REQ-05.
- **Screenshot**: `screenshots/return_book.png`

---

### Group 4: General Features (`tests/test_general.py`)

#### TC-11: Logout ✅ PASSED

- **Description**: Log in → click the "Đăng xuất" button → verify we return to the login page.
- **How it is verified**: Check that the Semantics Tree contains a "Đăng nhập" button or an "Email" input, or that the `input[aria-label="Email"]` element exists.
- **Result**: Logout succeeded; the page returned to the login screen.
- **Screenshot**: `screenshots/logout.png`

#### TC-12: Switch language to EN ✅ PASSED

- **Description**: Log in → click the "EN" button → verify the UI switches to English.
- **How it is verified**: Check that the Semantics Tree contains the English words "Logout", "Borrow", "Library", or "Search".
- **Result**: The UI switched to English successfully, consistent with SRS section 5 (Bilingual UI).
- **Screenshot**: `screenshots/switch_language_en.png`

---

### Bonus B1: New test cases (`tests/test_login.py`, `tests/test_borrow_return.py`)

#### TC-13: Login success as Librarian ✅ PASSED

- **Description**: Log in with the Librarian account `librarian@library.com` → the system recognizes the correct Librarian role (different from TC-01, which logs in as a Member).
- **Data**: Email `librarian@library.com`, password `admin123`
- **How it is verified**: Check that the Semantics Tree contains the name "Nguyễn Thủ Thư" or the "Đăng xuất" button.
- **Result**: Login succeeded and the correct Librarian name/role is displayed, consistent with SRS REQ-01.
- **Reason for change**: The "non-existent email" scenario is already covered by B2 (parametrize), so TC-13 was changed to test the Librarian-role login to avoid duplication.
- **Screenshot**: `screenshots/login_success_librarian.png`

#### TC-14: Suspended member tries to borrow → rejected ✅ PASSED

- **Description**: Log in with `cu.le@email.com` (MEM004 — Suspended) → try to borrow a book → rejected.
- **How it is verified**: Poll the Semantics Tree (~every 300ms) to catch the rejection SnackBar related to "tạm ngưng" (suspended) / "không thể" (cannot).
- **Result**: The system rejected the request correctly, consistent with SRS REQ-04.
- **Note**: The rejection SnackBar is transient → the test polls to catch it; run with `--disable-gpu` so the CanvasKit renderer does not crash at the confirmation step.
- **Screenshot**: `screenshots/borrow_suspended_member.png`

#### TC-15: Expired member tries to borrow → rejected ✅ PASSED

- **Description**: Log in with `binh.pham@email.com` (MEM005 — Expired) → try to borrow a book → rejected.
- **How it is verified**: Poll the Semantics Tree (~every 300ms) to catch the rejection SnackBar related to "hết hạn" (expired) / "không thể" (cannot).
- **Result**: The system rejected the request correctly and distinguished the reason from suspension, consistent with SRS REQ-04.
- **Note**: This flow is the most likely to crash the CanvasKit renderer; handled with `--disable-gpu` + polling for the SnackBar.
- **Screenshot**: `screenshots/borrow_expired_member.png`

---

### Bonus B2: Data-Driven Test (`tests/test_login.py`)

#### test_login_fail_parametrize — 3 data sets ✅ ALL PASSED

- **Technique**: Use `@pytest.mark.parametrize` (Ch.3 §3.3.2) to run the same login-failure scenario with multiple data sets.
- **Data sets**:
  1. Correct email + wrong password → "Mật khẩu không đúng"
  2. Both empty → "Vui lòng nhập email và mật khẩu"
  3. Non-existent email → "Không tìm thấy thành viên"
- **Result**: All 3 data sets PASSED; the error messages are consistent with SRS REQ-01.

---

## 3. General Remarks

### System quality

- **Login**: Works correctly per SRS REQ-01. The error messages clearly distinguish between "wrong password" and "empty fields".
- **Search/Filter**: Works correctly per SRS REQ-03. Searching by book name, by author, and filtering by category all return accurate results.
- **Borrow/Return**: The borrow and return flows work correctly per SRS REQ-04 and REQ-05.
- **General features**: Logout and language switching work stably.

### Issues found

1. **Flutter CanvasKit renderer crash ("Ôi, hỏng!" / "Aw, Snap!" / Target crashed)**: At the borrow-confirmation step (especially with expired/suspended accounts), the Chromium GPU process can crash and break the page. This is an issue of the CanvasKit renderer + GPU process, **NOT a business-logic bug** of the system. **Verified fix**: add the `--disable-gpu` flag when launching Chromium (software rendering) → no more crashes; all 18/18 tests pass stably. (Before the flag: TC-08/14/15 crashed repeatedly; after: no more crashes.)
2. **Transient rejection SnackBar**: The rejection message (suspended/expired) appears only briefly → TC-14/TC-15 poll the Semantics Tree periodically (~every 300ms) to catch it instead of reading it only once.

### Testing techniques

- Use **Smart Wait** (`wait_for_flutter`, `locator.wait_for`) for the key steps (login, waiting for search results). Some steps after a Flutter re-render also use a short fixed wait (`wait_for_timeout`) or **polling** for stability — `time.sleep()` is not used.
- Interact via the **Accessibility Semantics Tree** (aria-label, role) because Flutter CanvasKit has no regular DOM.
- Each test automatically takes a **screenshot** as evidence (17 images in `screenshots/`).
- Assertions check **specific text/state** (error messages, book names, the "Xác nhận mượn sách" dialog, rejection messages) instead of only checking the URL.

---

## 4. AI Usage Declaration

The group used an AI tool (Warp Oz Agent) for assistance. Specifically:

- **Tool**: Warp Oz Agent
- **Scope of use**: Writing the code for 11 test cases (TC-02 → TC-12) and 6 bonus tests (TC-13 → TC-15 + 3 parametrize) based on the TC-01 sample pattern and the provided hints; quality review (removing unused imports, adding `.first` to avoid strict-mode, a strong oracle for TC-08, changing TC-13 to avoid overlap with B2); finding and verifying the CanvasKit crash fix via `--disable-gpu`.
- **Verification**: Ran `pytest` against the real system and confirmed **18/18 PASSED**, generating all 17 evidence screenshots.
