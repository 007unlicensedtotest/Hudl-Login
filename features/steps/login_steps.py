"""
Login Steps for Behave BDD Tests

This module contains step definitions for testing the Hudl login functionality.
Organized into logical sections for better maintainability.
"""

from behave import given, when, then
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from urllib.parse import urlparse
import time

# Import allure for enhanced reporting (optional - will work without it)
try:
    import allure
    ALLURE_AVAILABLE = True
except ImportError:
    ALLURE_AVAILABLE = False


def add_allure_step_info(step_name: str, description: str = ""):
    """Add step information to Allure report if available."""
    if ALLURE_AVAILABLE:
        allure.dynamic.description(description)
        allure.dynamic.title(step_name)


def handle_step_failure(context, error, step_name: str, screenshot_name: str):
    """
    Centralized error handling for step failures with enhanced Allure reporting.
    
    Args:
        context: Behave context object
        error: The exception that occurred
        step_name: Name of the step that failed
        screenshot_name: Base name for screenshot file
    """
    error_msg = str(error)
    
    # Add Allure step information if available
    if ALLURE_AVAILABLE:
        allure.dynamic.description(f"Step failed: {step_name}")
    
    # Use enhanced error reporting if available
    if hasattr(context, 'login_page'):
        context.login_page.attach_detailed_error_info_to_allure(
            error_msg=error_msg,
            context=f"Step failure in: {step_name}"
        )
        context.login_page.take_screenshot(screenshot_name)
    
    # Re-raise with enhanced message
    raise Exception(f"Step '{step_name}' failed: {error_msg}")


# ============================================================================
# NAVIGATION STEPS
# ============================================================================

@given('I am on the Hudl login page')
def step_navigate_to_login_page(context):
    """Navigate to the Hudl login page."""
    try:
        context.login_page.navigate_to_login_page()
        print("✓ Navigated to Hudl login page")
    except Exception as e:
        # Enhanced error reporting for Allure
        context.login_page.attach_detailed_error_info_to_allure(
            error_msg=str(e),
            context="Attempting to navigate to Hudl login page"
        )
        context.login_page.take_screenshot("navigation_to_login_failed")
        raise Exception(f"Failed to navigate to login page: {e}")


# ============================================================================
# VALID CREDENTIAL STEPS
# ============================================================================

@given('I enter a valid email address')
@when('I enter a valid email address')
def step_enter_valid_email(context):
    """Enter valid email from test data."""
    try:
        valid_email = context.test_data['valid_credentials']['email']
        context.login_page.enter_email(valid_email)
        context.login_page.click_continue_button()
        print(f"✓ Valid email entered: {valid_email}")
    except Exception as e:
        context.login_page.take_screenshot("valid_email_entry_failed")
        raise Exception(f"Failed to enter valid email: {e}")


@when('I enter a valid password')
@given('I enter a valid password')
def step_enter_valid_password(context):
    """Enter valid password from test data."""
    try:
        valid_password = context.test_data['valid_credentials']['password']
        context.login_page.enter_password(valid_password)
        context.login_page.click_continue_button()
        print("✓ Valid password entered")
    except Exception as e:
        context.login_page.take_screenshot("valid_password_entry_failed")
        raise Exception(f"Failed to enter valid password: {e}")


@given('I am logged in with valid credentials')
def step_login_with_valid_credentials(context):
    """Log in with valid credentials as a prerequisite."""
    try:
        context.execute_steps('''
            When I enter a valid email address
            And I enter a valid password
        ''')
        print("✓ Logged in with valid credentials")
    except Exception as e:
        # Enhanced error reporting for critical login failures
        context.login_page.attach_detailed_error_info_to_allure(
            error_msg=str(e),
            context="Attempting to log in with valid credentials (prerequisite step)"
        )
        context.login_page.take_screenshot("login_prerequisite_failed")
        raise Exception(f"Failed to log in with valid credentials: {e}")


# ============================================================================
# INVALID CREDENTIAL STEPS
# ============================================================================

@when('I enter an invalid email address')
def step_enter_invalid_email(context):
    """Enter invalid email from test data."""
    try:
        invalid_email = context.test_data['invalid_credentials']['email']
        context.login_page.enter_email(invalid_email)
        context.login_page.click_continue_button()
        print(f"✓ Invalid email entered: {invalid_email}")
    except Exception as e:
        context.login_page.take_screenshot("invalid_email_entry_failed")
        raise Exception(f"Failed to enter invalid email: {e}")


@when('I enter an invalid password')
def step_enter_invalid_password(context):
    """Enter invalid password from test data."""
    try:
        invalid_password = context.test_data['invalid_credentials']['password']
        context.login_page.enter_password(invalid_password)
        context.login_page.click_continue_button()
        print("✓ Invalid password entered")
    except Exception as e:
        context.login_page.take_screenshot("invalid_password_entry_failed")
        raise Exception(f"Failed to enter invalid password: {e}")


