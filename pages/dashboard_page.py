"""
Dashboard page object for post-login verification.
Contains elements and interactions for the Hudl dashboard page.
"""

from selenium.webdriver.common.by import By
from typing import Dict, Any, List, Optional
from pages.base_page import BasePage


class DashboardPage(BasePage):
    """Page object for Hudl dashboard page."""
    
    # Page URLs
    HOME_URL = "/home"
    DASHBOARD_URL = "/dashboard"
    
    # Header elements
    USER_MENU = (By.CLASS_NAME, "hui-globalusermenu")
    USER_AVATAR = (By.CSS_SELECTOR, ".user-avatar")
    DISPLAY_NAME = (By.CLASS_NAME, "hui-globaluseritem__display-name")
    LOGOUT_BUTTON = (By.CSS_SELECTOR, "[data-qa-id='webnav-usermenu-logout']")
    SETTINGS_LINK = (By.CSS_SELECTOR, "[data-qa-id='settings-link']")
    
    # Navigation elements
    MAIN_NAVIGATION = (By.CSS_SELECTOR, ".main-nav")
    HOME_TAB = (By.CSS_SELECTOR, "[data-qa-id='home-tab']")
    HIGHLIGHTS_TAB = (By.CSS_SELECTOR, "[data-qa-id='highlights-tab']")
    TOOLS_TAB = (By.CSS_SELECTOR, "[data-qa-id='tools-tab']")
    LIBRARY_TAB = (By.CSS_SELECTOR, "[data-qa-id='library-tab']")
    
    # Dashboard content
    DASHBOARD_CONTENT = (By.CSS_SELECTOR, ".dashboard-content")
    WELCOME_MESSAGE = (By.CSS_SELECTOR, "[data-qa-id='welcome-message']")
    RECENT_HIGHLIGHTS = (By.CSS_SELECTOR, "[data-qa-id='recent-highlights']")
    TEAM_INFO = (By.CSS_SELECTOR, "[data-qa-id='team-info']")
    
    # Quick actions
    UPLOAD_VIDEO_BUTTON = (By.CSS_SELECTOR, "[data-qa-id='upload-video-btn']")
    CREATE_HIGHLIGHT_BUTTON = (By.CSS_SELECTOR, "[data-qa-id='create-highlight-btn']")
    VIEW_ROSTER_BUTTON = (By.CSS_SELECTOR, "[data-qa-id='view-roster-btn']")
    
    # Alternative locators
    USER_MENU_ALT = (By.CSS_SELECTOR, ".user-dropdown")
    LOGOUT_BUTTON_ALT = (By.XPATH, "//a[contains(text(), 'Log Out') or contains(text(), 'Sign Out')]")
    USER_NAME_ALT = (By.CSS_SELECTOR, ".user-display-name")
    
    # Loading elements
    DASHBOARD_LOADING = (By.CSS_SELECTOR, ".dashboard-loading")
    CONTENT_LOADING = (By.CSS_SELECTOR, ".content-loading")
    
    def __init__(self, driver, config=None):
        """
        Initialize dashboard page.
        
        Args:
            driver: WebDriver instance
            config: Configuration manager instance
        """
        super().__init__(driver, config)
    
    # Navigation verification methods
    def is_on_dashboard_page(self) -> bool:
        """
        Check if user is on the dashboard page.
        
        Returns:
            True if on dashboard page, False otherwise
        """
        current_url = self.get_current_url()
        print(f"Current URL: {current_url}")
        print(f"Expected URLs: {self.HOME_URL}, {self.DASHBOARD_URL}")
        return (self.HOME_URL in current_url or 
                self.DASHBOARD_URL in current_url or
                self.is_element_present(self.DASHBOARD_CONTENT, timeout=5))

    def get_display_name(self) -> str:

        """
        Get the display name from the dashboard page.
        
        Returns:
            Display name as a string, or empty string if not found
        """
        return self.get_element_text(self.DISPLAY_NAME)

    
    def wait_for_page_load(self, timeout: int = 15) -> bool:
        """
        Wait for dashboard page to fully load.
        
        Args:
            timeout: Timeout in seconds
            
        Returns:
            True if page loaded, False if timeout
        """
        try:
            # Wait for dashboard content or user menu to appear
            self.wait.until(
                lambda driver: self.is_element_present(self.DASHBOARD_CONTENT, timeout=2) or
                               self.is_element_present(self.USER_MENU, timeout=2) or
                               self.is_element_present(self.USER_MENU_ALT, timeout=2)
            )
            
            # Wait for loading indicators to disappear
            self.wait_for_element_invisible(self.DASHBOARD_LOADING, timeout=5)
            self.wait_for_element_invisible(self.CONTENT_LOADING, timeout=5)
            
            return True
        except Exception:
            return False
    
    # User information methods
    def get_user_name(self) -> str:
        """
        Get the displayed user name.
        
        Returns:
            User name or empty string if not found
        """
        try:
            return self.get_element_text(self.USER_NAME)
        except Exception:
            try:
                return self.get_element_text(self.USER_NAME_ALT)
            except Exception:
                return ""
    
    def is_user_logged_in(self) -> bool:
        """
        Check if user is logged in by verifying user menu presence.
        
        Returns:
            True if user is logged in, False otherwise
        """
        return (self.is_element_present(self.USER_MENU, timeout=5) or
                self.is_element_present(self.USER_MENU_ALT, timeout=5))
    
    def get_user_avatar_src(self) -> str:
        """
        Get user avatar image source.
        
        Returns:
            Avatar image source URL or empty string if not found
        """
        try:
            return self.get_element_attribute(self.USER_AVATAR, "src")
        except Exception:
            return ""
    
    # User menu interactions
    def open_user_menu(self) -> None:
        """Open the user menu dropdown."""
        try:
            self.click_element(self.USER_MENU)
        except Exception:
            self.click_element(self.USER_MENU_ALT)
    
    def click_logout(self) -> None:
        """Click the logout button."""
        # Open user menu if it's a dropdown
        if not self.is_element_visible(self.LOGOUT_BUTTON, timeout=2):
            self.open_user_menu()
        
        try:
            self.click_element(self.LOGOUT_BUTTON)
        except Exception:
            self.click_element(self.LOGOUT_BUTTON_ALT)
    
    def click_settings(self) -> None:
        """Click the settings link."""
        # Open user menu if it's a dropdown
        if not self.is_element_visible(self.SETTINGS_LINK, timeout=2):
            self.open_user_menu()
        
        self.click_element(self.SETTINGS_LINK)
    
    # Navigation methods
    def click_home_tab(self) -> None:
        """Click the Home tab."""
        self.click_element(self.HOME_TAB)
    
    def click_highlights_tab(self) -> None:
        """Click the Highlights tab."""
        self.click_element(self.HIGHLIGHTS_TAB)
    
    def click_tools_tab(self) -> None:
        """Click the Tools tab."""
        self.click_element(self.TOOLS_TAB)
    
    def click_library_tab(self) -> None:
        """Click the Library tab."""
        self.click_element(self.LIBRARY_TAB)
    
    # Dashboard content methods
    def get_welcome_message(self) -> str:
        """
        Get the welcome message text.
        
        Returns:
            Welcome message or empty string if not found
        """
        try:
            return self.get_element_text(self.WELCOME_MESSAGE)
        except Exception:
            return ""
    
    def get_team_info(self) -> str:
        """
        Get the team information.
        
        Returns:
            Team information or empty string if not found
        """
        try:
            return self.get_element_text(self.TEAM_INFO)
        except Exception:
            return ""
    
    def has_recent_highlights(self) -> bool:
        """
        Check if recent highlights section is present.
        
        Returns:
            True if recent highlights present, False otherwise
        """
        return self.is_element_present(self.RECENT_HIGHLIGHTS, timeout=5)
    
    # Quick action methods
    def click_upload_video(self) -> None:
        """Click the upload video button."""
        self.click_element(self.UPLOAD_VIDEO_BUTTON)
    
    def click_create_highlight(self) -> None:
        """Click the create highlight button."""
        self.click_element(self.CREATE_HIGHLIGHT_BUTTON)
    
    def click_view_roster(self) -> None:
        """Click the view roster button."""
        self.click_element(self.VIEW_ROSTER_BUTTON)
    
    # Validation methods
    def validate_successful_login(self) -> Dict[str, bool]:
        """
        Validate successful login by checking key indicators.
        
        Returns:
            Dictionary with validation results
        """
        return {
            'on_dashboard_page': self.is_on_dashboard_page(),
            'user_logged_in': self.is_user_logged_in(),
            'user_menu_present': self.is_element_present(self.USER_MENU) or self.is_element_present(self.USER_MENU_ALT),
            'dashboard_content_present': self.is_element_present(self.DASHBOARD_CONTENT),
            'navigation_present': self.is_element_present(self.MAIN_NAVIGATION),
            'logout_available': self.is_element_present(self.LOGOUT_BUTTON) or self.is_element_present(self.LOGOUT_BUTTON_ALT)
        }
    
    def get_page_elements_status(self) -> Dict[str, bool]:
        """
        Get status of all major page elements.
        
        Returns:
            Dictionary with element presence status
        """
        return {
            'user_menu': self.is_element_present(self.USER_MENU) or self.is_element_present(self.USER_MENU_ALT),
            'user_avatar': self.is_element_present(self.USER_AVATAR),
            'user_name': self.is_element_present(self.USER_NAME) or self.is_element_present(self.USER_NAME_ALT),
            'main_navigation': self.is_element_present(self.MAIN_NAVIGATION),
            'dashboard_content': self.is_element_present(self.DASHBOARD_CONTENT),
            'welcome_message': self.is_element_present(self.WELCOME_MESSAGE),
            'team_info': self.is_element_present(self.TEAM_INFO),
            'recent_highlights': self.is_element_present(self.RECENT_HIGHLIGHTS),
            'upload_video_button': self.is_element_present(self.UPLOAD_VIDEO_BUTTON),
            'create_highlight_button': self.is_element_present(self.CREATE_HIGHLIGHT_BUTTON),
            'view_roster_button': self.is_element_present(self.VIEW_ROSTER_BUTTON)
        }
    
    def get_dashboard_info(self) -> Dict[str, Any]:
        """
        Get comprehensive dashboard information.
        
        Returns:
            Dictionary with dashboard information
        """
        return {
            'url': self.get_current_url(),
            'title': self.get_page_title(),
            'user_name': self.get_user_name(),
            'welcome_message': self.get_welcome_message(),
            'team_info': self.get_team_info(),
            'user_avatar_src': self.get_user_avatar_src(),
            'login_validation': self.validate_successful_login(),
            'element_status': self.get_page_elements_status(),
            'page_load_time': self.get_page_load_time()
        }
    
    # Role-specific content methods
    def get_available_features(self) -> List[str]:
        """
        Get list of available features based on user role.
        
        Returns:
            List of available feature names
        """
        features = []
        
        if self.is_element_present(self.UPLOAD_VIDEO_BUTTON):
            features.append('upload_video')
        
        if self.is_element_present(self.CREATE_HIGHLIGHT_BUTTON):
            features.append('create_highlight')
        
        if self.is_element_present(self.VIEW_ROSTER_BUTTON):
            features.append('view_roster')
        
        if self.is_element_present(self.HIGHLIGHTS_TAB):
            features.append('highlights')
        
        if self.is_element_present(self.TOOLS_TAB):
            features.append('tools')
        
        if self.is_element_present(self.LIBRARY_TAB):
            features.append('library')
        
        return features
    
    def verify_user_role_features(self, expected_role: str) -> Dict[str, bool]:
        """
        Verify features available match expected user role.
        
        Args:
            expected_role: Expected user role (coach, player, admin, parent)
            
        Returns:
            Dictionary with role verification results
        """
        available_features = self.get_available_features()
        
        # Define expected features by role
        role_features = {
            'coach': ['upload_video', 'create_highlight', 'view_roster', 'highlights', 'tools', 'library'],
            'player': ['highlights', 'library'],
            'admin': ['upload_video', 'create_highlight', 'view_roster', 'highlights', 'tools', 'library'],
            'parent': ['highlights', 'library']
        }
        
        expected_features = role_features.get(expected_role.lower(), [])
        
        verification_results = {}
        for feature in expected_features:
            verification_results[f'has_{feature}'] = feature in available_features
        
        verification_results['role_match'] = all(verification_results.values())
        verification_results['available_features'] = available_features
        verification_results['expected_features'] = expected_features
        
        return verification_results
    
    # Logout flow
    def logout(self) -> bool:
        """
        Perform logout action.
        
        Returns:
            True if logout action completed, False otherwise
        """
        try:
            self.click_logout()
            
            # Wait for redirect or login page appearance
            return self.wait_for_url_contains('/login', timeout=10)
        except Exception:
            return False
    
    # Error detection methods
    def check_for_errors(self) -> Dict[str, Any]:
        """
        Check for various types of errors on the dashboard page.
        
        Returns:
            Dictionary with error information
        """
        errors = {
            'has_errors': False,
            'error_messages': [],
            'missing_elements': []
        }
        
        # Check for error messages
        error_selectors = [
            (By.CSS_SELECTOR, ".error-message"),
            (By.CSS_SELECTOR, ".alert-error"),
            (By.CSS_SELECTOR, "[data-qa-id='error']"),
            (By.XPATH, "//*[contains(text(), 'Error') or contains(text(), 'error')]")
        ]
        
        for selector in error_selectors:
            if self.is_element_present(selector, timeout=2):
                errors['has_errors'] = True
                try:
                    error_text = self.get_element_text(selector)
                    if error_text:
                        errors['error_messages'].append(error_text)
                except Exception:
                    pass
        
        # Check for missing critical elements
        critical_elements = {
            'user_menu': self.USER_MENU,
            'dashboard_content': self.DASHBOARD_CONTENT,
            'main_navigation': self.MAIN_NAVIGATION
        }
        
        for element_name, locator in critical_elements.items():
            if not self.is_element_present(locator, timeout=2):
                errors['missing_elements'].append(element_name)
                errors['has_errors'] = True
        
        return errors
