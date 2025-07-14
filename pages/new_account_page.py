"""
New Account page object for Hudl registration testing.
Contains all account creation/registration page elements and interactions.
"""

import time
from selenium.webdriver.common.by import By
from typing import Dict, Any, List, Tuple, Optional
from pages.base_page import BasePage
from urllib.parse import urlparse


class NewAccountPage(BasePage):
    """
    Hudl new account/registration page object for user registration testing.
    Handles all interactions with the sign-up/registration form.
    """
    
    # ====================================================================
    # CONSTANTS AND LOCATORS
    # ====================================================================
    
    # Page URLs
    REGISTRATION_URL = "/register"
    SIGNUP_URL = "/signup"
    
    # Personal Information Fields
    FIRST_NAME_FIELD = (By.NAME, "ulp-first-name")
    FIRST_NAME_FIELD_ALT = (By.ID, "first-name")
    FIRST_NAME_FIELD_CSS = (By.CSS_SELECTOR, "input[name*='first' i]")
    
    LAST_NAME_FIELD = (By.NAME, "ulp-last-name")
    LAST_NAME_FIELD_ALT = (By.ID, "last-name")
    LAST_NAME_FIELD_CSS = (By.CSS_SELECTOR, "input[name*='last' i]")
    
    
    # Email field locators
    EMAIL_FIELD = (By.NAME, "email")
    EMAIL_FIELD_ALT = (By.ID, "email")
    EMAIL_FIELD_TYPE = (By.CSS_SELECTOR, "input[type='email']")
    EMAIL_FIELD_NAME_PATTERN = (By.CSS_SELECTOR, "input[name*='email' i]")
    EMAIL_FIELD_PLACEHOLDER = (By.CSS_SELECTOR, "input[placeholder*='email' i]")
    
    
    # Social registration buttons
    GOOGLE_SIGNUP_BUTTON = (By.CSS_SELECTOR, "button[data-provider='google']")
    FACEBOOK_SIGNUP_BUTTON = (By.CSS_SELECTOR, "button[data-provider='facebook']")
    APPLE_SIGNUP_BUTTON = (By.CSS_SELECTOR, "button[data-provider='apple']")
    
    # Link locators
    LOGIN_LINK = (By.CSS_SELECTOR, "a[href*='/login']")
    TERMS_LINK = (By.CSS_SELECTOR, "a[href*='/terms']")
    PRIVACY_LINK = (By.CSS_SELECTOR, "a[href*='/privacy']")
    
    
    # ====================================================================
    # INITIALIZATION
    # ====================================================================
    
    def __init__(self, driver, config=None) -> None:
        """
        Initialize new account page.
        
        Args:
            driver: WebDriver instance for browser automation
            config: Configuration manager instance (optional)
        """
        super().__init__(driver, config)
        self._page_loaded: bool = False

    # ====================================================================
    # NAVIGATION METHODS
    # ====================================================================
    
    def navigate_to_registration_page(self) -> None:
        """Navigate to the account creation/registration page."""
        registration_url = self._get_registration_url()
        print(f"Navigating to registration page: {registration_url}")
        self.navigate_to(registration_url)
        
        # Check if we were redirected
        final_url = self.get_current_url()
        if final_url != registration_url:
            print(f"Redirected from {registration_url} to {final_url}")
        else:
            print(f"Successfully navigated to: {final_url}")

    def _get_registration_url(self) -> str:
        """Get the full registration URL."""
        if self.config:
            base_url = self.config.get_base_url()
            return f"{base_url.rstrip('/')}{self.REGISTRATION_URL}"
        return f"https://www.hudl.com{self.REGISTRATION_URL}"

    # ====================================================================
    # PERSONAL INFORMATION METHODS
    # ====================================================================
    
    def enter_first_name(self, first_name: str) -> None:
        """
        Enter first name in the first name field.
        
        Args:
            first_name: First name to enter
        """
        locators = [
            self.FIRST_NAME_FIELD,
            self.FIRST_NAME_FIELD_ALT,
            self.FIRST_NAME_FIELD_CSS
        ]
        self.send_keys_with_fallback(locators, first_name, "first name field")

    def enter_last_name(self, last_name: str) -> None:
        """
        Enter last name in the last name field.
        
        Args:
            last_name: Last name to enter
        """
        locators = [
            self.LAST_NAME_FIELD,
            self.LAST_NAME_FIELD_ALT,
            self.LAST_NAME_FIELD_CSS
        ]
        self.send_keys_with_fallback(locators, last_name, "last name field")

    def enter_full_name(self, full_name: str) -> None:
        """
        Enter full name in the full name field (if single name field is used).
        
        Args:
            full_name: Full name to enter
        """
        locators = [
            self.FULL_NAME_FIELD,
            self.FULL_NAME_FIELD_ALT,
            self.FULL_NAME_FIELD_CSS
        ]
        self.send_keys_with_fallback(locators, full_name, "full name field")

    def enter_email(self, email: str) -> None:
        """
        Enter email address in the email field.
        
        Args:
            email: Email address to enter
        """
        locators = [
            self.EMAIL_FIELD,
            self.EMAIL_FIELD_ALT,
            self.EMAIL_FIELD_TYPE,
            self.EMAIL_FIELD_NAME_PATTERN,
            self.EMAIL_FIELD_PLACEHOLDER
        ]
        self.send_keys_with_fallback(locators, email, "email field")

    def enter_password(self, password: str) -> None:
        """
        Enter password in the password field.
        
        Args:
            password: Password to enter
        """
        locators = [
            self.PASSWORD_FIELD,
            self.PASSWORD_FIELD_ALT,
            self.PASSWORD_FIELD_TYPE,
            self.PASSWORD_FIELD_NAME_PATTERN
        ]
        self.send_keys_with_fallback(locators, password, "password field")

    def enter_confirm_password(self, password: str) -> None:
        """
        Enter password confirmation in the confirm password field.
        
        Args:
            password: Password to confirm
        """
        locators = [
            self.CONFIRM_PASSWORD_FIELD,
            self.CONFIRM_PASSWORD_FIELD_ALT,
            self.CONFIRM_PASSWORD_FIELD_CSS
        ]
        self.send_keys_with_fallback(locators, password, "confirm password field")

    # ====================================================================
    # BUTTON INTERACTION METHODS
    # ====================================================================
    
    def click_create_account_button(self) -> None:
        """Click the create account/submit button."""
        locators = [
            self.CREATE_ACCOUNT_BUTTON,
            self.CREATE_ACCOUNT_BUTTON_ALT,
            self.SIGNUP_BUTTON,
            self.REGISTER_BUTTON
        ]
        self.click_with_fallback(locators, "create account button")

    def click_login_link(self) -> None:
        """Click the login link to go to login page."""
        self.click_element(self.LOGIN_LINK)
        print("✓ Clicked login link")

    def verify_required_fields_present(self) -> Dict[str, bool]:
        """
        Verify that the required form fields (first name, last name, email) are present on the page.
        
        Returns:
            Dictionary with field names as keys and boolean values indicating presence
        """
        field_results = {}
        
        # Check first name field
        first_name_locators = [
            self.FIRST_NAME_FIELD,
            self.FIRST_NAME_FIELD_ALT,
            self.FIRST_NAME_FIELD_CSS
        ]
        field_results["first_name"] = self.is_element_visible_with_fallback(first_name_locators, "first name field")
        
        # Check last name field
        last_name_locators = [
            self.LAST_NAME_FIELD,
            self.LAST_NAME_FIELD_ALT,
            self.LAST_NAME_FIELD_CSS
        ]
        field_results["last_name"] = self.is_element_visible_with_fallback(last_name_locators, "last name field")
        
        # Check email field
        email_locators = [
            self.EMAIL_FIELD,
            self.EMAIL_FIELD_ALT,
            self.EMAIL_FIELD_TYPE,
            self.EMAIL_FIELD_NAME_PATTERN,
            self.EMAIL_FIELD_PLACEHOLDER
        ]
        field_results["email"] = self.is_element_visible_with_fallback(email_locators, "email field")
        
        return field_results

    def are_required_fields_present(self) -> bool:
        """
        Check if all required fields (first name, last name, email) are present on the page.
        
        Returns:
            True if all required fields are present, False otherwise
        """
        field_results = self.verify_required_fields_present()
        all_present = all(field_results.values())
        
        if all_present:
            print("✓ All required fields (first name, last name, email) are present")
        else:
            missing_fields = [field for field, present in field_results.items() if not present]
            print(f"✗ Missing required fields: {', '.join(missing_fields)}")
        
        return all_present

    def verify_form_elements_visible(self) -> Dict[str, bool]:
        """
        Comprehensive verification of form elements visibility.
        
        Returns:
            Dictionary with element names as keys and visibility status as values
        """
        elements_to_check = {
            "first_name_field": [self.FIRST_NAME_FIELD, self.FIRST_NAME_FIELD_ALT, self.FIRST_NAME_FIELD_CSS],
            "last_name_field": [self.LAST_NAME_FIELD, self.LAST_NAME_FIELD_ALT, self.LAST_NAME_FIELD_CSS],
            "email_field": [self.EMAIL_FIELD, self.EMAIL_FIELD_ALT, self.EMAIL_FIELD_TYPE],
            "password_field": [self.PASSWORD_FIELD, self.PASSWORD_FIELD_ALT, self.PASSWORD_FIELD_TYPE],
            "create_account_button": [self.CREATE_ACCOUNT_BUTTON, self.CREATE_ACCOUNT_BUTTON_ALT, self.SIGNUP_BUTTON]
        }
        
        visibility_results = {}
        
        for element_name, locators in elements_to_check.items():
            visibility_results[element_name] = self.is_element_visible_with_fallback(locators, element_name)
        
        return visibility_results

    # ====================================================================
    # PRIVATE HELPER METHODS
    # ====================================================================
    
    def _find_field_with_fallback(self, locators: List[Tuple[str, str]], field_name: str):
        """
        Find field using multiple locator strategies with fallback.
        Uses the base page find_element_with_fallback method.
        
        Args:
            locators: List of locator tuples to try
            field_name: Name of the field for error reporting
            
        Returns:
            WebElement if found
            
        Raises:
            Exception if field not found with any locator
        """
        return self.find_element_with_fallback(locators, field_name)

    def _get_error_text(self, locators: List[Tuple[str, str]], error_type: str) -> str:
        """
        Get error text using multiple locator strategies.
        
        Args:
            locators: List of locator tuples to try
            error_type: Type of error for logging
            
        Returns:
            Error text or empty string if not found
        """
        return self.get_text_with_fallback(locators, error_type)

    def _get_text_from_elements(self, locators: List[Tuple[str, str]], element_type: str) -> str:
        """
        Get text from elements using multiple locator strategies.
        Uses the base page get_text_with_fallback method.
        
        Args:
            locators: List of locator tuples to try
            element_type: Type of element for logging
            
        Returns:
            Element text or empty string if not found
        """
        return self.get_text_with_fallback(locators, element_type)