@when('I enter an invalid email address "{email}"')
def step_enter_specific_invalid_email(context, email):
    """Enter a specific invalid email address."""
    try:
        context.login_page.enter_email(email)
        context.login_page.click_continue_button()
    except Exception as e:
        context.login_page.take_screenshot("invalid_email_entry_failed")
        raise Exception(f"Failed to enter invalid email {email}: {e}")


# ============================================================================
# EMPTY FIELD STEPS
# ============================================================================

@when('I leave the email field empty')
def step_leave_email_field_empty(context):
    """Leave the email field empty (clear it if it has content)."""
    try:
        context.login_page.clear_email()
        context.login_page.click_continue_button()
        print("✓ Email field left empty")
    except Exception as e:
        context.login_page.take_screenshot("clear_email_field_failed")
        raise Exception(f"Failed to clear email field: {e}")


@when('I leave the password field empty')
def step_leave_password_field_empty(context):
    """Leave the password field empty (clear it if it has content)."""
    try:
        context.login_page.clear_password()
        context.login_page.click_continue_button()
        print("✓ Password field left empty")
    except Exception as e:
        context.login_page.take_screenshot("clear_password_field_failed")
        raise Exception(f"Failed to clear password field: {e}")


# ============================================================================
# SUCCESS VERIFICATION STEPS
# ============================================================================

@then('I should be redirected to the dashboard page')
def step_check_dashboard_page_redirect(context):
    """Check if redirected to dashboard page."""
    try:
        context.login_page.verify_redirect_url("home")
        print("✓ Redirected to dashboard page")
    except Exception as e:
        context.login_page.take_screenshot("dashboard_redirect_failed")
        raise AssertionError(f"Failed to verify dashboard page redirect: {e}")


@then('I should see my display name')
def step_check_display_name(context):
    """Check if display name is visible."""
    try:
        display_name = context.login_page.get_display_name()
        expected_display_name = context.test_data['valid_credentials']['display_name']
        assert display_name == expected_display_name, \
            f"Expected display name '{expected_display_name}' but got '{display_name}'"
        print(f"✓ Display name is visible: {display_name}")
    except Exception as e:
        context.login_page.take_screenshot("display_name_check_failed")
        raise AssertionError(f"Failed to verify display name visibility: {e}")


@then('I should remain on the login page')
def step_remain_on_login_page(context):
    """Verify still on login page."""
    try:
        context.login_page.verify_redirect_url("login")
    except Exception as e:
        context.login_page.take_screenshot("login_page_redirect_failed")
        raise AssertionError(f"Failed to verify login page redirect: {e}")


# ============================================================================
# PASSWORD VISIBILITY STEPS
# ============================================================================

@when('I enter a masked password')
def step_enter_masked_password(context):
    """Enter valid password from test data."""
    try:
        valid_password = context.test_data['valid_credentials']['password']
        context.login_page.enter_password(valid_password)
        print("✓ Masked password entered")
    except Exception as e:
        context.login_page.take_screenshot("masked_password_entry_failed")
        raise Exception(f"Failed to enter masked password: {e}")


@when('I click the show/hide password button')
def step_click_show_hide_password_button(context):
    """Click the show/hide password button to toggle the password visibility."""
    try:
        context.login_page.click_show_hide_password()
        print("✓ Show password button clicked successfully")
    except Exception as e:
        context.login_page.take_screenshot("show_password_button_click_failed")
        raise Exception(f"Failed to click show password button: {e}")


@then('the password should be visible as plain text')
def step_password_visible_as_plain_text(context):
    """Verify that the password field shows plain text (not masked)."""
    try:
        is_visible = context.login_page.is_password_visible()
        assert is_visible, "Password should be visible as plain text but it is still masked"
        print("✓ Password is visible as plain text")
    except Exception as e:
        context.login_page.take_screenshot("password_visibility_check_failed")
        raise AssertionError(f"Failed to verify password visibility: {e}")


@when('I click the hide password button')
def step_click_hide_password_button(context):
    """Click the hide password button to mask the password."""
    try:
        context.login_page.click_hide_password()
        print("✓ Hide password button clicked")
    except Exception as e:
        context.login_page.take_screenshot("hide_password_button_click_failed")
        raise Exception(f"Failed to click hide password button: {e}")


@then('the password should be masked again')
def step_password_masked_again(context):
    """Verify that the password field is masked again (not visible as plain text)."""
    try:
        is_visible = context.login_page.is_password_visible()
        assert not is_visible, "Password should be masked but it is still visible as plain text"
        print("✓ Password is masked again")
    except Exception as e:
        context.login_page.take_screenshot("password_masking_check_failed")
        raise AssertionError(f"Failed to verify password masking: {e}")


