"""
Bag Counter Module
YOLO tracking + ROI-based counting
"""

import os
import sys
import logging
import warnings

# Suppress warnings and logging BEFORE imports
warnings.filterwarnings('ignore')
logging.basicConfig(level=logging.ERROR)
logging.getLogger().setLevel(logging.ERROR)

for logger_name in ['ultralytics', 'torch', 'google', 'urllib3']:
    logging.getLogger(logger_name).setLevel(logging.ERROR)
    logging.getLogger(logger_name).propagate = False

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

import numpy as np
import cv2
from ultralytics import YOLO
import torch
import threading
import queue
from datetime import datetime

from src.core.firebase_handler import save_license_plate_and_bag

def setup_device():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Device: {device}")
    return device

device = setup_device()

# Load YOLO model
print("Loading bag counter model...")
model = YOLO('runs/detect/ice_tracker/weights/best.pt')

# ROI configuration
region_points = np.array([[494, 335], [451, 709], [590, 677], [630, 363]], np.int32)
region_points = region_points.reshape((-1, 1, 2))

# State variables
alpha = 0.8
local_bag_count = 0
counted_ids = set()
firebase_queue = queue.Queue()
firebase_worker_stop = threading.Event()

def firebase_worker():
    while not firebase_worker_stop.is_set():
        try:
            bag_val = firebase_queue.get(timeout=0.5)
            try:
                save_license_plate_and_bag(plate_text=None, bag_count=bag_val)
            except Exception as e:
                logging.debug(f"Firebase bag update error: {e}")
            firebase_queue.task_done()
        except queue.Empty:
            continue

firebase_thread = threading.Thread(target=firebase_worker, daemon=True)
firebase_thread.start()

# ===========================
# Bag Counter Main Function
# ===========================
def run_bag_counter(video_path, frame_queue=None, stop_event=None):
    global local_bag_count
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"ERROR: Cannot open video: {video_path}")
        return

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    print("Starting bag counter...")

    try:
        while cap.isOpened():
            if stop_event and stop_event.is_set():
                break

            ret, frame = cap.read()
            if not ret:
                break

            results = model.track(
                frame,
                imgsz=640,
                conf=0.25,
                iou=0.5,
                device=device,
                half=True,
                verbose=False,
                persist=True
            )
            
            annotated_frame = results[0].plot()
            
            overlay = annotated_frame.copy()
            cv2.fillPoly(annotated_frame, [region_points], (128, 0, 128))
            cv2.addWeighted(overlay, alpha, annotated_frame, 1 - alpha, 0, annotated_frame)
            cv2.polylines(annotated_frame, [region_points], isClosed=True, color=(0, 0, 255), thickness=2)

            if results[0].boxes.id is not None:
                ids = results[0].boxes.id.cpu().numpy().astype(int)
                boxes = results[0].boxes.xyxy.cpu().numpy()
                
                for i, box in enumerate(boxes):
                    obj_id = ids[i]
                    x1, y1, x2, y2 = box
                    cx = int((x1 + x2) / 2)
                    cy = int((y1 + y2) / 2)
                    cv2.circle(annotated_frame, (cx, cy), 4, (0, 255, 0), -1)
                    
                    result = cv2.pointPolygonTest(region_points, (cx, cy), False)
                    if result >= 0:
                        if obj_id not in counted_ids:
                            counted_ids.add(obj_id)
                            local_bag_count += 1
                            print(f"Bags counted: {local_bag_count}")
                            firebase_queue.put(local_bag_count)

            cv2.putText(annotated_frame, f"Count: {local_bag_count}", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)

            if frame_queue is not None:
                try:
                    frame_queue.put(annotated_frame, block=False)
                except:
                    pass

    except Exception as e:
        print(f"ERROR: Bag counter failed: {e}")
    finally:
        firebase_worker_stop.set()
        cap.release()
        print("Bag counter video released")
