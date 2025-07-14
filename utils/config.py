"""
Configuration management for Hudl login testing.
Handles environment variables, test settings, and browser configuration.
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from dotenv import load_dotenv


class Config:
    """Configuration manager for test automation framework."""
    
    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize configuration manager.
        
        Args:
            config_file: Optional path to YAML config file
        """
        # Load environment variables from .env file
        load_dotenv()
        
        # Load configuration from YAML file if provided
        self.config_data = {}
        if config_file:
            self._load_config_file(config_file)
        else:
            # Try to load default config files
            self._load_default_config()
    
    def _load_config_file(self, config_file: str) -> None:
        """Load configuration from YAML file."""
        try:
            config_path = Path(config_file)
            if config_path.exists():
                with open(config_path, 'r') as f:
                    self.config_data = yaml.safe_load(f) or {}
            else:
                print(f"Warning: Config file {config_file} not found. Using defaults.")
        except Exception as e:
            print(f"Error loading config file {config_file}: {e}")
            self.config_data = {}
    
    def _load_default_config(self) -> None:
        """Load default configuration files."""
        # Look for config files in the config directory
        config_dir = Path(__file__).parent.parent / 'config'
        
        # Load main config file
        for config_file in ['test_config.yaml', 'config.yaml', 'settings.yaml']:
            config_path = config_dir / config_file
            if config_path.exists():
                self._load_config_file(str(config_path))
                break
        
        # Also load test data file if it exists
        test_data_path = config_dir / 'test_data.yaml'
        if test_data_path.exists():
            try:
                with open(test_data_path, 'r') as f:
                    test_data = yaml.safe_load(f) or {}
                    # Merge test data into config
                    if 'test_data' not in self.config_data:
                        self.config_data['test_data'] = test_data
                    else:
                        self.config_data['test_data'].update(test_data)
            except Exception as e:
                print(f"Error loading test data file: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value by key.
        
        Args:
            key: Configuration key (supports dot notation)
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        # First check environment variables
        env_key = key.upper().replace('.', '_')
        env_value = os.getenv(env_key)
        if env_value is not None:
            return env_value
        
        # Then check config file data
        keys = key.split('.')
        value = self.config_data
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def get_browser(self) -> str:
        """Get browser name for testing."""
        # Check for browser.name in config file first
        browser_name = self.get('browser.name', None)
        if browser_name:
            return browser_name.lower()
        
        # Fall back to BROWSER env var or simple 'browser' config
        return self.get('browser', 'chrome').lower()
    
    def get_base_url(self) -> str:
        """Get base URL for testing."""
        # Check nested configuration first
        base_url = self.get('urls.base_url', None)
        if base_url:
            return base_url
        
        # Fall back to simple config or env var
        return self.get('base_url', 'https://www.hudl.com')
    
    def get_base_url_path(self) -> str:
        """Get base URL path for the application."""
        # Check nested configuration first
        base_url_path = self.get('paths.base_url_path', None)
        if base_url_path:
            return base_url_path
        
        # Fall back to simple config or default path
        return self.get('base_url_path', '/')
    
    def get_login_url(self) -> str:
        """Get login page URL."""
        # Check if full login URL is configured
        login_url = self.get('urls.login_url', None)
        if login_url:
            return login_url
        
        # Build from base URL and path
        base_url = self.get_base_url()
        login_path = self.get('login_path', '/login')
        return f"{base_url}{login_path}"
    
    def get_implicit_wait(self) -> int:
        """Get implicit wait timeout in seconds."""
        return int(self.get('timeouts.implicit_wait', 10))
    
    def get_explicit_wait(self) -> int:
        """Get explicit wait timeout in seconds."""
        return int(self.get('timeouts.explicit_wait', 20))
    
    def get_page_load_timeout(self) -> int:
        """Get page load timeout in seconds."""
        return int(self.get('timeouts.page_load', 30))
    
    def is_headless(self) -> bool:
        """Check if browser should run in headless mode."""
        # Check for browser.headless in config file first
        headless = self.get('browser.headless', None)
        if headless is not None:
            return str(headless).lower() == 'true'
        
        # Fall back to HEADLESS env var or simple 'headless' config
        return self.get('headless', 'false').lower() == 'true'
    
    def get_window_size(self) -> tuple:
        """Get browser window size."""
        # Check nested configuration first
        width = self.get('browser.window_size.width', None)
        height = self.get('browser.window_size.height', None)
        
        if width and height:
            return (int(width), int(height))
        
        # Fall back to simple config
        width = int(self.get('window.width', 1920))
        height = int(self.get('window.height', 1080))
        return (width, height)
    
    def get_screenshot_on_failure(self) -> bool:
        """Check if screenshots should be taken on failure."""
        return self.get('reporting.screenshot_on_failure', 'true').lower() == 'true'
    
    def get_test_data(self) -> Dict[str, Any]:
        """Get test data configuration."""
        return self.get('test_data', {
            'valid_credentials': {
                'email': 'test.user@example.com',
                'password': 'TestPassword123!'
            },
            'invalid_credentials': {
                'email': 'invalid.user@example.com', 
                'password': 'WrongPassword'
            }
        })
    
    def get_error_timeout(self) -> int:
        """Get error detection timeout in seconds."""
        return int(self.get('timeouts.error_detection', 3))
    
    def get_social_login_timeout(self) -> int:
        """Get social login element detection timeout in seconds."""
        return int(self.get('timeouts.social_login', 2))

    def __str__(self) -> str:
        """String representation of configuration."""
        return f"Config(browser={self.get_browser()}, base_url={self.get_base_url()})"
