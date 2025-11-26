"""
Configuration Settings for Smart Ice Tracker
"""

import os
from pathlib import Path

# ==================== PATHS ====================
BASE_DIR = Path(__file__).parent.parent.parent  # smartIceTracker root
SRC_DIR = BASE_DIR / "src"
DATA_DIR = BASE_DIR / "data"
MODEL_DIR = BASE_DIR / "model"
CONFIG_DIR = BASE_DIR / "config"
DOCS_DIR = BASE_DIR / "docs"
TESTS_DIR = BASE_DIR / "tests"

# Video paths
VIDEO_LICENSE_PLATE = DATA_DIR / "video" / "LicensePlate" / "CaiSon_DocBangSo.mp4"
VIDEO_BAG_COUNTER = DATA_DIR / "video" / "Day" / "ice_tracker_video.mp4"

# Model paths
MODEL_YOLO_LICENSE = MODEL_DIR / "best.pt"
MODEL_YOLO_DETECTION = MODEL_DIR / "best.pt"

# Firebase
FIREBASE_KEY = BASE_DIR / "firebase-key.json"
FIREBASE_DB_URL = "https://smarticetracker-default-rtdb.asia-southeast1.firebasedatabase.app/"

# ==================== STREAMLIT ====================
STREAMLIT_PORT = 8501
STREAMLIT_THEME = "light"

# Cache settings
CACHE_TTL = 30  # seconds

# ==================== CAMERA ====================
CAMERA_1_RESIZE_RATIO = 0.7
CAMERA_2_RESIZE_RATIO = 0.7
DISPLAY_HEIGHT = 480
DISPLAY_WIDTH = 1280

# FPS target
TARGET_FPS = 30

# ==================== DATABASE ====================
MAX_RETRIES = 3
TIMEOUT = 10  # seconds

# ==================== DEBUG ====================
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
LOG_LEVEL = "INFO"

# ==================== VALIDATION ====================
def validate_paths():
    """Kiểm tra tất cả đường dẫn quan trọng tồn tại"""
    
    critical_paths = {
        "Firebase Key": FIREBASE_KEY,
        "Model YOLO": MODEL_YOLO_LICENSE,
    }
    
    warnings = []
    
    for name, path in critical_paths.items():
        if not path.exists():
            warnings.append(f"❌ {name} not found: {path}")
    
    if warnings:
        print("⚠️ Path validation warnings:")
        for w in warnings:
            print(f"   {w}")
    else:
        print("✅ All critical paths OK")
    
    return len(warnings) == 0

if __name__ == "__main__":
    print("=" * 60)
    print("🧊 Smart Ice Tracker - Configuration Check")
    print("=" * 60)
    print(f"Base Directory: {BASE_DIR}")
    print(f"Source Directory: {SRC_DIR}")
    print(f"Data Directory: {DATA_DIR}")
    print(f"Model Directory: {MODEL_DIR}")
    print(f"Firebase Key: {FIREBASE_KEY}")
    print(f"Streamlit Port: {STREAMLIT_PORT}")
    print(f"Debug Mode: {DEBUG}")
    print("=" * 60)
    validate_paths()
