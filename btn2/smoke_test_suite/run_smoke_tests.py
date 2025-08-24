#!/usr/bin/env python3
"""
Main Test Runner for Microblog Smoke Test Suite
Executes all smoke tests and generates comprehensive reports
"""

import os
import sys
import time
import argparse
from datetime import datetime

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tests.test_smoke import TestMicroblogSmoke
from tests.test_api_smoke import TestMicroblogAPISmoke
from tests.test_ui_smoke import TestMicroblogUISmoke
from utils.test_helpers import TestResultCollector
from utils.report_generator import SmokeTestReporter
from config.test_config import SmokeTestConfig


class SmokeTestRunner:
    """Main runner for all smoke tests"""
    
    def __init__(self, skip_ui=False, verbose=False):
        self.config = SmokeTestConfig()
        self.collector = TestResultCollector()
        self.reporter = SmokeTestReporter()
        self.skip_ui = skip_ui
        self.verbose = verbose
        self.start_time = datetime.now()
        
        print("🔍 Microblog Smoke Test Suite")
        print(f"Starting tests at: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Target URL: {self.config.BASE_URL}")
        print("-" * 60)
    
    def run_basic_smoke_tests(self):
        """Run basic smoke tests"""
        print("\n📋 Running Basic Smoke Tests...")
        
        test_instance = TestMicroblogSmoke()
        test_instance.setup_class()
        
        tests = [
            ("Application Startup", test_instance.test_application_startup),
            ("Home Page Access", test_instance.test_home_page_access),
            ("Registration Page", test_instance.test_registration_page_access),
            ("User Registration", test_instance.test_user_registration),
            ("Login Page", test_instance.test_login_page_access),
            ("User Login", test_instance.test_user_login),
            ("Explore Page", test_instance.test_explore_page),
            ("Critical Endpoints", test_instance.test_critical_endpoints),
            ("Post Creation", test_instance.test_post_creation),
            ("API Users Endpoint", test_instance.test_api_users_endpoint),
        ]
        
        for test_name, test_method in tests:
            try:
                if self.verbose:
                    print(f"  Running: {test_name}...")
                test_method()
                print(f"  ✅ {test_name}")
            except Exception as e:
                print(f"  ❌ {test_name}: {str(e)[:100]}...")
        
        # Merge results
        basic_summary = test_instance.collector.get_summary()
        for result in basic_summary['results']:
            self.collector.results.append(result)
            self.collector.total_tests += 1
            if result['status'] == 'pass':
                self.collector.passed_tests += 1
            else:
                self.collector.failed_tests += 1
        
        test_instance.teardown_class()
    
    def run_api_smoke_tests(self):
        """Run API smoke tests"""
        print("\n🌐 Running API Smoke Tests...")
        
        test_instance = TestMicroblogAPISmoke()
        test_instance.setup_class()
        
        tests = [
            ("API Root", test_instance.test_api_root_accessibility),
            ("API Users", test_instance.test_api_users_endpoint),
            ("API Tokens", test_instance.test_api_tokens_endpoint),
            ("API Error Handling", test_instance.test_api_error_handling),
            ("API Headers", test_instance.test_api_response_headers),
        ]
        
        for test_name, test_method in tests:
            try:
                if self.verbose:
                    print(f"  Running: {test_name}...")
                test_method()
                print(f"  ✅ {test_name}")
            except Exception as e:
                print(f"  ❌ {test_name}: {str(e)[:100]}...")
        
        # Merge results
        api_summary = test_instance.collector.get_summary()
        for result in api_summary['results']:
            self.collector.results.append(result)
            self.collector.total_tests += 1
            if result['status'] == 'pass':
                self.collector.passed_tests += 1
            else:
                self.collector.failed_tests += 1
    
    def run_ui_smoke_tests(self):
        """Run UI smoke tests"""
        if self.skip_ui:
            print("\n🖥️  Skipping UI Tests (--skip-ui flag provided)")
            return
            
        print("\n🖥️  Running UI Smoke Tests...")
        
        test_instance = TestMicroblogUISmoke()
        test_instance.setup_class()
        
        if not test_instance.driver:
            print("  ⚠️  WebDriver not available, skipping UI tests")
            return
        
        tests = [
            ("Home Page UI", test_instance.test_home_page_ui_elements),
            ("Login Page UI", test_instance.test_login_page_ui_elements),
            ("Registration UI", test_instance.test_registration_page_ui_elements),
            ("Page Performance", test_instance.test_page_load_performance),
            ("Responsive Design", test_instance.test_responsive_design_basic),
        ]
        
        for test_name, test_method in tests:
            try:
                if self.verbose:
                    print(f"  Running: {test_name}...")
                test_method()
                print(f"  ✅ {test_name}")
            except Exception as e:
                print(f"  ❌ {test_name}: {str(e)[:100]}...")
        
        # Merge results
        ui_summary = test_instance.collector.get_summary()
        for result in ui_summary['results']:
            self.collector.results.append(result)
            self.collector.total_tests += 1
            if result['status'] == 'pass':
                self.collector.passed_tests += 1
            else:
                self.collector.failed_tests += 1
        
        test_instance.teardown_class()
    
    def run_all_tests(self):
        """Run all smoke tests"""
        try:
            self.run_basic_smoke_tests()
            self.run_api_smoke_tests()
            self.run_ui_smoke_tests()
            
        except KeyboardInterrupt:
            print("\n\n❌ Tests interrupted by user")
            return False
        
        return True
    
    def generate_reports(self):
        """Generate test reports"""
        print("\n📊 Generating Reports...")
        
        summary = self.collector.get_summary()
        reports = self.reporter.generate_all_reports(summary)
        
        print("Reports generated:")
        for format_type, filepath in reports.items():
            print(f"  📄 {format_type.upper()}: {filepath}")
        
        return reports
    
    def print_final_summary(self):
        """Print final test summary"""
        end_time = datetime.now()
        duration = (end_time - self.start_time).total_seconds()
        summary = self.collector.get_summary()
        
        print("\n" + "=" * 60)
        print("🏁 FINAL SMOKE TEST SUMMARY")
        print("=" * 60)
        print(f"🕐 Start Time: {self.start_time.strftime('%H:%M:%S')}")
        print(f"🏁 End Time: {end_time.strftime('%H:%M:%S')}")
        print(f"⏱️  Total Duration: {duration:.2f} seconds")
        print(f"📊 Total Tests: {summary['total_tests']}")
        print(f"✅ Passed: {summary['passed_tests']}")
        print(f"❌ Failed: {summary['failed_tests']}")
        print(f"📈 Success Rate: {summary['success_rate']:.1%}")
        
        if summary['failed_tests'] > 0:
            print(f"\n❌ Failed Tests:")
            for result in summary['results']:
                if result['status'] != 'pass':
                    print(f"   • {result['test_name']}")
        
        print("=" * 60)
        
        # Determine exit code
        if summary['success_rate'] >= self.config.MIN_SUCCESS_RATE:
            print("🎉 SMOKE TESTS PASSED - Application appears healthy")
            return 0
        else:
            print("🚨 SMOKE TESTS FAILED - Application has critical issues")
            return 1


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Microblog Smoke Test Suite")
    parser.add_argument("--skip-ui", action="store_true", help="Skip UI tests")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--base-url", default="http://localhost:5000", help="Base URL for testing")
    parser.add_argument("--timeout", type=int, default=30, help="Request timeout in seconds")
    
    args = parser.parse_args()
    
    # Update config with command line arguments
    if args.base_url:
        SmokeTestConfig.BASE_URL = args.base_url
    if args.timeout:
        SmokeTestConfig.TIMEOUT = args.timeout
    
    # Create test runner
    runner = SmokeTestRunner(skip_ui=args.skip_ui, verbose=args.verbose)
    
    # Run tests
    success = runner.run_all_tests()
    
    if success:
        # Generate reports
        runner.generate_reports()
    
    # Print summary and exit
    exit_code = runner.print_final_summary()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
