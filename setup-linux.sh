#!/bin/bash
# README: Run this script from the jwt-security-analyzer project root
# usage: bash setup-linux.sh

set -e  # Exit on error

echo "🚀 JWT Security Analyzer - Linux Setup"
echo "======================================"

# Check Python version
echo ""
echo "✓ Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "  Found Python $PYTHON_VERSION"

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip3."
    exit 1
fi

# Create virtual environment
echo ""
echo "✓ Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "  Virtual environment created"
else
    echo "  Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "✓ Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "✓ Installing dependencies..."
pip install --upgrade pip setuptools wheel > /dev/null
pip install -r requirements.txt > /dev/null

# Create executable alias (optional)
echo ""
echo "✓ Checking secrets.txt..."
if [ -f "secrets.txt" ]; then
    echo "  secrets.txt found ✓"
else
    echo "  ⚠ secrets.txt not found - weak secret checks will be limited"
fi

echo ""
echo "✓ Checking dependencies..."
python main.py --help > /dev/null

echo ""
echo "======================================"
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Activate the Virtual Environment:"
echo "   source venv/bin/activate"
echo ""
echo "2. Analyze a JWT Token:"
echo "   python main.py scan <YOUR_TOKEN>"
echo ""
echo "3. View help:"
echo "   python main.py --help"
echo "   python main.py scan --help"
echo ""
echo "For detailed guide, see LINUX_SETUP.md"
