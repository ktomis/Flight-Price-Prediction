# Ứng Dụng Dự Đoán Giá Vé Máy Bay

## Tổng Quan Dự Án
Dự án web dự đoán giá vé máy bay (Flight Price Prediction) được xây dựng bằng Flask, HTML, CSS và JavaScript. Hệ thống sử dụng mô hình học máy để đưa ra dự đoán giá vé dựa trên thông tin chuyến bay mà người dùng cung cấp.

## Cấu Trúc Dự Án
```
AirfarePrediction_MC/
│
├── colab/                     # Jupyter Notebooks để huấn luyện mô hình
│   ├── MU.ipynb               # Notebook huấn luyện mô hình
│   ├── mu.py                  # Tập lệnh Python cho mô hình
│   └── xgboost_model.pkl      # Mô hình học máy đã lưu
│
├── data/                      # Thư mục dữ liệu
│   ├── processed/             # Dữ liệu đã xử lý
│   └── raw/                   # Dữ liệu thô
│
├── myenv/                     # Môi trường ảo Python
│
├── static/                    # Tệp tĩnh (CSS, JS, hình ảnh)
│   ├── css/
│   │   └── style.css          # Tệp CSS chính
│   ├── images/                # Tài nguyên hình ảnh
│   └── js/
│       └── script.js          # Tệp JavaScript cho các tương tác phía client
│
├── templates/                 # Mẫu HTML
│   └── index.html             # Giao diện chính
│
├── app.py                     # Ứng dụng Flask chính
├── createKey.py               # Tập lệnh tạo API key
├── requestFlask.py            # Tập lệnh kiểm tra nhanh Model
└── requirements.txt           # Các gói phụ thuộc của dự án
```

## Cài Đặt và Cấu Hình
1. **Clone Repository:**
   ```bash
   git clone https://github.com/ktomis/Flight-Price-Prediction.git
   cd AirfarePrediction_MC
   ```
2. **Tạo Môi Trường Ảo:**
   ```bash
   # Trên macOS/Linux
   python -m venv myenv
   source myenv/bin/activate  
   
   # Trên Windows
   myenv\Scripts\activate
   ```
3. **Cài Đặt Các Thư Viện:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Chạy Ứng Dụng:**
   ```bash
   python app.py
   ```
   Ứng dụng sẽ chạy trên `http://localhost:5000`

## Tính Năng Chính
- **Biểu Mẫu Nhập Liệu:** Người dùng có thể nhập thông tin chuyến bay như điểm đi, điểm đến và ngày khởi hành.
- **Dự Đoán Động:** Dự đoán giá vé thời gian thực dựa trên dữ liệu đầu vào của người dùng.
- **Giao Diện Thân Thiện:** Frontend được thiết kế bằng CSS, mang lại trải nghiệm tốt cho người dùng.

## Công Nghệ Sử Dụng
- **Backend:** Flask (Python 3.9+)
- **Frontend:** HTML, CSS, JavaScript ES6
- **Học Máy:** Mô hình XGBoost (v1.5.0, lưu dưới dạng `xgboost_model.pkl`)
- **Môi Trường:** Môi trường ảo Python (venv)

## Cách Hoạt Động
1. Người dùng nhập thông tin chuyến bay vào biểu mẫu.
2. Sau khi gửi, Flask sẽ xử lý dữ liệu và áp dụng mô hình học máy.
3. Kết quả dự đoán giá vé sẽ được hiển thị cho người dùng.

## Các Nâng Cấp Trong Tương Lai
- Triển khai thêm các mô hình học máy để tăng độ chính xác.
- Thêm xác thực người dùng và quản lý phiên làm việc.
- Tích hợp API từ các hãng hàng không để cập nhật dữ liệu chuyến bay trực tiếp.
- Mở rộng giao diện để hiển thị biểu đồ và xu hướng giá.

## Đóng Góp
Hãy thoải mái fork dự án và gửi pull request cho bất kỳ cải tiến hoặc sửa lỗi nào.

## Liên Hệ
Mọi thắc mắc xin liên hệ qua Nhóm 10 hoặc các thành viên của nhóm [Mis - Duy - Chính - Toàn].
