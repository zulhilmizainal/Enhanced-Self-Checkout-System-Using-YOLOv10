import tkinter as tk
from PIL import Image, ImageTk
import cv2
from ui.display_scanned import display_scanned_items
from utils.helpers import center_window, resource_path
from ultralytics import YOLO
import csv
from utils.cart import add_to_cart
from tkinter import messagebox
from utils.scanner_state import scanner_context
import os

# Only accept detections with confidence above this value
CONFIDENCE_THRESHOLD = 0.6

# Load YOLO model
model = YOLO(resource_path(os.path.join("runs", "datasets", "best.pt")))

# Load product prices from CSV
product_prices = {}
with open(resource_path(os.path.join("runs", "datasets", "ProductData.csv")), newline='', encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        name = row["product_name"].strip()
        product_prices[name] = float(row["price"])

def start_scanner(root):
    last_detected_label = ""
    current_frame_detections = set()

    # Save root (login window) in global context so we can bring it back later
    scanner_context["root"] = root

    # Close any existing Toplevel windows
    for window in root.winfo_children():
        if isinstance(window, tk.Toplevel):
            window.destroy()

    # Create scanner window WITHOUT making root the parent
    scanner_window = tk.Toplevel()
    scanner_context["window"] = scanner_window

    scanner_window.title("Scanner - Self-Checkout System")
    scanner_window.geometry("800x650")
    scanner_window.resizable(False, False)
    center_window(scanner_window, 800, 650)

    # Video display
    video_label = tk.Label(scanner_window)
    video_label.pack(pady=5)

    # Label for currently detected items
    detected_label = tk.Label(scanner_window, text="", font=("Helvetica", 12, "italic"))
    detected_label.pack(pady=5)

    tk.Label(scanner_window, text="Scanning items...", font=("Helvetica", 14)).pack(pady=5)

    # Buttons
    button_frame = tk.Frame(scanner_window)
    button_frame.pack(pady=10)

    def pay_and_show_items():
        cap.release()
        scanner_window.destroy()
        scanner_context["cap"] = None
        scanner_context["window"] = None
        display_scanned_items(root)

    tk.Button(button_frame, text="Pay", width=15,
              command=pay_and_show_items).grid(row=0, column=0, padx=10)

    def add_detected_item():
        nonlocal current_frame_detections
        if not current_frame_detections:
            messagebox.showinfo(
                "Info",
                "No high-confidence items detected. Please rescan."
            )
            return

        added_items = []
        for label in current_frame_detections:
            if label in product_prices:
                price = product_prices[label]
                add_to_cart(label, price)
                added_items.append(label)

        if added_items:
            messagebox.showinfo("Added", f"{', '.join(added_items)} added to cart.")
        else:
            messagebox.showwarning("Warning", "Detected items are not in product list.")

    tk.Button(button_frame, text="Add to Cart", width=15, command=add_detected_item).grid(row=0, column=1, padx=10)

    # Index 1 because using IVCam (iphone camera not webcam)
    cap = cv2.VideoCapture(0)
    scanner_context["cap"] = cap

    def update_frame():
        nonlocal last_detected_label, current_frame_detections
        ret, frame = cap.read()
        frame = cv2.resize(frame, (640, 480))

        if ret:
            results = model.predict(frame, imgsz=640, conf=0.25, verbose=False)

            current_frame_detections.clear()
            detected_summary = []

            for box in results[0].boxes:
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                if conf < CONFIDENCE_THRESHOLD:
                    continue
                label = results[0].names[cls_id]
                last_detected_label = label
                current_frame_detections.add(label)

                price = product_prices.get(label, "N/A")
                detected_summary.append(f"{label} - RM {price}")
                
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.putText(
                    frame,
                    f"{label} ({conf:.2f})",
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 255, 0),
                    2
                )

            detected_label.config(text=" | ".join(detected_summary) if detected_summary else "No item detected")

            annotated_frame = results[0].plot()
            rgb_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(rgb_frame)
            photo = ImageTk.PhotoImage(image=image)
            video_label.configure(image=photo)
            video_label.image = photo

        scanner_window.after(15, update_frame)

    update_frame()

    def on_close():
        cap.release()
        scanner_window.destroy()
        scanner_context["cap"] = None
        scanner_context["window"] = None
        root.deiconify()

    scanner_window.protocol("WM_DELETE_WINDOW", on_close)

