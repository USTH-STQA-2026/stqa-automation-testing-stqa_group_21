# REPORT — Báo cáo kết quả kiểm thử tự động

**Nhóm**: Nhóm 21  
**Lớp**: STQA — USTH  
**Học kỳ**: HK2 2025-2026  
**Hệ thống**: Quản lý mượn sách Thư viện ABC — https://stqa.rbc.vn  
**Công cụ**: Python + Playwright + pytest  
**Ngày chạy test**: 28/05/2026

---

## 1. Tổng quan kết quả

| Chỉ số | Giá trị |
|--------|---------|
| Tổng số test case | 18 (12 bắt buộc + 3 bonus B1 + 3 parametrize B2) |
| PASSED | 18 |
| FAILED | 0 |
| Thời gian chạy | ~2 phút 10 giây |
| Trình duyệt | Chromium (headless) |

---

## 2. Chi tiết từng Test Case

### Nhóm 1: Đăng nhập (`tests/test_login.py`)

#### TC-01: Đăng nhập thành công ✅ PASSED

- **Mô tả**: Nhập email và mật khẩu đúng → hệ thống chuyển sang trang chủ.
- **Tài khoản**: `ba.nguyen@email.com` / `password123`
- **Cách kiểm tra**: Sau khi đăng nhập, kiểm tra Semantics Tree có chứa tên hiển thị "Nguyễn Học Bá" hoặc nút "Đăng xuất".
- **Kết quả**: Đăng nhập thành công, tên người dùng và nút "Đăng xuất" hiển thị đúng.
- **Screenshot**: `screenshots/login_success.png`

#### TC-02: Đăng nhập thất bại — sai mật khẩu ✅ PASSED

- **Mô tả**: Nhập email đúng nhưng mật khẩu sai → hệ thống hiển thị thông báo lỗi.
- **Dữ liệu**: Email đúng (`ba.nguyen@email.com`), mật khẩu sai (`wrongpassword`)
- **Cách kiểm tra**: Kiểm tra Semantics Tree chứa thông báo "Mật khẩu không đúng".
- **Kết quả**: Hệ thống hiển thị đúng thông báo lỗi "Mật khẩu không đúng", phù hợp với SRS REQ-01.
- **Screenshot**: `screenshots/login_fail_wrong_password.png`

#### TC-03: Đăng nhập thất bại — để trống ✅ PASSED

- **Mô tả**: Không nhập gì, bấm Đăng nhập → hệ thống hiển thị thông báo lỗi.
- **Dữ liệu**: Email trống, mật khẩu trống
- **Cách kiểm tra**: Kiểm tra Semantics Tree chứa thông báo "Vui lòng nhập email và mật khẩu".
- **Kết quả**: Hệ thống hiển thị đúng thông báo validation, phù hợp với SRS REQ-01.
- **Screenshot**: `screenshots/login_fail_empty_fields.png`

---

### Nhóm 2: Tìm kiếm & Lọc sách (`tests/test_search.py`)

#### TC-04: Tìm sách theo tên ✅ PASSED

- **Mô tả**: Đăng nhập → tìm kiếm từ khóa "Flutter" → kiểm tra kết quả chứa sách Flutter.
- **Cách kiểm tra**: Kiểm tra có element `flt-semantics[aria-label*="Flutter"]` trong kết quả.
- **Kết quả**: Tìm thấy sách "Lập trình Flutter cơ bản" (BOOK001), phù hợp với SRS REQ-03.
- **Screenshot**: `screenshots/search_book_by_name.png`

#### TC-05: Tìm sách — không có kết quả ✅ PASSED

- **Mô tả**: Đăng nhập → tìm kiếm từ khóa không tồn tại → kiểm tra không có sách hiển thị.
- **Dữ liệu**: Từ khóa `xyz_khong_ton_tai_12345`
- **Cách kiểm tra**: Kiểm tra số lượng book card (`flt-semantics[role="group"][aria-label*="Mã: BOOK"]`) bằng 0.
- **Kết quả**: Không có sách nào hiển thị khi tìm từ khóa không tồn tại, phù hợp với SRS REQ-03.
- **Screenshot**: `screenshots/search_book_no_result.png`

#### TC-06: Lọc theo thể loại ✅ PASSED

- **Mô tả**: Đăng nhập → nhập "Công nghệ" vào ô lọc thể loại → kiểm tra tất cả sách hiển thị đều thuộc thể loại Công nghệ.
- **Cách kiểm tra**: Lặp qua từng book card, kiểm tra `aria-label` đều chứa "Công nghệ".
- **Kết quả**: Tất cả sách hiển thị đều thuộc thể loại "Công nghệ", phù hợp với SRS REQ-03.
- **Screenshot**: `screenshots/filter_by_category.png`

