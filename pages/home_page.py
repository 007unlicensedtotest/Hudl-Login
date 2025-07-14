"""
Home page object for Hudl main website.
Contains elements and interactions for the Hudl homepage before login.
"""

from selenium.webdriver.common.by import By
from typing import Dict, Any, Optional
from pages.base_page import BasePage


class HomePage(BasePage):
    """Page object for Hudl main homepage."""
    
    # Page URL
    HOME_URL = "/"
    
    # Login element
    LOGIN_BUTTON = (By.CSS_SELECTOR, "[data-qa-id='login-select']")
    
    def __init__(self, driver, config=None):
        """
        Initialize home page.
        
        Args:
            driver: WebDriver instance
            config: Configuration manager instance
        """
        super().__init__(driver, config)
    
    def click_login_button(self) -> None:
        """
        Click the login button to navigate to login page.
        """
        self.click_element(self.LOGIN_BUTTON)
    
    def is_login_button_visible(self) -> bool:
        """
        Check if the login button is visible on the page.
        
        Returns:
            True if login button is visible, False otherwise
        """
        return self.is_element_visible(self.LOGIN_BUTTON, timeout=5)
    
    def is_on_home_page(self) -> bool:
        """
        Check if user is on the main home page.
        
        Returns:
            True if on home page, False otherwise
        """
        current_url = self.get_current_url()
        return (self.HOME_URL in current_url or 
                current_url.endswith('/') or
                self.is_element_present(self.LOGIN_BUTTON, timeout=5))
    
    def get_login_button_text(self) -> str:
        """
        Get the text of the login button.
        
        Returns:
            Login button text or empty string if not found
        """
        try:
            return self.get_element_text(self.LOGIN_BUTTON)
        except Exception:
            return ""
    
    def wait_for_page_load(self, timeout: int = 15) -> bool:
        """
        Wait for home page to fully load.
        
        Args:
            timeout: Timeout in seconds
            
        Returns:
            True if page loaded, False if timeout
        """
        try:
            # Wait for login button to appear
            self.wait_for_element_visible(self.LOGIN_BUTTON, timeout=timeout)
            return True
        except Exception:
            return False
    
    def navigate_to_login(self) -> None:
        """
        Navigate to the login page by clicking the login button.
        """
        self.click_login_button()
        
    def get_page_info(self) -> Dict[str, Any]:
        """
        Get comprehensive page information.
        
        Returns:
            Dictionary with page information
        """
        return {
            'url': self.get_current_url(),
            'title': self.get_page_title(),
            'login_button_visible': self.is_login_button_visible(),
            'login_button_text': self.get_login_button_text(),
            'on_home_page': self.is_on_home_page()
        }
