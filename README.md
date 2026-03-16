# 🤖 Telegram UserBot: Web-to-Telegram Automation — Edition 2026
### 🛠 Phát triển bởi: [NgDanhThanhTrung](https://github.com/NgDanhThanhTrung)

![Tác giả](https://img.shields.io/badge/Author-NgDanhThanhTrung-blue?style=for-the-badge&logo=telegram)
![Ngôn ngữ](https://img.shields.io/badge/Language-Python-yellow?style=for-the-badge&logo=python)
![Trạng thái](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)
![Giao diện](https://img.shields.io/badge/UI-Modern_Dashboard-indigo?style=for-the-badge)
![Stars](https://img.shields.io/github/stars/NgDanhThanhTrung/UserBot?style=for-the-badge&color=gold)

Dự án này là một giải pháp tự động hóa đột phá được nghiên cứu và phát triển độc quyền bởi **NgDanhThanhTrung**. Hệ thống biến tài khoản Telegram cá nhân thành một công cụ thực thi lệnh mạnh mẽ thông qua giao diện Web Dashboard quản trị, tối ưu cho các tác vụ lặp lại và theo dõi biến động tài khoản.

---

## 💡 Bản Quyền & Chất Xám Tác Giả
Đây là sản phẩm trí tuệ dựa trên kinh nghiệm tối ưu hóa quy trình tương tác API của **NgDanhThanhTrung**. 

> **⚡ Thông điệp từ tác giả:**
> "Mã nguồn này được chia sẻ với mục đích học tập và hỗ trợ cộng đồng. Tôi hy vọng bạn sẽ tôn trọng chất xám của tôi bằng cách giữ nguyên ghi chú bản quyền và không sử dụng cho các mục đích thương mại trái phép."

---

## 🌟 Tính Năng Nổi Bật (Cập nhật 2026)
* **Modern Dashboard UI**: Giao diện web quản trị chuyên nghiệp, hiển thị trạng thái hoạt động và thống kê thời gian thực.
* **Thief Monitor (Bảng SV)**: Tự động ghi nhận, đếm số lần và xếp hạng những kẻ đã trộm tiền bạn (🥇🥈🥉) ngay trên giao diện web.
* **Unstoppable Execution**: Cơ chế thực thi xuyên suốt, không bị cản trở bởi bất kỳ tin nhắn rác nào, đảm bảo vòng lặp hoàn thành tuyệt đối.
* **Sequence Automation**: Hỗ trợ chạy các chuỗi lệnh liên hoàn (Combo) như TX-Farm và Trom-Farm với thời gian nghỉ nội bộ 1.0s.
* **Hard-coded Safety Delay**: Khóa cứng khoảng cách nghỉ giữa các lượt lặp là **5.0 giây** để bảo vệ tài khoản khỏi cơ chế quét spam.
* **Kill Switch**: Lệnh `/stop` trên web giúp ngắt mọi tác vụ đang chạy ngay lập tức.

---

## 📖 Cách Sử Dụng (API Endpoints)

### 1. Quản Lý Hệ Thống & Thống Kê
* **Trang chủ**: `/` ➜ Xem trạng thái UserBot (Rảnh/Bận) và tổng số lần bị trộm.
* **Bảng SV**: `/sv` ➜ Hiển thị danh sách bảng xếp hạng những kẻ đã móc túi bạn.
* **Reset SV**: `/clearsv` ➜ Xóa sạch dữ liệu thống kê để bắt đầu phiên mới.
* **Dừng khẩn cấp**: `/stop` ➜ Ngắt mọi vòng lặp đang chạy.

### 2. Chế độ Chuỗi Lệnh Tài Xỉu (TX-Farm)
Tự động thực hiện: **Gửi `/tx t {tiền}`** ➜ Nghỉ 1s ➜ **Gửi `/mua buatx`** ➜ Nghỉ 5s ➜ Lặp lại.
* **Cấu trúc URL**: `https://{ten-app}.onrender.com/tx-t-{tiền}/{số_lần}`
* **Ví dụ**: `/tx-t-5000000/100` ➜ Đánh 5 triệu và mua bùa 100 lần liên tục.

### 3. Chế độ Chuỗi Lệnh Trộm (Trom-Farm)
Tự động thực hiện: **Gửi `/trom {ID}`** ➜ Nghỉ 1s ➜ **Gửi `/mua mientu`** ➜ Nghỉ 5s ➜ Lặp lại.
* **Cấu trúc URL**: `https://{ten-app}.onrender.com/trom-{ID}/{số_lần}`
* **Ví dụ**: `/trom-7346983056/50` ➜ Thực hiện chuỗi trộm 50 lần cho mục tiêu cụ thể.

### 4. Lệnh Đơn Universal
* **URL**: `https://{ten-app}.onrender.com/{tên_bot}/{lệnh}/{số_lần}` (Thay dấu cách bằng `-`).
* **Ví dụ**: `/deptraikhongsoai_bot/diem-danh/1` ➜ Gửi `/diem danh`.

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
