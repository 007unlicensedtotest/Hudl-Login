"""
Base page class for Page Object Model implementation.
Contains common functionality shared across all page objects.
"""

import time
from typing import List, Optional, Tuple, Any, Dict
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import (
    TimeoutException, 
    NoSuchElementException, 
    StaleElementReferenceException,
    ElementNotInteractableException
)


class BasePage:
    """Base page class implementing common page functionality."""
    
    def __init__(self, driver, config=None):
        """
        Initialize base page.
        
        Args:
            driver: WebDriver instance
            config: Configuration manager instance
        """
        self.driver = driver
        self.config = config
        self.wait = WebDriverWait(
            driver, 
            config.get_explicit_wait() if config else 20
        )
        self.short_wait = WebDriverWait(driver, 5)
        self.action_chains = ActionChains(driver)
    
    # Element finding methods
    def find_element(self, locator: Tuple[str, str], timeout: int = None) -> WebElement:
        """
        Find a single element with explicit wait.
        
        Args:
            locator: Tuple of (By strategy, locator value)
            timeout: Custom timeout in seconds
            
        Returns:
            WebElement instance
            
        Raises:
            TimeoutException: If element not found within timeout
        """
        wait = WebDriverWait(self.driver, timeout) if timeout else self.wait
        return wait.until(EC.presence_of_element_located(locator))
    
    def find_elements(self, locator: Tuple[str, str], timeout: int = None) -> List[WebElement]:
        """
        Find multiple elements with explicit wait.
        
        Args:
            locator: Tuple of (By strategy, locator value)
            timeout: Custom timeout in seconds
            
        Returns:
            List of WebElement instances
        """
        wait = WebDriverWait(self.driver, timeout) if timeout else self.wait
        wait.until(EC.presence_of_element_located(locator))
        return self.driver.find_elements(*locator)
    
    def find_clickable_element(self, locator: Tuple[str, str], timeout: int = None) -> WebElement:
        """
        Find a clickable element with explicit wait.
        
        Args:
            locator: Tuple of (By strategy, locator value)
            timeout: Custom timeout in seconds
            
        Returns:
            WebElement instance
            
        Raises:
            TimeoutException: If element not clickable within timeout
        """
        wait = WebDriverWait(self.driver, timeout) if timeout else self.wait
        return wait.until(EC.element_to_be_clickable(locator))
    
    def find_visible_element(self, locator: Tuple[str, str], timeout: int = None) -> WebElement:
        """
        Find a visible element with explicit wait.
        
        Args:
            locator: Tuple of (By strategy, locator value)
            timeout: Custom timeout in seconds
            
        Returns:
            WebElement instance
            
        Raises:
            TimeoutException: If element not visible within timeout
        """
        wait = WebDriverWait(self.driver, timeout) if timeout else self.wait
        return wait.until(EC.visibility_of_element_located(locator))
    
    # Element interaction methods
    def click_element(self, locator: Tuple[str, str], timeout: int = None) -> None:
        """
        Click an element with retry logic.
        
        Args:
            locator: Tuple of (By strategy, locator value)
            timeout: Custom timeout in seconds
        """
        element = self.find_clickable_element(locator, timeout)
        self._click_with_retry(element)
    
    def _click_with_retry(self, element: WebElement, max_attempts: int = 3) -> None:
        """
        Click element with retry logic for stale element exceptions.
        
        Args:
            element: WebElement to click
            max_attempts: Maximum number of retry attempts
        """
        for attempt in range(max_attempts):
            try:
                element.click()
                return
            except StaleElementReferenceException:
                if attempt == max_attempts - 1:
                    raise
                time.sleep(0.5)
            except ElementNotInteractableException:
                # Try JavaScript click as fallback
                self.driver.execute_script("arguments[0].click();", element)
                return
    
    def send_keys_to_element(self, locator: Tuple[str, str], text: str, clear_first: bool = True) -> None:
        """
        Send keys to an element.
        
        Args:
            locator: Tuple of (By strategy, locator value)
            text: Text to send
            clear_first: Whether to clear field before typing
        """
        element = self.find_visible_element(locator)
        if clear_first:
            element.clear()
        element.send_keys(text)
    
    def get_element_text(self, locator: Tuple[str, str], timeout: int = None) -> str:
        """
        Get text content of an element.
        
        Args:
            locator: Tuple of (By strategy, locator value)
            timeout: Custom timeout in seconds
            
        Returns:
            Element text content
        """
        element = self.find_visible_element(locator, timeout)
        return element.text.strip()
    
    def get_element_attribute(self, locator: Tuple[str, str], attribute: str, timeout: int = None) -> str:
        """
        Get attribute value of an element.
        
        Args:
            locator: Tuple of (By strategy, locator value)
            attribute: Attribute name
            timeout: Custom timeout in seconds
            
        Returns:
            Attribute value
        """
        element = self.find_element(locator, timeout)
        return element.get_attribute(attribute) or ""
    
    def is_element_present(self, locator: Tuple[str, str], timeout: int = 5) -> bool:
        """
        Check if element is present in DOM.
        
        Args:
            locator: Tuple of (By strategy, locator value)
            timeout: Timeout in seconds
            
        Returns:
            True if element is present, False otherwise
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False
    
    def is_element_visible(self, locator: Tuple[str, str], timeout: int = 5) -> bool:
        """
        Check if element is visible.
        
        Args:
            locator: Tuple of (By strategy, locator value)
            timeout: Timeout in seconds
            
        Returns:
            True if element is visible, False otherwise
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False
    
    def is_element_clickable(self, locator: Tuple[str, str], timeout: int = 5) -> bool:
        """
        Check if element is clickable.
        
        Args:
            locator: Tuple of (By strategy, locator value)
            timeout: Timeout in seconds
            
        Returns:
            True if element is clickable, False otherwise
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            return True
        except TimeoutException:
            return False
    
    # Wait methods
    def wait_for_element_visible(self, locator: Tuple[str, str], timeout: int = None) -> WebElement:
        """
        Wait for element to be visible.
        
        Args:
            locator: Tuple of (By strategy, locator value)
            timeout: Custom timeout in seconds
            
        Returns:
            WebElement instance
        """
        return self.find_visible_element(locator, timeout)
    
    def wait_for_element_invisible(self, locator: Tuple[str, str], timeout: int = None) -> bool:
        """
        Wait for element to be invisible.
        
        Args:
            locator: Tuple of (By strategy, locator value)
            timeout: Custom timeout in seconds
            
        Returns:
            True if element becomes invisible, False otherwise
        """
        wait = WebDriverWait(self.driver, timeout) if timeout else self.wait
        try:
            return wait.until(EC.invisibility_of_element_located(locator))
        except TimeoutException:
            return False
    
    def wait_for_text_in_element(self, locator: Tuple[str, str], text: str, timeout: int = None) -> bool:
        """
        Wait for specific text to appear in element.
        
        Args:
            locator: Tuple of (By strategy, locator value)
            text: Text to wait for
            timeout: Custom timeout in seconds
            
        Returns:
            True if text appears, False otherwise
        """
        wait = WebDriverWait(self.driver, timeout) if timeout else self.wait
        try:
            return wait.until(EC.text_to_be_present_in_element(locator, text))
        except TimeoutException:
            return False
    
    def wait_for_url_contains(self, url_fragment: str, timeout: int = None) -> bool:
        """
        Wait for URL to contain specific fragment.
        
        Args:
            url_fragment: URL fragment to wait for
            timeout: Custom timeout in seconds
            
        Returns:
            True if URL contains fragment, False otherwise
        """
        wait = WebDriverWait(self.driver, timeout) if timeout else self.wait
        try:
            return wait.until(EC.url_contains(url_fragment))
        except TimeoutException:
            return False
    
    def wait_for_page_load(self, timeout: int = None) -> bool:
        """
        Wait for page to fully load.
        
        Args:
            timeout: Custom timeout in seconds
            
        Returns:
            True if page loaded, False otherwise
        """
        wait = WebDriverWait(self.driver, timeout) if timeout else self.wait
        try:
            return wait.until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
        except TimeoutException:
            return False
    
    # Navigation methods
    def navigate_to(self, url: str) -> None:
        """
        Navigate to a URL.
        
        Args:
            url: URL to navigate to
        """
        print(f"Navigating to URL: {url}")
        self.driver.get(url)
        self.wait_for_page_load()
    
    def refresh_page(self) -> None:
        """Refresh the current page."""
        self.driver.refresh()
        self.wait_for_page_load()
    
    def go_back(self) -> None:
        """Navigate back in browser history."""
        self.driver.back()
        self.wait_for_page_load()
    
    def go_forward(self) -> None:
        """Navigate forward in browser history."""
        self.driver.forward()
        self.wait_for_page_load()
    
    # Utility methods
    def get_current_url(self) -> str:
        """Get current page URL."""
        return self.driver.current_url
    
    def get_page_title(self) -> str:
        """Get current page title."""
        return self.driver.title
    
    def get_page_source(self) -> str:
        """Get current page source."""
        return self.driver.page_source
    
    def take_screenshot(self, filename: str) -> bool:
        """
        Take a screenshot.
        
        Args:
            filename: Screenshot filename
            
        Returns:
            True if successful, False otherwise
        """
        try:
            return self.driver.save_screenshot(filename)
        except Exception as e:
            print(f"Error taking screenshot: {e}")
            return False

    def attach_screenshot_to_allure(self, name: str = "Screenshot") -> None:
        """
        Take screenshot and attach to Allure report.
        
        Args:
            name: Name for the attachment in Allure
        """
        try:
            import allure
            screenshot = self.driver.get_screenshot_as_png()
            allure.attach(screenshot, name=name, attachment_type=allure.attachment_type.PNG)
        except ImportError:
            print("Allure not available, taking regular screenshot")
            self.take_screenshot(f"reports/{name.lower().replace(' ', '_')}.png")
        except Exception as e:
            print(f"Error attaching screenshot to Allure: {e}")

    def attach_page_source_to_allure(self, name: str = "Page Source") -> None:
        """
        Attach page source to Allure report.
        
        Args:
            name: Name for the attachment in Allure
        """
        try:
            import allure
            page_source = self.driver.page_source
            allure.attach(page_source, name=name, attachment_type=allure.attachment_type.HTML)
        except ImportError:
            print("Allure not available, saving page source to file")
            timestamp = int(time.time())
            with open(f"reports/page_source_{timestamp}.html", "w", encoding="utf-8") as f:
                f.write(self.driver.page_source)
        except Exception as e:
            print(f"Error attaching page source to Allure: {e}")

    def attach_browser_logs_to_allure(self, name: str = "Browser Logs") -> None:
        """
        Attach browser console logs to Allure report.
        
        Args:
            name: Name for the attachment in Allure
        """
        try:
            import allure
            logs = self.driver.get_log('browser')
            log_text = "\n".join([f"{log['timestamp']}: {log['level']}: {log['message']}" for log in logs])
            allure.attach(log_text, name=name, attachment_type=allure.attachment_type.TEXT)
        except ImportError:
            print("Allure not available, printing browser logs")
            try:
                logs = self.driver.get_log('browser')
                for log in logs:
                    print(f"Browser Log: {log['level']}: {log['message']}")
            except:
                print("Browser logs not available")
        except Exception as e:
            print(f"Error attaching browser logs to Allure: {e}")

    def attach_detailed_error_info_to_allure(self, error_msg: str, context: str = "") -> None:
        """
        Attach comprehensive error information to Allure report.
        
        Args:
            error_msg: The error message
            context: Additional context about what was being attempted
        """
        try:
            import allure
            
            # Get detailed environment info
            error_details = f"""
