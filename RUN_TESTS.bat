@echo off
REM Mail2PDF NextGen - Complete Testing Script
REM This script will:
REM 1. Check Python installation
REM 2. Install dependencies
REM 3. Run all tests
REM 4. Display startup instructions

echo.
echo ====================================================================
echo    Mail2PDF NextGen - Complete Testing & Verification
echo ====================================================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python 3.8+ from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo [OK] Python found
python --version
echo.

REM Install test requirements if needed
echo [INFO] Checking dependencies...
python -m pip install -q pytest 2>nul

REM Run the complete test script
echo.
echo ====================================================================
echo    Running Complete Test Suite
echo ====================================================================
echo.

python RUN_COMPLETE_TESTS.py

if errorlevel 1 (
    echo.
    echo WARNING: Some tests failed, but you can still try to start the server
    echo.
) else (
    echo.
    echo SUCCESS: All tests passed!
    echo.
)

echo.
echo ====================================================================
echo    NEXT STEPS:
echo ====================================================================
echo.
echo To START the Mail2PDF NextGen server:
echo.
echo   python app.py
echo.
echo Then open your browser to:
echo   http://localhost:5000
echo.
echo To access the configuration interface:
echo   http://localhost:5000/configure
echo.
echo ====================================================================
echo.
pause
