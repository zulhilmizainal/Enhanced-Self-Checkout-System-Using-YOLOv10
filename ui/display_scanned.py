# ui/display_scanned.py
import tkinter as tk
from ui.virtual_keyboard import open_virtual_keyboard
from utils.helpers import center_window
from utils.cart import get_cart
from utils.scanner_state import scanner_context

def display_scanned_items(parent):
    sales_data = get_cart()

    scanned_window = tk.Toplevel(parent)
    scanned_window.title("Scanned Items")
    scanned_window.geometry("700x900")

    tk.Label(scanned_window, text="Scanned Items", font=("Helvetica", 14)).pack(pady=10)
    tk.Label(scanned_window, text="Date: 2024-10-01", font=("Helvetica", 12)).pack(pady=5)

    tk.Label(scanned_window, text="+----+-----------------+-----+-------+--------+------+", font=("Courier", 12)).pack(anchor="w", padx=10)
    tk.Label(scanned_window, text="| No | Items           | Qty | Price | Amount | Edit |", font=("Courier", 12)).pack(anchor="w", padx=10)
    tk.Label(scanned_window, text="+----+-----------------+-----+-------+--------+------+", font=("Courier", 12)).pack(anchor="w", padx=10)

    item_container = tk.Frame(scanned_window)
    item_container.pack(anchor="w")

    separator_line1 = tk.Label(scanned_window, text="+----+-----------------+-----+-------+--------+------+", font=("Courier", 12))
    total_price_label = tk.Label(scanned_window, font=("Courier", 12, "bold"))
    separator_line2 = tk.Label(scanned_window, text="+----+-----------------+-----+-------+--------+------+", font=("Courier", 12))
    separator_line1.pack(anchor="w", padx=10)
    total_price_label.pack(anchor="w", padx=10)
    separator_line2.pack(anchor="w", padx=10)

    def refresh_scanned_items():
        nonlocal sales_data, total_price_label
        for widget in item_container.winfo_children():
            widget.destroy()

        for item in sales_data:
            row_frame = tk.Frame(item_container)
            row_frame.pack(anchor="w", padx=10)

            row_label = tk.Label(row_frame, text=f"| {item['no']:2} | {item['name']:<15} | {item['qty']:3} | {item['price']:5.2f} | {item['amount']:6.2f} |", font=("Courier", 12))
            row_label.pack(side="left")

            edit_button = tk.Button(row_frame, text="✏", command=lambda item=item: open_edit_item_window(item), width=3, height=1)
            edit_button.pack(side="left", padx=11)

            closing_bar = tk.Label(row_frame, text="|", font=("Courier", 12))
            closing_bar.pack(side="left")

        total = sum(item["amount"] for item in sales_data)
        total_price_label.config(text=f"|    | Total           |     |       | {total:6.2f} |      |")


    def open_edit_item_window(item):
        nonlocal sales_data

        def update_quantity(action):
            if action == "add":
                item["qty"] += 1
            elif action == "subtract" and item["qty"] > 0:
                item["qty"] -= 1
            item["amount"] = item["qty"] * item["price"]
            qty_label.config(text=f" {item['qty']} ")
            amount_label.config(text=f"Total: {item['amount']:.2f}")
            refresh_scanned_items()

        def remove_all():
            sales_data.remove(item)
            edit_window.destroy()
            refresh_scanned_items()

        edit_window = tk.Toplevel(scanned_window)
        edit_window.title(f"Edit {item['name']}")
        edit_window.geometry("300x200")
        center_window(edit_window, 300, 200)

        tk.Label(edit_window, text=item["name"], font=("Helvetica", 14)).pack(pady=10)
        qty_frame = tk.Frame(edit_window)
        qty_frame.pack(pady=10)

        tk.Button(qty_frame, text="-", command=lambda: update_quantity("subtract")).grid(row=0, column=0, padx=5)
        qty_label = tk.Label(qty_frame, text=f" {item['qty']} ", font=("Helvetica", 14))
        qty_label.grid(row=0, column=1, padx=5)
        tk.Button(qty_frame, text="+", command=lambda: update_quantity("add")).grid(row=0, column=2, padx=5)

        amount_label = tk.Label(edit_window, text=f"Total: {item['amount']:.2f}", font=("Helvetica", 12))
        amount_label.pack(pady=5)
        tk.Button(edit_window, text="Remove All", command=remove_all, bg="red", fg="white").pack(pady=5)

    def proceed_to_payment():
        # Stop scanner first
        if scanner_context["cap"]:
            scanner_context["cap"].release()
            scanner_context["cap"] = None

        if scanner_context["window"]:
            scanner_context["window"].destroy()
            scanner_context["window"] = None

        open_virtual_keyboard(sum(item["amount"] for item in sales_data), scanned_window, parent)

    refresh_scanned_items()

    tk.Button(scanned_window, text="Proceed to Payment", width=20,
          command=proceed_to_payment).pack(pady=10)
