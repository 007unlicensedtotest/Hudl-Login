#!/usr/bin/env python3
"""
Test runner script for Hudl login testing.
Provides convenient commands for running different types of tests.
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path


def run_command(command, description):
    """
    Run a command and handle errors.
    
    Args:
        command: Command to run
        description: Description of what the command does
    """
    print(f"\n{description}")
    print(f"Running: {command}")
    print("-" * 50)
    
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.stdout:
        print(result.stdout)
    
    if result.stderr:
        print(f"Error: {result.stderr}")
    
    if result.returncode != 0:
        print(f"Command failed with return code: {result.returncode}")
        sys.exit(1)
    
    print(f"✓ {description} completed successfully")


def setup_environment():
    """Set up the test environment."""
    print("Setting up test environment...")
    
    # Create .env file if it doesn't exist
    if not os.path.exists('.env'):
        print("Creating .env file from template...")
        subprocess.run(['cp', '.env.example', '.env'])
        print("Please update .env file with your test credentials")
    
    # Install dependencies
    run_command("pip install -r requirements.txt", "Installing Python dependencies")
    
    # Create reports directory
    os.makedirs('reports', exist_ok=True)
    print("✓ Test environment setup completed")


def run_all_tests():
    """Run all tests."""
    run_command("behave", "Running all Behave tests")


def run_smoke_tests():
    """Run smoke tests only."""
    run_command("behave --tags=@smoke", "Running smoke tests")


def run_positive_tests():
    """Run positive tests only."""
    run_command("behave --tags=@positive", "Running positive tests")


def run_negative_tests():
    """Run negative tests only."""
    run_command("behave --tags=@negative", "Running negative tests")


def run_ui_tests():
    """Run UI/UX tests only."""
    run_command("behave --tags=@ui", "Running UI/UX tests")


def run_security_tests():
    """Run security tests only."""
    run_command("behave --tags=@security", "Running security tests")


def run_with_html_report():
    """Run tests with HTML report."""
    run_command(
        "behave -f html -o reports/report.html",
        "Running tests with HTML report"
    )


def run_with_allure_report():
    """Run tests with Allure report."""
    # Clean previous results
    run_command("rm -rf reports/allure-results", "Cleaning previous Allure results")
    
    # Run tests with Allure formatter
    run_command(
        "behave -f allure_behave.formatter:AllureFormatter -o reports/allure-results",
        "Running tests with Allure formatter"
    )
    
    # Generate Allure report
    run_command(
        "allure generate reports/allure-results -o reports/allure-report --clean",
        "Generating Allure report"
    )
    
    print("\nAllure report generated in reports/allure-report/")
    print("To serve the report, run: allure serve reports/allure-results")


def run_smoke_tests_with_allure():
    """Run smoke tests with Allure report."""
    # Clean previous results
    run_command("rm -rf reports/allure-results", "Cleaning previous Allure results")
    
    # Run smoke tests with Allure formatter
    run_command(
        "behave --tags=@smoke -f allure_behave.formatter:AllureFormatter -o reports/allure-results",
        "Running smoke tests with Allure formatter"
    )
    
    # Generate Allure report
    run_command(
        "allure generate reports/allure-results -o reports/allure-report --clean",
        "Generating Allure report for smoke tests"
    )
    
    print("\nAllure report for smoke tests generated in reports/allure-report/")
    print("To serve the report, run: allure serve reports/allure-results")


def run_parallel_tests():
    """Run tests in parallel."""
    run_command(
        "behave --processes 4 --parallel-element scenario",
        "Running tests in parallel"
    )


def run_headless_tests():
    """Run tests in headless mode."""
    env = os.environ.copy()
    env['HEADLESS'] = 'true'
    
    print("\nRunning tests in headless mode")
    print("-" * 50)
    
    result = subprocess.run(
        ["behave"],
        env=env,
        capture_output=True,
        text=True
    )
    
    if result.stdout:
        print(result.stdout)
    
    if result.stderr:
        print(f"Error: {result.stderr}")
    
    if result.returncode == 0:
        print("✓ Headless tests completed successfully")
    else:
        print(f"Tests failed with return code: {result.returncode}")
        sys.exit(1)


def run_specific_feature(feature_file):
    """Run a specific feature file."""
    if not os.path.exists(feature_file):
        print(f"Feature file not found: {feature_file}")
        sys.exit(1)
    
    run_command(
        f"behave {feature_file}",
        f"Running feature: {feature_file}"
    )


def run_specific_scenario(scenario_name):
    """Run a specific scenario by name."""
    run_command(
        f"behave --name='{scenario_name}'",
        f"Running scenario: {scenario_name}"
    )


def validate_environment():
    """Validate that the environment is properly set up."""
    print("Validating test environment...")
    
    # Check Python version
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        print("Error: Python 3.8 or higher is required")
        sys.exit(1)
    print(f"✓ Python version: {python_version.major}.{python_version.minor}")
    
    # Check required files
    required_files = [
        'requirements.txt',
        'features/login.feature',
        'features/environment.py',
        'config/config.yaml',
        'config/test_data.yaml'
    ]
    
    for file_path in required_files:
        if not os.path.exists(file_path):
            print(f"Error: Required file not found: {file_path}")
            sys.exit(1)
        print(f"✓ Found: {file_path}")
    
    # Check if dependencies are installed
    try:
        import selenium
        import behave
        import yaml
        print("✓ Required packages are installed")
    except ImportError as e:
        print(f"Error: Missing required package: {e}")
        print("Run: pip install -r requirements.txt")
        sys.exit(1)
    
    print("✓ Environment validation completed successfully")


def main():
    """Main function to handle command line arguments."""
    parser = argparse.ArgumentParser(description='Hudl Login Test Runner')
    parser.add_argument('command', choices=[
        'setup', 'validate', 'all', 'smoke', 'positive', 'negative',
        'ui', 'security',
        'html', 'allure', 'smoke-allure', 'parallel', 'headless', 'feature', 'scenario'
    ], help='Command to run')
    
    parser.add_argument('--file', help='Feature file to run (for feature command)')
    parser.add_argument('--name', help='Scenario name to run (for scenario command)')
    parser.add_argument('--browser', help='Browser to use (chrome, firefox, edge, safari)')
    parser.add_argument('--env', help='Environment to test (local, staging, production)')
    
    args = parser.parse_args()
    
    # Set environment variables from arguments
    if args.browser:
        os.environ['BROWSER'] = args.browser
    
    if args.env:
        os.environ['TEST_ENV'] = args.env
    
    # Execute the requested command
    if args.command == 'setup':
        setup_environment()
    elif args.command == 'validate':
        validate_environment()
    elif args.command == 'all':
        run_all_tests()
    elif args.command == 'smoke':
        run_smoke_tests()
    elif args.command == 'positive':
        run_positive_tests()
    elif args.command == 'negative':
        run_negative_tests()
    elif args.command == 'ui':
        run_ui_tests()
    elif args.command == 'security':
        run_security_tests()
    elif args.command == 'html':
        run_with_html_report()
    elif args.command == 'allure':
        run_with_allure_report()
    elif args.command == 'smoke-allure':
        run_smoke_tests_with_allure()
    elif args.command == 'parallel':
        run_parallel_tests()
    elif args.command == 'headless':
        run_headless_tests()
    elif args.command == 'feature':
        if not args.file:
            print("Error: --file argument is required for feature command")
            sys.exit(1)
        run_specific_feature(args.file)
    elif args.command == 'scenario':
        if not args.name:
            print("Error: --name argument is required for scenario command")
            sys.exit(1)
        run_specific_scenario(args.name)


if __name__ == '__main__':
    main()
