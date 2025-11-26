@echo off
REM 🧊 Smart Ice Tracker - Windows Quick Launch
REM Run with: run.bat

cd /d "%~dp0"

echo ================================
echo Smart Ice Tracker
echo ================================
echo.
echo Starting system with: python run.py
echo.
echo Access Streamlit at: http://localhost:8501
echo.
echo Press Ctrl+C to stop
echo ================================
echo.

python run.py

pause
