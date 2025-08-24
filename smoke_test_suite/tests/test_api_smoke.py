"""
API Smoke Tests for Microblog Application
Tests API endpoints for basic functionality
"""

import json
import time
import requests
from utils.test_helpers import SmokeTestHelper, TestResultCollector
from config.test_config import SmokeTestConfig


class TestMicroblogAPISmoke:
    """API smoke tests for Microblog application"""
    
    @classmethod
    def setup_class(cls):
        """Setup for API tests"""
        cls.config = SmokeTestConfig()
        cls.helper = SmokeTestHelper()
        cls.collector = TestResultCollector()
        cls.session = requests.Session()
        cls.base_url = cls.config.BASE_URL
    
    def test_api_root_accessibility(self):
        """Test API root endpoint accessibility"""
        start_time = time.time()
        
        try:
            response = self.session.get(f"{self.base_url}/api", timeout=self.config.TIMEOUT)
            duration = time.time() - start_time
            
            # API root might not exist, but should not return 500
            assert response.status_code != 500, f"API root returned server error: {response.status_code}"
            
            self.collector.add_result(
                "API Root Accessibility",
                "pass",
                duration,
                details={"status_code": response.status_code}
            )
            
        except Exception as e:
            duration = time.time() - start_time
            self.collector.add_result("API Root Accessibility", "fail", duration, error=str(e))
            raise
    
    def test_api_users_endpoint(self):
        """Test API users endpoint"""
        start_time = time.time()
        
        try:
            response = self.session.get(f"{self.base_url}/api/users", timeout=self.config.TIMEOUT)
            duration = time.time() - start_time
            
            # Should return 401 for unauthenticated requests or 200 if public
            assert response.status_code in [200, 401], f"Unexpected status: {response.status_code}"
            
            # Check if response is JSON for successful requests
            if response.status_code == 200:
                try:
                    json_data = response.json()
                    assert isinstance(json_data, (list, dict)), "Invalid JSON response format"
                except json.JSONDecodeError:
                    pass  # Accept non-JSON responses for smoke test
            
            self.collector.add_result(
                "API Users Endpoint",
                "pass",
                duration,
                details={
                    "status_code": response.status_code,
                    "content_type": response.headers.get("content-type", "N/A")
                }
            )
            
        except Exception as e:
            duration = time.time() - start_time
            self.collector.add_result("API Users Endpoint", "fail", duration, error=str(e))
            raise
    
    def test_api_tokens_endpoint(self):
        """Test API tokens endpoint"""
        start_time = time.time()
        
        try:
            response = self.session.post(f"{self.base_url}/api/tokens", timeout=self.config.TIMEOUT)
            duration = time.time() - start_time
            
            # Should return 401 for unauthenticated requests
            assert response.status_code in [401, 405], f"Unexpected status: {response.status_code}"
            
            self.collector.add_result(
                "API Tokens Endpoint",
                "pass",
                duration,
                details={"status_code": response.status_code}
            )
            
        except Exception as e:
            duration = time.time() - start_time
            self.collector.add_result("API Tokens Endpoint", "fail", duration, error=str(e))
            raise
    
    def test_api_error_handling(self):
        """Test API error handling for non-existent endpoints"""
        start_time = time.time()
        
        try:
            response = self.session.get(f"{self.base_url}/api/nonexistent", timeout=self.config.TIMEOUT)
            duration = time.time() - start_time
            
            # Should return 404 for non-existent endpoints
            assert response.status_code == 404, f"Expected 404, got: {response.status_code}"
            
            self.collector.add_result(
                "API Error Handling",
                "pass",
                duration,
                details={"status_code": response.status_code}
            )
            
        except Exception as e:
            duration = time.time() - start_time
            self.collector.add_result("API Error Handling", "fail", duration, error=str(e))
            raise
    
    def test_api_response_headers(self):
        """Test API response headers"""
        start_time = time.time()
        
        try:
            response = self.session.get(f"{self.base_url}/api/users", timeout=self.config.TIMEOUT)
            duration = time.time() - start_time
            
            # Check for common security headers
            headers = response.headers
            
            # Basic header checks
            assert "content-type" in headers.keys(), "Missing Content-Type header"
            
            self.collector.add_result(
                "API Response Headers",
                "pass",
                duration,
                details={
                    "content_type": headers.get("content-type", "N/A"),
                    "server": headers.get("server", "N/A"),
                    "headers_count": len(headers)
                }
            )
            
        except Exception as e:
            duration = time.time() - start_time
            self.collector.add_result("API Response Headers", "fail", duration, error=str(e))
            raise


if __name__ == "__main__":
    # Run API smoke tests
    import sys
    
    test_instance = TestMicroblogAPISmoke()
    test_instance.setup_class()
    
    try:
        test_instance.test_api_root_accessibility()
        test_instance.test_api_users_endpoint()
        test_instance.test_api_tokens_endpoint()
        test_instance.test_api_error_handling()
        test_instance.test_api_response_headers()
        
    finally:
        # Print summary
        summary = test_instance.collector.get_summary()
        print(f"\n{'='*50}")
        print("API SMOKE TEST SUMMARY")
        print(f"{'='*50}")
        print(f"Total Tests: {summary['total_tests']}")
        print(f"Passed: {summary['passed_tests']}")
        print(f"Failed: {summary['failed_tests']}")
        print(f"Success Rate: {summary['success_rate']:.1%}")
        print(f"Total Duration: {summary['total_duration']:.2f}s")
        
        # Exit with appropriate code
        sys.exit(0 if summary['failed_tests'] == 0 else 1)
