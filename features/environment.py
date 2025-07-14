"""
Behave environment configuration for Hudl login testing.
This file contains hooks and setup/teardown logic for test execution.
"""

import os
import time
from datetime import datetime
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.home_page import HomePage
from pages.new_account_page import NewAccountPage
from pages.reset_password_page import ResetPasswordPage

def before_all(context):
    """
    Called once before all tests. Set up global configuration and test environment.
    """
    # Initialize configuration
    try:
        from utils.config import Config
        context.config_manager = Config()
    except ImportError:
        print("Warning: Configuration module not available. Using defaults.")
        context.config_manager = None
    
    # Set up test data
    if context.config_manager:
        context.test_data = context.config_manager.get_test_data()
    else:
        context.test_data = {
            'valid_credentials': {
                'email': 'test.user@example.com',
                'password': 'TestPassword123!'
            },
            'invalid_credentials': {
                'email': 'invalid.user@example.com',
                'password': 'WrongPassword'
            }
        }
    
    # Create reports directory if it doesn't exist
    os.makedirs('reports', exist_ok=True)
    
    # Initialize test metrics
    context.test_start_time = datetime.now()
    context.test_metrics = {
        'total_tests': 0,
        'passed_tests': 0,
        'failed_tests': 0,
        'skipped_tests': 0
    }
    
    print(f"Test execution started at: {context.test_start_time}")
    if context.config_manager:
        print(f"Browser: {context.config_manager.get_browser()}")
        print(f"Base URL: {context.config_manager.get_base_url()}")


def before_feature(context, feature):
    """
    Called before each feature. Set up feature-specific configuration.
    """
    print(f"\nStarting Feature: {feature.name}")
    context.feature_start_time = datetime.now()


def before_scenario(context, scenario):
    """
    Called before each scenario. Set up browser driver and test environment.
    """
    print(f"\nStarting Scenario: {scenario.name}")
    context.scenario_start_time = datetime.now()
    
    # Initialize driver manager
    try:
        from utils.driver_manager import DriverManager
        if context.config_manager:
            context.driver_manager = DriverManager(context.config_manager)
            context.driver = context.driver_manager.get_driver()
        else:
            # Fallback to basic Chrome setup
            from selenium import webdriver
            from selenium.webdriver.chrome.service import Service
            from webdriver_manager.chrome import ChromeDriverManager
            
            service = Service(ChromeDriverManager().install())
            context.driver = webdriver.Chrome(service=service)
    except ImportError as e:
        print(f"Warning: Could not initialize WebDriver: {e}")
        print("Please install dependencies: pip install -r requirements.txt")
        context.driver = None
        return
    
    # Set implicit wait
    if context.driver:
        implicit_wait = 10
        if context.config_manager:
            implicit_wait = context.config_manager.get_implicit_wait()
        context.driver.implicitly_wait(implicit_wait)
        
        # Maximize window unless running headless
        headless = os.getenv('HEADLESS', 'false').lower() == 'true'
        if not headless:
            context.driver.maximize_window()
    
    # Set up scenario-specific data
    context.scenario_data = {}
    
    # Initialize page objects without navigation
    if context.driver:
        config = context.config_manager if hasattr(context, 'config_manager') else None
        context.login_page = LoginPage(context.driver, config)
        context.dashboard_page = DashboardPage(context.driver, config)
        context.home_page = HomePage(context.driver, config)
        context.new_account_page = NewAccountPage(context.driver, config)
        context.reset_password_page = ResetPasswordPage(context.driver, config)
        
        print("Page objects initialized")
    
    # Navigation happens explicitly in Given steps
    print(f"Starting scenario: {scenario.name}")
    
    # Update test metrics
    context.test_metrics['total_tests'] += 1


