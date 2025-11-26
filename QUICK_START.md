# 🚀 Quick Start - Smart Ice Tracker

## ⚡ Chạy Ứng Dụng Nhanh Nhất

### Cách 1: Script Batch (Windows)

```bash
# Chạy cả camera processor và Streamlit UI
run.bat

# Hoặc chỉ chạy Streamlit UI
run_streamlit.bat
```

### Cách 2: PowerShell

```powershell
.\run_streamlit.ps1
```

### Cách 3: Python Command

```bash
# Chạy tất cả
python run.py

# Hoặc chỉ Streamlit
streamlit run src/ui/app_camera.py
```

---

## 🌐 Truy Cập Ứng Dụng

**URL mặc định:** `http://localhost:8501`

Muốn truy cập từ máy khác trong mạng:

```bash
streamlit run src/ui/app_camera.py --server.address 0.0.0.0
```

---

## 📺 Các Trang Chính

### 1. 🎥 Xem Camera (app_camera.py)

- Hiển thị 2 camera thời gian thực
- Camera 1: Đếm bao nước đá
- Camera 2: Nhận diện biển số xe
- Auto-refresh dữ liệu Firebase (10 giây)

### 2. 📊 Quản Lý Dữ Liệu (app_basic.py / app_advanced.py)

- Lấy dữ liệu từ Firebase
- Thống kê theo ngày/tháng
- Xuất CSV/Excel
- Biểu đồ trực quan

---

## ✅ Kiểm Tra Cài Đặt

```bash
# Kiểm tra Python version
python --version

# Kiểm tra các thư viện chính
python -c "import streamlit; import torch; import cv2; import firebase_admin; print('✅ All packages OK')"
```

---

## 🔧 Yêu Cầu

1. **Firebase Key:** File `firebase-key.json` phải có trong thư mục gốc
2. **Video Files:** Đặt video trong `data/video/Day/` hoặc `data/video/Night/`
3. **Model Files:** YOLO model trong `model/best.pt`

---

## 💡 Mẹo Sử Dụng

- **Auto-reload:** Streamlit tự động reload khi code thay đổi
- **Cache:** Dữ liệu Firebase cache 10 giây (có thể tùy chỉnh)
- **Debug Mode:** Thêm flag `--logger.level=debug` để xem chi tiết

```bash
streamlit run src/ui/app_camera.py --logger.level=debug
```

---

## 🆘 Khắc Phục Sự Cố

### Lỗi: Module Not Found

```bash
pip install -r requirements.txt
```

### Port 8501 đã được sử dụng

```bash
streamlit run src/ui/app_camera.py --server.port 8502
```

### Firebase không kết nối

- Kiểm tra `firebase-key.json` tồn tại và format đúng
- Kiểm tra internet connection
- Xem Firebase Console rules

### Camera không hiển thị

- Kiểm tra đường dẫn video trong `config/settings.py`
- Đảm bảo file video tồn tại
- Kiểm tra camera permission (nếu dùng webcam)

---

**🎉 Xong! Bắt đầu sử dụng Smart Ice Tracker!**
