# 🎉 SMART ICE TRACKER - BẮT ĐẦU TẠI ĐÂY

## ✅ Tóm Tắt Dự Án

**Smart Ice Tracker** - Hệ thống theo dõi nước đá thông minh với:

- 🎥 **2 Camera Live:** Nhận diện biển số + Đếm bao
- 🔥 **Firebase Realtime Database:** Lưu trữ & truy vấn dữ liệu
- 🌐 **Streamlit Web UI:** Xem camera, thống kê, export dữ liệu
- ⚡ **GPU Support:** CUDA 12.1, PyTorch acceleration

---

## 🚀 Chạy Ngay (1 Lệnh)

```bash
# Windows - Chạy tất cả (camera + Streamlit)
run.bat

# Hoặc chỉ chạy Streamlit UI
run_streamlit.bat

# Hoặc dùng Python
python run.py
```

**Truy cập:** `http://localhost:8501`

---

## 📁 Cấu Trúc Dự Án

```
smartIceTracker/
├── src/
│   ├── core/              # Camera & ML logic
│   │   ├── camera_manager.py
│   │   ├── license_plate.py
│   │   ├── bag_counter.py
│   │   └── firebase_handler.py
│   ├── ui/                # Streamlit apps
│   │   ├── app_basic.py
│   │   ├── app_advanced.py
│   │   └── app_camera.py
│   └── utils/             # Helpers
│       └── camera_helper.py
├── config/                # Configuration
├── data/                  # Videos & datasets
├── model/                 # YOLO models
└── tests/                 # Test files
```

---

## 📖 Tài Liệu Hướng Dẫn

| File             | Mô Tả             |
| ---------------- | ----------------- |
| `README.md`      | Tổng quan dự án   |
| `QUICK_START.md` | Hướng dẫn nhanh   |
| `SETUP.md`       | Cài đặt chi tiết  |
| `STRUCTURE.md`   | Chi tiết cấu trúc |

---

## 🛠️ Tech Stack

- **Python 3.12** + PyTorch 2.5
- **YOLO v8** + EasyOCR
- **Firebase Admin SDK**
- **Streamlit** + OpenCV
- **CUDA 12.1** (GPU Support)

---

## 💻 Yêu Cầu Hệ Thống

| Thành Phần   | Yêu Cầu                  |
| ------------ | ------------------------ |
| Python       | 3.8+                     |
| RAM          | 4GB+                     |
| GPU          | CUDA 11.8+ (khuyến nghị) |
| Internet     | Có (cho Firebase)        |
| Firebase Key | `firebase-key.json`      |

---

## 💡 Lưu Ý Quan Trọng

1. **Firebase Key:** Đặt file `firebase-key.json` trong thư mục gốc
2. **Video Files:** Đặt video trong `data/video/Day/` hoặc `data/video/Night/`
3. **YOLO Model:** File `model/best.pt` phải tồn tại

---

## 🔧 Cài Đặt Lần Đầu

```bash
# 1. Tạo virtual environment
python -m venv venv

# 2. Kích hoạt venv
# Windows
venv\Scripts\activate

# 3. Cài đặt dependencies
pip install -r requirements.txt

# 4. Chạy ứng dụng
python run.py
```

---

## 📺 Tính Năng Chính

### Trang 1: Xem Camera 🎥

- Hiển thị 2 camera thời gian thực
- Nhận diện biển số xe
- Đếm bao nước đá
- Thống kê realtime

### Trang 2: Quản Lý Dữ Liệu 📊

- Xem dữ liệu từ Firebase
- Biểu đồ thống kê (bar chart, line chart)
- Tìm kiếm và lọc dữ liệu
- Xuất CSV/Excel

---

## 🆘 Khắc Phục Sự Cố

### Lỗi Module Not Found

```bash
pip install -r requirements.txt
```

### Port 8501 đã sử dụng

```bash
streamlit run src/ui/app_camera.py --server.port 8502
```

### Firebase không kết nối

- Kiểm tra `firebase-key.json` tồn tại
- Kiểm tra format JSON hợp lệ
- Kiểm tra kết nối internet

### Camera không hiển thị

- Kiểm tra đường dẫn video trong `config/settings.py`
- Đảm bảo file video tồn tại
- Kiểm tra quyền truy cập camera

---

## 📞 Hỗ Trợ

Xem các file hướng dẫn chi tiết:

- `README.md` - Tổng quan
- `QUICK_START.md` - Quick start
- `SETUP.md` - Cài đặt
- `STRUCTURE.md` - Cấu trúc

---

**🎉 Bắt đầu ngay với Smart Ice Tracker!**

_Last Updated: November 2025_
