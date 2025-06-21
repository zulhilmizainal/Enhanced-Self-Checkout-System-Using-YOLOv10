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
    """Resolve path to a resource bundled alongside the executable.

    When running from source, any path inside ``runs`` is redirected to the
    ``dist`` folder so that both ``.py`` and packaged ``.exe`` modes operate on
    the same files.
    """

    if getattr(sys, "frozen", False):
        # When running as a PyInstaller binary, place runtime files next to the exe
        base_path = os.path.dirname(sys.executable)
    else:
        # Running from source - project root is one level above this file
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

        # Redirect runs/ -> dist/runs/ when executing from source
        if os.path.normpath(relative_path).split(os.sep)[0] == "runs":
            base_path = os.path.join(base_path, "dist")

    return os.path.join(base_path, relative_path)
