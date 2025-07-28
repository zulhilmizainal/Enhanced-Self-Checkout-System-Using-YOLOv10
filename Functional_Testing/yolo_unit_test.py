from ultralytics import YOLO
import os

# Load your trained YOLOv10 model
model = YOLO("best.pt")

# Path to your test image folder
base_dir = os.path.dirname(__file__)
test_folder = os.path.join(base_dir, "test_images")
output_folder = os.path.join(base_dir, "test_results")

# Make test_results folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Loop through test images
for filename in os.listdir(test_folder):
    if filename.lower().endswith((".jpg", ".jpeg", ".png")):
        image_path = os.path.join(test_folder, filename)
        print(f"\n--- Testing {filename} ---")

        # Run detection
        results = model(image_path)

        # Save result with bounding boxes to test_results/
        results[0].save(filename=os.path.join(output_folder, filename))

        # Print class + confidence
        for box in results[0].boxes:
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])
            label = model.names[cls_id]
            print(f"Detected: {label} ({conf:.2f})")
