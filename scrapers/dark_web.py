# In scrapers/dark_web.py
import json
import sqlite3
import os
from datetime import datetime

DB_PATH = os.getenv("DB_PATH", "../data/caeser.db")

def store_dark_web_data():
    mock_data = [{"text": "Counterfeit sneakers trending", "likes": 50}]
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    for item in mock_data:
        cursor.execute("""
            INSERT INTO social_data (text, likes, source, timestamp)
            VALUES (?, ?, ?, ?)
        """, (item['text'], item['likes'], "dark_web", datetime.now().isoformat()))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    store_dark_web_data()