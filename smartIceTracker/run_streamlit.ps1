# Script chạy Streamlit App - Smart Ice Tracker
# Sử dụng: .\run_streamlit.ps1

# Kiểm tra xem có trong đúng thư mục không
if (!(Test-Path "venv")) {
    Write-Host "❌ Lỗi: Virtual environment không tìm thấy!" -ForegroundColor Red
    Write-Host "Chạy: python -m venv venv" -ForegroundColor Yellow
    exit 1
}

# Kích hoạt virtual environment
& ".\venv\Scripts\Activate.ps1"

# Hiển thị thông tin
Write-Host "" -ForegroundColor White
Write-Host "====================================================="-ForegroundColor Cyan
Write-Host "   🧊 Smart Ice Tracker - Streamlit Application     "-ForegroundColor Cyan
Write-Host "====================================================="-ForegroundColor Cyan
Write-Host "" -ForegroundColor White
Write-Host "✅ Ứng dụng sẽ mở tại: http://localhost:8501" -ForegroundColor Green
Write-Host "⏹️  Nhấn Ctrl+C để dừng ứng dụng" -ForegroundColor Yellow
Write-Host "" -ForegroundColor White

# Chạy Streamlit
streamlit run streamlit_app.py
