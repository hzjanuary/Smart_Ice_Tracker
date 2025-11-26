"""
Firebase Handler Module
Realtime Database operations for License Plates and Bag Counts
"""

import logging
import os
import sys

# Disable all verbose logging BEFORE importing firebase
logging.basicConfig(level=logging.ERROR)
logging.getLogger('firebase_admin').setLevel(logging.ERROR)
logging.getLogger('google.cloud').setLevel(logging.ERROR)
logging.getLogger('google.auth').setLevel(logging.ERROR)
logging.getLogger('streamlit').setLevel(logging.ERROR)
logging.getLogger('urllib3').setLevel(logging.ERROR)

# Suppress environment variable warnings
os.environ['PYTHONWARNINGS'] = 'ignore'

import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime

# --- Firebase setup ---
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase-key.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://smarticetracker-default-rtdb.asia-southeast1.firebasedatabase.app/'
    })

# --- Biến toàn cục để theo dõi biển số hiện tại ---
current_plate = None


def save_license_plate_and_bag(plate_text=None, bag_count=None):
    """
    Save data to Firebase:
    /license_plates/YYYY-MM-DD/plate:<license_plate>/
        - plate
        - bag
        - timestamp
    """
    global current_plate
    try:
        today = datetime.now().strftime("%Y-%m-%d")
        timestamp = datetime.now().strftime("%H:%M:%S")

        if not plate_text:
            return

        ref = db.reference(f"license_plates/{today}/plate:{plate_text}")

        if plate_text != current_plate:
            current_plate = plate_text
            ref.set({
                "plate": plate_text,
                "bag": 0,
                "timestamp": timestamp
            })
            return

        update_data = {"timestamp": timestamp}
        if bag_count is not None:
            update_data["bag"] = bag_count

        ref.update(update_data)

    except Exception as e:
        logging.debug(f"Firebase save error: {e}")


# --- Các hàm phụ ---
def update_total_count(new_count):
    """Update total bag count."""
    try:
        total_ref = db.reference("total_count")
        total_ref.set(new_count)
    except Exception as e:
        logging.debug(f"Total count update error: {e}")


def listen_total_count(callback):
    """Lắng nghe thay đổi của total_count từ Firebase."""
    ref = db.reference("total_count")

    def listener(event):
        if event.data is not None:
            callback(event.data)

    ref.listen(listener)
