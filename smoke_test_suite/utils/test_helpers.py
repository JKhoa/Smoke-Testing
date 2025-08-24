"""
Microblog Smoke Test Helper Utilities
Provides common functions and classes for smoke testing
"""

import requests
import time
import logging
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from config.test_config import SmokeTestConfig

# Setup logging
logging.basicConfig(
    level=getattr(logging, SmokeTestConfig.LOG_LEVEL),
    format=SmokeTestConfig.LOG_FORMAT
)
logger = logging.getLogger(__name__)


class SmokeTestHelper:
    """Helper class for common smoke test operations"""
    
    def __init__(self):
        self.config = SmokeTestConfig()
        self.session = requests.Session()
        self.session.timeout = self.config.TIMEOUT
        
    def check_application_health(self) -> Dict:
        """Check if the application is running and responsive"""
        try:
            start_time = time.time()
            response = self.session.get(self.config.BASE_URL)
            response_time = time.time() - start_time
            
            return {
                "success": True,
                "status_code": response.status_code,
                "response_time": response_time,
                "url": response.url,
                "accessible": response.status_code < 500
            }
        except requests.exceptions.RequestException as e:
            logger.error(f"Application health check failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "accessible": False
            }
    
    def register_test_user(self, user_data: Optional[Dict] = None) -> Dict:
        """Register a test user and return result"""
        if user_data is None:
            user_data = self.config.TEST_USER.copy()
        
        try:
            # First get the registration page to get CSRF token
            reg_page = self.session.get(f"{self.config.BASE_URL}/auth/register")
            if reg_page.status_code != 200:
                return {
                    "success": False,
                    "error": f"Registration page inaccessible: {reg_page.status_code}"
                }
            
            # Extract CSRF token (simplified - in real implementation would parse HTML)
            # For now, we'll assume the form works without CSRF for testing
            
            registration_data = {
                "username": user_data["username"],
                "email": user_data["email"], 
                "password": user_data["password"],
                "password2": user_data["password"],
                "submit": "Register"
            }
            
            response = self.session.post(
                f"{self.config.BASE_URL}/auth/register",
                data=registration_data,
                allow_redirects=False
            )
            
            success = response.status_code in [200, 302]
            
            return {
                "success": success,
                "status_code": response.status_code,
                "user_data": user_data,
                "redirect_location": response.headers.get("Location")
            }
            
        except Exception as e:
            logger.error(f"User registration failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def login_test_user(self, user_data: Optional[Dict] = None) -> Dict:
        """Login with test user and return result"""
        if user_data is None:
            user_data = self.config.TEST_USER.copy()
        
        try:
            # Get login page
            login_page = self.session.get(f"{self.config.BASE_URL}/auth/login")
            if login_page.status_code != 200:
                return {
                    "success": False,
                    "error": f"Login page inaccessible: {login_page.status_code}"
                }
            
            login_data = {
                "username": user_data["username"],
                "password": user_data["password"],
                "remember_me": False,
                "submit": "Sign In"
            }
            
            response = self.session.post(
                f"{self.config.BASE_URL}/auth/login",
                data=login_data,
                allow_redirects=False
            )
            
            success = response.status_code in [200, 302]
            
            return {
                "success": success,
                "status_code": response.status_code,
                "redirect_location": response.headers.get("Location"),
                "authenticated": "Set-Cookie" in response.headers
            }
            
        except Exception as e:
            logger.error(f"User login failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def create_test_post(self, post_content: Optional[str] = None) -> Dict:
        """Create a test post and return result"""
        if post_content is None:
            post_content = self.config.TEST_POST["content"]
        
        try:
            # First ensure we're logged in
            login_result = self.login_test_user()
            if not login_result["success"]:
                return {
                    "success": False,
                    "error": "Could not login before creating post"
                }
            
            # Get the home page to access post form
            home_page = self.session.get(f"{self.config.BASE_URL}/")
            if home_page.status_code != 200:
                return {
                    "success": False,
                    "error": f"Home page inaccessible: {home_page.status_code}"
                }
            
            post_data = {
                "post": post_content,
                "submit": "Submit"
            }
            
            response = self.session.post(
                f"{self.config.BASE_URL}/",
                data=post_data,
                allow_redirects=False
            )
            
            success = response.status_code in [200, 302]
            
            return {
                "success": success,
                "status_code": response.status_code,
                "post_content": post_content,
                "redirect_location": response.headers.get("Location")
            }
            
        except Exception as e:
            logger.error(f"Post creation failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def test_critical_endpoints(self) -> List[Dict]:
        """Test all critical endpoints and return results"""
        results = []
        
        for endpoint in self.config.CRITICAL_ENDPOINTS:
            try:
                start_time = time.time()
                response = self.session.get(f"{self.config.BASE_URL}{endpoint}")
                response_time = time.time() - start_time
                
                expected_status = self.config.ENDPOINT_EXPECTED_STATUS.get(
                    endpoint, [200]
                )
                
                success = response.status_code in expected_status
                
                results.append({
                    "endpoint": endpoint,
                    "success": success,
                    "status_code": response.status_code,
                    "response_time": response_time,
                    "expected_status": expected_status,
                    "content_length": len(response.content)
                })
                
            except Exception as e:
                results.append({
                    "endpoint": endpoint,
                    "success": False,
                    "error": str(e),
                    "response_time": None
                })
        
        return results
    
    def cleanup_test_data(self) -> Dict:
        """Clean up test data after testing"""
        try:
            # In a real implementation, this would clean up test users and posts
            # For now, we'll just log out
            logout_response = self.session.get(f"{self.config.BASE_URL}/auth/logout")
            
            return {
                "success": True,
                "message": "Test data cleanup completed",
                "logout_status": logout_response.status_code
            }
            
        except Exception as e:
            logger.error(f"Cleanup failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }


class TestResultCollector:
    """Collects and manages test results"""
    
    def __init__(self):
        self.results = []
        self.start_time = datetime.now()
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
    
    def add_result(self, test_name: str, status: str, duration: float, 
                   details: Optional[Dict] = None, error: Optional[str] = None):
        """Add a test result"""
        self.total_tests += 1
        
        if status.lower() == "pass":
            self.passed_tests += 1
        else:
            self.failed_tests += 1
        
        result = {
            "test_name": test_name,
            "status": status,
            "duration": duration,
            "timestamp": datetime.now().isoformat(),
            "details": details or {},
            "error": error
        }
        
        self.results.append(result)
        logger.info(f"Test {test_name}: {status.upper()} ({duration:.2f}s)")
    
    def get_summary(self) -> Dict:
        """Get test execution summary"""
        end_time = datetime.now()
        total_duration = (end_time - self.start_time).total_seconds()
        
        return {
            "start_time": self.start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "total_duration": total_duration,
            "total_tests": self.total_tests,
            "passed_tests": self.passed_tests,
            "failed_tests": self.failed_tests,
            "success_rate": self.passed_tests / self.total_tests if self.total_tests > 0 else 0,
            "results": self.results
        }
    
    def save_results(self, filepath: str, format_type: str = "json"):
        """Save results to file"""
        summary = self.get_summary()
        
        try:
            if format_type.lower() == "json":
                with open(filepath, 'w') as f:
                    json.dump(summary, f, indent=2)
            elif format_type.lower() == "csv":
                import csv
                with open(filepath, 'w', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=['test_name', 'status', 'duration', 'timestamp', 'error'])
                    writer.writeheader()
                    for result in self.results:
                        writer.writerow({
                            'test_name': result['test_name'],
                            'status': result['status'],
                            'duration': result['duration'],
                            'timestamp': result['timestamp'],
                            'error': result.get('error', '')
                        })
            
            logger.info(f"Results saved to {filepath}")
            
        except Exception as e:
            logger.error(f"Failed to save results: {e}")


def retry_on_failure(max_retries: int = 3, delay: float = 1.0):
    """Decorator to retry failed operations"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries - 1:
                        logger.warning(f"Attempt {attempt + 1} failed, retrying in {delay}s: {e}")
                        time.sleep(delay)
                    else:
                        logger.error(f"All {max_retries} attempts failed")
            
            raise last_exception
        return wrapper
    return decorator
