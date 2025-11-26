"""
Path utilities for Smart Ice Tracker
"""

from pathlib import Path
import sys

# Lấy base directory
BASE_DIR = Path(__file__).parent.parent.parent

def get_src_path():
    """Lấy đường dẫn src"""
    return BASE_DIR / "src"

def add_src_to_path():
    """Thêm src vào sys.path để import từ src"""
    src_path = str(get_src_path())
    if src_path not in sys.path:
        sys.path.insert(0, src_path)
    print(f"✅ Added to sys.path: {src_path}")

def get_project_root():
    """Lấy root directory của project"""
    return BASE_DIR

# Auto-add src to path khi import
add_src_to_path()

__all__ = [
    'BASE_DIR',
    'get_src_path',
    'get_project_root',
    'add_src_to_path',
]