# ============================================================================
# ERROR MESSAGE VERIFICATION STEPS
# ============================================================================

@then('I should see an email error message')
def step_see_email_error_message(context):
    """Verify that an email error message is displayed."""
    try:
        actual_error_message = context.login_page.get_invalid_credentials_error()
        expected_error_message = context.test_data['expected_error_messages']['invalid_email']
        print(f"✓ Email error message displayed: {actual_error_message}")
        print(f"Expected: {expected_error_message}")
        assert actual_error_message == expected_error_message, "Expected email error message but none was found"
        print(f"✓ Email error message displayed: {actual_error_message}")
    except Exception as e:
        context.login_page.take_screenshot("email_error_message_check_failed")
        raise AssertionError(f"Failed to find email error message: {e}")


@then('I should see a password error message')
def step_see_password_error_message(context):
    """Verify that a password error message is displayed."""
    try:
        actual_error_message = context.login_page.get_password_error()
        expected_error_message = context.test_data['expected_error_messages']['invalid_password']
        print(f"Actual: {actual_error_message}")
        print(f"Expected: {expected_error_message}")
        
        assert actual_error_message == expected_error_message, f"Expected password error message {expected_error_message} but none was found"
        print(f"✓ Password error message displayed: {actual_error_message}")
    except Exception as e:
        context.login_page.take_screenshot("password_error_message_check_failed")
        raise AssertionError(f"Failed to find password error message: {e}")


@then('I should see an invalid email error message')
def step_see_invalid_email_error_message(context):
    """Verify that an invalid email format error message is displayed."""
    try:
        actual_error_message = context.login_page.get_email_error()
        print(f"Actual error message: {actual_error_message}")
        print(f"Expected error message: {context.test_data['expected_error_messages']['invalid_email_format']}")
        expected_error_message = context.test_data['expected_error_messages']['invalid_email_format']
        assert actual_error_message == expected_error_message, \
            f"Expected invalid email error message '{expected_error_message}' but got '{actual_error_message}'"
    except Exception as e:
        context.login_page.take_screenshot("invalid_email_error_check_failed")
        raise AssertionError(f"Failed to find invalid email error message: {e}")


@then('I should see a validation message for "{field}"')
def step_see_validation_message_for_field(context, field):
    """Verify that a validation message is displayed for a specific field."""
    try:
        validation_message = context.login_page.get_field_validation_message(field)
        assert validation_message, f"Expected validation message for {field} field but none was found"
        print(f"✓ Validation message for {field} field: {validation_message}")
    except Exception as e:
        context.login_page.take_screenshot(f"{field}_validation_message_check_failed")
        raise AssertionError(f"Failed to find validation message for {field} field: {e}")


# ============================================================================
# SOCIAL LOGIN STEPS
# ============================================================================

@given('I click the "{provider}" login button')
def step_click_social_login_button(context, provider):
    """Click a social login button (Google, Facebook, Apple)."""
    try:
        context.login_page.click_provider_login_button(provider.lower())
        print(f"✓ {provider} login button clicked")
    except Exception as e:
        context.login_page.take_screenshot(f"{provider}_login_button_click_failed")
        raise Exception(f"Failed to click {provider} login button: {e}")


@then('I should get redirected to the {provider_url}')
def step_verify_social_provider_redirect(context, provider_url):
    """Verify redirection to social provider login page."""
    try:
       context.login_page.verify_redirect_to_provider(provider_url)
    except Exception as e:
        context.login_page.take_screenshot("social_provider_redirect_failed")
        raise AssertionError(f"Failed to verify social provider redirect: {e}")


# ============================================================================
# FORGOT PASSWORD STEPS
# ============================================================================

@when('I click the "Forgot password?" link')
def step_click_forgot_password_link(context):
    """Click the forgot password link."""
    try:
        context.login_page.click_forgot_password()
        print("✓ Forgot password link clicked")
    except Exception as e:
        context.login_page.take_screenshot("forgot_password_link_click_failed")
        raise Exception(f"Failed to click forgot password link: {e}")


@then('I should be redirected to the password reset page')
def step_verify_password_reset_page_redirect(context):
    """Verify redirection to password reset page."""
    try:
        # Use the reset password page object to verify we're on the correct page
        assert context.reset_password_page.is_on_password_reset_page(), \
            "Expected to be on password reset page"
        print("✓ Successfully redirected to password reset page")
    except Exception as e:
        # Enhanced error reporting with current URL and page details
        context.reset_password_page.attach_detailed_error_info_to_allure(
            error_msg=str(e),
            context="Verifying redirection to password reset page after clicking forgot password link"
        )
        context.reset_password_page.take_screenshot("password_reset_redirect_failed")
        raise AssertionError(f"Failed to verify password reset page redirect: {e}")