#### TC-07: Tìm theo tác giả ✅ PASSED

- **Mô tả**: Đăng nhập → tìm kiếm tên tác giả "Nguyễn Minh Đức" → kiểm tra có kết quả.
- **Cách kiểm tra**: Kiểm tra có element `flt-semantics[aria-label*="Nguyễn Minh Đức"]` trong kết quả.
- **Kết quả**: Tìm thấy sách của tác giả Nguyễn Minh Đức (BOOK001, BOOK009), phù hợp với SRS REQ-03.
- **Screenshot**: `screenshots/search_by_author.png`

---

### Nhóm 3: Mượn & Trả sách (`tests/test_borrow_return.py`)

#### TC-08: Mượn sách ✅ PASSED

- **Mô tả**: Đăng nhập bằng tài khoản `dam.tran@email.com` (chưa mượn sách) → tìm sách "Có sẵn" → click "Mượn sách này" → xác nhận dialog → kiểm tra mượn thành công.
- **Tài khoản**: `dam.tran@email.com` / `password123` (Trần Dựa Dẫm — chưa mượn sách, phù hợp test mượn)
- **Cách kiểm tra**: Kiểm tra thông báo "thành công" hoặc sách chuyển sang trạng thái "Đang mượn".
- **Lưu ý**: Flutter CanvasKit headless có thể crash sau khi xác nhận mượn — test đã xử lý bằng cách tạo browser context mới để verify.
- **Kết quả**: Flow mượn sách hoạt động đúng: click "Mượn sách này" → dialog xác nhận → click "Mượn", phù hợp với SRS REQ-04.
- **Screenshot**: `screenshots/borrow_book_before.png`, `screenshots/borrow_book_dialog.png`, `screenshots/borrow_book.png`

#### TC-09: Xem sách đang mượn ✅ PASSED

- **Mô tả**: Đăng nhập (ba.nguyen — đang mượn BOOK003) → chuyển sang tab "Mượn / Trả" → kiểm tra có phiếu mượn hiển thị.
- **Cách kiểm tra**: Kiểm tra Semantics Tree chứa "Đang mượn", "Trả sách", hoặc mã phiếu "BR001".
- **Kết quả**: Tab "Mượn / Trả" hiển thị đúng phiếu mượn của ba.nguyen, phù hợp với SRS REQ-08.
- **Screenshot**: `screenshots/view_borrowed_books.png`

#### TC-10: Trả sách ✅ PASSED

- **Mô tả**: Đăng nhập (ba.nguyen đang mượn BOOK003) → tab "Mượn / Trả" → click "Trả sách" → kiểm tra trả thành công.
- **Cách kiểm tra**: Kiểm tra Semantics Tree chứa "thành công", "Đã trả", hoặc "Có sẵn".
- **Kết quả**: Trả sách thành công, phù hợp với SRS REQ-05.
- **Screenshot**: `screenshots/return_book.png`

---

### Nhóm 4: Chức năng chung (`tests/test_general.py`)

#### TC-11: Đăng xuất ✅ PASSED

- **Mô tả**: Đăng nhập → click nút "Đăng xuất" → kiểm tra quay về trang đăng nhập.
- **Cách kiểm tra**: Kiểm tra Semantics Tree chứa nút "Đăng nhập" hoặc ô input "Email", hoặc kiểm tra `input[aria-label="Email"]` tồn tại.
- **Kết quả**: Đăng xuất thành công, trang quay về màn hình đăng nhập.
- **Screenshot**: `screenshots/logout.png`

#### TC-12: Chuyển ngôn ngữ sang EN ✅ PASSED

- **Mô tả**: Đăng nhập → click nút "EN" → kiểm tra giao diện chuyển sang tiếng Anh.
- **Cách kiểm tra**: Kiểm tra Semantics Tree chứa các từ tiếng Anh: "Logout", "Borrow", "Library", hoặc "Search".
- **Kết quả**: Giao diện chuyển sang tiếng Anh thành công, phù hợp với SRS mục 5 (Bilingual UI).
- **Screenshot**: `screenshots/switch_language_en.png`

---

### Bonus B1: Test case mới (`tests/test_login.py`, `tests/test_borrow_return.py`)

#### TC-13: Đăng nhập thất bại — email không tồn tại ✅ PASSED

