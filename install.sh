#!/bin/bash

echo "Installing Simple Wake-on-LAN..."
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed."
    echo "Please install Python 3.7 or higher using your package manager:"
    echo "  Ubuntu/Debian: sudo apt install python3 python3-pip python3-tk"
    echo "  Fedora/RHEL: sudo dnf install python3 python3-pip python3-tkinter"
    echo "  Arch: sudo pacman -S python python-pip tk"
    exit 1
fi

# Check if tkinter is available
python3 -c "import tkinter" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "tkinter is not installed."
    echo "Please install tkinter using your package manager:"
    echo "  Ubuntu/Debian: sudo apt install python3-tk"
    echo "  Fedora/RHEL: sudo dnf install python3-tkinter"
    echo "  Arch: sudo pacman -S tk"
    exit 1
fi

# Install required packages
echo "Installing required packages..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "Failed to install required packages."
    echo "You may need to install pip first:"
    echo "  Ubuntu/Debian: sudo apt install python3-pip"
    echo "  Fedora/RHEL: sudo dnf install python3-pip"
    echo "  Arch: sudo pacman -S python-pip"
    exit 1
fi

# Make the script executable
chmod +x run.sh

echo
echo "Installation completed successfully!"
echo "You can now run the application with: ./run.sh"
echo