ERROR DETAILS:
=============
Error Message: {error_msg}
Context: {context}
Current URL: {self.driver.current_url}
Page Title: {self.driver.title}
Window Size: {self.driver.get_window_size()}
Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}

BROWSER INFO:
============
User Agent: {self.driver.execute_script('return navigator.userAgent;')}
Viewport: {self.driver.execute_script('return {width: window.innerWidth, height: window.innerHeight};')}
"""
            
            allure.attach(error_details, name="Error Details", attachment_type=allure.attachment_type.TEXT)
            
            # Also attach screenshot, page source, and logs
            self.attach_screenshot_to_allure("Error Screenshot")
            self.attach_page_source_to_allure("Error Page Source")
            self.attach_browser_logs_to_allure("Error Browser Logs")
            
        except Exception as e:
            print(f"Error creating detailed error report: {e}")

    # ====================================================================
    # FALLBACK LOCATOR METHODS
    # ====================================================================

    def find_element_with_fallback(self, locators: List[Tuple[str, str]], timeout: int = 3) -> Optional[WebElement]:
        """
        Try multiple locators until one finds an element.
        
        Args:
            locators: List of locator tuples to try
            timeout: Timeout for each locator attempt
            
        Returns:
            WebElement if found, None otherwise
        """
        for locator in locators:
            try:
                return self.find_element(locator, timeout=timeout)
            except Exception:
                continue
        return None

    def send_keys_with_fallback(self, locators: List[Tuple[str, str]], text: str, timeout: int = 3) -> bool:
        """
        Try multiple locators to find an element and send keys to it.
        
        Args:
            locators: List of locator tuples to try
            text: Text to send to the element
            timeout: Timeout for each locator attempt
            
        Returns:
            True if successful, False otherwise
        """
        for locator in locators:
            try:
                element = self.find_element(locator, timeout=timeout)
                element.clear()
                element.send_keys(text)
                return True
            except Exception:
                continue
        return False

    def click_with_fallback(self, locators: List[Tuple[str, str]], timeout: int = 3) -> bool:
        """
        Try multiple locators to find an element and click it.
        
        Args:
            locators: List of locator tuples to try
            timeout: Timeout for each locator attempt
            
        Returns:
            True if successful, False otherwise
        """
        for locator in locators:
            try:
                element = self.find_element(locator, timeout=timeout)
                element.click()
                return True
            except Exception:
                continue
        return False

    def is_element_visible_with_fallback(self, locators: List[Tuple[str, str]], element_name: str = "element", timeout: int = 2) -> bool:
        """
        Try multiple locators to check if any element is visible.
        
        Args:
            locators: List of locator tuples to try
            element_name: Name of element for debugging (unused but kept for compatibility)
            timeout: Timeout for each locator attempt
            
        Returns:
            True if any element is visible, False otherwise
        """
        for locator in locators:
            try:
                if self.is_element_visible(locator, timeout=timeout):
                    return True
            except Exception:
                continue
        return False

    # ...existing code...


