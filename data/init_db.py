from api.utils.logging import setup_logging
logger = setup_logging()

```python
import sqlite3
import os
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def init_db():
    """Initialize the SQLite database for CÆSER."""
    db_path = os.path.join(os.path.dirname(__file__), "caeser.db")
    
    try:
        # Create database file if it doesn't exist
        if not os.path.exists(db_path):
            open(db_path, 'a').close()
            logger.info(f"Created database file at {db_path}")
        
        # Connect to database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Create cultural_insights table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cultural_insights (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                location TEXT NOT NULL,
                category TEXT NOT NULL,
                data TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create index
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_insights ON cultural_insights(location, category)
        """)
        
        conn.commit()
        logger.info("Database initialized successfully")
    except sqlite3.Error as e:
        logger.error(f"Failed to initialize database: {str(e)}")
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    init_db()
```
