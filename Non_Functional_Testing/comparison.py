import os
import time
import cv2
from ultralytics import YOLO

# Load trained YOLOv10 model
model = YOLO("bruno.pt")

# Define folders
base_dir = os.path.dirname(__file__)
test_folder = os.path.join(base_dir, "test_images")
output_folder = os.path.join(base_dir, "test_results")
os.makedirs(output_folder, exist_ok=True)

# Expected labels for verification
expected_labels = {
    "test_airpods.jpg": "airpods",
    "test_vaseline.jpg": "vaseline",
    "test_eye_drop.jpg": "eye_drop"
}

# Loop through test images
for filename in os.listdir(test_folder):
    if filename.lower().endswith((".jpg", ".jpeg", ".png")):
        image_path = os.path.join(test_folder, filename)
        print(f"\n--- Testing {filename} ---")

        # Start timer
        start_time = time.time()
        results = model(image_path)
        end_time = time.time()

        detection_time = end_time - start_time
        fps = 1.0 / detection_time if detection_time > 0 else 0

        # Save YOLO-rendered image first (with bounding boxes)
        output_path = os.path.join(output_folder, filename)
        results[0].save(filename=output_path)

        # Load the YOLO-rendered image for additional overlay
        img = cv2.imread(output_path)
        height, width = img.shape[:2]
        scale_factor = height / 640
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.8 * scale_factor
        thickness = int(2 * scale_factor)
        line_spacing = int(10 * scale_factor)
        x, y = int(10 * scale_factor), int(30 * scale_factor)

        # Process detections
        detected = False
        for box in results[0].boxes:
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])
            label = model.names[cls_id]
            detected = True

            print(f"Detected: {label} ({conf:.2f})")

            if filename in expected_labels:
                expected = expected_labels[filename]
                correct = (label == expected)
                result = "✅ Correct" if correct else "❌ Wrong"
                print(f"Expected: {expected} → {result}")

                # Text overlay logic
                label_text = "Correct Prediction" if correct else "Wrong Prediction"
                result_text = f"{label} ({conf:.2f})"
                overlay_color = (0, 255, 0) if correct else (0, 0, 255)

                cv2.putText(img, label_text, (x, y), font, font_scale, overlay_color, thickness)
                cv2.putText(img, result_text, (x, y + int(30 * scale_factor) + line_spacing), font, font_scale, overlay_color, thickness)

        if not detected:
            print("❌ No object detected")
            overlay_color = (0, 0, 255)
            cv2.putText(img, "❌ No object detected", (x, y), font, font_scale, overlay_color, thickness)

        print(f"Detection Time: {detection_time:.3f} seconds")
        print(f"Estimated FPS: {fps:.2f}")

        # Save final image (YOLO boxes + custom overlay)
        cv2.imwrite(output_path, img)


