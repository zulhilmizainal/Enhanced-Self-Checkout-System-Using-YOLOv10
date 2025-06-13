# Enhanced Self-Checkout System Using Yolov10 (Main Entry Point)
import tkinter as tk
from ui.login import create_login_window
from utils.sales_db import create_table
create_table()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Self-Checkout System - Admin Login")
    root.geometry("300x220")

    # Centering function
    def center_window(window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        window.geometry(f"{width}x{height}+{x}+{y}")

    center_window(root, 300, 220)
    create_login_window(root)
    root.mainloop()
