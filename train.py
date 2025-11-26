from ultralytics import YOLO

model = YOLO("model/yolov8n.pt")

# Train với dataset từ Roboflow
results = model.train(
    data="data/smartIceTracker-1/data.yaml",
    epochs=50,        # số vòng lặp
    imgsz=640,        # kích thước ảnh
    batch=16,         # batch size
    name="ice_tracker"
)
