"""
Login page object for Hudl login testing.
Contains all login page elements and interactions.
"""

import time
from selenium.webdriver.common.by import By
from typing import Dict, Any, List, Tuple, Optional
from pages.base_page import BasePage
from urllib.parse import urlparse


class LoginPage(BasePage):
    """
    Hudl login page object for authentication testing.
    Navigation should be handled explicitly in test steps following BDD principles.
    """
    
    # ====================================================================
    # CONSTANTS AND LOCATORS
    # ====================================================================
    
    # Page URL
    LOGIN_URL = "/login"
    
    # Email field locators
    EMAIL_FIELD = (By.NAME, "username")      # Primary: Works on identifier page
    EMAIL_FIELD_ALT = (By.ID, "username")    # Fallback: For other pages
    EMAIL_FIELD_TYPE = (By.CSS_SELECTOR, "input[type='email']")
    EMAIL_FIELD_NAME_PATTERN = (By.CSS_SELECTOR, "input[name*='email' i]")
    EMAIL_FIELD_PLACEHOLDER = (By.CSS_SELECTOR, "input[placeholder*='email' i]")
    
    # Password field locators
    PASSWORD_FIELD = (By.NAME, "password")   # Primary: Universal selector
    PASSWORD_FIELD_ALT = (By.ID, "password") # Fallback
    PASSWORD_FIELD_TYPE = (By.CSS_SELECTOR, "input[type='password']")
    PASSWORD_FIELD_NAME_PATTERN = (By.CSS_SELECTOR, "input[name*='password' i]")
    PASSWORD_FIELD_PLACEHOLDER = (By.CSS_SELECTOR, "input[placeholder*='password' i]")
    
    # Button locators
    CONTINUE_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")  # Primary (confirmed working)
    CONTINUE_BUTTON_ALT = (By.NAME, "action")    
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")     # Alias for continue button
    LOGIN_BUTTON_ALT = (By.NAME, "action")                       # Fallback alias
    SHOW_HIDE_PASSWORD_BUTTON = (By.CSS_SELECTOR, "button[data-action='toggle']")
    
    # Social login button locators
    GOOGLE_LOGIN_BUTTON = (By.CSS_SELECTOR, "button[data-provider='google']")
    FACEBOOK_LOGIN_BUTTON = (By.CSS_SELECTOR, "button[data-provider='facebook']")
    APPLE_LOGIN_BUTTON = (By.CSS_SELECTOR, "button[data-provider='apple']")
    
    # Link locators
    FORGOT_PASSWORD_LINK = (By.CSS_SELECTOR, "a[href*='/u/login/password-reset-start']")
    SIGN_UP_LINK = (By.CSS_SELECTOR, ".ulp-alternate-action a")
    
    # Error message locators
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".ulp-input-error-message")           # Primary selector
    EMAIL_ERROR = (By.ID, "error-element-username")                         # Specific email errors
    PASSWORD_ERROR = (By.ID, "error-element-password")                      # Specific password errors
    GENERIC_ERROR = (By.CSS_SELECTOR, "[data-qa-id='login-error']")         # Generic login errors
    INVALID_CREDENTIALS_ERROR = (By.CSS_SELECTOR, ".ulp-error-message")  # Invalid credentials error

    # User display elements (post-login)
    DISPLAY_NAME = (By.CSS_SELECTOR, ".hui-globaluseritem__display-name span")  # User display name

    # ====================================================================
    # INITIALIZATION
    # ====================================================================
    
    def __init__(self, driver, config=None) -> None:
        """
        Initialize login page without automatic navigation.
        
        Args:
            driver: WebDriver instance for browser automation
            config: Configuration manager instance (optional)
        """
        super().__init__(driver, config)
        self._page_loaded: bool = False

    # ====================================================================
    # NAVIGATION METHODS
    # ====================================================================
    
    def navigate_to_login_page(self) -> None:
        """Navigate to the login page."""
        login_url = self._get_login_url()
        print(f"Navigating to login page: {login_url}")
        self.navigate_to(login_url)
        
        # Check if we were redirected
        final_url = self.get_current_url()
        if final_url != login_url:
            print(f"Redirected from {login_url} to {final_url}")
        else:
            print(f"Successfully navigated to: {final_url}")

    def verify_redirect_url(self, path_fragment: str) -> None:
        """
        Verify redirection to application URL by checking the path.
        
        Args:
            path_fragment: Expected path fragment to verify (e.g., "password-reset", "registration")
        """
        self.wait_for_page_load(10)
        current_url = self.get_current_url()
        
        # Parse the current URL to get the path
        current_parsed = urlparse(current_url)
        current_path = current_parsed.path.lower()
        
        # Check if the path contains the expected fragment
        path_fragment_lower = path_fragment.lower()
        if path_fragment_lower not in current_path:
            assert False, f"Expected URL path to contain \"{path_fragment}\", but got path: {current_path} (full URL: {current_url})"
        
        print(f"✓ Application redirect successful: path contains '{path_fragment}'")

    def verify_redirect_to_provider(self, expected_url: str) -> None:
        """
        Verify redirection to external provider by checking the domain/host.
        
        Args:
            expected_url: Expected provider URL to verify (domain will be checked)
        """
        self.wait_for_page_load(10)
        current_url = self.get_current_url()
        
        # Strip quotes from expected URL if present
        expected_url_clean = expected_url.strip('"\'')
        
        # Parse both URLs to compare domains
        current_parsed = urlparse(current_url)
        expected_parsed = urlparse(expected_url_clean)
        
        # Check if the domain matches (allowing for OAuth parameters and path differences)
        current_domain = current_parsed.netloc.lower()
        expected_domain = expected_parsed.netloc.lower()
        
        if expected_domain not in current_domain and current_domain != expected_domain:
            assert False, f"Expected to be redirected to domain \"{expected_domain}\", but got domain: {current_domain} (full URL: {current_url})"
        
        print(f"✓ Provider redirect successful: redirected to {expected_domain}")

    # ====================================================================
    # FIELD INTERACTION METHODS (Generic)
    # ====================================================================
    
    def enter_field_value(self, field_type: str, value: str) -> None:
        """
        Enter value into any field using field type.
        
        Args:
            field_type: Type of field ('email' or 'password')
            value: Value to enter
        """
        locators = self._get_field_locators(field_type)
        self._try_locators_with_action(
            locators,
            self.send_keys_to_element,
            f"{field_type.title()} entry",
            value
        )
    
    def clear_field(self, field_type: str) -> None:
        """
        Clear any field using field type.
        
        Args:
            field_type: Type of field ('email' or 'password')
        """
        locators = self._get_field_locators(field_type)
        self._try_locators_with_action(
            locators,
            self._clear_element_with_locator,
            f"{field_type.title()} field clear"
        )

    def get_field_error(self, field_type: str) -> str:
        """
        Get error message for any field using field type.
        
        Args:
            field_type: Type of field ('email' or 'password')
            
        Returns:
            Field error message or empty string if no error
        """
        field_error_locators = {
            'email': self.EMAIL_ERROR,
            'password': self.PASSWORD_ERROR
        }
        
        error_locator = field_error_locators.get(field_type.lower())
        if not error_locator:
            raise ValueError(f"Unsupported field type: {field_type}")
            
        try:
            return self.get_element_text(error_locator)
        except Exception:
            return ""

    # ====================================================================
    # FIELD INTERACTION METHODS (Backward Compatibility)
    # ====================================================================
    
    def enter_email(self, email: str) -> None:
        """Enter email address using confirmed working locators."""
        self.enter_field_value('email', email)
    
    def enter_password(self, password: str) -> None:
        """Enter password using confirmed working locators."""
        self.enter_field_value('password', password)
    
    def clear_email(self) -> None:
        """Clear the email field."""
        self.clear_field('email')
    
    def clear_password(self) -> None:
        """Clear the password field."""
        self.clear_field('password')
    
    def get_email_error(self) -> str:
        """Get email field error message."""
        return self.get_field_error('email')
    
    def get_invalid_credentials_error(self) -> str:
        """Get invalid credentials error message."""
        #Invalid credentials shows on the password field
        return self.get_field_error('password')

    def get_password_error(self) -> str:
        """Get password field error message."""
        return self.get_field_error('password')

    # ====================================================================
    # BUTTON AND LINK INTERACTION METHODS
    # ====================================================================
    
    def click_continue_button(self) -> None:
        """Click the continue button using confirmed working selectors."""
        locators = self._get_field_locators('continue_button')
        self._try_locators_with_action(
            locators,
            self.click_element,
            "Continue button click"
        )

    def click_forgot_password(self) -> None:
        """Click the forgot password link."""
        self.click_element(self.FORGOT_PASSWORD_LINK)

    def click_sign_up_link(self) -> None:
        """Click the sign up link."""
        self.click_element(self.SIGN_UP_LINK)

    def click_show_hide_password(self) -> None:
        """Click the show/hide password button."""
        self.click_element(self.SHOW_HIDE_PASSWORD_BUTTON)
    
    def click_provider_login_button(self, provider: str) -> None:
        """Click a social login button based on provider."""
        provider = provider.lower().strip('"\'')  # Remove quotes and convert to lowercase
        if provider == 'google':
            self.click_element(self.GOOGLE_LOGIN_BUTTON)
        elif provider == 'facebook':
            self.click_element(self.FACEBOOK_LOGIN_BUTTON)
        elif provider == 'apple':
            self.click_element(self.APPLE_LOGIN_BUTTON)
        else:
            raise ValueError(f"Unsupported social login provider: {provider}")

    # ====================================================================
    # VALIDATION AND ERROR HANDLING METHODS
    # ====================================================================
    
    def get_validation_message(self, field_locator: Optional[Tuple[str, str]] = None) -> str:
        """
        Get HTML5 validation message for a field.
        
        Args:
            field_locator: Field locator tuple, defaults to EMAIL_FIELD
            
        Returns:
            Validation message or empty string
        """
        try:
            # Use email field by default
            locator = field_locator or self.EMAIL_FIELD
            
            # Get validation message using base page method
            validation_message = self.get_element_attribute(locator, "validationMessage", timeout=1)
            if validation_message:
                print(f"Found validation message: '{validation_message}'")
                return validation_message
            return ""
            
        except Exception as e:
            print(f"Error getting validation message: {e}")
            return ""
    
    def get_field_validation_message(self, field_name: str) -> str:
        """
        Get HTML5 validation message for any form field.
        
        Args:
            field_name: The field name ('email', 'password')
            
        Returns:
            Validation message string or empty string if none found
        """
        # Map field names to their input field locators
        field_input_locators = {
            'email': self.EMAIL_FIELD,
            'password': self.PASSWORD_FIELD
        }
        
        input_locator = field_input_locators.get(field_name.lower())
        if not input_locator:
            print(f"❌ Unknown field name: {field_name}")
            return ""
        
        # Delegate to the main validation message method
        return self.get_validation_message(input_locator)

    def get_error_message(self) -> str:
        """
        Get general error message from multiple possible locations.
        
        Returns:
            Error message text or empty string if no error
        """
        # Try different error detection strategies
        error_detection_strategies = [
            self._find_error_by_locators,
            self._find_error_by_text_patterns
        ]
        
        for strategy in error_detection_strategies:
            error_message = strategy()
            if error_message:
                return error_message
        
        print("No error message found on page")
        return ""

    def get_empty_field_error(self, element_locator) -> str:
        """
        Get error message for empty fields.
        
        Args:
            element_locator: Tuple containing locator strategy and value
        
        Returns:
            Error message if fields are empty, otherwise empty string
        """
        try:
            # Find the specific element using the provided locator
            element = self.find_element(element_locator)
            validation_message = element.get_attribute("validationMessage")
            print(f"Validation message for {element_locator}: '{validation_message}'")
            return validation_message or ""
            
        except Exception as e:
            print(f"Error getting validation message for {element_locator}: {e}")
            return ""
    
    def has_error_message(self) -> bool:
        """
        Check if any error message is displayed.
        
        Returns:
            True if error message present, False otherwise
        """
        error_timeout = self.config.get_error_timeout() if self.config else 3
        return (self.is_element_visible(self.ERROR_MESSAGE, timeout=error_timeout) or
                self.is_element_visible(self.EMAIL_ERROR, timeout=error_timeout) or
                self.is_element_visible(self.PASSWORD_ERROR, timeout=error_timeout) or
                self.is_element_visible(self.GENERIC_ERROR, timeout=error_timeout))

    # ====================================================================
    # PAGE STATE AND INSPECTION METHODS
    # ====================================================================
    
    def is_login_page_loaded(self) -> bool:
        """Check if currently on login page."""
        current_url = self.driver.current_url
        return "login" in current_url.lower()
    
    def is_password_visible(self) -> bool:
        """
        Check if password is visible by examining the input field type.
        
        Returns:
            True if password is visible (type='text'), False if masked (type='password')
        """
        try:
            password_field = self.find_element(self.PASSWORD_FIELD)
            field_type = password_field.get_attribute("type")
            is_visible = field_type == "text"
            print(f"Password field type: '{field_type}' - {'visible' if is_visible else 'masked'}")
            return is_visible
        except Exception as e:
            print(f"Error checking password visibility: {e}")
            return False

    def get_password_value(self) -> str:
        """
        Get current password field value.
        
        Returns:
            Password field value
        """
        try:
            return self.get_element_attribute(self.PASSWORD_FIELD, "value")
        except Exception:
            return self.get_element_attribute(self.PASSWORD_FIELD_ALT, "value")
    
    def is_login_button_enabled(self) -> bool:
        """
        Check if login button is enabled.
        
        Returns:
            True if enabled, False otherwise
        """
        try:
            element = self.find_element(self.LOGIN_BUTTON)
            return element.is_enabled()
        except Exception:
            try:
                element = self.find_element(self.LOGIN_BUTTON_ALT)
                return element.is_enabled()
            except Exception:
                return False
    
    def has_social_login_options(self) -> bool:
        """
        Check if social login options are available.
        
        Returns:
            True if social login options present, False otherwise
        """
        social_timeout = self.config.get_social_login_timeout() if self.config else 2
        return (self.is_element_present(self.GOOGLE_LOGIN_BUTTON, timeout=social_timeout) or
                self.is_element_present(self.FACEBOOK_LOGIN_BUTTON, timeout=social_timeout))

    def get_page_info(self) -> Dict[str, Any]:
        """
        Get comprehensive page information.
        
        Returns:
            Dictionary with page information
        """
        return {
            'url': self.get_current_url(),
            'title': self.get_page_title(),
            'password_value': self.get_password_value(),
            'login_button_enabled': self.is_login_button_enabled(),
            'has_errors': self.has_error_message(),
            'error_message': self.get_error_message()
        }

    def get_display_name(self) -> str:
        """
        Get the user's display name after successful login.
        
        Returns:
            The display name text, or empty string if not found
        """
        try:
            display_name_element = self.wait_for_element_visible(self.DISPLAY_NAME, timeout=10)
            return display_name_element.text.strip() if display_name_element else ""
        except Exception:
            return ""
    
    def is_display_name_visible(self) -> bool:
        """
        Check if the user's display name is visible (indicates successful login).
        
        Returns:
            True if display name is visible, False otherwise
        """
        return self.is_element_present(self.DISPLAY_NAME, timeout=5)

    # ====================================================================
    # PRIVATE UTILITY METHODS
    # ====================================================================
    
    def _get_login_url(self) -> str:
        """Get full login URL."""
        if self.config:
            return self.config.get_login_url()
        else:
            base_url = "https://www.hudl.com"
            return f"{base_url}{self.LOGIN_URL}"
    
    def _get_field_locators(self, field_type: str) -> List[Tuple[str, str]]:
        """
        Get list of field locators in order of preference for any field type.
        
        Args:
            field_type: Type of field ('email', 'password', 'continue_button')
        
        Returns:
            List of locator tuples for the specified field
            
        Raises:
            ValueError: If field_type is not supported
        """
        field_locator_map = {
            'email': [
                self.EMAIL_FIELD,                # Primary: input[name='username']
                self.EMAIL_FIELD_ALT,            # Fallback: input[id='username']
                self.EMAIL_FIELD_TYPE,           # Type-based: input[type='email']
                self.EMAIL_FIELD_NAME_PATTERN,   # Name pattern: input[name*='email' i]
                self.EMAIL_FIELD_PLACEHOLDER     # Placeholder: input[placeholder*='email' i]
            ],
            'password': [
                self.PASSWORD_FIELD,                # Primary: input[name='password']
                self.PASSWORD_FIELD_ALT,            # Fallback: input[id='password'] 
                self.PASSWORD_FIELD_TYPE,           # Type-based: input[type='password']
                self.PASSWORD_FIELD_NAME_PATTERN,   # Name pattern: input[name*='password' i]
                self.PASSWORD_FIELD_PLACEHOLDER     # Placeholder: input[placeholder*='password' i]
            ],
            'continue_button': [
                self.CONTINUE_BUTTON,     # Primary: button[type='submit']
                self.CONTINUE_BUTTON_ALT  # Fallback: input[name='action']
            ]
        }
        
        locators = field_locator_map.get(field_type.lower())
        if not locators:
            raise ValueError(f"Unsupported field type: {field_type}. Supported types: {list(field_locator_map.keys())}")
        
        return locators

    def _get_email_locators(self) -> List[Tuple[str, str]]:
        """Get list of email field locators in order of preference."""
        return self._get_field_locators('email')
    
    def _get_password_locators(self) -> List[Tuple[str, str]]:
        """Get list of password field locators in order of preference."""
        return self._get_field_locators('password')
    
    def _get_continue_button_locators(self) -> List[Tuple[str, str]]:
        """Get list of continue button locators in order of preference."""
        return self._get_field_locators('continue_button')
    
    def _try_locators_with_action(self, locators: List[Tuple[str, str]], action_func, field_name: str, *args) -> None:
        """
        Try multiple locators with a given action function until one succeeds.
        
        Args:
            locators: List of locator tuples to try
            action_func: Function to execute on found element
            field_name: Name of field for error messages
            *args: Additional arguments to pass to action_func
            
        Raises:
            Exception: If none of the locators work
        """
        for locator in locators:
            try:
                action_func(locator, *args)
                print(f"✓ {field_name} action successful using locator: {locator}")
                return
            except Exception as e:
                print(f"Failed {field_name} action with locator {locator}: {e}")
                continue
        
        raise Exception(f"Could not find {field_name} with any of the available locators")
    
    def _clear_element_with_locator(self, locator: Tuple[str, str], *args) -> None:
        """
        Helper method to clear an element using wait and clear.
        
        Args:
            locator: Element locator tuple
            *args: Additional arguments (not used for clear action)
        """
        element = self.find_visible_element(locator)
        element.clear()

    def _find_error_by_locators(self) -> str:
        """
        Find error message using predefined error locators.
        
        Returns:
            Error message text or empty string if none found
        """
        error_locators = [
            self.ERROR_MESSAGE,
            self.GENERIC_ERROR,
            self.EMAIL_ERROR,
            self.PASSWORD_ERROR
        ]
        
        error_timeout = self.config.get_error_timeout() if self.config else 3
        
        for locator in error_locators:
            try:
                element = self.find_visible_element(locator, timeout=error_timeout)
                if element:
                    error_text = element.text.strip()
                    if error_text:  # Only return non-empty error messages
                        print(f"Found error message: '{error_text}' using locator: {locator}")
                        return error_text
            except Exception as e:
                print(f"No error found with locator {locator}: {e}")
                continue
        return ""
    
    def _find_error_by_text_patterns(self) -> str:
        """
        Find error message by searching for common error text patterns.
        
        Returns:
            Error message text or empty string if none found
        """
        try:
            error_patterns = [
                "incorrect", "invalid", "wrong", "error", "failed", 
                "not found", "does not exist", "try again", "password"
            ]
            
            for pattern in error_patterns:
                xpath = f"//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{pattern}')]"
                elements = self.find_elements((By.XPATH, xpath))
                for element in elements:
                    if element.is_displayed() and element.text.strip():
                        error_text = element.text.strip()
                        print(f"Found error by text pattern '{pattern}': '{error_text}'")
                        return error_text
        except Exception as e:
            print(f"Error searching by text patterns: {e}")
        return ""
