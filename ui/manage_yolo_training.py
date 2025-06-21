# ui/manage_yolo_training.py
import tkinter as tk
from tkinter import messagebox
import os
import subprocess
from utils.helpers import center_window, resource_path
from tkinter import ttk
import threading
import platform
from utils.train_yolo import train_yolo_model


def open_product_upload(parent_window):
    for window in parent_window.winfo_children():
        if isinstance(window, tk.Toplevel):
            window.destroy()

    product_window = tk.Toplevel()
    product_window.title("Manage YOLO Training")
    product_window.geometry("600x500")
    center_window(product_window, 600, 500)

    tk.Label(product_window, text="Manage Product Training Files", font=("Helvetica", 16, "bold")).pack(pady=(30, 20))

    button_frame = tk.Frame(product_window)
    button_frame.pack(pady=10)

    # Open folders
    tk.Button(button_frame, text="\U0001F4C1 Open Training Folder", width=35,
              command=lambda: open_folder(os.path.join("runs", "datasets"))).pack(pady=5)

    # Train button
    tk.Button(button_frame, text="\U0001F9E0 Train YOLOv10", width=35, bg="#007acc", fg="white", font=("Helvetica", 10, "bold"),
              command=lambda: trigger_training()).pack(pady=15)

    # Hidden initially
    status_label = tk.Label(product_window, text="", font=("Helvetica", 11))
    progress = ttk.Progressbar(product_window, mode='indeterminate')
    log_text = tk.Text(product_window, height=10, width=70, font=("Courier New", 9))
    log_text.pack(padx=15, pady=(5, 10), fill=tk.BOTH, expand=True)
    log_text.insert(tk.END, "Initializing...\n")
    log_text.config(state=tk.DISABLED)

    product_window.status_label = status_label
    product_window.progress = progress

    def trigger_training():
        status_label.pack(pady=5)
        progress.pack(pady=(0, 5))
        product_window.status_label.config(text="Training model... please wait.")
        product_window.progress.start(10)

        def ui_callback(msg):
            log_text.config(state=tk.NORMAL)
            log_text.insert(tk.END, msg + "\n")
            log_text.see(tk.END)
            log_text.config(state=tk.DISABLED)

        def run_training():
            log_text.config(state=tk.NORMAL)
            log_text.delete(1.0, tk.END)
            log_text.config(state=tk.DISABLED)
            try:
                train_yolo_model(callback=ui_callback)
                product_window.status_label.config(text="\u2705 Training completed successfully!")
                messagebox.showinfo("Success", "Model training completed!")
            except Exception as e:
                ui_callback(f"Error: {e}")
                product_window.status_label.config(text="\u274C Training failed.")
                messagebox.showerror("Error", "An error occurred during training.")
            finally:
                product_window.progress.stop()

        threading.Thread(target=run_training).start()

    # Bottom padding
    tk.Label(product_window, text="").pack()


def open_folder(path):
    abs_path = resource_path(path)
    os.makedirs(abs_path, exist_ok=True)
    if platform.system() == "Windows":
        os.startfile(abs_path)
    elif platform.system() == "Darwin":
        subprocess.run(["open", abs_path])
    else:
        subprocess.run(["xdg-open", abs_path])
