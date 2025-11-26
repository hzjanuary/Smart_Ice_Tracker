"""
Camera Stream Helper - Hỗ trợ hiển thị video stream trực tiếp trên Streamlit
"""

import cv2
import numpy as np
import threading
import queue
from datetime import datetime
import time


class CameraStreamManager:
    """Quản lý stream từ 2 camera"""
    
    def __init__(self, video_path1, video_path2):
        self.video_path1 = video_path1  # Bag counter
        self.video_path2 = video_path2  # License plate
        
        self.frame_queue1 = queue.Queue(maxsize=2)
        self.frame_queue2 = queue.Queue(maxsize=2)
        
        self.stop_event = threading.Event()
        self.current_plate = None
        self.current_bag_count = 0
        
    def start_camera_1(self):
        """Thread chạy camera 1 (Bag Counter)"""
        thread = threading.Thread(
            target=self._run_camera_1,
            daemon=True,
            name="Camera1-BagCounter"
        )
        thread.start()
        
    def start_camera_2(self):
        """Thread chạy camera 2 (License Plate)"""
        thread = threading.Thread(
            target=self._run_camera_2,
            daemon=True,
            name="Camera2-LicensePlate"
        )
        thread.start()
        
    def _run_camera_1(self):
        """Chạy video bag counter"""
        cap = cv2.VideoCapture(self.video_path1)
        
        if not cap.isOpened():
            print(f"❌ Không thể mở camera 1: {self.video_path1}")
            return
        
        print(f"✅ Camera 1 (Bag Counter) mở thành công")
        
        while not self.stop_event.is_set():
            ret, frame = cap.read()
            if not ret:
                # Video kết thúc, loop lại
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue
            
            # Resize frame để giảm kích thước
            frame = cv2.resize(frame, (640, 480))
            
            # Thêm timestamp lên frame
            timestamp = datetime.now().strftime("%H:%M:%S")
            cv2.putText(
                frame, 
                f"Bag Count: {self.current_bag_count} | {timestamp}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )
            
            # Thêm frame vào queue
            try:
                self.frame_queue1.put_nowait(frame)
            except queue.Full:
                pass
        
        cap.release()
        
    def _run_camera_2(self):
        """Chạy video license plate"""
        cap = cv2.VideoCapture(self.video_path2)
        
        if not cap.isOpened():
            print(f"❌ Không thể mở camera 2: {self.video_path2}")
            return
        
        print(f"✅ Camera 2 (License Plate) mở thành công")
        
        while not self.stop_event.is_set():
            ret, frame = cap.read()
            if not ret:
                # Video kết thúc, loop lại
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue
            
            # Resize frame để giảm kích thước
            frame = cv2.resize(frame, (640, 480))
            
            # Thêm thông tin biển số lên frame
            timestamp = datetime.now().strftime("%H:%M:%S")
            plate_text = self.current_plate if self.current_plate else "Chưa phát hiện"
            
            # Background box cho text
            cv2.rectangle(frame, (10, 10), (400, 60), (255, 255, 0), -1)
            cv2.putText(
                frame, 
                f"Plate: {plate_text}",
                (20, 45),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 0),
                2
            )
            cv2.putText(
                frame, 
                f"Time: {timestamp}",
                (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 0, 255),
                1
            )
            
            # Thêm frame vào queue
            try:
                self.frame_queue2.put_nowait(frame)
            except queue.Full:
                pass
        
        cap.release()
        
    def get_frame_1(self, timeout=0.1):
        """Lấy frame từ camera 1"""
        try:
            return self.frame_queue1.get(timeout=timeout)
        except queue.Empty:
            return None
        
    def get_frame_2(self, timeout=0.1):
        """Lấy frame từ camera 2"""
        try:
            return self.frame_queue2.get(timeout=timeout)
        except queue.Empty:
            return None
        
    def update_plate(self, plate):
        """Cập nhật biển số hiện tại"""
        self.current_plate = plate
        
    def update_bag_count(self, count):
        """Cập nhật số bao hiện tại"""
        self.current_bag_count = count
        
    def stop(self):
        """Dừng tất cả camera"""
        self.stop_event.set()
        print("⏹️ Dừng tất cả camera")


# ===== Hàm hỗ trợ chuyển đổi OpenCV frame sang RGB =====
def frame_to_rgb(frame):
    """Chuyển frame OpenCV (BGR) sang RGB cho Streamlit"""
    if frame is None:
        return None
    return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)


# ===== Hàm hỗ trợ vẽ bounding box =====
def draw_bbox(frame, x1, y1, x2, y2, label="Object", color=(0, 255, 0), thickness=2):
    """Vẽ bounding box lên frame"""
    cv2.rectangle(frame, (x1, y1), (x2, y2), color, thickness)
    cv2.putText(
        frame,
        label,
        (x1, y1 - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        color,
        2
    )
    return frame


# ===== Hàm hỗ trợ tính FPS =====
class FPSCounter:
    """Đếm FPS của video stream"""
    
    def __init__(self):
        self.prev_time = 0
        self.fps = 0
        
    def update(self):
        """Cập nhật FPS"""
        curr_time = time.time()
        if self.prev_time > 0:
            self.fps = 1 / (curr_time - self.prev_time)
        self.prev_time = curr_time
        return self.fps
    
    def get_fps(self):
        """Lấy FPS hiện tại"""
        return self.fps
    
    def draw_fps(self, frame):
        """Vẽ FPS lên frame"""
        cv2.putText(
            frame,
            f"FPS: {self.fps:.1f}",
            (10, frame.shape[0] - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )
        return frame
