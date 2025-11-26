"""
Test Script - Kiểm tra cài đặt Streamlit
Chạy: python test_streamlit_setup.py
"""

import sys
from datetime import datetime

print("=" * 60)
print("🧊 Smart Ice Tracker - Kiểm Tra Cài Đặt Streamlit")
print("=" * 60)
print(f"⏰ Thời gian: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
print(f"🐍 Python: {sys.version}")
print("=" * 60)
print()

# Test 1: Streamlit
print("1️⃣  Kiểm tra Streamlit...")
try:
    import streamlit as st
    print(f"   ✅ Streamlit {st.__version__} - OK")
except ImportError as e:
    print(f"   ❌ Lỗi: {e}")

# Test 2: Pandas
print("2️⃣  Kiểm tra Pandas...")
try:
    import pandas as pd
    print(f"   ✅ Pandas {pd.__version__} - OK")
except ImportError as e:
    print(f"   ❌ Lỗi: {e}")

# Test 3: NumPy
print("3️⃣  Kiểm tra NumPy...")
try:
    import numpy as np
    print(f"   ✅ NumPy {np.__version__} - OK")
except ImportError as e:
    print(f"   ❌ Lỗi: {e}")

# Test 4: Firebase
print("4️⃣  Kiểm tra Firebase...")
try:
    import firebase_admin
    print(f"   ✅ Firebase Admin SDK - OK")
except ImportError as e:
    print(f"   ❌ Lỗi: {e}")

# Test 5: OpenCV
print("5️⃣  Kiểm tra OpenCV...")
try:
    import cv2
    print(f"   ✅ OpenCV {cv2.__version__} - OK")
except ImportError as e:
    print(f"   ❌ Lỗi: {e}")

# Test 6: PyTorch
print("6️⃣  Kiểm tra PyTorch...")
try:
    import torch
    print(f"   ✅ PyTorch {torch.__version__} - OK")
    if torch.cuda.is_available():
        print(f"   🎮 GPU: {torch.cuda.get_device_name(0)}")
    else:
        print(f"   ⚠️  GPU không khả dụng (dùng CPU)")
except ImportError as e:
    print(f"   ❌ Lỗi: {e}")

# Test 7: Firebase Key
print("7️⃣  Kiểm tra Firebase Key...")
from pathlib import Path
if Path("firebase-key.json").exists():
    print("   ✅ firebase-key.json tồn tại")
else:
    print("   ❌ firebase-key.json KHÔNG tồn tại")

# Test 8: Streamlit Config
print("8️⃣  Kiểm tra Streamlit Config...")
config_path = Path(".streamlit/config.toml")
if config_path.exists():
    print("   ✅ .streamlit/config.toml tồn tại")
else:
    print("   ❌ .streamlit/config.toml KHÔNG tồn tại")

# Test 9: App Files
print("9️⃣  Kiểm tra App Files...")
app_files = [
    "streamlit_app.py",
    "streamlit_app_advanced.py",
    "camera_helper.py"
]
for f in app_files:
    if Path(f).exists():
        print(f"   ✅ {f}")
    else:
        print(f"   ❌ {f} KHÔNG tồn tại")

# Test 10: Documentation
print("🔟 Kiểm tra Tài Liệu...")
docs = [
    "README_STREAMLIT.md",
    "QUICK_START.md",
    "CAMERA_INTEGRATION.md",
    "INSTALLATION_SUMMARY.md"
]
for d in docs:
    if Path(d).exists():
        print(f"   ✅ {d}")
    else:
        print(f"   ⚠️  {d} KHÔNG tồn tại")

print()
print("=" * 60)
print("✅ Kiểm tra hoàn tất!")
print("=" * 60)
print()
print("🚀 Để chạy ứng dụng:")
print("   streamlit run streamlit_app.py")
print("   hoặc")
print("   .\run_streamlit.bat")
print()
print("📖 Xem tài liệu: QUICK_START.md")
print("=" * 60)
