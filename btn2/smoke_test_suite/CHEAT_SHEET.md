# 🎯 SMOKE TEST CHEAT SHEET

> **Commands và tricks thường dùng cho Smoke Testing**

## ⚡ COMMANDS CƠ BẢN

```powershell
# Chạy tất cả tests
python run_smoke_tests.py

# Chỉ basic tests (nhanh nhất)
python run_smoke_tests.py --skip-ui

# Debug mode (chi tiết)
python run_smoke_tests.py --verbose

# Custom URL
python run_smoke_tests.py --base-url http://localhost:8080
```

## 🔧 TROUBLESHOOTING NHANH

| Lỗi | Command fix |
|-----|-------------|
| **Connection refused** | `cd microblog && flask run` |
| **WebDriver not found** | `python run_smoke_tests.py --skip-ui` |
| **Module not found** | `pip install -r requirements.txt` |
| **Permission denied** | Run PowerShell as Administrator |

## 📊 PYTEST COMMANDS

```powershell
# Chạy một test cụ thể
python -m pytest tests/test_smoke.py::test_application_startup -v

# Chạy tests với filter
python -m pytest tests/ -k "login" -v

# Stop tại lỗi đầu tiên
python -m pytest tests/ -x

# Parallel execution (4 workers)
python -m pytest tests/ -n 4

# Chỉ failed tests từ lần trước
python -m pytest --lf
```

## 🔍 DEBUG TRICKS

```powershell
# Xem chi tiết HTTP requests
python run_smoke_tests.py --verbose --debug

# Check single endpoint
curl http://localhost:5000/auth/login

# Test Python imports
python -c "import pytest, requests, selenium; print('OK')"

# Check Chrome version
chrome --version

# Check if port busy
netstat -an | findstr 5000
```

## 📈 REPORTING SHORTCUTS

```powershell
# Generate only HTML report
python run_smoke_tests.py --html-only

# Open latest report
start reports/smoke_report_*.html

# Convert JSON to CSV
python -c "
import json, csv, glob
files = glob.glob('reports/*.json')
with open(files[-1]) as f:
    data = json.load(f)
    # Process data...
"
```

## ⚙️ CONFIG SHORTCUTS

```powershell
# Quick config check
python -c "
from config.test_config import SmokeTestConfig
print(f'URL: {SmokeTestConfig.BASE_URL}')
print(f'Timeout: {SmokeTestConfig.DEFAULT_TIMEOUT}')
"

# Override timeout
$env:SMOKE_TEST_TIMEOUT = "60"
python run_smoke_tests.py

# Override URL
$env:SMOKE_TEST_BASE_URL = "http://staging.app.com"
python run_smoke_tests.py
```

## 🎭 ENVIRONMENT MANAGEMENT

```powershell
# Dev environment
python run_smoke_tests.py --config dev

# Staging environment
python run_smoke_tests.py --base-url https://staging.app.com --headless

# Production smoke check
python run_smoke_tests.py --base-url https://prod.app.com --skip-ui --timeout 120
```

## 🔄 CI/CD SHORTCUTS

```powershell
# Headless run (cho CI)
python run_smoke_tests.py --headless --skip-ui

# Exit code 0 nếu >= 80% pass
python run_smoke_tests.py --min-success-rate 0.8

# Generate JUnit XML
python -m pytest tests/ --junitxml=reports/junit.xml

# Upload to GitHub Pages
python run_smoke_tests.py --public-report
```

## 📱 MOBILE TESTING

```powershell
# Test mobile viewport
python run_smoke_tests.py --mobile-viewport

# Test với Chrome mobile
python run_smoke_tests.py --user-agent mobile
```

## 🔧 ADVANCED TRICKS

```powershell
# Run với retry
for ($i=1; $i -le 3; $i++) {
    python run_smoke_tests.py
    if ($LASTEXITCODE -eq 0) { break }
    Write-Host "Retry $i..."
}

# Backup reports
$date = Get-Date -Format "yyyyMMdd_HHmmss"
Copy-Item reports/ "backup/reports_$date/" -Recurse

# Clean old reports (keep last 10)
Get-ChildItem reports/*.html | Sort-Object CreationTime -Descending | Select-Object -Skip 10 | Remove-Item

# Monitor application during tests
Start-Job { while ($true) { 
    curl -s http://localhost:5000 | Out-Null
    if ($LASTEXITCODE -ne 0) { Write-Host "App down!" }
    Start-Sleep 5
}}
```

## 📊 METRICS COLLECTION

```powershell
# Collect performance metrics
python -c "
import time, requests
start = time.time()
r = requests.get('http://localhost:5000')
print(f'Response time: {time.time() - start:.2f}s')
print(f'Status: {r.status_code}')
print(f'Size: {len(r.content)} bytes')
"

# Memory usage check
Get-Process python | Select-Object Name, CPU, WorkingSet

# Disk space check
Get-WmiObject -Class Win32_LogicalDisk | Select-Object DeviceID, FreeSpace
```

## 🎯 KEYBOARD SHORTCUTS

| Action | Shortcut |
|--------|----------|
| **Cancel running test** | `Ctrl + C` |
| **Clear terminal** | `cls` |
| **Open HTML report** | `start reports\*.html` |
| **View last log** | `Get-Content logs\*.log -Tail 20` |

---

**💡 Pro Tip**: Bookmark file này và luôn có terminal mở tại `smoke_test_suite/` folder!

**⏰ Save time**: Tạo alias cho commands thường dùng:
```powershell
Set-Alias smoke 'python run_smoke_tests.py'
Set-Alias smokequick 'python run_smoke_tests.py --skip-ui'
```
