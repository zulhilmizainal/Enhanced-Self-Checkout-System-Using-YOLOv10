# ui/dashboard.py
import tkinter as tk
from ui.scanner import start_scanner
from ui.product_upload import open_product_upload
from ui.sales_view import view_sales_transactions
from utils.helpers import center_window

def open_dashboard(root):
    for window in root.winfo_children():
        if isinstance(window, tk.Toplevel):
            window.destroy()

    dashboard = tk.Toplevel()
    dashboard.title("Dashboard - Self-Checkout System")
    dashboard.geometry("500x400")
    center_window(dashboard, 500, 400)

    tk.Label(dashboard, text="Welcome to the Dashboard", font=("Helvetica", 16)).pack(pady=20)

    tk.Button(dashboard, text="Manage YOLO Training", command=lambda: open_product_upload(dashboard)).pack(pady=10)
    tk.Button(dashboard, text="View Sales Transactions", command=lambda: view_sales_transactions(dashboard)).pack(pady=10)
    tk.Button(dashboard, text="Logout", command=lambda: [dashboard.destroy(), root.deiconify()]).pack(pady=10)
