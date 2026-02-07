@echo off
setlocal
echo ===================================================
echo Mail2PDF NextGen - Verification and Run Script
echo ===================================================

if not exist "data\config_dynamic.json" (
    echo [WARNING] data\config_dynamic.json not found. Using defaults.
) else (
    echo [OK] data\config_dynamic.json found.
)

if not exist "data\languages.json" (
    echo [WARNING] data\languages.json not found. Using internal defaults.
    echo Please verify that the file exists for complete translations.
) else (
    echo [OK] data\languages.json found.
)

REM Try to find python
where python >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    set PYTHON_CMD=python
    goto :FOUND_PYTHON
)

where py >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    set PYTHON_CMD=py
    goto :FOUND_PYTHON
)

echo.
echo [ERROR] Python not found in PATH.
echo Please ensure Python is installed and added to your PATH.
echo.
pause
exit /b 1

:FOUND_PYTHON
echo [INFO] Using Python: %PYTHON_CMD%
%PYTHON_CMD% --version

echo.
echo [1/2] Running Tests (tests/test_ui_config.py)...
%PYTHON_CMD% tests/test_ui_config.py
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Tests failed!
    pause
    exit /b 1
) else (
    echo [SUCCESS] Tests passed!
)

echo.
echo [2/2] Starting Application...
echo Access the app at http://localhost:5000
echo Press Ctrl+C to stop.
echo.
%PYTHON_CMD% app.py

endlocal
