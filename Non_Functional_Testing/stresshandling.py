import os
import time
import cv2
from ultralytics import YOLO

# Load trained YOLOv10 model
model = YOLO("best.pt")

# Define folders
base_dir = os.path.dirname(__file__)
test_folder = os.path.join(base_dir, "stress_test_images")
output_folder = os.path.join(base_dir, "stress_test_results")
os.makedirs(output_folder, exist_ok=True)

# Loop through test images
for filename in os.listdir(test_folder):
    if filename.lower().endswith((".jpg", ".jpeg", ".png")):
        image_path = os.path.join(test_folder, filename)
        print(f"\n--- Stress Testing {filename} ---")

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
        if results[0].boxes:
            overlay_color = (0, 255, 255)  # Yellow
            y_offset = 0

            # Header (shown once)
            cv2.putText(img, "Stress Test Detection", (x, y), font, font_scale, overlay_color, thickness)
            y_offset = int(30 * scale_factor) + line_spacing

            for box in results[0].boxes:
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                label = model.names[cls_id]

                print(f"Detected: {label} ({conf:.2f})")

                result_text = f"{label} ({conf:.2f})"
                cv2.putText(img, result_text, (x, y + y_offset), font, font_scale, overlay_color, thickness)
                y_offset += int(30 * scale_factor) + line_spacing
        else:
            print("❌ No object detected")
            cv2.putText(img, "❌ No object detected", (x, y), font, font_scale, (0, 0, 255), thickness)

        print(f"Detection Time: {detection_time:.3f} seconds")
        print(f"Estimated FPS: {fps:.2f}")

        # Save final image (YOLO boxes + custom overlay)
        cv2.imwrite(output_path, img)


# import os
# import time
# import cv2
# from ultralytics import YOLO

# # Load trained YOLOv10 model
# model = YOLO("bruno.pt")

# # Define folders
# base_dir = os.path.dirname(__file__)
# test_folder = os.path.join(base_dir, "stress_test_images")
# output_folder = os.path.join(base_dir, "stress_test_results")
# os.makedirs(output_folder, exist_ok=True)

# # Loop through test images
# for filename in os.listdir(test_folder):
#     if filename.lower().endswith((".jpg", ".jpeg", ".png")):
#         image_path = os.path.join(test_folder, filename)
#         print(f"\n--- Stress Testing {filename} ---")

#         # Start timer
#         start_time = time.time()
#         results = model(image_path)
#         end_time = time.time()

#         detection_time = end_time - start_time
#         fps = 1.0 / detection_time if detection_time > 0 else 0

#         # Save YOLO-rendered image first (with bounding boxes)
#         output_path = os.path.join(output_folder, filename)
#         results[0].save(filename=output_path)

#         # Load the YOLO-rendered image for additional overlay
#         img = cv2.imread(output_path)
#         height, width = img.shape[:2]
#         scale_factor = height / 640
#         font = cv2.FONT_HERSHEY_SIMPLEX
#         font_scale = 0.8 * scale_factor
#         thickness = int(2 * scale_factor)
#         line_spacing = int(10 * scale_factor)
#         x, y = int(10 * scale_factor), int(30 * scale_factor)

#         # Process detections
#         if results[0].boxes:
#             y_offset = 0
#             for box in results[0].boxes:
#                 cls_id = int(box.cls[0])
#                 conf = float(box.conf[0])
#                 label = model.names[cls_id]

#                 print(f"Detected: {label} ({conf:.2f})")

#                 # Text overlay
#                 overlay_color = (0, 255, 255)  # Yellow

#                 # Show header once (only for the first detection)
#                 if y_offset == 0:
#                     cv2.putText(img, "Stress Test Detection", (x, y), font, font_scale, overlay_color, thickness)
#                     y_offset += int(40 * scale_factor)

#                 # Then print each detected object result underneath
#                 result_text = f"{label} ({conf:.2f})"
#                 cv2.putText(img, result_text, (x, y + y_offset), font, font_scale, overlay_color, thickness)
#                 y_offset += int(30 * scale_factor) + line_spacing

#                 y_offset += int(70 * scale_factor)  # vertical spacing between detections
#         else:
#             print("❌ No object detected")
#             cv2.putText(img, "❌ No object detected", (x, y), font, font_scale, (0, 0, 255), thickness)

#         print(f"Detection Time: {detection_time:.3f} seconds")
#         print(f"Estimated FPS: {fps:.2f}")

#         # Save final image (YOLO boxes + custom overlay)
#         cv2.imwrite(output_path, img)
