# 📚 HƯỚNG DẪN CHI TIẾT SMOKE TESTING TỪ A ĐẾN Z

## 📋 MỤC LỤC

- [1. GIỚI THIỆU TỔNG QUAN](#1-giới-thiệu-tổng-quan)
- [2. CÀI ĐẶT MÔI TRƯỜNG](#2-cài-đặt-môi-trường)
- [3. THIẾT LẬP REPOSITORY](#3-thiết-lập-repository)
- [4. CẤU HÌNH SMOKE TEST SUITE](#4-cấu-hình-smoke-test-suite)
- [5. CHẠY SMOKE TESTS](#5-chạy-smoke-tests)
- [6. PHÂN TÍCH KẾT QUẢ](#6-phân-tích-kết-quả)
- [7. TROUBLESHOOTING](#7-troubleshooting)
- [8. CUSTOMIZATION](#8-customization)
- [9. BEST PRACTICES](#9-best-practices)
- [10. FAQ](#10-faq)

---

## 1. GIỚI THIỆU TỔNG QUAN

### 1.1. Smoke Testing là gì?

**Smoke Testing** (còn gọi là Build Verification Testing) là một loại kiểm thử phần mềm được thực hiện để đảm bảo rằng các chức năng quan trọng nhất của ứng dụng hoạt động bình thường sau khi có những thay đổi mới.

### 1.2. Tại sao cần Smoke Testing?

- ⚡ **Phát hiện sớm**: Tìm ra lỗi nghiêm trọng ngay từ đầu
- 💰 **Tiết kiệm chi phí**: Tránh lãng phí thời gian test những build bị lỗi
- 🚀 **Tăng tốc**: Đảm bảo build ổn định trước khi test chi tiết
- 🔒 **Tin cậy**: Xác nhận các chức năng cốt lõi vẫn hoạt động

### 1.3. Smoke Test Suite này bao gồm gì?

```
📦 Smoke Test Suite
├── 🔧 20 Test Cases tự động
├── 📊 Multi-format Reporting (HTML, JSON, CSV)
├── 🌐 API + UI Testing
├── ⚙️ Configurable Settings
└── 🔄 CI/CD Integration Ready
```

---

## 2. CÀI ĐẶT MÔI TRƯỜNG

### 2.1. Yêu cầu hệ thống

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| **Python** | 3.7+ | 3.9+ |
| **RAM** | 2GB | 4GB+ |
| **Storage** | 500MB | 1GB+ |
| **Browser** | Chrome 90+ | Chrome Latest |

### 2.2. Cài đặt Python

#### Windows:
```powershell
# Tải Python từ python.org
# Hoặc sử dụng chocolatey
choco install python

# Kiểm tra cài đặt
python --version
pip --version
```

#### Kiểm tra Python PATH:
```powershell
where python
where pip
```

### 2.3. Cài đặt Git (nếu chưa có)

```powershell
# Sử dụng chocolatey
choco install git

# Hoặc tải từ git-scm.com
# Kiểm tra
git --version
```

---

## 3. THIẾT LẬP REPOSITORY

### 3.1. Clone Microblog Repository

```powershell
# Di chuyển đến thư mục làm việc
cd d:\Study\KiemThuPhanMem\btn2

# Clone repository Microblog
git clone https://github.com/miguelgrinberg/microblog.git
cd microblog
```

### 3.2. Cài đặt Microblog Application

```powershell
# Tạo virtual environment
python -m venv venv

# Activate virtual environment
# Windows PowerShell:
.\venv\Scripts\Activate.ps1

# Cài đặt dependencies
pip install -r requirements.txt

# Thiết lập environment variables
$env:FLASK_APP = "microblog.py"
$env:FLASK_ENV = "development"

# Khởi tạo database
flask db upgrade

# Chạy application (terminal riêng)
flask run
```

### 3.3. Xác minh Microblog đang chạy

```powershell
# Test bằng curl hoặc browser
curl http://localhost:5000

# Hoặc mở browser: http://localhost:5000
```

---

## 4. CẤU HÌNH SMOKE TEST SUITE

### 4.1. Cài đặt Smoke Test Dependencies

```powershell
# Di chuyển đến smoke test suite
cd d:\Study\KiemThuPhanMem\btn2\smoke_test_suite

# Cài đặt requirements
pip install -r requirements.txt

# Kiểm tra cài đặt thành công
python -c "import pytest, requests, selenium; print('✅ All dependencies installed')"
```

### 4.2. Cài đặt Chrome WebDriver

#### Tự động (Recommended):
```powershell
# WebDriver sẽ được tự động download bởi selenium-manager
# Không cần cài đặt thêm gì
```

#### Thủ công (nếu cần):
```powershell
# Tải ChromeDriver từ https://chromedriver.chromium.org/
# Giải nén và thêm vào PATH
# Hoặc đặt trong thư mục smoke_test_suite/drivers/
```

### 4.3. Cấu hình Test Settings

#### Mở file `config/test_config.py`:

```python
class SmokeTestConfig:
    # URL của Microblog application
    BASE_URL = "http://localhost:5000"
    
    # Timeout settings (giây)
    DEFAULT_TIMEOUT = 30
    PAGE_LOAD_TIMEOUT = 30
    ELEMENT_WAIT_TIMEOUT = 10
    
    # Test user credentials
    TEST_USER = {
        "username": "smoketest_user",
        "email": "smoketest@example.com", 
        "password": "SmokeTest123!"
    }
    
    # Browser settings cho UI tests
    BROWSER_CONFIG = {
        "headless": False,  # Set True cho CI/CD
        "window_size": (1920, 1080),
        "implicit_wait": 10
    }
```

### 4.4. Tùy chỉnh Test Data

#### Mở file `config/test_data.json` và review:

```json
{
    "test_scenarios": [
        {
            "name": "Basic Application Health",
            "description": "Verify application is running and responsive",
            "priority": "critical",
            "tests": [
                "test_application_startup",
                "test_home_page_access"
            ]
        }
    ],
    "test_data": {
        "users": [
            {
                "username": "testuser1",
                "email": "testuser1@example.com",
                "password": "TestPass123!"
            }
        ]
    }
}
```

---

## 5. CHẠY SMOKE TESTS

### 5.1. Chạy Basic Smoke Tests

```powershell
# Chạy tất cả smoke tests
python run_smoke_tests.py

# Chạy với verbose output
python run_smoke_tests.py --verbose

# Chạy chỉ basic tests (bỏ qua UI tests)
python run_smoke_tests.py --skip-ui
```

### 5.2. Chạy từng loại test riêng biệt

```powershell
# Chỉ Basic Smoke Tests
python -m pytest tests/test_smoke.py -v

# Chỉ API Tests  
python -m pytest tests/test_api_smoke.py -v

# Chỉ UI Tests
python -m pytest tests/test_ui_smoke.py -v
```

### 5.3. Chạy với options khác nhau

```powershell
# Custom base URL
python run_smoke_tests.py --base-url http://staging.myapp.com

# Custom timeout
python run_smoke_tests.py --timeout 60

# Headless mode cho UI tests
python run_smoke_tests.py --headless

# Tạo detailed report
python run_smoke_tests.py --detailed-report
```

### 5.4. Sample Output khi chạy thành công

```
🔍 Microblog Smoke Test Suite
Starting tests at: 2025-08-24 15:30:25
Target URL: http://localhost:5000
Browser: Chrome (Headless: False)
====================================================================

📋 Running Basic Smoke Tests...
  ✅ test_application_startup ........................... PASSED
  ✅ test_home_page_access ............................ PASSED  
  ✅ test_registration_page_access .................... PASSED
  ✅ test_user_registration ........................... PASSED
  ✅ test_login_page_access ........................... PASSED
  ✅ test_user_login .................................. PASSED
  ✅ test_explore_page ................................ PASSED
  ✅ test_critical_endpoints .......................... PASSED
  ✅ test_post_creation ............................... PASSED
  ✅ test_api_users_endpoint .......................... PASSED

🌐 Running API Smoke Tests...
  ✅ test_api_root_accessibility ...................... PASSED
  ✅ test_api_users_endpoint .......................... PASSED
  ✅ test_api_tokens_endpoint ......................... PASSED
  ✅ test_api_error_handling .......................... PASSED
  ✅ test_api_response_headers ........................ PASSED

🖥️  Running UI Smoke Tests...
  ✅ test_home_page_ui_elements ....................... PASSED
  ✅ test_login_page_ui_elements ...................... PASSED  
  ✅ test_registration_page_ui ........................ PASSED
  ✅ test_page_load_performance ....................... PASSED
  ✅ test_responsive_design_basic ..................... PASSED

📊 Generating Reports...
Reports generated successfully:
  📄 HTML Report: reports/smoke_report_20250824_153045.html
  📄 JSON Report: reports/smoke_results_20250824_153045.json
  📄 CSV Report: reports/smoke_results_20250824_153045.csv

====================================================================
🏁 SMOKE TEST SUMMARY
====================================================================
🕐 Start Time: 15:30:25
🏁 End Time: 15:30:47  
⏱️  Total Duration: 22.45 seconds
📊 Total Tests: 20
✅ Passed: 20
❌ Failed: 0
📈 Success Rate: 100.0%

🎉 ALL SMOKE TESTS PASSED - Application is healthy and ready for further testing!
====================================================================
```

---

## 6. PHÂN TÍCH KẾT QUẢ

### 6.1. Hiểu Smoke Test Output

#### Status Indicators:
- ✅ **PASSED**: Test thành công
- ❌ **FAILED**: Test thất bại
- ⚠️ **SKIPPED**: Test bị bỏ qua
- 🔄 **RETRY**: Test đang retry

#### Test Categories:
- **📋 Basic**: Các test cơ bản về khả năng hoạt động
- **🌐 API**: Test các API endpoints
- **🖥️ UI**: Test giao diện người dùng

### 6.2. Đọc HTML Report

Mở file HTML report trong browser để xem:

```powershell
# Mở report trong browser
start reports/smoke_report_20250824_153045.html
```

**HTML Report bao gồm:**
- 📊 **Dashboard**: Tổng quan metrics
- 📈 **Charts**: Biểu đồ success rate
- 📋 **Test Details**: Chi tiết từng test case
- ⏱️ **Timeline**: Thời gian thực hiện
- 🔍 **Filtering**: Lọc theo status/category

### 6.3. Phân tích JSON Report

```powershell
# Xem JSON report
cat reports/smoke_results_20250824_153045.json | jq .
```

**JSON Report Structure:**
```json
{
    "summary": {
        "total_tests": 20,
        "passed": 20,
        "failed": 0,
        "success_rate": 100.0,
        "total_duration": 22.45
    },
    "test_results": [
        {
            "test_name": "test_application_startup",
            "category": "basic",
            "status": "passed",
            "duration": 1.23,
            "message": "Application startup successful"
        }
    ]
}
```

### 6.4. Sử dụng CSV Report

```powershell
# Import vào Excel hoặc Google Sheets
# Hoặc phân tích bằng Python pandas
python -c "
import pandas as pd
df = pd.read_csv('reports/smoke_results_20250824_153045.csv')
print(df.groupby('category')['status'].value_counts())
"
```

---

## 7. TROUBLESHOOTING

### 7.1. Lỗi thường gặp và cách khắc phục

#### ❌ **Connection Error**
```
Error: requests.exceptions.ConnectionError: HTTPConnectionPool
```

**Nguyên nhân**: Microblog app không chạy
**Khắc phục**:
```powershell
# Kiểm tra app có chạy không
curl http://localhost:5000

# Nếu không, start lại Microblog
cd microblog
flask run
```

#### ❌ **WebDriver Error**
```
Error: selenium.common.exceptions.WebDriverException
```

**Nguyên nhân**: Chrome WebDriver không tìm thấy
**Khắc phục**:
```powershell
# Cài đặt lại selenium
pip install --upgrade selenium

# Hoặc chạy without UI tests
python run_smoke_tests.py --skip-ui
```

#### ❌ **Import Error**
```
Error: ModuleNotFoundError: No module named 'pytest'
```

**Khắc phục**:
```powershell
# Cài đặt lại dependencies
pip install -r requirements.txt

# Kiểm tra Python path
python -c "import sys; print(sys.path)"
```

#### ❌ **Permission Error**
```
Error: PermissionError: [Errno 13] Permission denied
```

**Khắc phục**:
```powershell
# Chạy PowerShell as Administrator
# Hoặc thay đổi execution policy
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 7.2. Debug Mode

```powershell
# Chạy với debug verbose
python run_smoke_tests.py --verbose --debug

# Tạm dừng tại lỗi đầu tiên
python -m pytest tests/test_smoke.py -v -x

# Chạy một test cụ thể
python -m pytest tests/test_smoke.py::TestBasicSmoke::test_application_startup -v
```

### 7.3. Kiểm tra Log Files

```powershell
# Xem logs từ test runs
cat logs/smoke_test_debug.log

# Xem logs của Microblog app
# (Check terminal running flask run)
```

---

## 8. CUSTOMIZATION

### 8.1. Thêm Test Cases mới

#### Tạo test case trong `tests/test_smoke.py`:

```python
def test_custom_feature(self):
    """Test custom feature functionality"""
    # Setup
    response = self.session.get(f"{self.base_url}/custom-feature")
    
    # Assert
    assert response.status_code == 200, f"Custom feature not accessible: {response.status_code}"
    assert "Expected Content" in response.text, "Custom feature content missing"
    
    # Log result
    self.results.append({
        "test_name": "test_custom_feature",
        "status": "passed",
        "message": "Custom feature working correctly"
    })
```

### 8.2. Thêm Test Scenarios mới

#### Sửa `config/test_data.json`:

```json
{
    "test_scenarios": [
        {
            "name": "Custom Feature Testing",
            "description": "Test custom application features",
            "priority": "medium",
            "tests": [
                "test_custom_feature",
                "test_custom_api"
            ]
        }
    ]
}
```

### 8.3. Customize Report Templates

#### Sửa `utils/report_generator.py`:

```python
# Thêm custom CSS/styling
CUSTOM_CSS = """
<style>
.custom-style {
    background-color: #f0f8ff;
    border: 2px solid #4169e1;
}
</style>
"""

# Thêm custom sections
def generate_custom_section(self):
    return f"""
    <div class="custom-section">
        <h3>Custom Analysis</h3>
        <p>Your custom content here</p>
    </div>
    """
```

### 8.4. Environment-specific Configs

#### Tạo config cho staging:

```python
# config/staging_config.py
class StagingConfig(SmokeTestConfig):
    BASE_URL = "https://staging.myapp.com"
    DEFAULT_TIMEOUT = 60
    BROWSER_CONFIG = {
        "headless": True,  # Headless cho staging
        "window_size": (1920, 1080)
    }
```

```powershell
# Chạy với staging config
python run_smoke_tests.py --config staging
```

---

## 9. BEST PRACTICES

### 9.1. Test Organization

- ✅ **Group by functionality**: Authentication, Core Features, API
- ✅ **Prioritize critical paths**: Test most important features first
- ✅ **Keep tests independent**: Mỗi test có thể chạy độc lập
- ✅ **Use descriptive names**: `test_user_can_login_with_valid_credentials`

### 9.2. Test Data Management

- ✅ **Use unique test data**: Tránh conflicts
- ✅ **Clean up after tests**: Xóa test data sau khi chạy
- ✅ **External test data**: Sử dụng files JSON/CSV
- ✅ **Environment variables**: Cho sensitive data

### 9.3. Reporting

- ✅ **Multi-format reports**: HTML cho humans, JSON cho tools
- ✅ **Include screenshots**: Cho UI test failures
- ✅ **Timestamp everything**: Để tracking
- ✅ **Version information**: App version, test suite version

### 9.4. CI/CD Integration

```yaml
# .github/workflows/smoke-tests.yml
name: Smoke Tests
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  smoke-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      
      - name: Install dependencies
        run: |
          cd smoke_test_suite
          pip install -r requirements.txt
      
      - name: Run Smoke Tests
        run: |
          cd smoke_test_suite
          python run_smoke_tests.py --skip-ui --headless
      
      - name: Upload Reports
        uses: actions/upload-artifact@v3
        with:
          name: smoke-test-reports
          path: smoke_test_suite/reports/
```

---

## 10. FAQ

### ❓ **Smoke tests khác gì với Unit tests?**

| Aspect | Smoke Tests | Unit Tests |
|--------|-------------|------------|
| **Scope** | End-to-end critical paths | Individual functions/methods |
| **Frequency** | Sau mỗi build/deploy | Trong development |
| **Speed** | Nhanh (< 30 phút) | Rất nhanh (< 5 phút) |
| **Purpose** | Build verification | Code quality |

### ❓ **Khi nào nên chạy smoke tests?**

- ✅ Sau mỗi build mới
- ✅ Trước khi chạy regression tests
- ✅ Sau khi deploy lên staging/production
- ✅ Trước khi release
- ❌ Không nên thay thế full test suite

### ❓ **Smoke tests nên cover bao nhiêu functionality?**

- 🎯 **10-30%** của total test cases
- 🎯 **80-90%** critical user paths
- 🎯 **100%** core business functions
- 🎯 **Key integration points**

### ❓ **Làm sao để speed up smoke tests?**

```powershell
# Parallel execution
python -m pytest tests/ -n 4  # 4 workers

# Skip slow tests
python run_smoke_tests.py --skip-ui --skip-slow

# Use test markers
python -m pytest -m "not slow"
```

### ❓ **Smoke tests fail thì làm gì?**

1. **🛑 Stop**: Dừng further testing
2. **🔍 Investigate**: Check logs, reports
3. **🏥 Fix**: Fix critical issues
4. **🔄 Retry**: Re-run smoke tests
5. **✅ Proceed**: Continue with full testing

### ❓ **Có thể run smoke tests trên mobile không?**

```python
# Thêm mobile testing với Appium
from appium import webdriver

def test_mobile_app_startup(self):
    caps = {
        'platformName': 'Android',
        'deviceName': 'emulator',
        'app': '/path/to/app.apk'
    }
    driver = webdriver.Remote('http://localhost:4723/wd/hub', caps)
    # Mobile smoke tests here
```

### ❓ **Integrate với Slack/Teams notifications?**

```python
# utils/notifications.py
import requests

def send_slack_notification(results):
    webhook_url = "YOUR_SLACK_WEBHOOK"
    message = {
        "text": f"🔥 Smoke Tests: {results['success_rate']}% passed"
    }
    requests.post(webhook_url, json=message)
```

---

## 🎯 KẾT LUẬN

Bây giờ bạn đã có đầy đủ kiến thức để:

- ✅ **Setup** smoke test environment từ đầu
- ✅ **Run** smoke tests với nhiều options khác nhau  
- ✅ **Analyze** kết quả và reports
- ✅ **Troubleshoot** các vấn đề thường gặp
- ✅ **Customize** cho project riêng
- ✅ **Integrate** với CI/CD pipeline

### 📞 Liên hệ & Support

Nếu có vấn đề:
1. Check [Troubleshooting Section](#7-troubleshooting)
2. Review logs trong `logs/` folder
3. Tạo issue với detailed error message
4. Include environment info (OS, Python version, etc.)

### 🚀 Next Steps

1. **Practice**: Chạy smoke tests nhiều lần
2. **Extend**: Thêm test cases cho project của bạn
3. **Automate**: Setup CI/CD integration  
4. **Monitor**: Track smoke test metrics theo thời gian

**Happy Testing! 🎉**

---

*Guide tạo bởi: Smoke Test Suite v1.0*  
*Last updated: August 24, 2025*
