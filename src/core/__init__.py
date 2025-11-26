"""
Smart Ice Tracker - Core Package
Module xử lý camera, YOLO, Firebase
"""

__version__ = "1.0.0"
__author__ = "Smart Ice Tracker Team"

# Import chính để dễ access
try:
    from .license_plate import run_license_plate
    from .bag_counter import run_bag_counter
    from .firebase_handler import save_license_plate_and_bag
    from .camera_manager import main as run_camera_main
except ImportError as e:
    print(f"⚠️ Import error in src.core: {e}")

__all__ = [
    'run_license_plate',
    'run_bag_counter',
    'save_license_plate_and_bag',
    'run_camera_main',
]
