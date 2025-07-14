# Hudl.com Login Page Testing Suite

A comprehensive test automation suite for testing the Hudl.com login page using Python, Selenium WebDriver, and Behave BDD framework.

## Project Structure

```
├── features/                   # Behave feature files
│   ├── login.feature          # Login test scenarios (17 scenarios)
│   ├── steps/                 # Step definitions
│   │   └── login_steps.py     # Comprehensive step definitions with Allure integration
│   └── environment.py         # Behave hooks and setup
├── pages/                     # Page Object Model with fallback strategies
│   ├── base_page.py          # Base page with robust error handling and fallback locators
│   ├── login_page.py         # Login page with email/password validation
│   ├── home_page.py          # Main homepage navigation
│   ├── dashboard_page.py     # Post-login dashboard verification
│   ├── new_account_page.py   # Account creation page object
│   └── reset_password_page.py # Password reset functionality
├── utils/                     # Utility modules
│   ├── config.py             # Configuration management
│   ├── driver_manager.py     # WebDriver management with browser support
│   └── test_data.py          # Test data management
├── config/                    # Configuration files
│   ├── config.yaml           # Test configuration settings
│   └── test_data.yaml        # Test credentials and data
├── reports/                   # Test reports and screenshots
│   ├── allure-results/       # Allure test results
│   ├── allure-report/        # Generated Allure HTML reports
│   └── *.png                 # Failure screenshots
├── docs/                      # Documentation
├── requirements.txt          # Python dependencies
├── run_tests.py             # Test runner with multiple execution options
├── TEST_SCENARIOS.md        # Detailed scenario documentation
└── README.md                # This file
```

## Test Scenarios Covered

### 1. ✅ **Positive Login Scenarios** (`@smoke @positive`)
- Successful login with valid email and password
- Dashboard redirect verification and display name confirmation
- Provider authentication (Google, Facebook, Apple) redirection testing

### 2. ✅ **Negative Validation Scenarios** (`@negative @validation`)
- Login with invalid email and valid password
- Login with valid email and invalid password
- Login with empty email field
- Login with empty password field
- Comprehensive invalid email format testing:
  - `invalid.email` (missing @ symbol)
  - `@domain.com` (missing local part)
  - `user@` (missing domain)
  - `user@.com` (invalid domain format)
  - `user name@domain.com` (spaces in local part)

### 3. ✅ **UI/UX Functionality Testing** (`@ui @functionality`)
- Password show/hide toggle functionality
- Password field masking verification
- "Forgot password?" link navigation and functionality
- "Sign up" link navigation to registration page

### 4. ✅ **Session Management** (`@logout @cleanup`)
- Successful logout functionality
- Session cleanup verification
- Post-logout redirect validation

### 5. ✅ **Advanced Error Handling & Reporting**
- Fallback locator strategies for robust element finding
- Automatic screenshot capture on test failures
- Page source and browser log capture
- Allure integration with rich test reporting
- Comprehensive error messages with context

## Setup Instructions

### Prerequisites
- Python 3.8+ installed
- Chrome browser (default) or Firefox/Edge/Safari
- Git for version control

### 1. **Environment Setup**:
   ```bash
   # Clone the repository and navigate to project directory
   cd /path/to/hudl-login-testing
   
   # Create and activate virtual environment
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   # venv\Scripts\activate   # On Windows
   ```

### 2. **Install Python Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### 3. **Install Allure CLI** (for advanced HTML reporting):
   ```bash
   # macOS
   brew install allure
   
   # Linux (Ubuntu/Debian)
   sudo apt-get install allure
   
   # Windows (using Scoop)
   scoop install allure
   ```

### 4. **Configuration**:
   The project uses YAML configuration files in the `config/` directory:
   - `config.yaml`: Test settings and browser configuration
   - `test_data.yaml`: Test credentials and validation data

