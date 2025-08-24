# ⚡ QUICK START GUIDE - SMOKE TESTING

> **Hướng dẫn nhanh 5 phút để bắt đầu với Smoke Testing**

## 🚀 SETUP NHANH (5 PHÚT)

### Bước 1: Chuẩn bị môi trường
```powershell
# Kiểm tra Python
python --version  # Cần Python 3.7+

# Clone và setup Microblog
git clone https://github.com/miguelgrinberg/microblog.git
cd microblog
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Setup environment
$env:FLASK_APP = "microblog.py"
flask db upgrade
flask run  # Chạy trong terminal riêng
```

### Bước 2: Setup Smoke Test Suite
```powershell
# Di chuyển đến smoke test suite
cd ..\smoke_test_suite

# Cài đặt dependencies
pip install -r requirements.txt

# Test cài đặt
python -c "import pytest, requests; print('✅ Ready to test!')"
```

### Bước 3: Chạy Smoke Tests
```powershell
# Chạy tất cả tests
python run_smoke_tests.py

# Hoặc chỉ basic tests (nhanh hơn)
python run_smoke_tests.py --skip-ui
```

---

## 📊 KẾT QUẢ MONG ĐỢI

```
🔍 Microblog Smoke Test Suite
✅ All 20 tests passed (22.45 seconds)
📄 Reports: reports/smoke_report_*.html
🎉 Application is healthy!
```

---

## 🆘 NẾU CÓ LỖI

| Lỗi | Khắc phục nhanh |
|-----|----------------|
| Connection Error | `flask run` trong microblog/ |
| WebDriver Error | `python run_smoke_tests.py --skip-ui` |
| Import Error | `pip install -r requirements.txt` |
| Permission Error | Run PowerShell as Administrator |

---

## 📁 CẤU TRÚC THƯ MỤC

```
btn2/
├── microblog/                    # Microblog app
│   └── (flask run ở đây)
├── smoke_test_suite/             # Test suite
│   ├── run_smoke_tests.py        # ← Chạy file này
│   ├── config/                   # Cấu hình
│   ├── tests/                    # Test cases
│   └── reports/                  # Kết quả
└── smoke_testing_report.md       # Báo cáo lý thuyết
```

---

## 🎯 COMMANDS QUAN TRỌNG

```powershell
# Chạy tất cả
python run_smoke_tests.py

# Chỉ API tests (nhanh)
python run_smoke_tests.py --skip-ui

# Debug mode
python run_smoke_tests.py --verbose

# Custom URL
python run_smoke_tests.py --base-url http://localhost:8000
```

---

## 📖 ĐỌC THÊM

- **Chi tiết**: `COMPLETE_GUIDE.md` - Hướng dẫn đầy đủ A-Z
- **Lý thuyết**: `../smoke_testing_report.md` - Báo cáo 30+ trang
- **Cấu hình**: `config/test_config.py` - Settings
- **Troubleshooting**: `COMPLETE_GUIDE.md#troubleshooting`

---

**Thời gian đọc: 2 phút | Setup: 5 phút | Chạy test: 30 giây** ⚡
