from ultralytics import YOLO

# Load a pretrained YOLOv10 model
model = YOLO("yolov10b.pt")  

# Train the model
model.train(
    data="yolov10_custom.yaml",  # dataset config
    epochs=50,                   # can reduce/increase
    imgsz=640,                   # image size (default is 640)
    batch=8,                     # for CPU training, keep small
    patience = 20,               # early stopping patience
)

model.val()
model.val(split='test')

# from ultralytics import YOLO

# # Load a pretrained YOLOv10 model (smallest version to start with)
# model = YOLO("yolov10b.pt")  

# # Train the model
# model.train(
#     data="/content/My-First-Project-1/data.yaml",  # your dataset config
#     epochs=50,                   # you can reduce/increase later
#     imgsz=640,                   # image size (default is 640)
#     batch=16,                     # for CPU training, keep small
#     patience = 20,                # early stopping patience
# )

# model.val()
# model.val(split='test')