### 5. **Run Tests**:
   ```bash
   # Activate virtual environment first
   source venv/bin/activate
   
   # Using run_tests.py script (recommended)
   python run_tests.py smoke              # Run critical smoke tests
   python run_tests.py smoke-allure       # Run smoke tests with Allure report
   python run_tests.py positive           # Run positive test scenarios
   python run_tests.py negative           # Run negative/validation tests
   python run_tests.py all               # Run all test scenarios
   python run_tests.py html               # Run all tests with HTML report
   python run_tests.py allure             # Run all tests with Allure report
   
   # Direct behave commands (alternative)
   behave                                  # Run all tests
   behave features/login.feature           # Run specific feature
   behave --tags=@smoke                    # Run smoke tests only
   behave --tags=@positive                 # Run positive scenarios
   behave --tags=@negative                 # Run negative/validation tests
   behave --tags=@ui                       # Run UI functionality tests
   behave -f html -o reports/report.html   # Basic HTML report
   
   # Browser selection
   python run_tests.py smoke --browser firefox
   python run_tests.py all --browser edge
   ```

## Advanced Features

### **Robust Error Handling**
The framework includes comprehensive fallback strategies:
- **Multiple locator strategies**: Automatic fallback if primary locator fails
- **Retry logic**: Automatic retries for flaky elements
- **Screenshot capture**: Automatic screenshots on test failures
- **Browser log capture**: Console logs saved for debugging
- **Page source capture**: Full page HTML saved on failures

### **Allure Reporting Workflow**
```bash
# Run tests with Allure reporting
python run_tests.py smoke-allure
   
# Generate and serve Allure reports
allure serve reports/allure-results/

# Or generate static report
allure generate reports/allure-results -o reports/allure-report --clean
open reports/allure-report/index.html
```

### **Test Execution Options**
```bash
# Available commands in run_tests.py
python run_tests.py setup              # Environment setup and validation
python run_tests.py validate           # Validate test environment
python run_tests.py all               # Run all test scenarios  
python run_tests.py smoke             # Run critical smoke tests
python run_tests.py positive          # Run positive test scenarios
python run_tests.py negative          # Run negative/validation tests
python run_tests.py ui                # Run UI functionality tests
python run_tests.py security          # Run security-related tests
python run_tests.py html              # Generate basic HTML reports
python run_tests.py allure            # Generate Allure reports
python run_tests.py smoke-allure      # Smoke tests with Allure
python run_tests.py parallel          # Parallel test execution
python run_tests.py headless          # Headless browser execution
python run_tests.py feature --file features/login.feature  # Run specific feature
python run_tests.py scenario --name "Scenario Name"        # Run specific scenario
```

## Configuration

The test suite supports comprehensive configuration options:

### **Browser Support**
- **Chrome** (default): Full feature support with extensive logging
- **Firefox**: Cross-browser validation with Gecko driver
- **Safari**: macOS native browser testing  
- **Edge**: Microsoft Edge browser support

### **Execution Modes**
- **GUI Mode**: Visual browser execution for debugging
- **Headless Mode**: Background execution for CI/CD pipelines
- **Parallel Execution**: Multiple browser instances for faster execution

### **Environment Configuration**
Configuration managed through `config/config.yaml`:
```yaml
browser:
  default: chrome
  headless: false
  timeout: 30

urls:
  base_url: "https://www.hudl.com"
  login_page: "https://www.hudl.com/login"

waits:
  implicit_wait: 10
  explicit_wait: 30
  page_load_timeout: 60
```

### **Test Data Management**
Test data organized in `config/test_data.yaml`:
```yaml
valid_credentials:
  email: "test.user@example.com"
  password: "SecurePass123!"

invalid_credentials:
  email: "invalid.user@example.com" 
  password: "WrongPassword!"

invalid_email_formats:
  - "invalid.email"
  - "@domain.com"
  - "user@"
  # ... additional test cases
```

## Reporting

The suite generates comprehensive test reports with multiple output formats:

### **Allure Reports (Recommended)**
- **Requirements**: Allure CLI must be installed (`brew install allure`)
- **Command**: `python run_tests.py allure` or `python run_tests.py smoke-allure`
- **Features**: 
  - Interactive dashboard with test execution trends
  - Step-by-step execution details with precise timing
  - Automatic screenshot embedding on failures
  - Page source and browser console logs attached
  - Test categorization by tags and severity
  - Historical trend analysis across test runs
  - Environment and configuration information
  - Rich filtering and search capabilities

### **Basic HTML Reports**
- **Location**: `reports/report.html`
- **Command**: `python run_tests.py html`
- **Features**: Simple pass/fail overview with basic step details

### **Console Output & Debugging**
- **Real-time feedback**: Live test execution progress
- **Failure screenshots**: Automatically saved to `reports/failure_*.png`
- **Page source capture**: Full HTML saved on step failures
- **Browser logs**: Console logs captured and attached
- **Detailed error messages**: Enhanced error context with fallback attempt details

