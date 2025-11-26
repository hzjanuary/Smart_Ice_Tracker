# 🎯 Smart Ice Tracker - Cài Đặt & Chạy

## ⚡ Chạy Ngay (Nhanh Nhất)

### Windows

```bash
# Chạy tất cả (camera + Streamlit)
run.bat

# Hoặc chỉ Streamlit UI
run_streamlit.bat
```

### Linux / Mac / Cross-platform

```bash
python run.py
```

---

## ✨ Hệ Thống Sẽ Khởi Động

```
✅ Camera Processor
   └─ Nhận diện biển số
   └─ Đếm bao nước đá
   └─ Lưu dữ liệu vào Firebase

✅ Streamlit Web UI
   └─ Xem 2 camera livestream
   └─ Biểu đồ thống kê
   └─ Auto refresh mỗi 10 giây
   └─ Export CSV/Excel
```

**Truy cập:** `http://localhost:8501`

---

## 📋 Cài Đặt Lần Đầu

### Bước 1: Tạo Virtual Environment

```bash
python -m venv venv
```

### Bước 2: Kích Hoạt Environment

```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### Bước 3: Cài Dependencies

```bash
pip install -r requirements.txt
```

### Bước 4: Chuẩn Bị Files

- ✅ Đặt `firebase-key.json` trong thư mục gốc
- ✅ Đặt video trong `data/video/Day/` hoặc `data/video/Night/`
- ✅ Đảm bảo `model/best.pt` tồn tại

### Bước 5: Chạy Ứng Dụng

```bash
python run.py
```

---

## 🎯 Giao Diện Ứng Dụng

### Tab 1: 🎥 Xem Camera

- 2 camera live stream (biển số + đếm bao)
- Thống kê realtime
- Lịch sử phát hiện gần đây

### Tab 2: 📊 Quản Lý Dữ Liệu

- Bảng dữ liệu từ Firebase
- Biểu đồ thống kê (bar chart, line chart)
- Tìm kiếm & filter
- Export CSV/Excel

---

## 🛑 Dừng Hệ Thống

```bash
# Nhấn trong terminal
Ctrl+C

# Hoặc nhấn trong cửa sổ camera
q
```

---

## 💻 Yêu Cầu Hệ Thống

| Thành Phần | Yêu Cầu                  |
| ---------- | ------------------------ |
| Python     | 3.8+                     |
| RAM        | 4GB+                     |
| GPU        | CUDA 11.8+ (khuyến nghị) |
| Internet   | Có (cho Firebase)        |
| Disk       | 2GB+ free space          |

---

## ⚙️ Tùy Chỉnh (Nâng Cao)

### Đổi Video Path

File: `src/core/camera_manager.py`

```python
run_license_plate("YOUR_VIDEO_1.mp4", ...)
run_bag_counter("YOUR_VIDEO_2.mp4", ...)
```

### Đổi Cache Time (Auto-refresh)

File: `src/ui/app_camera.py`

```python
@st.cache_data(ttl=5)  # 5 giây thay vì 10
```

### Đổi Port Streamlit

```bash
streamlit run src/ui/app_camera.py --server.port 8502
```

---

## 🆘 Khắc Phục Sự Cố

### Lỗi: Module Not Found

```bash
pip install -r requirements.txt
```

### Port 8501 đã sử dụng

```bash
streamlit run src/ui/app_camera.py --server.port 8502
```

### Firebase không kết nối

- Kiểm tra `firebase-key.json` tồn tại
- Kiểm tra internet connection
- Xem Firebase Console logs

### Camera không hiển thị

- Kiểm tra đường dẫn video trong code
- Đảm bảo file video tồn tại
- Kiểm tra permissions

### Lỗi CUDA/GPU

```bash
# Kiểm tra CUDA
python -c "import torch; print(torch.cuda.is_available())"

# Nếu không có GPU, YOLO vẫn chạy trên CPU (chậm hơn)
```

---

## 📖 Tài Liệu Thêm

- `README.md` - Tổng quan dự án
- `QUICK_START.md` - Hướng dẫn nhanh
- `STRUCTURE.md` - Chi tiết cấu trúc
- `00_START_HERE.md` - Bắt đầu từ đây

---

## 🛠️ Tech Stack

- Python 3.12 + PyTorch 2.5
- YOLO v8 + EasyOCR
- Firebase Admin SDK
- Streamlit + OpenCV
- CUDA 12.1 (GPU Support)

---

**🎉 Sẵn sàng sử dụng Smart Ice Tracker!**

_Last Updated: November 2025_
