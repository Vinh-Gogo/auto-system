# auto-system

`Kiếm trúc pdf sai một ít chính tả. Tôi sẽ thêm hướng dẫn cách cài đặt sau. xin cảm ơn.`

Kiến trúc hệ thống: automation-image-generator.pdf

Link image-generated: https://drive.google.com/drive/folders/1eik5Qr7e1S0CYwCpDFFHoV9VoCXH0Vk3?usp=sharing

Link sheet: https://docs.google.com/spreadsheets/d/1stgBPwj0oNmUseNZES0_-4Ua5r4HScLFA6DdmVVqLog/edit?usp=sharing

# Prompt Engineer / Automation Engineer tại Athena.
## Bài test 1: Tự động hóa (Automation Task)
Mục tiêu là thiết kế và xây dựng một quy trình tự động hóa hoàn chỉnh.
Đầu vào: Dữ liệu từ một file Google Sheets, chứa các trường như mô tả, URL tài sản mẫu, định dạng đầu ra mong muốn (PNG, JPG, GIF, MP3), và chỉ định mô hình AI (OpenAI hoặc Claude).
## Quy trình:
1. Tự động tạo ra các sản phẩm đầu ra dựa trên thông tin đầu vào.
2. Lưu trữ các sản phẩm này một cách có hệ thống vào Google Drive.
3. Tự động gửi email và thông báo qua Slack khi một tác vụ hoàn thành (thành công hoặc thất bại).
4. Ghi lại chi tiết về trạng thái (thành công/thất bại) của mỗi tác vụ vào một cơ sở dữ liệu riêng.
5. Tổng hợp các ghi chép hàng ngày thành một báo cáo toàn diện, tạo biểu đồ phân tích tỷ lệ thành công và lỗi, sau đó gửi email bản tóm tắt này cho quản trị viên (admin).
6. Công cụ: Bạn có thể sử dụng Python hoặc các nền tảng low-code như n8n, Zapier, hoặc Make.com.
## Bài test 2: Kỹ thuật Prompt (AI Prompt Engineering)
Mục tiêu là thể hiện khả năng tạo ra các câu lệnh (prompt) hiệu quả để sinh ra tài sản game (game assets) chất lượng cao.
## Nhiệm vụ:
Thiết kế các prompt chính xác và hiệu quả để tạo ra tài sản game dựa trên các tài sản tham chiếu được cung cấp.
Kiểm tra và xác thực hiệu quả của các prompt đã tạo bằng cách sử dụng các nền tảng như layer.ai hoặc các công cụ tương tự, và so sánh kết quả với tài sản game mẫu.
* Ghi lại tài liệu cho mọi giai đoạn của quá trình, bao gồm lý do lựa chọn prompt, phương pháp kiểm thử và các điều chỉnh đã thực hiện.