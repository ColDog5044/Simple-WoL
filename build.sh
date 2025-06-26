#!/bin/bash
# Linux/macOS build script for Simple Wake-on-LAN

echo "Building Simple Wake-on-LAN for Linux..."
echo

# Check if Python is available
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "Error: Python is not installed or not in PATH"
    echo "Please install Python 3.7+ using your package manager"
    exit 1
fi

# Prefer python3 if available
if command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
else
    PYTHON_CMD=python
fi

# Install build dependencies if needed
echo "Installing build dependencies..."
$PYTHON_CMD -m pip install -r requirements-build.txt

# Run the build script
echo
echo "Running build..."
$PYTHON_CMD build/build_linux.py

echo
echo "Build process completed."
