#!/bin/bash
# Run script for the modular Simple Wake-on-LAN application (Linux/macOS)

echo "Starting Simple Wake-on-LAN (Modular Version)..."
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

# Run the application
$PYTHON_CMD run_modular.py

# Check exit code
if [ $? -ne 0 ]; then
    echo
    echo "Application exited with an error"
    read -p "Press Enter to continue..."
fi
