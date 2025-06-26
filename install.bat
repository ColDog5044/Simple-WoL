@echo off
echo Installing Simple Wake-on-LAN...
echo.

REM Check if Python is installed
py --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH.
    echo Please install Python 3.7 or higher from https://python.org
    pause
    exit /b 1
)

REM Install required packages
echo Installing required packages...
py -m pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo Failed to install required packages.
    pause
    exit /b 1
)

echo.
echo Installation completed successfully!
echo You can now run the application with: python simple_wol.py
echo.
pause
