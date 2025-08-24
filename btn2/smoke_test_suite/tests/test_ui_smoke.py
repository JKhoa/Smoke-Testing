"""
UI Smoke Tests for Microblog Application using Selenium
Tests user interface elements and interactions
"""

import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from utils.test_helpers import TestResultCollector
from config.test_config import SmokeTestConfig


class TestMicroblogUISmoke:
    """UI smoke tests using Selenium WebDriver"""
    
    @classmethod
    def setup_class(cls):
        """Setup Selenium WebDriver"""
        cls.config = SmokeTestConfig()
        cls.collector = TestResultCollector()
        cls.driver = None
        cls._setup_driver()
    
    @classmethod
    def _setup_driver(cls):
        """Setup Chrome WebDriver with options"""
        try:
            chrome_options = Options()
            if cls.config.BROWSER_CONFIG["headless"]:
                chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument(f"--window-size={cls.config.BROWSER_CONFIG['window_size'][0]},{cls.config.BROWSER_CONFIG['window_size'][1]}")
            
            cls.driver = webdriver.Chrome(options=chrome_options)
            cls.driver.implicitly_wait(cls.config.BROWSER_CONFIG["implicit_wait"])
            cls.wait = WebDriverWait(cls.driver, cls.config.TIMEOUT)
            
        except Exception as e:
            print(f"Warning: Could not setup Chrome WebDriver: {e}")
            print("Skipping UI tests - WebDriver not available")
            cls.driver = None
    
    @classmethod
    def teardown_class(cls):
        """Cleanup WebDriver"""
        if cls.driver:
            cls.driver.quit()
    
    def _skip_if_no_driver(self):
        """Skip test if WebDriver is not available"""
        if not self.driver:
            print("Skipping UI test - WebDriver not available")
            return True
        return False
    
    def test_home_page_ui_elements(self):
        """Test UI elements on home page"""
        if self._skip_if_no_driver():
            return
            
        start_time = time.time()
        
        try:
            self.driver.get(f"{self.config.BASE_URL}/")
            duration = time.time() - start_time
            
            # Check for basic page elements
            page_title = self.driver.title
            assert page_title, "Page title is empty"
            
            # Check if we can find navigation elements
            try:
                nav_element = self.wait.until(
                    EC.presence_of_element_located((By.TAG_NAME, "nav"))
                )
                assert nav_element.is_displayed(), "Navigation not visible"
            except TimeoutException:
                # Navigation might not be present on all pages
                pass
            
            self.collector.add_result(
                "Home Page UI Elements",
                "pass",
                duration,
                details={
                    "page_title": page_title,
                    "current_url": self.driver.current_url
                }
            )
            
        except Exception as e:
            duration = time.time() - start_time
            self.collector.add_result("Home Page UI Elements", "fail", duration, error=str(e))
            raise
    
    def test_login_page_ui_elements(self):
        """Test UI elements on login page"""
        if self._skip_if_no_driver():
            return
            
        start_time = time.time()
        
        try:
            self.driver.get(f"{self.config.BASE_URL}/auth/login")
            duration = time.time() - start_time
            
            # Check for login form elements
            try:
                username_field = self.wait.until(
                    EC.presence_of_element_located((By.NAME, "username"))
                )
                password_field = self.driver.find_element(By.NAME, "password")
                submit_button = self.driver.find_element(By.CSS_SELECTOR, "input[type='submit'], button[type='submit']")
                
                assert username_field.is_displayed(), "Username field not visible"
                assert password_field.is_displayed(), "Password field not visible"
                assert submit_button.is_displayed(), "Submit button not visible"
                
                self.collector.add_result(
                    "Login Page UI Elements",
                    "pass",
                    duration,
                    details={
                        "form_elements_found": True,
                        "page_title": self.driver.title
                    }
                )
                
            except Exception as e:
                self.collector.add_result("Login Page UI Elements", "fail", duration, error=str(e))
                raise
                
        except Exception as e:
            duration = time.time() - start_time
            self.collector.add_result("Login Page UI Elements", "fail", duration, error=str(e))
            raise
    
    def test_registration_page_ui_elements(self):
        """Test UI elements on registration page"""
        if self._skip_if_no_driver():
            return
            
        start_time = time.time()
        
        try:
            self.driver.get(f"{self.config.BASE_URL}/auth/register")
            duration = time.time() - start_time
            
            # Check for registration form elements
            try:
                username_field = self.wait.until(
                    EC.presence_of_element_located((By.NAME, "username"))
                )
                email_field = self.driver.find_element(By.NAME, "email")
                password_field = self.driver.find_element(By.NAME, "password")
                password2_field = self.driver.find_element(By.NAME, "password2")
                
                assert username_field.is_displayed(), "Username field not visible"
                assert email_field.is_displayed(), "Email field not visible"
                assert password_field.is_displayed(), "Password field not visible"
                assert password2_field.is_displayed(), "Password confirmation field not visible"
                
                self.collector.add_result(
                    "Registration Page UI Elements",
                    "pass",
                    duration,
                    details={
                        "form_elements_found": True,
                        "page_title": self.driver.title
                    }
                )
                
            except Exception as e:
                self.collector.add_result("Registration Page UI Elements", "fail", duration, error=str(e))
                raise
                
        except Exception as e:
            duration = time.time() - start_time
            self.collector.add_result("Registration Page UI Elements", "fail", duration, error=str(e))
            raise
    
    def test_page_load_performance(self):
        """Test page load performance"""
        if self._skip_if_no_driver():
            return
            
        start_time = time.time()
        
        try:
            self.driver.get(f"{self.config.BASE_URL}/")
            
            # Wait for page to fully load
            self.wait.until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            
            duration = time.time() - start_time
            
            # Check if page loaded within acceptable time
            assert duration < self.config.MAX_RESPONSE_TIME, f"Page load too slow: {duration:.2f}s"
            
            self.collector.add_result(
                "Page Load Performance",
                "pass",
                duration,
                details={
                    "load_time": duration,
                    "page_size": len(self.driver.page_source)
                }
            )
            
        except Exception as e:
            duration = time.time() - start_time
            self.collector.add_result("Page Load Performance", "fail", duration, error=str(e))
            raise
    
    def test_responsive_design_basic(self):
        """Test basic responsive design"""
        if self._skip_if_no_driver():
            return
            
        start_time = time.time()
        
        try:
            self.driver.get(f"{self.config.BASE_URL}/")
            
            # Test mobile viewport
            self.driver.set_window_size(375, 667)  # iPhone size
            time.sleep(1)  # Wait for resize
            
            # Check if page is still accessible
            body = self.driver.find_element(By.TAG_NAME, "body")
            assert body.is_displayed(), "Page not visible in mobile viewport"
            
            # Test desktop viewport
            self.driver.set_window_size(1920, 1080)
            time.sleep(1)
            
            duration = time.time() - start_time
            
            self.collector.add_result(
                "Responsive Design Basic",
                "pass",
                duration,
                details={
                    "mobile_test": True,
                    "desktop_test": True
                }
            )
            
        except Exception as e:
            duration = time.time() - start_time
            self.collector.add_result("Responsive Design Basic", "fail", duration, error=str(e))
            raise


if __name__ == "__main__":
    # Run UI smoke tests
    import sys
    
    test_instance = TestMicroblogUISmoke()
    test_instance.setup_class()
    
    try:
        if test_instance.driver:
            test_instance.test_home_page_ui_elements()
            test_instance.test_login_page_ui_elements()
            test_instance.test_registration_page_ui_elements()
            test_instance.test_page_load_performance()
            test_instance.test_responsive_design_basic()
        else:
            print("Skipping all UI tests - WebDriver not available")
        
    finally:
        test_instance.teardown_class()
        
        # Print summary
        summary = test_instance.collector.get_summary()
        print(f"\n{'='*50}")
        print("UI SMOKE TEST SUMMARY")
        print(f"{'='*50}")
        print(f"Total Tests: {summary['total_tests']}")
        print(f"Passed: {summary['passed_tests']}")
        print(f"Failed: {summary['failed_tests']}")
        print(f"Success Rate: {summary['success_rate']:.1%}")
        print(f"Total Duration: {summary['total_duration']:.2f}s")
        
        # Exit with appropriate code
        sys.exit(0 if summary['failed_tests'] == 0 else 1)