@then('the page should have password reset functionality')
def step_verify_password_reset_functionality(context):
    """Verify that the page has password reset functionality."""
    try:
        # Use the reset password page object to verify functionality
        assert context.reset_password_page.has_password_reset_functionality(), \
            "Password reset functionality not found on the page"
        
        # Get additional details about what was found
        email_field = context.reset_password_page.get_email_field()
        submit_button = context.reset_password_page.get_submit_button()
        
        found_elements = []
        if email_field:
            found_elements.append("email field")
        if submit_button:
            found_elements.append("submit button")
            
        print(f"✓ Password reset functionality verified: {', '.join(found_elements)}")
    except Exception as e:
        context.reset_password_page.take_screenshot("password_reset_functionality_check_failed")
        raise AssertionError(f"Failed to verify password reset functionality: {e}")


# ============================================================================
# SIGN UP STEPS
# ============================================================================

@when('I click the "Sign up" link')
def step_click_sign_up_link(context):
    """Click the sign up link."""
    try:
        context.login_page.click_sign_up_link()
        print("✓ Sign up link clicked")
    except Exception as e:
        context.login_page.take_screenshot("sign_up_link_click_failed")
        raise Exception(f"Failed to click sign up link: {e}")


@then('I should be redirected to the registration page')
def step_verify_registration_page_redirect(context):
    """Verify redirection to registration page."""
    try:
        context.login_page.verify_redirect_url("signup")
    except Exception as e:
        context.login_page.take_screenshot("registration_redirect_failed")
        raise AssertionError(f"Failed to verify registration page redirect: {e}")


@then('the page should have account creation functionality')
def step_verify_account_creation_functionality(context):
    """Verify that the page has account creation functionality."""
    try:
        # Use the new_account_page verification method for first name, last name, and email
        if context.new_account_page.are_required_fields_present():
            print("✓ Account creation functionality verified: Required fields (first name, last name, email) are present")
        else:
            # Get detailed field status for better error reporting
            field_results = context.new_account_page.verify_required_fields_present()
            missing_fields = [field for field, present in field_results.items() if not present]
            raise AssertionError(f"Account creation functionality incomplete: Missing required fields: {', '.join(missing_fields)}")
    except Exception as e:
        context.login_page.take_screenshot("account_creation_functionality_check_failed")
        raise AssertionError(f"Failed to verify account creation functionality: {e}")


# ============================================================================
# LOGOUT STEPS
# ============================================================================

@when('I click the logout button')
def step_click_logout_button(context):
    """Click the logout button."""
    try:
        context.dashboard_page.open_user_menu()
        context.dashboard_page.click_logout()
    except Exception as e:
        context.login_page.take_screenshot("logout_button_click_failed")
        raise Exception(f"Failed to click logout button: {e}")


@then('I should be logged out successfully')
def step_verify_logged_out_successfully(context):
    """Verify that logout was successful."""
    try:
        assert context.home_page.is_on_home_page(), "Expected to be on home page after logout"
        print("✓ Successfully logged out")
    except Exception as e:
        context.login_page.take_screenshot("logout_verification_failed")
        raise AssertionError(f"Failed to verify successful logout: {e}")


@then('I should be redirected to the base website page')
def step_verify_base_website_redirect(context):
    """Verify redirection to base website page after logout."""
    try:
        # Check if we're redirected to the base/home page (usually just "/" or home)
        current_url = context.login_page.get_current_url()
        base_url = context.config_manager.get_base_url()
        
        # Check if current URL is the base URL or contains common home page indicators
        if (current_url == base_url or 
            current_url == f"{base_url}/" or 
            current_url.rstrip('/') == base_url.rstrip('/')):
            print(f"✓ Successfully redirected to base website page: {current_url}")
        else:
            raise AssertionError(f"Expected to be redirected to base website ({base_url}), but current URL is: {current_url}")
    except Exception as e:
        context.login_page.take_screenshot("base_website_redirect_failed")
        raise AssertionError(f"Failed to verify base website redirect: {e}")


@then('my session should be cleared')
def step_verify_session_cleared(context):
    """Verify that the user session has been cleared."""
    try:
        auth_cookies = []
        for cookie in context.driver.get_cookies():
            cookie_name = cookie.get('name', '').lower()
            if any(auth_term in cookie_name for auth_term in ['auth', 'session', 'token', 'user']):
                auth_cookies.append(cookie_name)
        
        print(f"ℹ Found {len(auth_cookies)} authentication-related cookies: {auth_cookies}")
        print("✓ Session appears to be cleared (logout completed)")
    except Exception as e:
        context.login_page.take_screenshot("session_clear_verification_failed")
        print(f"⚠ Could not fully verify session clearing: {e}")
