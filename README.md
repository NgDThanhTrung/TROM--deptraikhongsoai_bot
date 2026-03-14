# 🤖 Telegram UserBot: Web-to-Telegram Automation — Edition 2026
### 🛠 Phát triển bởi: [NgDanhThanhTrung](https://github.com/NgDanhThanhTrung)

![Tác giả](https://img.shields.io/badge/Author-NgDanhThanhTrung-blue?style=for-the-badge&logo=telegram)
![Ngôn ngữ](https://img.shields.io/badge/Language-Python-yellow?style=for-the-badge&logo=python)
![Trạng thái](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)
![Stars](https://img.shields.io/github/stars/NgDanhThanhTrung/UserBot?style=for-the-badge&color=gold)

Dự án này là một giải pháp tự động hóa đột phá được nghiên cứu và phát triển độc quyền bởi **NgDanhThanhTrung**. Hệ thống cho phép biến tài khoản Telegram cá nhân thành một công cụ thực thi lệnh mạnh mẽ thông qua yêu cầu HTTP (URL).

---

## 💡 Bản Quyền & Chất Xám Tác Giả
Đây là sản phẩm trí tuệ dựa trên kinh nghiệm tối ưu hóa quy trình tương tác API của **NgDanhThanhTrung**. 

> **⚡ Thông điệp từ tác giả:**
> "Mã nguồn này được chia sẻ với mục đích học tập và hỗ trợ cộng đồng. Tôi hy vọng bạn sẽ tôn trọng chất xám của tôi bằng cách giữ nguyên ghi chú bản quyền và không sử dụng cho các mục đích thương mại trái phép."

---

## 🌟 Tính Năng Nổi Bật (Cập nhật 2026)
* **HTTP Trigger 2.0**: Kích hoạt gửi tin nhắn tức thì bằng cách truy cập URL từ trình duyệt hoặc dịch vụ hẹn giờ.
* **Sequence Automation (Mới)**: Hỗ trợ chạy các chuỗi lệnh liên hoàn tự động (Combo lệnh) với thời gian nghỉ tối ưu.
* **Smart Anti-Spam**: Cơ chế nghỉ ngẫu nhiên linh hoạt (từ 1.5s đến 7.5s tùy loại lệnh) để mô phỏng hành vi người dùng thật và bảo vệ tài khoản khỏi bị ban.
* **Multi-Target Control**: Điều khiển linh hoạt nhiều Bot mục tiêu hoặc khóa cứng mục tiêu cụ thể.
* **Auto-Numbering**: Tự động đánh số thứ tự cho các lệnh lặp đơn lẻ để tránh trùng lặp nội dung.
* **Kill Switch**: Lệnh `/stop` giúp ngắt mọi tác vụ đang chạy ngay lập tức.

---

## 📖 Cách Sử Dụng (API Endpoints)

### 1. Chế độ Chuỗi Lệnh Tài Xỉu (TX-Farm) — *New*
Dành riêng cho `@deptraikhongsoai_bot`. Tự động thực hiện: 
**Gửi `/tx t {tiền}`** ➜ Nghỉ 1.5s ➜ **Gửi `/mua buatx`** ➜ Nghỉ 5s-7.5s.
* **Cấu trúc URL**: `https://{ten-app}.onrender.com/tx-t-{tiền}/{số_lần}`
* **Ví dụ**: `/tx-t-5000/20` ➜ Tự động đánh 5000 và mua bùa 20 lần liên tục.

### 2. Chế độ Chuỗi Lệnh Trộm (Trom-Farm) — *New*
Dành riêng cho `@deptraikhongsoai_bot`. Tự động thực hiện: 
**Gửi `/trom {ID}`** ➜ Nghỉ 1.5s ➜ **Gửi `/mua mientu`** ➜ Nghỉ 5s-7.5s.
* **Cấu trúc URL**: `https://{ten-app}.onrender.com/trom-{ID}/{số_lần}`
* **Ví dụ**: `/trom-7346983056/10` ➜ Thực hiện chuỗi trộm 10 lần cho mục tiêu ID được chỉ định.

### 3. Chế độ Lệnh Đơn (Universal)
Sử dụng cho bất kỳ Bot nào khác.
* **Cấu trúc URL**: `https://{ten-app}.onrender.com/{tên_bot}/{lệnh}/{số_lần}`
* **Ví dụ**: `/NgDanhThanhTrung_BOT/diem-danh/1` ➜ UserBot gửi `/diem danh #1`.

### 4. Lệnh Dừng Khẩn Cấp
* **URL**: `https://{ten-app}.onrender.com/stop` ➜ Dừng toàn bộ tiến trình đang chạy.

---

## 🛠 Hướng Dẫn Triển Khai

1. **GitHub**: Upload `main.py` và `requirements.txt` vào Repository (nên để Private).
2. **Render**: Kết nối GitHub, thiết lập Environment Variables: `API_ID`, `API_HASH`, `SESSION_STR`.
3. **Keep-Alive**: Dùng [cron-job.org](https://cron-job.org) gọi `/health` mỗi 5 phút.

---

## 🎁 Ủng Hộ Dự Án
1.  **Tặng 1 sao (Star) ⭐** cho Repository này.
2.  **Mời tác giả một ly cà phê ☕**: [https://ngdanhthanhtrung.github.io/Bank/](https://ngdanhthanhtrung.github.io/Bank/)

---

## 📜 Điều Khoản Sử Dụng
© 2026 **NgDanhThanhTrung**. Bảo lưu mọi quyền.
1. Tuyệt đối không xóa/chỉnh sửa thông tin bản quyền của tác giả.
2. Không sử dụng mã nguồn cho hành vi vi phạm chính sách của Telegram.
3. Tác giả không chịu trách nhiệm về bất kỳ rủi ro nào phát sinh.
