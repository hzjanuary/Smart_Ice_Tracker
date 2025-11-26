# 📁 Cấu Trúc Thư Mục Smart Ice Tracker

```
smartIceTracker/
│
├── 📁 src/                           # SOURCE CODE
│   ├── 📁 core/                      # Code chính xử lý camera
│   │   ├── __init__.py
│   │   ├── camera_manager.py         # (từ main.py)
│   │   ├── license_plate.py          # (từ licensePlate.py)
│   │   ├── bag_counter.py            # (từ bagCount.py)
│   │   └── firebase_handler.py       # (từ database.py)
│   │
│   ├── 📁 ui/                        # Streamlit UI
│   │   ├── __init__.py
│   │   ├── app_basic.py              # (từ streamlit_app.py)
│   │   ├── app_advanced.py           # (từ streamlit_app_advanced.py)
│   │   └── app_camera.py             # (từ streamlit_app_camera.py)
│   │
│   └── 📁 utils/                     # Utilities
│       ├── __init__.py
│       └── camera_helper.py          # (từ camera_helper.py)
│
├── 📁 scripts/                       # Scripts chạy
│   ├── run_main.sh                   # Chạy main
│   ├── run_streamlit.sh              # Chạy Streamlit
│   ├── run_full.bat                  # Windows - chạy cả 2
│   ├── run_full.sh                   # Linux/Mac - chạy cả 2
│   └── run_full.py                   # Python - chạy cả 2
│
├── 📁 config/                        # Cấu hình
│   ├── .streamlit/
│   │   └── config.toml               # Streamlit config
│   ├── settings.py                   # App settings
│   └── paths.py                      # Đường dẫn tuyệt đối
│
├── 📁 docs/                          # Tài liệu hướng dẫn
│   ├── 00_START_HERE.md
│   ├── QUICK_START.md
│   ├── SETUP_GUIDE.md
│   ├── CAMERA_SETUP.md
│   ├── PROJECT_STRUCTURE.md
│   ├── API_REFERENCE.md
│   └── TROUBLESHOOTING.md
│
├── 📁 tests/                         # Test & Debug
│   ├── test_main.py
│   ├── test_firebase.py
│   ├── test_camera.py
│   └── test_streamlit.py
│
├── 📁 data/                          # Dữ liệu (đã có)
│   ├── frames/
│   ├── smartIceTracker-1/
│   └── video/
│
├── 📁 model/                         # Model ML (đã có)
│   ├── best.pt                       # YOLOv8 trained
│   └── yolov8n.pt
│
├── 📁 runs/                          # Output từ training (đã có)
│   └── detect/
│
├── 📁 .streamlit/                    # Streamlit config
│   └── config.toml
│
├── 📁 venv/                          # Virtual environment
│
├── 📝 requirements.txt                # Dependencies
├── 📝 requirements-streamlit.txt      # Streamlit only
├── 🔑 firebase-key.json              # Firebase credentials
│
├── 📋 Project Files (Root)
│   ├── README.md                     # Main readme
│   ├── STRUCTURE.md                  # Cấu trúc thư mục này
│   ├── CHANGELOG.md                  # Lịch sử thay đổi
│   └── .gitignore                    # Git ignore
│
└── 📁 __pycache__/                   # Cache
```

---

## 🎯 Quy Tắc Phân Loại

### **src/core/** - Xử lý Camera & ML

- `camera_manager.py` - Điều phối 2 camera
- `license_plate.py` - YOLO + OCR biển số
- `bag_counter.py` - YOLO đếm bao
- `firebase_handler.py` - Kết nối Firebase

### **src/ui/** - Giao Diện

- `app_basic.py` - Version cơ bản
- `app_advanced.py` - Version nâng cao
- `app_camera.py` - Version camera-integrated

### **src/utils/** - Hỗ Trợ

- `camera_helper.py` - Queue, FPS, convert frame

### **scripts/** - Chạy

- Shell scripts (.sh)
- Batch scripts (.bat)
- Python scripts (.py)

### **config/** - Cấu Hình

- Streamlit config
- Settings app
- Đường dẫn tuyệt đối

### **docs/** - Tài Liệu

- Hướng dẫn chi tiết
- API reference
- Troubleshooting

### **tests/** - Debug

- Unit tests
- Integration tests

---

## 📋 File Cần Di Chuyển

```bash
# CORE
src/core/
├── camera_manager.py    ← main.py
├── license_plate.py     ← licensePlate.py
├── bag_counter.py       ← bagCount.py
└── firebase_handler.py  ← database.py

# UI
src/ui/
├── app_basic.py         ← streamlit_app.py
├── app_advanced.py      ← streamlit_app_advanced.py
└── app_camera.py        ← streamlit_app_camera.py

# UTILS
src/utils/
└── camera_helper.py     ← camera_helper.py

# SCRIPTS
scripts/
├── run_full.bat         ← run_full_app.bat
├── run_full.py          ← run_full_app.py
└── run_full.sh          ← NEW for Linux/Mac

# CONFIG
config/
├── config.toml          ← .streamlit/config.toml
├── settings.py          ← NEW
└── paths.py             ← NEW

# DOCS
docs/
├── *.md                 ← tất cả README*.md, SETUP.md, etc.

# TESTS
tests/
├── test_main.py
├── test_streamlit_setup.py
└── test_camera.py (new)
```

---

## 🚀 Lợi Ích

✅ **Dễ Tìm File:** Mỗi phần có thư mục riêng  
✅ **Dễ Debug:** Tách biệt core, UI, utils  
✅ **Dễ Mở Rộng:** Thêm tính năng không ảnh hưởng khác  
✅ **Dễ Bảo Trì:** Import rõ ràng, modular  
✅ **Dễ Test:** Tests tách riêng  
✅ **Dễ Deploy:** Config tập trung

---

## 📝 Cách Import Sau Khi Reorganize

### Trước:

```python
from licensePlate import run_license_plate
from bagCount import run_bag_counter
from database import save_license_plate_and_bag
```

### Sau:

```python
from src.core.license_plate import run_license_plate
from src.core.bag_counter import run_bag_counter
from src.core.firebase_handler import save_license_plate_and_bag
```

### Hoặc (Nếu Thêm **init**.py):

```python
from src.core import run_license_plate, run_bag_counter
```

---

## ⚙️ Steps Reorganize

1. ✅ Tạo cấu trúc thư mục
2. ⏳ Move file vào thư mục đúng
3. ⏳ Update imports trong code
4. ⏳ Tạo **init**.py cho mỗi thư mục
5. ⏳ Test chạy lại

---

**Tiếp tục bước nào?** → Move files hoặc update imports?
