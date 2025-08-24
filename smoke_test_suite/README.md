# Microblog Smoke Test Suite

Công cụ kiểm thử tự động được phát triển để thực hiện Smoke Testing cho ứng dụng Microblog.

## 📋 Mô tả

Smoke Test Suite này được thiết kế để kiểm tra các chức năng cơ bản và quan trọng nhất của ứng dụng Microblog, đảm bảo rằng ứng dụng hoạt động ổn định trước khi tiến hành các bài kiểm thử chi tiết hơn.

## 📖 Hướng dẫn Sử dụng

### 📚 Các tài liệu hướng dẫn:

| Tài liệu | Mô tả | Thời gian đọc | Khi nào sử dụng |
|----------|-------|---------------|-----------------|
| **⚡ QUICK_START.md** | Hướng dẫn nhanh để bắt đầu | 5 phút | Muốn chạy test ngay lập tức |
| **📖 COMPLETE_GUIDE.md** | Hướng dẫn chi tiết từ A đến Z | 30 phút | Cần hiểu sâu + troubleshooting |
| **🎯 CHEAT_SHEET.md** | Commands và tricks thường dùng | 2 phút | Cần reference nhanh |
| **🚨 TROUBLESHOOTING.md** | Tất cả lỗi và cách khắc phục | 15 phút | Gặp lỗi cần fix |
| **📋 ../smoke_testing_report.md** | Báo cáo lý thuyết đầy đủ | 1-2 giờ | Học lý thuyết smoke testing |

### 🎯 Lựa chọn theo nhu cầu:
- **🚀 Mới bắt đầu?** → Đọc `QUICK_START.md`
- **❌ Gặp lỗi?** → Xem `TROUBLESHOOTING.md`
- **� Cần commands?** → Dùng `CHEAT_SHEET.md`
- **📚 Hiểu sâu?** → Đọc `COMPLETE_GUIDE.md`
- **📖 Lý thuyết?** → Xem `smoke_testing_report.md`

## 🎯 Mục đích

- **Kiểm tra sức khỏe ứng dụng**: Xác minh ứng dụng khởi động và phản hồi bình thường
- **Validation các chức năng cốt lõi**: Đăng ký, đăng nhập, tạo bài viết
- **API Testing**: Kiểm tra các endpoint API quan trọng
- **UI Testing**: Kiểm tra giao diện người dùng cơ bản
- **Performance**: Đánh giá thời gian phản hồi cơ bản

## 🏗️ Cấu trúc dự án

```
smoke_test_suite/
├── config/
│   ├── test_config.py       # Cấu hình kiểm thử
│   └── test_data.json       # Dữ liệu kiểm thử
├── tests/
│   ├── test_smoke.py        # Kiểm thử cơ bản
│   ├── test_api_smoke.py    # Kiểm thử API
│   └── test_ui_smoke.py     # Kiểm thử giao diện
├── utils/
│   ├── test_helpers.py      # Hàm hỗ trợ
│   └── report_generator.py  # Tạo báo cáo
├── requirements.txt         # Phụ thuộc
├── run_smoke_tests.py       # Chạy kiểm thử
└── README.md               # Tài liệu này
```

## 🚀 Cài đặt và Sử dụng

### 1. Yêu cầu hệ thống

- Python 3.8+
- Chrome browser (cho UI tests)
- Ứng dụng Microblog đang chạy tại `http://localhost:5000`

### 2. Cài đặt dependencies

```bash
cd smoke_test_suite
pip install -r requirements.txt
```

### 3. Cấu hình

Chỉnh sửa `config/test_config.py` nếu cần:

```python
class SmokeTestConfig:
    BASE_URL = "http://localhost:5000"  # URL ứng dụng
    TIMEOUT = 30                        # Timeout (giây)
    MAX_RESPONSE_TIME = 5.0            # Thời gian phản hồi tối đa
```

### 4. Chạy kiểm thử

#### Chạy tất cả tests:
```bash
python run_smoke_tests.py
```

#### Chạy với tùy chọn:
```bash
# Skip UI tests (nếu không có Chrome)
python run_smoke_tests.py --skip-ui

# Verbose output
python run_smoke_tests.py --verbose

# Custom URL
python run_smoke_tests.py --base-url http://localhost:8000

# Custom timeout
python run_smoke_tests.py --timeout 60
```

