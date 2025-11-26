"""
License Plate Detection Module
YOLO-based detection + EasyOCR recognition
"""

import os
import sys
import logging
import warnings

# Suppress warnings and logging BEFORE imports
warnings.filterwarnings('ignore')
logging.basicConfig(level=logging.ERROR)
logging.getLogger().setLevel(logging.ERROR)

for logger_name in ['ultralytics', 'easyocr', 'torch', 'google', 'urllib3']:
    logging.getLogger(logger_name).setLevel(logging.ERROR)
    logging.getLogger(logger_name).propagate = False

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

import cv2
import torch
from ultralytics import YOLO
import easyocr
import numpy as np
import time
from datetime import datetime

from src.core.firebase_handler import save_license_plate_and_bag

def setup_device():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}")
    return device

device = setup_device()

# Load YOLO model for license plate detection
print("Loading license plate model...")
model = YOLO("model/best.pt")

# Initialize EasyOCR (GPU if available)
print("Initializing OCR...")
reader = easyocr.Reader(['en'], gpu=torch.cuda.is_available(), verbose=False)

# ==============================
# License Plate Detection Function
# ==============================
def run_license_plate(video_path, frame_queue=None, stop_event=None):
    print(f"Opening license plate video: {video_path}")
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print(f"ERROR: Cannot open license plate video: {video_path}")
        return
    
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) * 0.7)
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) * 0.7)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    
    print(f"Video info: {width}x{height} @ {fps}fps")

    last_plate = None
    last_ocr_time = 0
    ocr_cooldown = 1.5
    frame_skip = 1
    frame_count = 0

    try:
        while cap.isOpened():
            if stop_event and stop_event.is_set():
                break

            ret, frame = cap.read()
            if not ret:
                break
            
            frame_count += 1
            if frame_count % frame_skip != 0:
                continue

            frame = cv2.resize(frame, (width, height))
            
            h, w = frame.shape[:2]
            if h > w:
                frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
            
            results = model.predict(frame, imgsz=640, conf=0.4, device=device, verbose=False)
            annotated_frame = results[0].plot()

            if results[0].boxes:
                for box in results[0].boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    conf = float(box.conf[0])
                    plate_crop = frame[y1:y2, x1:x2]
                    if plate_crop.size == 0:
                        continue

                    current_time = time.time()
                    plate_text = "Unknown"

                    if current_time - last_ocr_time > ocr_cooldown:
                        text_results = reader.readtext(plate_crop)
                        if text_results:
                            plate_text = max(text_results, key=lambda x: x[2])[1]
                            last_ocr_time = current_time

                    cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(annotated_frame, plate_text, (x1, max(y1 - 10, 20)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)

                    if plate_text != "Unknown" and plate_text != last_plate:
                        last_plate = plate_text
                        print(f"License plate detected: {plate_text}")

                        try:
                            save_license_plate_and_bag(plate_text=plate_text, bag_count=None)
                        except Exception as e:
                            logging.debug(f"Firebase save error: {e}")

            if frame_queue is not None:
                try:
                    frame_queue.put(annotated_frame, block=False)
                except:
                    pass

    except Exception as e:
        print(f"ERROR: License plate detection failed: {e}")
    finally:
        cap.release()
        print("License plate video released")
