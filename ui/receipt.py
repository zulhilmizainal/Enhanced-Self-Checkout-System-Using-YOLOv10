# ui/receipt.py
import tkinter as tk
from utils.scanner_state import scanner_context

def open_receipt_window(card_number, root=None):
    receipt_window = tk.Toplevel()
    receipt_window.title("Receipt")
    receipt_window.geometry("700x900")

    tk.Label(receipt_window, text="Receipt", font=("Helvetica", 14)).pack(pady=10)

    from utils.cart import get_cart
    sales_data = [{"date": "2024-10-01", "items": get_cart()}]

    for transaction in sales_data:
        tk.Label(receipt_window, text=f"Date: {transaction['date']}", font=("Helvetica", 12)).pack(pady=5)

        # Table header
        tk.Label(receipt_window, text="+----+-----------------+-----+-------+--------+", font=("Courier", 12)).pack(anchor="w", padx=10)
        tk.Label(receipt_window, text="| No | Items           | Qty | Price | Amount |", font=("Courier", 12)).pack(anchor="w", padx=10)
        tk.Label(receipt_window, text="+----+-----------------+-----+-------+--------+", font=("Courier", 12)).pack(anchor="w", padx=10)

        for item in transaction["items"]:
            tk.Label(
                receipt_window,
                text=f"| {item['no']:2} | {item['name']:<15} | {item['qty']:3} | {item['price']:5.2f} | {item['amount']:6.2f} |",
                font=("Courier", 12)
            ).pack(anchor="w", padx=10)

        total_price = sum(item['amount'] for item in transaction['items'])
        tk.Label(receipt_window, text="+----+-----------------+-----+-------+--------+", font=("Courier", 12)).pack(anchor="w", padx=10)
        tk.Label(receipt_window, text=f"|    | Total           |     |       | {total_price:6.2f} |", font=("Courier", 12, "bold")).pack(anchor="w", padx=10)
        tk.Label(receipt_window, text="+----+-----------------+-----+-------+--------+", font=("Courier", 12)).pack(anchor="w", padx=10)

        tk.Label(receipt_window, text=f"Paid in Full with Card Number: {card_number}", font=("Helvetica", 12, "bold"), fg="green").pack(pady=10)

    def close_receipt():
        receipt_window.destroy()
        
        if scanner_context.get("root"):
            scanner_context["root"].deiconify()

    tk.Button(receipt_window, text="Done", command=close_receipt, font=("Helvetica", 12)).pack(pady=10)
