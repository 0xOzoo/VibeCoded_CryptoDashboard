@echo off
title Crypto Dashboard
color 0A

echo.
echo ========================================
echo    🚀 CRYPTO PORTFOLIO DASHBOARD
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Python is not installed or not in PATH
    echo 💡 Please install Python 3.8 or higher
    echo 📥 Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check if we're in the right directory
if not exist "app_enhanced.py" (
    echo ❌ ERROR: Please run this script from the projet_ia directory
    echo 💡 Navigate to the projet_ia folder and try again
    pause
    exit /b 1
)

echo ✅ Starting Crypto Dashboard...
echo 📊 Dashboard will be available at: http://localhost:8050
echo 🔄 Auto-refresh every 30 seconds
echo ⏹️  Press Ctrl+C to stop
echo.

REM Start the dashboard
python start_dashboard.py

pause
