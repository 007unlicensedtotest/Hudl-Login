"""
Test data management for Hudl login testing.
Provides test data for different scenarios and user types.
"""

import json
import random
import string
from typing import Dict, List, Any, Optional
from pathlib import Path


class TestDataManager:
    """Manages test data for different testing scenarios."""
    
    def __init__(self, config=None):
        """
        Initialize test data manager.
        
        Args:
            config: Configuration manager instance
        """
        self.config = config
        self._load_test_data()
    
    def _load_test_data(self) -> None:
        """Load test data from configuration or use defaults."""
        if self.config:
            self.test_data = self.config.get_test_data()
        else:
            self.test_data = self._get_default_test_data()
    
    def _get_default_test_data(self) -> Dict[str, Any]:
        """Get default test data."""
        return {
            'valid_credentials': {
                'email': 'test.user@example.com',
                'password': 'TestPassword123!'
            },
            'invalid_credentials': [
                {'email': 'invalid.user@example.com', 'password': 'WrongPassword'},
                {'email': 'nonexistent@example.com', 'password': 'AnotherWrongPassword'},
                {'email': '', 'password': ''},
                {'email': 'test.user@example.com', 'password': ''},
                {'email': '', 'password': 'TestPassword123!'},
                {'email': 'invalid-email-format', 'password': 'ValidPassword123!'},
                {'email': 'test@', 'password': 'ValidPassword123!'},
                {'email': '@example.com', 'password': 'ValidPassword123!'}
            ],
            'test_users': {
                'coach': {
                    'email': 'coach@example.com',
                    'password': 'CoachPassword123!',
                    'role': 'coach',
                    'team': 'Eagles Football',
                    'permissions': ['view_team_data', 'manage_roster', 'create_highlights']
                },
                'player': {
                    'email': 'player@example.com',
                    'password': 'PlayerPassword123!',
                    'role': 'player',
                    'team': 'Eagles Football',
                    'permissions': ['view_personal_data', 'view_team_highlights']
                },
                'admin': {
                    'email': 'admin@example.com',
                    'password': 'AdminPassword123!',
                    'role': 'admin',
                    'permissions': ['manage_users', 'system_settings', 'view_analytics']
                },
                'parent': {
                    'email': 'parent@example.com',
                    'password': 'ParentPassword123!',
                    'role': 'parent',
                    'linked_players': ['player@example.com']
                }
            },
            'security_test_data': {
                'sql_injection_attempts': [
                    "'; DROP TABLE users; --",
                    "admin'--",
                    "admin'/*",
                    "' OR '1'='1",
                    "' OR '1'='1' --",
                    "' OR '1'='1' #",
                    "' OR '1'='1'/*",
                    "') OR '1'='1' --"
                ],
                'xss_attempts': [
                    "<script>alert('XSS')</script>",
                    "<img src=x onerror=alert('XSS')>",
                    "javascript:alert('XSS')",
                    "<svg onload=alert('XSS')>",
                    "';alert('XSS');//",
                    "\"><script>alert('XSS')</script>"
                ],
                'csrf_test_tokens': [
                    "invalid_token_12345",
                    "",
                    "expired_token_67890",
                    "malformed_token_!@#$%"
                ]
            }
        }
    
    def get_valid_credentials(self) -> Dict[str, str]:
        """Get valid login credentials."""
        return self.test_data['valid_credentials'].copy()
    
    def get_invalid_credentials(self) -> List[Dict[str, str]]:
        """Get list of invalid credential combinations."""
        return self.test_data['invalid_credentials'].copy()
    
    def get_random_invalid_credentials(self) -> Dict[str, str]:
        """Get random invalid credentials."""
        invalid_creds = self.get_invalid_credentials()
        return random.choice(invalid_creds)
    
    def get_test_user(self, role: str) -> Optional[Dict[str, Any]]:
        """
        Get test user data by role.
        
        Args:
            role: User role (coach, player, admin, parent)
            
        Returns:
            User data dictionary or None if not found
        """
        test_users = self.test_data.get('test_users', {})
        return test_users.get(role, {}).copy() if role in test_users else None
    
    def get_all_test_users(self) -> Dict[str, Dict[str, Any]]:
        """Get all test users."""
        return self.test_data.get('test_users', {}).copy()
    
    def get_security_test_data(self, test_type: str) -> List[str]:
        """
        Get security test data by type.
        
        Args:
            test_type: Type of security test (sql_injection_attempts, xss_attempts, csrf_test_tokens)
            
        Returns:
            List of test values
        """
        security_data = self.test_data.get('security_test_data', {})
        return security_data.get(test_type, []).copy()
    
    def get_sql_injection_payloads(self) -> List[str]:
        """Get SQL injection test payloads."""
        return self.get_security_test_data('sql_injection_attempts')
    
    def get_xss_payloads(self) -> List[str]:
        """Get XSS test payloads."""
        return self.get_security_test_data('xss_attempts')
    
    def get_csrf_tokens(self) -> List[str]:
        """Get CSRF test tokens."""
        return self.get_security_test_data('csrf_test_tokens')
    
    def generate_random_email(self, domain: str = 'example.com') -> str:
        """
        Generate random email address.
        
        Args:
            domain: Email domain
            
        Returns:
            Random email address
        """
        username_length = random.randint(5, 15)
        username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=username_length))
        return f"{username}@{domain}"
    
    def generate_random_password(self, length: int = 12, include_special: bool = True) -> str:
        """
        Generate random password.
        
        Args:
            length: Password length
            include_special: Include special characters
            
        Returns:
            Random password
        """
        chars = string.ascii_letters + string.digits
        if include_special:
            chars += '!@#$%^&*'
        
        # Ensure password has at least one uppercase, lowercase, digit, and special char
        password = [
            random.choice(string.ascii_uppercase),
            random.choice(string.ascii_lowercase),
            random.choice(string.digits)
        ]
        
        if include_special:
            password.append(random.choice('!@#$%^&*'))
        
        # Fill remaining length with random characters
        remaining_length = length - len(password)
        password.extend(random.choices(chars, k=remaining_length))
        
        # Shuffle the password
        random.shuffle(password)
        return ''.join(password)
    
    def generate_boundary_test_data(self) -> Dict[str, Any]:
        """Generate boundary test data for input validation."""
        return {
            'email_boundaries': {
                'min_length': 'a@b.co',  # Minimum valid email
                'max_length': f"{'a' * 60}@{'b' * 60}.com",  # Very long email
                'empty': '',
                'whitespace_only': '   ',
                'special_chars': 'test+user@example.com',
                'unicode': 'tëst@ëxämplë.com'
            },
            'password_boundaries': {
                'min_length': 'Ab1!',  # 4 characters
                'max_length': 'A' * 128 + 'b1!',  # Very long password
                'empty': '',
                'whitespace_only': '    ',
                'no_uppercase': 'password123!',
                'no_lowercase': 'PASSWORD123!',
                'no_digits': 'Password!',
                'no_special': 'Password123',
                'only_spaces': ' ' * 10,
                'unicode': 'Pässwörd123!'
            }
        }
    
    def get_mobile_test_devices(self) -> List[Dict[str, Any]]:
        """Get mobile device configurations for testing."""
        return [
            {
                'name': 'iPhone 12',
                'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15',
                'viewport': {'width': 390, 'height': 844},
                'device_scale_factor': 3
            },
            {
                'name': 'iPhone SE',
                'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15',
                'viewport': {'width': 375, 'height': 667},
                'device_scale_factor': 2
            },
            {
                'name': 'Pixel 5',
                'user_agent': 'Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36',
                'viewport': {'width': 393, 'height': 851},
                'device_scale_factor': 2.75
            },
            {
                'name': 'Galaxy S21',
                'user_agent': 'Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36',
                'viewport': {'width': 384, 'height': 854},
                'device_scale_factor': 2.75
            },
            {
                'name': 'iPad',
                'user_agent': 'Mozilla/5.0 (iPad; CPU OS 14_0 like Mac OS X) AppleWebKit/605.1.15',
                'viewport': {'width': 768, 'height': 1024},
                'device_scale_factor': 2
            },
            {
                'name': 'iPad Pro',
                'user_agent': 'Mozilla/5.0 (iPad; CPU OS 14_0 like Mac OS X) AppleWebKit/605.1.15',
                'viewport': {'width': 1024, 'height': 1366},
                'device_scale_factor': 2
            }
        ]
    
    def load_test_data_from_file(self, file_path: str) -> Dict[str, Any]:
        """
        Load test data from JSON file.
        
        Args:
            file_path: Path to JSON file
            
        Returns:
            Test data dictionary
        """
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading test data from {file_path}: {e}")
            return {}
    
    def save_test_data_to_file(self, data: Dict[str, Any], file_path: str) -> bool:
        """
        Save test data to JSON file.
        
        Args:
            data: Test data to save
            file_path: Path to save file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Create directory if it doesn't exist
            Path(file_path).parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving test data to {file_path}: {e}")
            return False
    
    def get_localization_test_data(self) -> Dict[str, Dict[str, str]]:
        """Get localization test data for different languages."""
        return {
            'en': {
                'login_button': 'Sign In',
                'email_placeholder': 'Email',
                'password_placeholder': 'Password',
                'remember_me': 'Remember me',
                'forgot_password': 'Forgot Password?',
                'invalid_credentials_error': 'Invalid email or password'
            },
            'es': {
                'login_button': 'Iniciar Sesión',
                'email_placeholder': 'Correo electrónico',
                'password_placeholder': 'Contraseña',
                'remember_me': 'Recordarme',
                'forgot_password': '¿Olvidaste tu contraseña?',
                'invalid_credentials_error': 'Correo electrónico o contraseña inválidos'
            },
            'fr': {
                'login_button': 'Se connecter',
                'email_placeholder': 'E-mail',
                'password_placeholder': 'Mot de passe',
                'remember_me': 'Se souvenir de moi',
                'forgot_password': 'Mot de passe oublié?',
                'invalid_credentials_error': 'E-mail ou mot de passe invalide'
            }
        }
    
    def create_test_scenario_data(self, scenario_name: str) -> Dict[str, Any]:
        """
        Create test data for specific scenario.
        
        Args:
            scenario_name: Name of the test scenario
            
        Returns:
            Scenario-specific test data
        """
        scenario_data = {
            'scenario_name': scenario_name,
            'timestamp': str(random.randint(1000000000, 9999999999)),
            'test_id': f"TEST_{scenario_name.upper()}_{random.randint(1000, 9999)}"
        }
        
        # Add scenario-specific data based on scenario name
        if 'login' in scenario_name.lower():
            scenario_data.update({
                'credentials': self.get_valid_credentials(),
                'expected_redirect': '/dashboard'
            })
        elif 'invalid' in scenario_name.lower():
            scenario_data.update({
                'credentials': self.get_random_invalid_credentials(),
                'expected_error': 'Invalid email or password'
            })
        elif 'security' in scenario_name.lower():
            scenario_data.update({
                'security_payloads': {
                    'sql_injection': random.choice(self.get_sql_injection_payloads()),
                    'xss': random.choice(self.get_xss_payloads())
                }
            })
        
        return scenario_data