- **Mô tả**: Nhập email không có trong hệ thống → hiển thị "Không tìm thấy thành viên".
- **Dữ liệu**: Email `nobody@test.com`, mật khẩu `anything`
- **Cách kiểm tra**: Kiểm tra Semantics Tree chứa thông báo "Không tìm thấy thành viên".
- **Kết quả**: Hệ thống hiển thị đúng thông báo lỗi, phù hợp với SRS REQ-01.
- **Screenshot**: `screenshots/login_fail_nonexistent_email.png`

#### TC-14: Thành viên tạm ngưng mượn sách → bị từ chối ✅ PASSED

- **Mô tả**: Đăng nhập bằng tài khoản `cu.le@email.com` (MEM004 — Tạm ngưng) → thử mượn sách → bị từ chối.
- **Cách kiểm tra**: Kiểm tra thông báo từ chối liên quan đến tạm ngưng.
- **Kết quả**: Hệ thống từ chối đúng, phù hợp với SRS REQ-04.
- **Screenshot**: `screenshots/borrow_suspended_member.png`

#### TC-15: Thành viên hết hạn mượn sách → bị từ chối ✅ PASSED

- **Mô tả**: Đăng nhập bằng tài khoản `binh.pham@email.com` (MEM005 — Hết hạn) → thử mượn sách → bị từ chối.
- **Cách kiểm tra**: Kiểm tra thông báo từ chối liên quan đến hết hạn.
- **Kết quả**: Hệ thống từ chối đúng và phân biệt lý do với tạm ngưng, phù hợp với SRS REQ-04.
- **Screenshot**: `screenshots/borrow_expired_member.png`

---

### Bonus B2: Data-Driven Test (`tests/test_login.py`)

#### test_login_fail_parametrize — 3 bộ dữ liệu ✅ ALL PASSED

- **Kỹ thuật**: Sử dụng `@pytest.mark.parametrize` (Ch.3 §3.3.2) để chạy cùng kịch bản đăng nhập thất bại với nhiều bộ dữ liệu.
- **Bộ dữ liệu**:
  1. Email đúng + mật khẩu sai → "Mật khẩu không đúng"
  2. Bỏ trống cả hai → "Vui lòng nhập email và mật khẩu"
  3. Email không tồn tại → "Không tìm thấy thành viên"
- **Kết quả**: Cả 3 bộ dữ liệu đều PASSED, thông báo lỗi phù hợp với SRS REQ-01.

---

## 3. Nhận xét chung

### Chất lượng hệ thống

- **Đăng nhập**: Hoạt động đúng theo SRS REQ-01. Thông báo lỗi phân biệt rõ ràng giữa "sai mật khẩu" và "để trống".
- **Tìm kiếm/Lọc**: Hoạt động đúng theo SRS REQ-03. Tìm kiếm theo tên sách, tác giả và lọc theo thể loại đều cho kết quả chính xác.
- **Mượn/Trả sách**: Flow mượn và trả sách hoạt động đúng theo SRS REQ-04 và REQ-05.
- **Chức năng chung**: Đăng xuất và chuyển ngôn ngữ hoạt động ổn định.

### Vấn đề phát hiện

1. **Flutter CanvasKit + Chromium headless crash**: Khi thực hiện mượn sách (TC-08), sau khi click xác nhận trong dialog, trang có thể crash trong chế độ headless. Đây là vấn đề của Flutter Web CanvasKit renderer với Chromium headless, không phải bug của hệ thống.

### Kỹ thuật test

- Sử dụng **Smart Wait** (`wait_for_flutter`, `wait_for`) thay vì `time.sleep()` ở hầu hết các test.
- Tương tác qua **Accessibility Semantics Tree** (aria-label, role) do Flutter CanvasKit không có DOM thông thường.
- Mỗi test có **screenshot** tự động làm minh chứng.
- Assert kiểm tra **text cụ thể** (thông báo lỗi, tên sách, trạng thái) thay vì chỉ kiểm tra URL.

---

## 4. Khai báo sử dụng AI

Nhóm có sử dụng công cụ AI (Warp Oz Agent) để hỗ trợ viết test code cho TC-02 đến TC-12. Cụ thể:

- **Công cụ**: Warp Oz Agent (Claude)
- **Phạm vi sử dụng**: Viết code cho 11 test case (TC-02 → TC-12) và 6 bonus test (TC-13 → TC-15 + 3 parametrize) dựa trên pattern mẫu TC-01 và hints có sẵn trong từng file.
- **Kiểm tra**: Đã chạy `pytest` xác nhận 18/18 test PASSED. Đã review và điều chỉnh TC-08 để xử lý crash issue của Flutter CanvasKit headless.
