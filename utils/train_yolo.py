from ultralytics import YOLO
import os
from utils.helpers import resource_path


def train_yolo_model(callback=None):
    """Train YOLOv10 model and report progress via callback."""

    def log(message):
        if callback:
            callback(message)
        else:
            print(message)

    log("Starting training...")
    weights_path = resource_path(os.path.join("runs", "datasets", "yolov10b.pt"))
    data_path = resource_path(os.path.join("runs", "datasets", "yolov10_custom.yaml"))

    log("Loading model...")
    model = YOLO(weights_path)
    log("Model loaded. Beginning training...")

    model.train(
        data=data_path,
        epochs=2,
        imgsz=640,
        batch=8,
        patience=20
    )

    log("Training complete. Evaluating model...")
    model.val()
    model.val(split='test')
    log("Training and evaluation finished.")
