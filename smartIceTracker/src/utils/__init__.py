"""
Smart Ice Tracker - Utils Package
Module hỗ trợ (camera helpers, converters, etc.)
"""

__version__ = "1.0.0"
__author__ = "Smart Ice Tracker Team"

# Import utilities
try:
    from .camera_helper import CameraStreamManager, FPSCounter, frame_to_rgb
except ImportError as e:
    print(f"⚠️ Import error in src.utils: {e}")

__all__ = [
    'CameraStreamManager',
    'FPSCounter',
    'frame_to_rgb',
]
