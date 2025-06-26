@echo off
REM Run script for the modular Simple Wake-on-LAN application (Windows)

echo Starting Simple Wake-on-LAN (Modular Version)...
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://python.org
    pause
    exit /b 1
)

REM Run the application
python run_modular.py

REM Keep window open if there was an error
if %errorlevel% neq 0 (
    echo.
    echo Application exited with error code %errorlevel%
    pause
)
