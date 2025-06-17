# # train_model.py
import sys
import os

# ✅ Fix import path so `utils.helpers` can be found when run from dist/
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

from ultralytics import YOLO
from utils.helpers import resource_path

# ✅ Load pretrained YOLOv10 model
model = YOLO(os.path.join("runs", "datasets", "yolov10b.pt"))

# ✅ Start training
model.train(
    data=resource_path(os.path.join("runs", "datasets", "yolov10_custom.yaml")),  # dataset config
    epochs=2,         # adjust as needed
    imgsz=640,        # image size
    batch=8,          # lower for CPU
    patience=20       # early stopping
)

# ✅ Evaluate after training
model.val()
model.val(split='test')
