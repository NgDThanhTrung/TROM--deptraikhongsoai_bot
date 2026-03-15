# 🤖 Telegram UserBot: Web-to-Telegram Automation — Edition 2026
### 🛠 Phát triển bởi: [NgDanhThanhTrung](https://github.com/NgDanhThanhTrung)

![Tác giả](https://img.shields.io/badge/Author-NgDanhThanhTrung-blue?style=for-the-badge&logo=telegram)
![Ngôn ngữ](https://img.shields.io/badge/Language-Python-yellow?style=for-the-badge&logo=python)
![Trạng thái](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)
![Stars](https://img.shields.io/github/stars/NgDanhThanhTrung/UserBot?style=for-the-badge&color=gold)

Dự án này là một giải pháp tự động hóa đột phá được nghiên cứu và phát triển độc quyền bởi **NgDanhThanhTrung**. Hệ thống biến tài khoản Telegram cá nhân thành một công cụ thực thi lệnh mạnh mẽ thông qua yêu cầu HTTP (URL), tối ưu cho các tác vụ lặp lại và phản xạ tự động.

---

## 💡 Bản Quyền & Chất Xám Tác Giả
Đây là sản phẩm trí tuệ dựa trên kinh nghiệm tối ưu hóa quy trình tương tác API của **NgDanhThanhTrung**. 

> **⚡ Thông điệp từ tác giả:**
> "Mã nguồn này được chia sẻ với mục đích học tập và hỗ trợ cộng đồng. Tôi hy vọng bạn sẽ tôn trọng chất xám của tôi bằng cách giữ nguyên ghi chú bản quyền và không sử dụng cho các mục đích thương mại trái phép."

---

## 🌟 Tính Năng Nổi Bật (Cập nhật 2026)
* **HTTP Trigger 2.0**: Kích hoạt gửi tin nhắn tức thì bằng cách truy cập URL từ trình duyệt hoặc bất kỳ dịch vụ gọi API nào.
* **Anti-Thief Reflection (Mới)**: Tự động nhận diện tin nhắn bị móc túi từ Bot mục tiêu và ngay lập tức kích hoạt phản công kẻ trộm.
* **Sequence Automation**: Hỗ trợ chạy các chuỗi lệnh liên hoàn (Combo) như TX-Farm và Trom-Farm với thời gian nghỉ tối ưu.
* **Smart Anti-Spam**: Cơ chế nghỉ ngẫu nhiên linh hoạt (từ 1.5s đến 7.5s) để mô phỏng hành vi người dùng thật và bảo vệ tài khoản khỏi bị ban.
* **Multi-Target Control**: Điều khiển linh hoạt nhiều Bot mục tiêu hoặc khóa cứng mục tiêu cụ thể.
* **Kill Switch**: Lệnh `/stop` giúp ngắt mọi tác vụ đang chạy ngay lập tức.

---

## 📖 Cách Sử Dụng (API Endpoints)

### 1. Phản Công Tự Động (Anti-Thief) — *Hot*
Hệ thống luôn lắng nghe tin nhắn từ `@deptraikhongsoai_bot`. Nếu phát hiện nội dung thông báo bạn bị trộm tiền, UserBot sẽ:
1. **Dừng** mọi tác vụ hiện tại (TX hoặc Trom cũ).
2. **Tự động trích xuất** Username của kẻ trộm từ tin nhắn.
3. **Thực thi** chuỗi lệnh `/trom {kẻ_trộm}` + `/mua mientu` liên tục **100 lần**.

### 2. Chế độ Chuỗi Lệnh Tài Xỉu (TX-Farm)
Dành riêng cho `@deptraikhongsoai_bot`. Tự động thực hiện: 
**Gửi `/tx t {tiền}`** ➜ Nghỉ 1.5s ➜ **Gửi `/mua buatx`** ➜ Nghỉ 5s-7.5s.
* **Cấu trúc URL**: `https://{ten-app}.onrender.com/tx-t-{tiền}/{số_lần}`
* **Ví dụ**: `/tx-t-5000/20` ➜ Tự động đánh 5000 và mua bùa 20 lần liên tục.

### 3. Chế độ Chuỗi Lệnh Trộm (Trom-Farm)
Dành riêng cho `@deptraikhongsoai_bot`. Tự động thực hiện: 
**Gửi `/trom {ID}`** ➜ Nghỉ 1.5s ➜ **Gửi `/mua mientu`** ➜ Nghỉ 5s-7.5s.
* **Cấu trúc URL**: `https://{ten-app}.onrender.com/trom-{ID}/{số_lần}`
* **Ví dụ**: `/trom-7346983056/10` ➜ Thực hiện chuỗi trộm 10 lần cho mục tiêu cụ thể.

### 4. Lệnh Đơn Universal
* **URL**: `https://{ten-app}.onrender.com/{tên_bot}/{lệnh}/{số_lần}`
* **Ví dụ**: `/NgDanhThanhTrung_BOT/diem-danh/1` ➜ Gửi `/diem danh #1`.

---

## 🛠 Hướng Dẫn Triển Khai

1. **GitHub**: Upload `main.py` và `requirements.txt` vào Repository (nên để Private).
2. **Render**: Kết nối GitHub, thiết lập Environment Variables: `API_ID`, `API_HASH`, `SESSION_STR`.
3. **Keep-Alive**: Dùng [cron-job.org](https://cron-job.org) gọi vào địa chỉ `/health` mỗi 5 phút để Render không bị "ngủ".

---

## 🎁 Ủng Hộ & Liên Hệ
* **Ủng hộ tác giả**: [https://ngdanhthanhtrung.github.io/Bank/](https://ngdanhthanhtrung.github.io/Bank/)
* **Telegram Hỗ Trợ**: [@NgDanhThanhTrung](https://t.me/NgDanhThanhTrung)

---

## 📜 Điều Khoản Sử Dụng
© 2026 **NgDanhThanhTrung**. Bảo lưu mọi quyền.
1. Tuyệt đối không xóa/chỉnh sửa thông tin bản quyền của tác giả.
2. Không sử dụng mã nguồn cho hành vi vi phạm chính sách của Telegram.
3. Tác giả không chịu trách nhiệm về bất kỳ rủi ro nào phát sinh.
