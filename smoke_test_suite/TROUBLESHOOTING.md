# 🚨 TROUBLESHOOTING GUIDE - SMOKE TESTING

> **Tất cả lỗi thường gặp và cách khắc phục chi tiết**

## 📋 MỤC LỤC

- [1. Connection & Network Errors](#1-connection--network-errors)
- [2. WebDriver & Browser Errors](#2-webdriver--browser-errors)
- [3. Python & Dependencies Errors](#3-python--dependencies-errors)
- [4. Application Errors](#4-application-errors)
- [5. Permission & Security Errors](#5-permission--security-errors)
- [6. Performance Issues](#6-performance-issues)
- [7. Reporting Errors](#7-reporting-errors)

---

## 1. CONNECTION & NETWORK ERRORS

### ❌ `ConnectionError: HTTPConnectionPool(...): Max retries exceeded`

**Nguyên nhân**: Ứng dụng Microblog không chạy

**Khắc phục**:
```powershell
# Kiểm tra app có chạy không
curl http://localhost:5000
# Nếu lỗi, start Microblog:
cd microblog
.\venv\Scripts\Activate.ps1
$env:FLASK_APP = "microblog.py"
flask run
```

**Verify**: Mở browser -> `http://localhost:5000`

### ❌ `Connection refused on port 5000`

**Nguyên nhân**: Port 5000 bị block hoặc đã sử dụng

**Khắc phục**:
```powershell
# Check port usage
netstat -an | findstr 5000

# Kill process nếu cần
taskkill /F /PID <process_id>

# Hoặc dùng port khác
flask run --port 8000
python run_smoke_tests.py --base-url http://localhost:8000
```

### ❌ `ReadTimeout: HTTPSConnectionPool(...): Read timed out`

**Nguyên nhân**: Network chậm hoặc server quá tải

**Khắc phục**:
```powershell
# Tăng timeout
python run_smoke_tests.py --timeout 120

# Hoặc sửa config
# config/test_config.py
DEFAULT_TIMEOUT = 60
```

### ❌ `SSL Certificate verification failed`

**Nguyên nhân**: HTTPS certificate không hợp lệ

**Khắc phục**:
```powershell
# Disable SSL verification (chỉ cho testing)
# utils/test_helpers.py
session.verify = False
```

---

## 2. WEBDRIVER & BROWSER ERRORS

### ❌ `WebDriverException: 'chromedriver' executable needs to be in PATH`

**Nguyên nhân**: ChromeDriver không cài đặt hoặc không trong PATH

**Khắc phục**:
```powershell
# Method 1: Auto-download (Selenium 4.6+)
pip install --upgrade selenium

# Method 2: Manual download
# Download từ https://chromedriver.chromium.org/
# Giải nén vào smoke_test_suite/drivers/

# Method 3: Skip UI tests
python run_smoke_tests.py --skip-ui
```

### ❌ `SessionNotCreatedException: Message: session not created: This version of ChromeDriver only supports Chrome version X`

**Nguyên nhân**: Version mismatch giữa Chrome và ChromeDriver

**Khắc phục**:
```powershell
# Check Chrome version
chrome --version

# Reinstall selenium với webdriver-manager
pip install webdriver-manager
# Code sẽ tự động download đúng version
```

### ❌ `WebDriverException: chrome not reachable`

**Nguyên nhân**: Chrome browser không tìm thấy

**Khắc phục**:
```powershell
# Install Chrome nếu chưa có
choco install googlechrome

# Hoặc specify Chrome path
# tests/test_ui_smoke.py
chrome_options.binary_location = "C:/Program Files/Google/Chrome/Application/chrome.exe"
```

### ❌ `TimeoutException: Message: timeout: Timed out receiving message from renderer`

**Nguyên nhân**: Page load quá chậm

**Khắc phục**:
```powershell
# Tăng timeout
# config/test_config.py
PAGE_LOAD_TIMEOUT = 60
ELEMENT_WAIT_TIMEOUT = 30

# Hoặc enable headless mode
python run_smoke_tests.py --headless
```

---

## 3. PYTHON & DEPENDENCIES ERRORS

### ❌ `ModuleNotFoundError: No module named 'pytest'`

**Nguyên nhân**: Dependencies chưa cài đặt

**Khắc phục**:
```powershell
# Cài đặt dependencies
pip install -r requirements.txt

# Check installation
pip list | findstr pytest
python -c "import pytest, requests, selenium; print('OK')"
```

### ❌ `ImportError: cannot import name 'xyz' from 'module'`

**Nguyên nhân**: Version conflict hoặc package bị corrupt

**Khắc phục**:
```powershell
# Reinstall packages
pip uninstall pytest requests selenium
pip install -r requirements.txt

# Clear cache
pip cache purge

# Recreate virtual environment
deactivate
Remove-Item venv -Recurse -Force
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### ❌ `SyntaxError: invalid syntax`

**Nguyên nhân**: Python version không tương thích

**Khắc phục**:
```powershell
# Check Python version
python --version  # Cần 3.7+

# Upgrade Python nếu cần
choco upgrade python

# Hoặc use specific version
py -3.9 run_smoke_tests.py
```

### ❌ `UnicodeDecodeError: 'utf-8' codec can't decode`

**Nguyên nhân**: Encoding issues với file

**Khắc phục**:
```powershell
# Set environment encoding
$env:PYTHONIOENCODING = "utf-8"

# Hoặc fix trong code
# open(file, 'r', encoding='utf-8-sig')
```

---

## 4. APPLICATION ERRORS

### ❌ Test fails với `404 Not Found`

**Nguyên nhân**: URL endpoint không tồn tại

**Khắc phục**:
```powershell
# Check application routes
cd microblog
flask routes

# Verify URL in browser
start http://localhost:5000/auth/login

# Update config nếu cần
# config/test_config.py
BASE_URL = "http://localhost:5000"
```

### ❌ `500 Internal Server Error`

**Nguyên nhân**: Application error

**Khắc phục**:
```powershell
# Check Microblog logs
# Xem terminal đang chạy flask run

# Check database
cd microblog
flask db upgrade

# Reset database nếu cần
Remove-Item app.db
flask db upgrade
```

### ❌ `CSRF token missing or incorrect`

**Nguyên nhân**: Flask CSRF protection

**Khắc phục**:
```powershell
# Option 1: Disable CSRF cho testing
# microblog/config.py
WTF_CSRF_ENABLED = False

# Option 2: Handle CSRF trong tests
# tests/test_smoke.py - đã implement
```

### ❌ `User registration fails`

**Nguyên nhân**: User đã tồn tại hoặc validation lỗi

**Khắc phục**:
```powershell
# Use unique usernames
# config/test_data.json
"username": "testuser_20250824_153045"

# Hoặc cleanup database
cd microblog
Remove-Item app.db
flask db upgrade
```

---

## 5. PERMISSION & SECURITY ERRORS

### ❌ `PermissionError: [Errno 13] Permission denied`

**Nguyên nhân**: Không có quyền write file

**Khắc phục**:
```powershell
# Run PowerShell as Administrator
# Right-click PowerShell -> Run as Administrator

# Hoặc change execution policy
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

# Check file permissions
icacls smoke_test_suite
```

### ❌ `ExecutionPolicy restriction`

**Nguyên nhân**: PowerShell execution policy

**Khắc phục**:
```powershell
# Allow script execution
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

# Temporary bypass
powershell -ExecutionPolicy Bypass -File .\run_script.ps1

# Check current policy
Get-ExecutionPolicy
```

### ❌ `Access denied to Chrome profile`

**Nguyên nhân**: Chrome profile đang được sử dụng

**Khắc phục**:
```powershell
# Close all Chrome instances
taskkill /F /IM chrome.exe

# Use incognito mode
# tests/test_ui_smoke.py
chrome_options.add_argument("--incognito")

# Hoặc custom profile
chrome_options.add_argument("--user-data-dir=temp_profile")
```

---

## 6. PERFORMANCE ISSUES

### ❌ Tests chạy quá chậm

**Nguyên nhân**: Network latency, heavy UI tests

**Khắc phục**:
```powershell
# Skip UI tests
python run_smoke_tests.py --skip-ui

# Use headless mode
python run_smoke_tests.py --headless

# Parallel execution
pip install pytest-xdist
python -m pytest tests/ -n 4

# Reduce timeout
python run_smoke_tests.py --timeout 15
```

### ❌ Memory usage cao

**Nguyên nhân**: Chrome instances không được cleanup

**Khắc phục**:
```powershell
# Add explicit cleanup
# tests/test_ui_smoke.py
def tearDown(self):
    if hasattr(self, 'driver'):
        self.driver.quit()

# Kill orphaned processes
taskkill /F /IM chrome.exe /T
taskkill /F /IM chromedriver.exe /T
```

### ❌ Disk space đầy

**Nguyên nhân**: Log files và reports tích tụ

**Khắc phục**:
```powershell
# Clean old reports
Get-ChildItem reports/*.html | Where-Object CreationTime -lt (Get-Date).AddDays(-7) | Remove-Item

# Clean logs
Remove-Item logs/*.log

# Add to script
# utils/cleanup.py
```

---

## 7. REPORTING ERRORS

### ❌ `UnicodeEncodeError` khi generate report

**Nguyên nhân**: Special characters trong test output

**Khắc phục**:
```powershell
# Set encoding
$env:PYTHONIOENCODING = "utf-8"

# Fix trong code
# utils/report_generator.py
with open(filename, 'w', encoding='utf-8') as f:
```

### ❌ HTML report không mở được

**Nguyên nhân**: File path hoặc browser issue

**Khắc phục**:
```powershell
# Use full path
$report = (Get-ChildItem reports/*.html | Sort-Object CreationTime -Descending | Select-Object -First 1).FullName
start $report

# Hoặc copy to web server
Copy-Item reports/*.html C:/inetpub/wwwroot/
```

### ❌ CSV export bị lỗi format

**Nguyên nhân**: Comma trong dữ liệu

**Khắc phục**:
```powershell
# Use proper CSV escaping
# utils/report_generator.py
import csv
writer = csv.writer(file, quoting=csv.QUOTE_ALL)
```

---

## 🆘 EMERGENCY RESET

Nếu mọi thứ bị hỏng:

```powershell
# 1. Stop all processes
taskkill /F /IM python.exe
taskkill /F /IM chrome.exe
taskkill /F /IM chromedriver.exe

# 2. Reset environment
deactivate
Remove-Item venv -Recurse -Force
python -m venv venv
.\venv\Scripts\Activate.ps1

# 3. Fresh install
pip install --upgrade pip
pip install -r requirements.txt

# 4. Reset Microblog
cd microblog
Remove-Item app.db -ErrorAction SilentlyContinue
flask db upgrade

# 5. Test installation
python -c "import pytest, requests, selenium; print('✅ Ready!')"

# 6. Run basic test
python run_smoke_tests.py --skip-ui --verbose
```

---

## 📞 LẤY HỖ TRỢ

Khi cần help:

1. **Check version info**:
```powershell
python --version
pip list | findstr -E "(pytest|requests|selenium)"
chrome --version
```

2. **Collect error info**:
```powershell
python run_smoke_tests.py --verbose > error_log.txt 2>&1
```

3. **Include environment**:
- OS version
- Python version  
- Chrome version
- Error message đầy đủ
- Steps to reproduce

**💡 Remember**: Hầu hết lỗi đều có thể fix bằng reinstall dependencies hoặc restart application!