### **Report Locations**
```
reports/
├── allure-results/          # Raw Allure test data
├── allure-report/           # Generated Allure HTML reports  
├── report.html              # Basic HTML report
├── failure_*.png            # Automatic failure screenshots
├── step_failure_*.html      # Page source on failures
└── test_summary.txt         # Test execution summary
```

## Framework Architecture

### **Page Object Model Implementation**
- **BasePage**: Centralized error handling, fallback locators, and Allure integration
- **Inheritance**: All page classes inherit robust base functionality
- **Fallback Strategies**: Multiple locator strategies with automatic retry
- **Error Recovery**: Graceful handling of stale elements and timeouts

### **BDD Test Structure**  
- **Natural Language**: Tests written in business-readable Gherkin syntax
- **Step Reusability**: Modular step definitions with comprehensive coverage
- **Tag Organization**: `@smoke`, `@positive`, `@negative`, `@ui`, `@functionality` tags
- **Background Steps**: Common setup steps executed before each scenario

### **Advanced Error Handling**
- **Fallback Locators**: `find_element_with_fallback()` with multiple strategies
- **Retry Logic**: `click_with_fallback()` and `send_keys_with_fallback()` 
- **Screenshot Integration**: Automatic capture and Allure attachment
- **Log Aggregation**: Browser console logs and page source preservation
- **Context Preservation**: Detailed error context for efficient debugging

## Best Practices Implemented

### **Test Design Patterns**
1. **Page Object Model**: Complete separation of test logic from page interactions
2. **BDD Approach**: Tests written in natural language using Gherkin syntax
3. **Fallback Strategies**: Robust element finding with multiple locator approaches
4. **Error Recovery**: Comprehensive retry logic and graceful error handling

### **Code Quality & Maintenance**
5. **Configuration Management**: Centralized YAML-based configuration
6. **Wait Strategies**: Explicit waits with proper timeout handling
7. **Cross-browser Support**: Unified driver management across browsers
8. **Modular Architecture**: Reusable components and inheritance patterns

### **Reporting & Debugging**
9. **Enhanced Reporting**: Allure integration with rich test documentation
10. **Failure Analysis**: Automatic screenshot, page source, and log capture
11. **Step Tracking**: Detailed step execution with timing and context
12. **Error Context**: Comprehensive error messages with debugging information

## Current Implementation Status

### ✅ **Fully Implemented & Tested**
- **17 Test Scenarios**: Complete coverage of login functionality
- **68 Step Definitions**: Comprehensive step implementation with error handling
- **5 Page Objects**: Login, Dashboard, Home, New Account, Reset Password pages
- **Fallback Strategies**: Multiple locator strategies with automatic retry
- **Allure Integration**: Rich reporting with screenshots and attachments
- **Cross-Browser Support**: Chrome, Firefox, Edge, Safari compatibility
- **Error Handling**: Robust failure capture and recovery mechanisms

### 🏗️ **Framework Features**
- **Advanced Error Reporting**: Screenshots, logs, and page source capture
- **Flexible Test Execution**: Multiple execution modes and configurations
- **BDD Test Structure**: Natural language test scenarios
- **YAML Configuration**: Easy maintenance and environment management
- **Comprehensive Documentation**: Detailed setup and usage instructions

## Quick Start

```bash
# Setup and run smoke tests
cd /path/to/hudl-testing
source venv/bin/activate
python run_tests.py smoke-allure

# View results
allure serve reports/allure-results/
```

## Contributing

### **Adding New Test Scenarios**
1. **Update Feature File**: Add Gherkin scenarios to `features/login.feature`
2. **Implement Steps**: Add step definitions to `features/steps/login_steps.py`
3. **Update Page Objects**: Extend page classes in `pages/` directory
4. **Test Data**: Update `config/test_data.yaml` as needed
5. **Documentation**: Update `TEST_SCENARIOS.md` with new scenarios

### **Code Standards**
- Follow existing Page Object Model patterns
- Use fallback locator strategies from BasePage
- Include comprehensive error handling and Allure integration
- Add appropriate tags (`@smoke`, `@positive`, `@negative`, etc.)
- Ensure all tests pass before submitting changes
- Update documentation for any new features or scenarios
