from api.utils.logging import setup_logging
logger = setup_logging()
import sqlite3
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def init_db():
    db_path = os.path.join(os.path.dirname(__file__), "caeser.db")
    
    try:
        if not os.path.exists(db_path):
            open(db_path, 'a').close()
            logger.info(f"Created database file at {db_path}")
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cultural_insights (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                location TEXT NOT NULL,
                category TEXT NOT NULL,
                data TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_insights ON cultural_insights(location, category)
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS hype_scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                score REAL NOT NULL,
                category TEXT NOT NULL,
                location TEXT NOT NULL,
                sentiment REAL NOT NULL,
                product_name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS llm_data_quality (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                metric TEXT NOT NULL,
                value REAL NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS data_quality (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                metric TEXT NOT NULL,
                value REAL NOT NULL,
                source TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS marked_products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                product_name TEXT NOT NULL,
                category TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS social_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                likes INTEGER NOT NULL,
                source TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
        """)
        logger.info("Added social_data table to database schema")
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_hype_scores ON hype_scores(category, location, created_at)
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS feedback_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                product_name TEXT NOT NULL,
                category TEXT NOT NULL,
                feedback_text TEXT,
                sentiment_weight REAL DEFAULT 1.0,
                timestamp TEXT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS model_weights (
                key TEXT PRIMARY KEY,
                value REAL NOT NULL
            )
        """)

        # Seed weights
        cursor.execute("""
            INSERT OR IGNORE INTO model_weights(key, value) VALUES
                ('sentiment_weight', 1.0),
                ('popularity_weight', 1.0),
                ('trend_weight', 1.0);
        """)
        logger.info("Seeded default model weights")

        # New tables
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS behavioral_trends (
                id INTEGER PRIMARY KEY,
                category TEXT,
                avg_hype_7d REAL,
                date DATE
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS synthetic_personas (
                id INTEGER PRIMARY KEY,
                age INTEGER,
                income INTEGER
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS request_state (
                id INTEGER PRIMARY KEY,
                endpoint TEXT,
                payload TEXT,
                ts TEXT
            );
        """)
        logger.info("Created new tables: behavioral_trends, synthetic_personas, request_state")

        # 100 mock personas
        cursor.execute("""
            INSERT INTO synthetic_personas(age, income)
            WITH RECURSIVE cte(x) AS (
                SELECT 1 UNION ALL SELECT x+1 FROM cte LIMIT 100
            ) SELECT abs(random()%48)+18, abs(random()%80000)+20000 FROM cte;
        """)
        logger.info("Inserted 100 mock personas")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS logistics_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                retailer TEXT,
                shipment_count INTEGER,
                timestamp TEXT NOT NULL,
                source TEXT DEFAULT 'mock'
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS error_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                endpoint TEXT,
                error_msg TEXT,
                stack_trace TEXT,
                timestamp TEXT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS api_calls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                endpoint TEXT,
                duration_ms REAL,
                timestamp TEXT NOT NULL
            )
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