def after_scenario(context, scenario):
    """
    Called after each scenario. Clean up and capture results.
    """
    scenario_duration = datetime.now() - context.scenario_start_time
    
    # Update test metrics based on scenario status
    if scenario.status == 'passed':
        context.test_metrics['passed_tests'] += 1
        print(f"✓ Scenario PASSED: {scenario.name} (Duration: {scenario_duration})")
    elif scenario.status == 'failed':
        context.test_metrics['failed_tests'] += 1
        print(f"✗ Scenario FAILED: {scenario.name} (Duration: {scenario_duration})")
        
        # Take screenshot on failure
        if hasattr(context, 'driver') and context.driver:
            try:
                screenshot_name = f"failure_{scenario.name.replace(' ', '_')}_{int(time.time())}.png"
                screenshot_path = os.path.join('reports', screenshot_name)
                context.driver.save_screenshot(screenshot_path)
                print(f"Screenshot saved: {screenshot_path}")
            except Exception as e:
                print(f"Failed to take screenshot: {e}")
    else:
        context.test_metrics['skipped_tests'] += 1
        print(f"- Scenario SKIPPED: {scenario.name}")
    
    # Clean up driver
    if hasattr(context, 'driver') and context.driver:
        try:
            context.driver.quit()
        except Exception as e:
            print(f"Error closing driver: {e}")
    
    # Clean up scenario data
    if hasattr(context, 'scenario_data'):
        del context.scenario_data


def after_feature(context, feature):
    """
    Called after each feature. Report feature results.
    """
    feature_duration = datetime.now() - context.feature_start_time
    print(f"\nCompleted Feature: {feature.name} (Duration: {feature_duration})")


def after_all(context):
    """
    Called once after all tests. Generate final reports and cleanup.
    """
    test_duration = datetime.now() - context.test_start_time
    
    # Print final test summary
    print("\n" + "="*50)
    print("TEST EXECUTION SUMMARY")
    print("="*50)
    print(f"Total Duration: {test_duration}")
    print(f"Total Tests: {context.test_metrics['total_tests']}")
    print(f"Passed: {context.test_metrics['passed_tests']}")
    print(f"Failed: {context.test_metrics['failed_tests']}")
    print(f"Skipped: {context.test_metrics['skipped_tests']}")
    
    if context.test_metrics['total_tests'] > 0:
        pass_rate = (context.test_metrics['passed_tests'] / context.test_metrics['total_tests']) * 100
        print(f"Pass Rate: {pass_rate:.2f}%")
    
    print("="*50)
    
    # Generate summary report file
    try:
        with open('reports/test_summary.txt', 'w') as f:
            f.write(f"Test Execution Summary\n")
            f.write(f"=====================\n")
            f.write(f"Execution Date: {context.test_start_time}\n")
            f.write(f"Duration: {test_duration}\n")
            if context.config_manager:
                f.write(f"Browser: {context.config_manager.get_browser()}\n")
                f.write(f"Base URL: {context.config_manager.get_base_url()}\n")
            f.write(f"Total Tests: {context.test_metrics['total_tests']}\n")
            f.write(f"Passed: {context.test_metrics['passed_tests']}\n")
            f.write(f"Failed: {context.test_metrics['failed_tests']}\n")
            f.write(f"Skipped: {context.test_metrics['skipped_tests']}\n")
            if context.test_metrics['total_tests'] > 0:
                pass_rate = (context.test_metrics['passed_tests'] / context.test_metrics['total_tests']) * 100
                f.write(f"Pass Rate: {pass_rate:.2f}%\n")
    except Exception as e:
        print(f"Failed to write summary report: {e}")


def before_step(context, step):
    """
    Called before each step. Can be used for step-level setup.
    """
    pass


def after_step(context, step):
    """
    Called after each step. Can be used for step-level verification.
    """
    # Add small delay between steps for stability
    time.sleep(0.5)
    
    # Log step execution for debugging
    if step.status == 'failed':
        print(f"Step failed: {step.name}")
        
        # Optionally capture page source on step failure
        if hasattr(context, 'driver') and context.driver:
            try:
                page_source_name = f"step_failure_{int(time.time())}.html"
                page_source_path = os.path.join('reports', page_source_name)
                with open(page_source_path, 'w', encoding='utf-8') as f:
                    f.write(context.driver.page_source)
                print(f"Page source saved: {page_source_path}")
            except Exception as e:
                print(f"Failed to save page source: {e}")