#### Chạy từng loại test riêng biệt:
```bash
# Chỉ basic smoke tests
python tests/test_smoke.py

# Chỉ API tests
python tests/test_api_smoke.py

# Chỉ UI tests  
python tests/test_ui_smoke.py
```

## 📊 Báo cáo

Sau khi chạy xong, công cụ sẽ tạo ra các báo cáo trong thư mục `reports/`:

- **HTML Report**: Báo cáo chi tiết với giao diện đẹp
- **JSON Report**: Dữ liệu kết quả để xử lý tự động
- **CSV Report**: Dữ liệu dạng bảng để phân tích

## 🧪 Các Test Cases

### Basic Smoke Tests (test_smoke.py)

1. **Application Startup**: Kiểm tra ứng dụng khởi động
2. **Home Page Access**: Truy cập trang chủ
3. **Registration Page**: Kiểm tra trang đăng ký
4. **User Registration**: Đăng ký user mới
5. **Login Page**: Kiểm tra trang đăng nhập
6. **User Login**: Đăng nhập user
7. **Explore Page**: Truy cập trang khám phá
8. **Critical Endpoints**: Kiểm tra các endpoint quan trọng
9. **Post Creation**: Tạo bài viết mới
10. **API Users Endpoint**: Kiểm tra API người dùng

### API Smoke Tests (test_api_smoke.py)

1. **API Root Accessibility**: Truy cập API root
2. **API Users Endpoint**: Endpoint danh sách người dùng
3. **API Tokens Endpoint**: Endpoint xác thực
4. **API Error Handling**: Xử lý lỗi API
5. **API Response Headers**: Kiểm tra headers

### UI Smoke Tests (test_ui_smoke.py)

1. **Home Page UI Elements**: Elements trang chủ
2. **Login Page UI Elements**: Elements trang đăng nhập
3. **Registration Page UI**: Elements trang đăng ký
4. **Page Load Performance**: Hiệu suất tải trang
5. **Responsive Design**: Thiết kế responsive

## ⚙️ Cấu hình nâng cao

### Environment Variables

Tạo file `.env` để override config:

```bash
SMOKE_TEST_BASE_URL=http://localhost:5000
SMOKE_TEST_TIMEOUT=30
SMOKE_TEST_HEADLESS=true
SMOKE_TEST_MIN_SUCCESS_RATE=0.8
```

### Custom Test Data

Chỉnh sửa `config/test_data.json` để thay đổi dữ liệu test.

## 🔧 Troubleshooting

### Chrome WebDriver Issues
```bash
# Cài đặt Chrome WebDriver
pip install webdriver-manager

# Hoặc tải thủ công từ:
# https://chromedriver.chromium.org/
```

### Connection Issues
```bash
# Kiểm tra ứng dụng đang chạy
curl http://localhost:5000

# Kiểm tra firewall/port
netstat -an | grep 5000
```

### Permission Issues
```bash
# Linux/Mac
chmod +x run_smoke_tests.py

# Windows - chạy với quyền Administrator nếu cần
```

## 📈 Tích hợp CI/CD

### GitHub Actions

Tạo `.github/workflows/smoke-tests.yml`:

```yaml
name: Smoke Tests
on: [push, pull_request]

jobs:
  smoke-tests:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v3
      with:
        python-version: '3.9'
    - name: Install dependencies
      run: |
        pip install -r smoke_test_suite/requirements.txt
    - name: Run smoke tests
      run: |
        cd smoke_test_suite
        python run_smoke_tests.py --skip-ui
```

## 🤝 Đóng góp

1. Fork repository
2. Tạo feature branch
3. Thêm tests cho tính năng mới
4. Commit với message rõ ràng
5. Tạo Pull Request

## 📄 License

Dự án này được phát triển cho mục đích giáo dục trong môn Kiểm thử Phần mềm.

## 🔗 Tham khảo

- [Microblog Repository](https://github.com/miguelgrinberg/microblog)
- [Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)
- [Selenium Documentation](https://selenium-python.readthedocs.io/)
- [Requests Documentation](https://requests.readthedocs.io/)

---

**Phát triển bởi**: Nhóm Kiểm thử Phần mềm  
**Ngày cập nhật**: 24/08/2025
