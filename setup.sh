#!/bin/bash

# Hudl Login Testing - Quick Start Script
# This script sets up the testing environment and runs basic tests

set -e  # Exit on any error

echo "🚀 Hudl Login Testing - Quick Start"
echo "=================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check Python version
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✅ Python version: $python_version"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "⚙️ Creating environment configuration..."
    cp .env.example .env
    echo "📝 Please update .env file with your test credentials if needed"
fi

# Create reports directory
mkdir -p reports

# Validate environment
echo "🔍 Validating environment..."
python3 -c "
import sys
try:
    import selenium
    import behave
    import yaml
    print('✅ All required packages are installed')
except ImportError as e:
    print(f'❌ Missing package: {e}')
    sys.exit(1)
"

echo ""
echo "🎯 Environment setup complete! You can now run tests:"
echo ""
echo "Basic Commands:"
echo "  python3 run_tests.py all              # Run all tests"
echo "  python3 run_tests.py smoke            # Run smoke tests"
echo "  python3 run_tests.py html             # Run tests with HTML report"
echo "  behave                                 # Direct Behave command"
echo ""
echo "Advanced Commands:"
echo "  python3 run_tests.py security         # Run security tests"
echo "  python3 run_tests.py headless         # Run in headless mode"
echo "  python3 run_tests.py allure           # Generate Allure report"
echo ""
echo "Browser Options:"
echo "  python3 run_tests.py all --browser chrome"
echo "  python3 run_tests.py all --browser firefox"
echo "  python3 run_tests.py all --browser edge"
echo ""
echo "🏃‍♂️ Running a quick smoke test..."
echo ""

# Run smoke tests
python3 run_tests.py smoke

echo ""
echo "🎉 Setup and smoke test completed successfully!"
echo "📊 Check the reports/ directory for test results"
echo ""
echo "Next steps:"
echo "1. Update .env file with actual test credentials"
echo "2. Run 'python3 run_tests.py all' for full test suite"
echo "3. Check README.md for detailed documentation"
