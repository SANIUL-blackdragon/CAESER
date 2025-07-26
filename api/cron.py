import asyncio, requests, sqlite3
from datetime import datetime, timedelta
import sys

async def health_check_loop():
    while True:
        # basic check
        try:
            r = requests.get("http://localhost:8000/health", timeout=5)
            ok = r.status_code == 200
        except:
            ok = False
        # log
        conn = sqlite3.connect("./data/caeser.db")
        conn.execute("INSERT INTO error_logs(endpoint, error_msg, timestamp) VALUES (?,?,?)",
                     ("/health", "DOWN" if not ok else "UP", datetime.utcnow().isoformat()))
        conn.commit()

        # Discord suggestion on prediction drift
        cur = conn.execute("SELECT COUNT(*) FROM predictions WHERE predicted_uplift > 90")
        if cur.fetchone()[0] > 5:
            requests.post("https://discord.com/api/webhooks/...", json={
                "content": "🤖 Consider adding Google Trends to reduce high-score drift."
            })
        conn.close()
        await asyncio.sleep(300)  # 5 min

# Add this to run the health check loop when executed as a module
if __name__ == "__main__":
    print("Starting health monitoring service...")
    print("Press Ctrl+C to stop")
    try:
        asyncio.run(health_check_loop())
    except KeyboardInterrupt:
        print("\nHealth monitoring stopped")
        sys.exit(0)