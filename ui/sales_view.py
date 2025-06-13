# ui/sales_view.py
import tkinter as tk
from utils.helpers import center_window

def view_sales_transactions(parent_window):
    from ui.dashboard import open_dashboard
    for window in parent_window.winfo_children():
        if isinstance(window, tk.Toplevel):
            window.destroy()

    sales_window = tk.Toplevel()
    sales_window.title("Sales Transactions")
    sales_window.geometry("700x900")
    center_window(sales_window, 700, 900)

    tk.Label(sales_window, text="Sales Transactions", font=("Helvetica", 14)).pack(pady=10)

    from utils.sales_db import get_all_sales
    from collections import defaultdict
    sales_by_date = defaultdict(list)
    for date, name, qty, price, amount in get_all_sales():
        sales_by_date[date].append({
            "name": name,
            "qty": qty,
            "price": price,
            "amount": amount
        })

    for date, items in sales_by_date.items():
        tk.Label(sales_window, text=f"Date: {date}", font=("Helvetica", 12)).pack(pady=5)
        tk.Label(sales_window, text="+----+-----------------+-----+-------+--------+", font=("Courier", 12)).pack(anchor="w", padx=10)
        tk.Label(sales_window, text="| No | Items           | Qty | Price | Amount |", font=("Courier", 12)).pack(anchor="w", padx=10)
        tk.Label(sales_window, text="+----+-----------------+-----+-------+--------+", font=("Courier", 12)).pack(anchor="w", padx=10)

        for idx, item in enumerate(items, start=1):  # 👈 here’s enumerate()
            tk.Label(
                sales_window,
                text=f"| {idx:2} | {item['name']:<15} | {item['qty']:3} | {item['price']:5.2f} | {item['amount']:6.2f} |",
                font=("Courier", 12)
            ).pack(anchor="w", padx=10)

        total_price = sum(item['amount'] for item in items)
        tk.Label(sales_window, text="+----+-----------------+-----+-------+--------+", font=("Courier", 12)).pack(anchor="w", padx=10)
        tk.Label(sales_window, text=f"|    | Total           |     |       | {total_price:6.2f} |", font=("Courier", 12, "bold")).pack(anchor="w", padx=10)
        tk.Label(sales_window, text="+----+-----------------+-----+-------+--------+", font=("Courier", 12)).pack(anchor="w", padx=10)

    tk.Button(sales_window, text="Done", width=12,
              command=lambda: [sales_window.destroy(), open_dashboard(parent_window)]).pack(pady=10)
