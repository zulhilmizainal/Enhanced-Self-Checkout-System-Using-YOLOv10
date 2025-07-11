import sqlite3
import os

from utils.helpers import resource_path

# Determine the absolute path to the bundled database so PyInstaller
# executables can locate it regardless of the current working directory.
# DB_NAME = resource_path("sales.db")
DB_NAME = resource_path(os.path.join("runs", "datasets", "sales.db"))


def connect_db():
    return sqlite3.connect(DB_NAME)

def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            name TEXT,
            qty INTEGER,
            price REAL,
            amount REAL
        )
    ''')
    conn.commit()
    conn.close()

def insert_sale(date, name, qty, price, amount):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO sales (date, name, qty, price, amount)
        VALUES (?, ?, ?, ?, ?)
    ''', (date, name, qty, price, amount))
    conn.commit()
    conn.close()

def get_all_sales():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT date, name, qty, price, amount FROM sales ORDER BY date DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows
