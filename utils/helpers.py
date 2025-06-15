# utils/helpers.py
import os
import sys


def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")


def resource_path(relative):
    base = getattr(sys, "_MEIPASS", os.path.abspath("."))
    return os.path.join(base, relative)
