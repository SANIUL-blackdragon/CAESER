from alembic import config, command
import sqlite3
import os
from datetime import datetime, timedelta
import logging

def init_db():
    # Alembic migrations
    alembic_cfg = config.Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")

    # Ensure dynamic insight_types table exists
    conn = sqlite3.connect(os.getenv("DB_PATH", "./data/caeser.db"))
    conn.execute("""
        CREATE TABLE IF NOT EXISTS insight_types (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type_name TEXT UNIQUE NOT NULL
        )
    """)
    # Seed default values only if table is empty
    defaults = ["brand", "demographics", "heatmap"]
    for t in defaults:
        conn.execute("INSERT OR IGNORE INTO insight_types(type_name) VALUES (?)", (t,))
    conn.commit()
    conn.close()
    
    alembic_cfg = config.Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")   # ← no "alembic." prefix

if __name__ == "__main__":
    init_db()