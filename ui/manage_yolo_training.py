# ui/manage_yolo_training.py
import tkinter as tk
from tkinter import messagebox
import os
import subprocess
from utils.helpers import center_window
from tkinter import ttk
import threading
import platform

def open_product_upload(parent_window):
    for window in parent_window.winfo_children():
        if isinstance(window, tk.Toplevel):
            window.destroy()

    product_window = tk.Toplevel()
    product_window.title("Manage YOLO Training")
    product_window.geometry("600x400")
    center_window(product_window, 600, 400)

    tk.Label(product_window, text="Manage Product Training Files", font=("Helvetica", 16, "bold")).pack(pady=(30, 20))

    button_frame = tk.Frame(product_window)
    button_frame.pack(pady=10)

    # Open folders
    tk.Button(button_frame, text="📁 Open Training Folder", width=35,
              command=lambda: open_folder(os.path.join("runs", "datasets"))).pack(pady=5)

    # Train button
    tk.Button(button_frame, text="🧠 Train YOLOv10", width=35, bg="#007acc", fg="white", font=("Helvetica", 10, "bold"),
              command=lambda: trigger_training()).pack(pady=15)

    # Hidden initially
    status_label = tk.Label(product_window, text="", font=("Helvetica", 11))
    progress = ttk.Progressbar(product_window, mode='indeterminate')
    
    # Attach to window
    product_window.status_label = status_label
    product_window.progress = progress

    def trigger_training():
        status_label.pack(pady=5)
        progress.pack(pady=(0, 5))
        product_window.status_label.config(text="Training model... please wait.")
        product_window.progress.start(10)  # animate every 10ms

        def run_training():
            try:
                subprocess.run(["python", "train_model.py"], check=True)
                product_window.progress.stop()
                product_window.status_label.config(text="✅ Training completed successfully!")
                messagebox.showinfo("Success", "Model training completed!")
            except subprocess.CalledProcessError:
                product_window.progress.stop()
                product_window.status_label.config(text="❌ Training failed.")
                messagebox.showerror("Error", "An error occurred during training.")

        threading.Thread(target=run_training).start()

    # Bottom padding
    tk.Label(product_window, text="").pack()

def open_folder(path):
    abs_path = os.path.abspath(path)
    os.makedirs(abs_path, exist_ok=True)  # 💡 Ensure folder exists
    if platform.system() == "Windows":
        os.startfile(abs_path)
    elif platform.system() == "Darwin":  # macOS
        subprocess.run(["open", abs_path])
    else:  # Linux
        subprocess.run(["xdg-open", abs_path])