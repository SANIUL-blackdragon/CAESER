# In scrapers/credit_card_spending.py
import pandas as pd
import sqlite3
import os
from datetime import datetime

DB_PATH = os.getenv("DB_PATH", "../data/caeser.db")

def init_spending_table():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS spending_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,
            spend_total REAL,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

def store_spending_data():
    mock_data = pd.DataFrame({"category": ["sneakers"], "spend_total": [1000.0]})
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    for _, row in mock_data.iterrows():
        cursor.execute("""
            INSERT INTO spending_data (category, spend_total, timestamp)
            VALUES (?, ?, ?)
        """, (row['category'], row['spend_total'], datetime.now().isoformat()))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_spending_table()
    store_spending_data()