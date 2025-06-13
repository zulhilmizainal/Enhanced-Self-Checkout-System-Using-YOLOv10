# ui/login.py
import tkinter as tk
from tkinter import messagebox
from ui.dashboard import open_dashboard
from ui.scanner import start_scanner
from tkinter import messagebox
import tkinter as tk
from ui.dashboard import open_dashboard

def create_login_window(root):
    def admin_login():
        username = username_entry.get()
        password = password_entry.get()
        if username == "admin" and password == "admin":
            root.withdraw()
            open_dashboard(root)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def start_scanner_and_close():
        root.withdraw()
        start_scanner(root)

    tk.Label(root, text="Username:").pack(pady=5)
    username_entry = tk.Entry(root)
    username_entry.pack(pady=5)

    tk.Label(root, text="Password:").pack(pady=5)
    password_entry = tk.Entry(root, show="*")
    password_entry.pack(pady=5)

    username_entry.bind("<Return>", lambda event: password_entry.focus())
    password_entry.bind("<Return>", lambda event: admin_login())

    tk.Button(root, text="Login", command=admin_login).pack(pady=10)
    tk.Button(root, text="Start Scanner", command=start_scanner_and_close).pack(pady=10)

