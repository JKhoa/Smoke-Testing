# Microblog Smoke Test Suite Configuration

class SmokeTestConfig:
    """Configuration for Microblog smoke tests"""
    
    # Application settings
    BASE_URL = "http://localhost:5000"
    TIMEOUT = 30
    RETRY_COUNT = 3
    PAGE_LOAD_TIMEOUT = 10
    
    # Test user credentials
    TEST_USER = {
        "username": "smoketest_user_2025",
        "email": "smoketest2025@example.com", 
        "password": "SmokeTest123!",
        "about_me": "Smoke test user for automated testing"
    }
    
    # Test post data
    TEST_POST = {
        "content": "This is a smoke test post created by automation.",
        "content_long": "This is a longer smoke test post to verify that the application can handle posts with more content. The post should be successfully created and displayed in the timeline."
    }
    
    # Critical endpoints to test
    CRITICAL_ENDPOINTS = [
        "/",
        "/index", 
        "/auth/login",
        "/auth/register",
        "/explore",
        "/api/users",
        "/api/tokens"
    ]
    
    # Expected HTTP status codes for endpoints
    ENDPOINT_EXPECTED_STATUS = {
        "/": [200, 302],  # 302 if redirected to login
        "/index": [200, 302],
        "/auth/login": [200],
        "/auth/register": [200],
        "/explore": [200, 302],
        "/api/users": [200, 401],  # 401 for unauthenticated requests
        "/api/tokens": [401, 405]  # 401 for unauthenticated, 405 for GET method
    }
    
    # Database configuration for testing
    DATABASE_CHECK_QUERY = "SELECT COUNT(*) FROM user;"
    
    # Test thresholds
    MAX_RESPONSE_TIME = 5.0  # seconds
    MIN_SUCCESS_RATE = 0.8   # 80% of tests should pass
    
    # Browser configuration for Selenium
    BROWSER_CONFIG = {
        "headless": True,
        "window_size": (1920, 1080),
        "implicit_wait": 10
    }
    
    # Report settings
    REPORT_FORMATS = ["html", "json", "csv"]
    REPORT_DIR = "reports"
    
    # Logging configuration
    LOG_LEVEL = "INFO"
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
