@echo off
REM Mail2PDF NextGen - Server Startup Script

echo.
echo ====================================================================
echo           Mail2PDF NextGen - Server Starting
echo ====================================================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH!
    echo.
    echo Solution:
    echo 1. Install Python 3.8+ from https://www.python.org/downloads/
    echo 2. During installation, check "Add Python to PATH"
    echo 3. Right-click this file and select "Run as administrator"
    echo.
    pause
    exit /b 1
)

REM Check if dependencies are installed
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo WARNING: Dependencies not installed!
    echo.
    echo Installing dependencies... this may take a few minutes...
    python -m pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo ERROR: Failed to install dependencies!
        echo Please check your internet connection or Python installation.
        echo.
        pause
        exit /b 1
    )
)

echo.
echo [OK] Python and dependencies verified
echo.
echo ====================================================================
echo    Starting Mail2PDF NextGen Server
echo ====================================================================
echo.
echo Server is starting on:
echo   → http://localhost:5000
echo.
echo Access the application at:
echo   → Web Interface:    http://localhost:5000
echo   → Configuration:    http://localhost:5000/configure
echo   → Documentation:    http://localhost:5000/documentation
echo.
echo To stop the server, press Ctrl+C
echo.
echo ====================================================================
echo.

REM Start the Flask application
python app.py

if errorlevel 1 (
    echo.
    echo ERROR: Server failed to start!
    echo Check the error messages above for details.
    echo.
    pause
    exit /b 1
)
