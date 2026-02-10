@echo off
REM Stellar Compass Desktop Launcher
REM Double-click this file to start the app

title Stellar Compass - DeFi Assistant

echo.
echo ========================================================
echo    Stellar Compass - DeFi Assistant
echo ========================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

echo [1/3] Activating virtual environment...
if exist "backend\venv\Scripts\activate.bat" (
    call backend\venv\Scripts\activate.bat
) else if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
) else (
    echo WARNING: Virtual environment not found
    echo Running with system Python...
)

echo [2/3] Checking dependencies...
pip show flask >nul 2>&1
if errorlevel 1 (
    echo Installing required packages...
    pip install -r backend\requirements.txt
)

echo [3/3] Starting Stellar Compass...
echo.
python stellar_compass.py

if errorlevel 1 (
    echo.
    echo ERROR: Failed to start the application
    echo Check the error messages above
    pause
)
