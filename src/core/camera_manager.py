"""
Smart Ice Tracker - Main Controller
Run 2 cameras in parallel: License Plate Detection + Bag Counter
"""

import os
import sys
import logging
import warnings

# Suppress ALL warnings and logging BEFORE any imports
warnings.filterwarnings('ignore')
logging.basicConfig(level=logging.ERROR)
logging.getLogger().setLevel(logging.ERROR)

for logger_name in ['streamlit', 'firebase_admin', 'google', 'urllib3', 'asyncio', 'werkzeug']:
    logging.getLogger(logger_name).setLevel(logging.ERROR)
    logging.getLogger(logger_name).propagate = False

print("=" * 60)
print("STARTING SMART ICE TRACKER")
print("=" * 60)

import threading
import time
import cv2
import queue
import signal

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

print("OK: Basic libraries imported")

from src.core.license_plate import run_license_plate
from src.core.bag_counter import run_bag_counter

print("OK: Modules imported")

# --- Event to control thread shutdown ---
stop_event = threading.Event()

# --- Create 2 queues shared between threads ---
bag_queue = queue.Queue(maxsize=2)
plate_queue = queue.Queue(maxsize=2)

# --- Function to display video frames ---
def display_thread():
    print("Starting 2-stream display thread...")
    
    # Keep last frame to avoid black screen
    last_bag_frame = None
    last_plate_frame = None

    while not stop_event.is_set():
        bag_frame = None
        plate_frame = None

        try:
            if not bag_queue.empty():
                bag_frame = bag_queue.get(timeout=0.1)
                last_bag_frame = bag_frame

            if not plate_queue.empty():
                plate_frame = plate_queue.get(timeout=0.1)
                last_plate_frame = plate_frame
        except queue.Empty:
            pass

        # Use last frame if no new frame available
        if bag_frame is None and last_bag_frame is not None:
            bag_frame = last_bag_frame
        if plate_frame is None and last_plate_frame is not None:
            plate_frame = last_plate_frame

        # ONLY display when BOTH FRAMES are available
        if bag_frame is not None and plate_frame is not None:
            # Get original dimensions
            h_bag, w_bag = bag_frame.shape[:2]
            h_plate, w_plate = plate_frame.shape[:2]
            
            # Set fixed height for both cameras (horizontal merge)
            target_height = 480  # Fixed height
            
            # Resize both frames to same height, keep aspect ratio
            bag_frame_resized = cv2.resize(bag_frame, (int(w_bag * target_height / h_bag), target_height))
            plate_frame_resized = cv2.resize(plate_frame, (int(w_plate * target_height / h_plate), target_height))

            # Merge horizontally (left/right)
            combined = cv2.hconcat([plate_frame_resized, bag_frame_resized])
            cv2.imshow("Smart Ice Tracker (License + Bag)", combined)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            print("Pressed 'q' - Stopping display")
            stop_event.set()
            break

    cv2.destroyAllWindows()
    print("OK: Display window closed")


# --- License Plate detection thread ---
def start_license_plate_thread():
    print("Starting license plate detection thread...")
    try:
        run_license_plate(
            "data/video/LicensePlate/CaiSon_DocBangSo.mp4", 
            frame_queue=plate_queue,
            stop_event=stop_event
        )
    except Exception as e:
        print(f"ERROR: License plate thread failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("OK: License plate detection thread ended")

# --- Bag counter thread ---
def start_bag_counter_thread():
    print("Starting bag counter thread...")
    try:
        run_bag_counter(
            "data/video/Day/nuoc_da_bao1_ngay.mp4", 
            frame_queue=bag_queue,
            stop_event=stop_event
        )
    except Exception as e:
        print(f"ERROR: Bag counter thread failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("OK: Bag counter thread ended")


def signal_handler(sig, frame):
    """Handle Ctrl+C signal"""
    print("\nStop signal received (Ctrl+C)...")
    stop_event.set()


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("SYSTEM SETUP")
    print("=" * 60)
    
    # Register Ctrl+C signal handler
    signal.signal(signal.SIGINT, signal_handler)
    print("OK: Signal handler registered")
    
    # Create 3 threads with daemon=True
    t1 = threading.Thread(target=start_license_plate_thread, daemon=True, name="LicensePlate")
    t2 = threading.Thread(target=start_bag_counter_thread, daemon=True, name="BagCounter")
    t_display = threading.Thread(target=display_thread, daemon=True, name="Display")
    
    print("OK: 3 threads created")

    print("\n" + "=" * 60)
    print("STARTING SYSTEM")
    print("=" * 60)
    
    t1.start()
    print("OK: License Plate thread started")
    
    t2.start()
    print("OK: Bag Counter thread started")
    
    t_display.start()
    print("OK: Display thread started")

    print("\nSystem startup successful!")
    print("Press Ctrl+C or 'q' in video window to stop.\n")

    try:
        # Wait until stop_event is triggered
        while not stop_event.is_set():
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nReceived KeyboardInterrupt...")
        stop_event.set()
    finally:
        print("\n" + "=" * 60)
        print("STOPPING SYSTEM")
        print("=" * 60)
        
        # Wait max 5 seconds for threads to finish
        print("Waiting for License Plate thread...")
        t1.join(timeout=5)
        
        print("Waiting for Bag Counter thread...")
        t2.join(timeout=5)
        
        print("Waiting for Display thread...")
        t_display.join(timeout=5)
        
        # Ensure all OpenCV windows are closed
        cv2.destroyAllWindows()
        
        print("\n" + "=" * 60)
        print("OK: SYSTEM FULLY STOPPED")
        print("=" * 60)
        sys.exit(0)
