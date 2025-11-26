# 🧊 Smart Ice Tracker

> Hệ thống theo dõi nước đá thông minh với camera realtime, YOLO detection và Firebase backend

## 🎯 Tính Năng Chính

✅ **2 Camera Live Stream** - Nhận diện biển số (YOLO + EasyOCR) & Đếm bao (YOLO detection)  
✅ **Firebase Realtime Database** - Lưu trữ và truy vấn dữ liệu thời gian thực  
✅ **Web UI (Streamlit)** - Xem camera, biểu đồ thống kê, export CSV/Excel  
✅ **GPU Support** - CUDA 12.1 (RTX 3050), PyTorch acceleration

---

## 🚀 Quick Start

### 1. Cài Đặt Dependencies

```bash
pip install -r requirements.txt
```

### 2. Chạy Ứng Dụng

**Chạy camera processor và Streamlit UI:**

```bash
# Windows
run.bat

# Hoặc sử dụng Python
python run.py
```

**Chỉ chạy Streamlit UI:**

```bash
# Windows
run_streamlit.bat

# Hoặc
streamlit run src/ui/app_camera.py
```

### 3. Truy Cập

```
🎬 Camera: OpenCV window (nhấn 'q' để thoát)
🌐 Streamlit: http://localhost:8501
```

---

## 📁 Cấu Trúc Dự Án

```
smartIceTracker/
├── src/
│   ├── core/              # Camera & ML processing logic
│   │   ├── camera_manager.py
│   │   ├── license_plate.py
│   │   ├── bag_counter.py
│   │   └── firebase_handler.py
│   ├── ui/                # Streamlit applications
│   │   ├── app_basic.py
│   │   ├── app_advanced.py
│   │   └── app_camera.py
│   └── utils/             # Helper utilities
│       └── camera_helper.py
├── config/                # Configuration files
├── data/                  # Videos & training data
├── model/                 # YOLO models
├── tests/                 # Test files
└── docs/                  # Documentation
```

---

## 🛠️ Tech Stack

- **Python 3.12** - Core language
- **YOLO v8** - Object detection
- **EasyOCR** - License plate recognition
- **PyTorch 2.5** - GPU acceleration
- **Firebase Admin** - Realtime database
- **Streamlit** - Web UI
- **OpenCV** - Video processing

---

## 📖 Tài Liệu

- **`00_START_HERE.md`** - Hướng dẫn tổng quan
- **`QUICK_START.md`** - Quick start guide
- **`SETUP.md`** - Cài đặt chi tiết
- **`STRUCTURE.md`** - Chi tiết cấu trúc thư mục

---

## 🔧 Development

### Chạy riêng từng module

```bash
# Camera processor
python src/core/camera_manager.py

# Streamlit basic
streamlit run src/ui/app_basic.py

# Streamlit with camera
streamlit run src/ui/app_camera.py
```

### Testing

```bash
python tests/test_main.py
python tests/test_firebase.py
```

---

## 📞 Hỗ Trợ

Gặp vấn đề? Xem các tài liệu hướng dẫn trong thư mục gốc hoặc kiểm tra Firebase logs.

---

**🎉 Smart Ice Tracker - Production Ready**

_Last Updated: November 2025_
