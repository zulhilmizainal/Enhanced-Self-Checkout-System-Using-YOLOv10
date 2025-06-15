# utils/helpers.py
import os
import sys


def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")


def resource_path(relative_path: str) -> str:
    """Return absolute path to resource, compatible with PyInstaller."""
    # Resolve to the project root (one level above this file's directory)
    base_path = getattr(
        sys,
        "_MEIPASS",
        os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)),
    )
    return os.path.join(base_path, relative_path)
