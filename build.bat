@echo off
REM Windows build script for Simple Wake-on-LAN

echo Building Simple Wake-on-LAN for Windows...
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://python.org
    pause
    exit /b 1
)

REM Install build dependencies if needed
echo Installing build dependencies...
python -m pip install -r requirements-build.txt

REM Run the build script
echo.
echo Running build...
python build\build_windows.py

echo.
echo Build process completed.
pause
