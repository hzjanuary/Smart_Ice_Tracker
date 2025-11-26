@echo off
REM Script chạy Streamlit App - Smart Ice Tracker
REM Chạy từ thư mục dự án

cd /d "%~dp0"

REM Kích hoạt virtual environment
call venv\Scripts\activate.bat

REM Chạy Streamlit
echo.
echo =====================================================
echo    🧊 Smart Ice Tracker - Streamlit Application
echo =====================================================
echo.
echo Ứng dụng sẽ mở tại: http://localhost:8501
echo Nhấn Ctrl+C để dừng ứng dụng
echo.

streamlit run streamlit_app.py

pause
