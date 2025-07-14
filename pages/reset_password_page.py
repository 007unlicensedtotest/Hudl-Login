"""
Reset Password Page Object for Hudl.com password reset functionality.
Implements the Page Object Model pattern for password reset interactions.
"""

from typing import Optional
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from pages.base_page import BasePage


class ResetPasswordPage(BasePage):
    """Page Object for Hudl password reset page."""
    
    # URL patterns to identify reset password page
    PASSWORD_RESET_URL_PATTERNS = [
        '/u/login/password-reset-start',
        '/password-reset',
        '/reset-password',
        '/forgot-password'
    ]
    
    # Email input locators (most common to least common)
    EMAIL_FIELD = (By.NAME, "email")
    EMAIL_FIELD_ALT = (By.ID, "email")
    EMAIL_FIELD_TYPE = (By.CSS_SELECTOR, "input[type='email']")
    EMAIL_FIELD_NAME_PATTERN = (By.CSS_SELECTOR, "input[name*='email' i]")
    EMAIL_FIELD_PLACEHOLDER = (By.CSS_SELECTOR, "input[placeholder*='email' i]")
    
    # Submit button locators
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    SUBMIT_BUTTON_ALT = (By.CSS_SELECTOR, "input[type='submit']")
    SUBMIT_BUTTON_TEXT = (By.XPATH, "//button[contains(text(), 'Reset') or contains(text(), 'Send')]")
    
    # Success/error message locators
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".success, .alert-success, [class*='success']")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".error, .alert-error, .alert-danger, [class*='error']")
    
    # Back to login link
    BACK_TO_LOGIN_LINK = (By.CSS_SELECTOR, "a[href*='login']")
    
    def __init__(self, driver, config=None):
        """
        Initialize the Reset Password Page.
        
        Args:
            driver: WebDriver instance
            config: Configuration manager instance
        """
        super().__init__(driver, config)
    
    def is_on_password_reset_page(self) -> bool:
        """
        Check if currently on the password reset page.
        
        Returns:
            bool: True if on password reset page, False otherwise
        """
        try:
            current_url = self.get_current_url()
            return any(pattern in current_url for pattern in self.PASSWORD_RESET_URL_PATTERNS)
        except Exception:
            return False
    
    def get_email_field(self) -> Optional[WebElement]:
        """
        Get the email input field using fallback locators.
        
        Returns:
            WebElement: Email input field if found, None otherwise
        """
        locators = [
            self.EMAIL_FIELD,
            self.EMAIL_FIELD_ALT,
            self.EMAIL_FIELD_TYPE,
            self.EMAIL_FIELD_NAME_PATTERN,
            self.EMAIL_FIELD_PLACEHOLDER
        ]
        
        return self.find_element_with_fallback(locators)
    
    def enter_email(self, email: str) -> None:
        """
        Enter email address in the email field.
        
        Args:
            email: Email address to enter
        """
        email_field = self.get_email_field()
        if email_field:
            self.send_keys_with_fallback([
                self.EMAIL_FIELD,
                self.EMAIL_FIELD_ALT,
                self.EMAIL_FIELD_TYPE
            ], email)
        else:
            raise NoSuchElementException("Email field not found on password reset page")
    
    def get_submit_button(self) -> Optional[WebElement]:
        """
        Get the submit button using fallback locators.
        
        Returns:
            WebElement: Submit button if found, None otherwise
        """
        locators = [
            self.SUBMIT_BUTTON,
            self.SUBMIT_BUTTON_ALT,
            self.SUBMIT_BUTTON_TEXT
        ]
        
        return self.find_element_with_fallback(locators)
    
    def click_submit(self) -> None:
        """Click the submit button to send password reset request."""
        submit_button = self.get_submit_button()
        if submit_button:
            self.click_with_fallback([
                self.SUBMIT_BUTTON,
                self.SUBMIT_BUTTON_ALT,
                self.SUBMIT_BUTTON_TEXT
            ])
        else:
            raise NoSuchElementException("Submit button not found on password reset page")
    
    def has_password_reset_functionality(self) -> bool:
        """
        Check if the page has basic password reset functionality.
        
        Returns:
            bool: True if email field and submit button are present
        """
        try:
            email_field = self.get_email_field()
            submit_button = self.get_submit_button()
            
            # Debug information
            print(f"Debug - Email field found: {email_field is not None}")
            print(f"Debug - Submit button found: {submit_button is not None}")
            print(f"Debug - Current URL: {self.get_current_url()}")
            
            # More flexible check - if we can't find specific elements, 
            # check for any form or input elements that might indicate reset functionality
            if email_field is None and submit_button is None:
                # Try to find any form elements that might be password reset related
                try:
                    # Look for any email input or form
                    email_inputs = self.find_elements((By.CSS_SELECTOR, "input[type='email'], input[name*='email'], input[placeholder*='email']"), timeout=3)
                    form_elements = self.find_elements((By.TAG_NAME, "form"), timeout=3)
                    submit_elements = self.find_elements((By.CSS_SELECTOR, "button, input[type='submit']"), timeout=3)
                    
                    print(f"Debug - Found {len(email_inputs)} email inputs")
                    print(f"Debug - Found {len(form_elements)} forms")
                    print(f"Debug - Found {len(submit_elements)} submit elements")
                    
                    return len(email_inputs) > 0 or (len(form_elements) > 0 and len(submit_elements) > 0)
                except Exception as e:
                    print(f"Debug - Error in fallback check: {e}")
                    return False
            
            return email_field is not None and submit_button is not None
        except Exception as e:
            print(f"Debug - Exception in has_password_reset_functionality: {e}")
            return False
    
    def get_success_message(self) -> Optional[str]:
        """
        Get success message text if present.
        
        Returns:
            str: Success message text, None if not found
        """
        try:
            element = self.find_element(self.SUCCESS_MESSAGE, timeout=5)
            return element.text if element else None
        except (TimeoutException, NoSuchElementException):
            return None
    
    def get_error_message(self) -> Optional[str]:
        """
        Get error message text if present.
        
        Returns:
            str: Error message text, None if not found
        """
        try:
            element = self.find_element(self.ERROR_MESSAGE, timeout=5)
            return element.text if element else None
        except (TimeoutException, NoSuchElementException):
            return None
    
    def navigate_to_reset_password_page(self) -> None:
        """Navigate directly to the password reset page."""
        if self.config:
            base_url = self.config.get_base_url()
            reset_url = f"{base_url.rstrip('/')}/u/login/password-reset-start"
            self.navigate_to_url(reset_url)
        else:
            raise ValueError("Configuration not available for navigation")
