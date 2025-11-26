"""
Smart Ice Tracker - UI Package
Module Streamlit applications
"""

__version__ = "1.0.0"
__author__ = "Smart Ice Tracker Team"

# Import chính UI apps
try:
    from .app_basic import main as run_app_basic
    from .app_advanced import main as run_app_advanced
    from .app_camera import main as run_app_camera
except ImportError as e:
    print(f"⚠️ Import error in src.ui: {e}")

__all__ = [
    'run_app_basic',
    'run_app_advanced',
    'run_app_camera',
]
