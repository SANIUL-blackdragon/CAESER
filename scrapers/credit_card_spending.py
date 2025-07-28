# In scrapers/credit_card_spending.py
import pandas as pd
import sqlite3
import os
from datetime import datetime
import requests

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

def fetch_credit_card_data():
    # Example: Fetch data from a hypothetical credit card API
    url = "https://api.creditcard.com/v1/transactions"
    headers = {"Authorization": f"Bearer {os.getenv('CREDIT_CARD_API_KEY')}"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Failed to fetch credit card data: {str(e)}")
        return []

def store_spending_data():
    data = fetch_credit_card_data()
    if not data:
        return
    df = pd.DataFrame(data)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO spending_data (category, spend_total, timestamp)
            VALUES (?, ?, ?)
        """, (row['category'], row['spend_total'], datetime.now().isoformat()))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_spending_table()
    store_spending_data()