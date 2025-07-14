# Pages package for Page Object Model classes

from .base_page import BasePage
from .login_page import LoginPage
from .dashboard_page import DashboardPage
from .home_page import HomePage
from .new_account_page import NewAccountPage

__all__ = [
    'BasePage',
    'LoginPage', 
    'DashboardPage',
    'HomePage',
    'NewAccountPage'
]
