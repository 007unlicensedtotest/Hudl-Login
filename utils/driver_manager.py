"""
WebDriver management for Hudl login testing.
Handles browser initialization, configuration, and cleanup.
"""

import os
import platform
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from typing import Optional, Dict, Any


class DriverManager:
    """Manages WebDriver instances for different browsers."""
    
    def __init__(self, config=None):
        """
        Initialize driver manager with configuration.
        
        Args:
            config: Configuration manager instance
        """
        self.config = config
        self.driver = None
        
    def get_driver(self, browser: Optional[str] = None) -> webdriver.Remote:
        """
        Get WebDriver instance for specified browser.
        
        Args:
            browser: Browser name (chrome, firefox, edge, safari)
            
        Returns:
            WebDriver instance
        """
        if browser is None:
            browser = self.config.get_browser() if self.config else 'chrome'
        
        browser = browser.lower()
        
        if browser == 'chrome':
            self.driver = self._get_chrome_driver()
        elif browser == 'firefox':
            self.driver = self._get_firefox_driver()
        elif browser == 'edge':
            self.driver = self._get_edge_driver()
        elif browser == 'safari':
            self.driver = self._get_safari_driver()
        else:
            raise ValueError(f"Unsupported browser: {browser}")
        
        # Configure driver timeouts
        self._configure_timeouts()
        
        # Set window size
        self._configure_window()
        
        return self.driver
    
    def _get_chrome_driver(self) -> webdriver.Chrome:
        """Get Chrome WebDriver instance."""
        print("Initializing Chrome WebDriver...")
        options = ChromeOptions()
        
        # Get browser options from config
        if self.config:
            print(f"Using config - Headless mode: {self.config.is_headless()}")
            
            # Add default arguments
            default_args = [
                '--no-sandbox',
                '--disable-dev-shm-usage',
                '--window-size=1920,1080'
            ]
            for arg in default_args:
                print(f"Adding Chrome argument: {arg}")
                options.add_argument(arg)
            
            # Set default preferences
            default_prefs = {
                'profile.default_content_setting_values.notifications': 2
            }
            print(f"Setting Chrome preferences: {default_prefs}")
            options.add_experimental_option('prefs', default_prefs)
            
            # Headless mode
            if self.config.is_headless():
                print("Running in headless mode")
                options.add_argument('--headless')
            else:
                print("Running in normal (visible) mode")
        else:
            print("No config provided, using default options")
            # Default options
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            if os.getenv('HEADLESS', 'false').lower() == 'true':
                options.add_argument('--headless')
        
        # Set up service
        print("Setting up Chrome service...")
        try:
            # Try to use webdriver-manager first
            service = ChromeService(ChromeDriverManager().install())
        except Exception as e:
            print(f"WebDriver Manager failed: {e}")
            print("Trying to use system ChromeDriver...")
            # Fall back to system ChromeDriver
            import shutil
            chromedriver_path = shutil.which('chromedriver')
            if chromedriver_path:
                print(f"Found system ChromeDriver at: {chromedriver_path}")
                service = ChromeService(chromedriver_path)
            else:
                raise Exception("No ChromeDriver found. Please install ChromeDriver manually.")
        
        print("Creating Chrome WebDriver instance...")
        try:
            driver = webdriver.Chrome(service=service, options=options)
            print("Chrome WebDriver created successfully!")
            return driver
        except Exception as e:
            print(f"Failed to create Chrome WebDriver: {e}")
            raise
    
    def _get_firefox_driver(self) -> webdriver.Firefox:
        """Get Firefox WebDriver instance."""
        options = FirefoxOptions()
        
        # Get browser options from config
        if self.config:
            # Add default arguments
            default_args = ['--width=1920', '--height=1080']
            for arg in default_args:
                options.add_argument(arg)
            
            # Set default preferences
            default_prefs = {'dom.webnotifications.enabled': False}
            for key, value in default_prefs.items():
                options.set_preference(key, value)
            
            # Headless mode
            if self.config.is_headless():
                options.add_argument('--headless')
        else:
            # Default options
            if os.getenv('HEADLESS', 'false').lower() == 'true':
                options.add_argument('--headless')
        
        # Set up service
        service = FirefoxService(GeckoDriverManager().install())
        
        return webdriver.Firefox(service=service, options=options)
    
    def _get_edge_driver(self) -> webdriver.Edge:
        """Get Edge WebDriver instance."""
        options = EdgeOptions()
        
        # Get browser options from config
        if self.config:
            # Add default arguments
            default_args = [
                '--no-sandbox',
                '--disable-dev-shm-usage',
                '--window-size=1920,1080'
            ]
            for arg in default_args:
                options.add_argument(arg)
            
            # Headless mode
            if self.config.is_headless():
                options.add_argument('--headless')
        else:
            # Default options
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            if os.getenv('HEADLESS', 'false').lower() == 'true':
                options.add_argument('--headless')
        
        # Set up service
        service = EdgeService(EdgeChromiumDriverManager().install())
        
        return webdriver.Edge(service=service, options=options)
    
    def _get_safari_driver(self) -> webdriver.Safari:
        """Get Safari WebDriver instance."""
        # Safari only available on macOS
        if platform.system() != 'Darwin':
            raise RuntimeError("Safari WebDriver is only available on macOS")
        
        # Safari doesn't support headless mode
        return webdriver.Safari()
    
    def _configure_timeouts(self) -> None:
        """Configure WebDriver timeouts."""
        if not self.driver:
            return
        
        if self.config:
            # Set timeouts from config
            implicit_wait = self.config.get_implicit_wait()
            page_load_timeout = self.config.get_page_load_timeout()
        else:
            # Default timeouts
            implicit_wait = 10
            page_load_timeout = 30
        
        self.driver.implicitly_wait(implicit_wait)
        self.driver.set_page_load_timeout(page_load_timeout)
    
    def _configure_window(self) -> None:
        """Configure browser window."""
        if not self.driver:
            return
        
        # Don't maximize in headless mode
        headless = self.config.is_headless() if self.config else os.getenv('HEADLESS', 'false').lower() == 'true'
        
        if not headless:
            if self.config:
                width, height = self.config.get_window_size()
                self.driver.set_window_size(width, height)
            else:
                self.driver.maximize_window()
    
    def get_mobile_driver(self, device_name: str) -> webdriver.Chrome:
        """
        Get mobile emulation WebDriver.
        
        Args:
            device_name: Mobile device name to emulate
            
        Returns:
            Chrome WebDriver with mobile emulation
        """
        mobile_emulation = {"deviceName": device_name}
        
        options = ChromeOptions()
        options.add_experimental_option("mobileEmulation", mobile_emulation)
        
        # Add common mobile testing arguments
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        if self.config and self.config.is_headless():
            options.add_argument('--headless')
        
        service = ChromeService(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=options)
    
    def get_remote_driver(self, hub_url: str, browser: str, version: str = None, platform: str = None) -> webdriver.Remote:
        """
        Get remote WebDriver instance for Selenium Grid or cloud testing.
        
        Args:
            hub_url: Selenium Grid hub URL
            browser: Browser name
            version: Browser version (optional)
            platform: Platform name (optional)
            
        Returns:
            Remote WebDriver instance
        """
        capabilities = {
            'browserName': browser,
            'browserVersion': version or 'latest',
            'platformName': platform or 'ANY'
        }
        
        # Add browser-specific options
        if browser.lower() == 'chrome':
            options = ChromeOptions()
            if self.config:
                browser_opts = self.config.get_browser_options().get('chrome', {})
                for arg in browser_opts.get('arguments', []):
                    options.add_argument(arg)
            capabilities.update(options.to_capabilities())
        elif browser.lower() == 'firefox':
            options = FirefoxOptions()
            if self.config:
                browser_opts = self.config.get_browser_options().get('firefox', {})
                for arg in browser_opts.get('arguments', []):
                    options.add_argument(arg)
            capabilities.update(options.to_capabilities())
        
        return webdriver.Remote(
            command_executor=hub_url,
            desired_capabilities=capabilities
        )
    
    def quit_driver(self) -> None:
        """Quit the WebDriver instance."""
        if self.driver:
            try:
                self.driver.quit()
            except Exception as e:
                print(f"Error quitting driver: {e}")
            finally:
                self.driver = None
    
    def restart_driver(self, browser: Optional[str] = None) -> webdriver.Remote:
        """
        Restart the WebDriver instance.
        
        Args:
            browser: Browser name (optional)
            
        Returns:
            New WebDriver instance
        """
        self.quit_driver()
        return self.get_driver(browser)
    
    def take_screenshot(self, filename: str) -> bool:
        """
        Take a screenshot and save to file.
        
        Args:
            filename: Screenshot filename
            
        Returns:
            True if successful, False otherwise
        """
        if not self.driver:
            return False
        
        try:
            return self.driver.save_screenshot(filename)
        except Exception as e:
            print(f"Error taking screenshot: {e}")
            return False
    
    def get_driver_info(self) -> Dict[str, Any]:
        """
        Get information about the current driver.
        
        Returns:
            Dictionary with driver information
        """
        if not self.driver:
            return {}
        
        try:
            return {
                'browser_name': self.driver.capabilities.get('browserName'),
                'browser_version': self.driver.capabilities.get('browserVersion'),
                'platform': self.driver.capabilities.get('platformName'),
                'session_id': self.driver.session_id,
                'current_url': self.driver.current_url,
                'window_size': self.driver.get_window_size(),
                'window_position': self.driver.get_window_position()
            }
        except Exception as e:
            print(f"Error getting driver info: {e}")
            return {}
