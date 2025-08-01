import os
import boto3
import requests
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import logging
import asyncio
from typing import Optional
import asyncpg

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

POSTGRES_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/caeser")
pg_pool: Optional[asyncpg.Pool] = None

# ------------------------------------------------------------------
def _get_secret(secret_id: str) -> str:
    """
    Get secret from AWS Secrets Manager with fallback to environment variables.
    Initializes boto3 client on demand to avoid issues during import.
    """
    secret_value = ""
    try:
        # First, try environment variables (often used in CI/CD or local dev)
        env_var_name = secret_id.upper().replace("-", "_")
        secret_value = os.getenv(env_var_name, "")
        if secret_value:
            return secret_value

        # If not in env, try AWS Secrets Manager
        secrets_client = boto3.client('secretsmanager', region_name=os.getenv("AWS_REGION", "us-east-1"))
        secret_value = secrets_client.get_secret_value(SecretId=secret_id)['SecretString']
        return secret_value
    except Exception as e:
        # This will catch botocore.exceptions.NoCredentialsError if AWS isn't configured
        logger.warning(f"Could not retrieve secret '{secret_id}'. Error: {e}. Service may be disabled.")
        return "" # Return empty string to signify failure

# ------------------------------------------------------------------
async def is_product_marked(product_name: str, category: str) -> bool:
    if not pg_pool:
        logger.error("PostgreSQL connection pool not initialized. Cannot check if product is marked.")
        return False
    try:
        async with pg_pool.acquire() as conn:
            count = await conn.fetchval(
                "SELECT COUNT(*) FROM marked_products WHERE product_name = $1 AND category = $2",
                product_name, category
            )
            return count > 0
    except Exception as e:
        logger.error(f"Failed to check if product is marked in PostgreSQL: {e}")
        return False

# ------------------------------------------------------------------
# Batched alert queues
discord_alerts = []
slack_alerts   = []
email_alerts   = []

def _flush_discord():
    if not discord_alerts:
        return
    
    DISCORD_WEBHOOK_URL = _get_secret("discord_webhook")
    if not DISCORD_WEBHOOK_URL:
        logger.warning("DISCORD_WEBHOOK_URL not set. Cannot send Discord alerts.")
        discord_alerts.clear()
        return

    payload = {"content": "\n".join(discord_alerts)}
    try:
        requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=5).raise_for_status()
        logger.info("Discord batch sent (%d alerts)", len(discord_alerts))
    except Exception as e:
        logger.error("Failed Discord batch: %s", e)
    discord_alerts.clear()

def _flush_slack():
    if not slack_alerts:
        return

    SLACK_WEBHOOK_URL = _get_secret("slack_webhook")
    if not SLACK_WEBHOOK_URL:
        logger.warning("SLACK_WEBHOOK_URL not set. Cannot send Slack alerts.")
        slack_alerts.clear()
        return

    payload = {"text": "\n".join(slack_alerts)}
    try:
        requests.post(SLACK_WEBHOOK_URL, json=payload, timeout=5).raise_for_status()
        logger.info("Slack batch sent (%d alerts)", len(slack_alerts))
    except Exception as e:
        logger.error("Failed Slack batch: %s", e)
    slack_alerts.clear()

def _flush_email():
    if not email_alerts:
        return

    EMAIL_HOST = _get_secret("email_host")
    EMAIL_PORT_STR = _get_secret("email_port")
    EMAIL_USER = _get_secret("email_user")
    EMAIL_PASSWORD = _get_secret("email_password")
    EMAIL_RECIPIENT = _get_secret("email_recipient")

    if not all([EMAIL_HOST, EMAIL_PORT_STR, EMAIL_USER, EMAIL_PASSWORD, EMAIL_RECIPIENT]):
        logger.warning("Email settings are incomplete. Cannot send email alerts.")
        email_alerts.clear()
        return
        
    try:
        EMAIL_PORT = int(EMAIL_PORT_STR)
    except (ValueError, TypeError):
        logger.error(f"Invalid EMAIL_PORT: {EMAIL_PORT_STR}. Must be an integer.")
        email_alerts.clear()
        return

    body = "\n\n".join(email_alerts)
    msg = MIMEText(body)
    msg["Subject"] = "CÆSER Alert Batch"
    msg["From"]    = EMAIL_USER
    msg["To"]      = EMAIL_RECIPIENT

    try:
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            server.send_message(msg)
        logger.info("Email batch sent (%d alerts)", len(email_alerts))
    except Exception as e:
        logger.error("Failed email batch: %s", e)
    email_alerts.clear()

# ------------------------------------------------------------------
# The send_*_alert functions remain unchanged as they only append to lists
async def send_discord_alert(prediction, hype_data):
    product_name = prediction['product'].get('name', 'Unknown Product')
    category = prediction['product'].get('category', 'Unknown')

    if not await is_product_marked(product_name, category):
        logger.info("Product %s not marked – skipping Discord", product_name)
        return {"success": True, "message": "Product not marked, alert skipped"}

    alert = (
        f"**{product_name}** ({category})\n"
        f"Uplift: {prediction['uplift']:.2f}% | "
        f"Confidence: {prediction['confidence']:.2f} | "
        f"Strategy: {prediction['strategy']} | "
        f"Hype: {hype_data['averageScore']:.2f} | "
        f"Sentiment Δ: {hype_data['hourly_sentiment_change']:.2f}%"
    )
    if hype_data.get("change_detected"):
        alert += f" ⚠️ Hype changed by {hype_data['change_percent']:.2f}%!"
    discord_alerts.append(alert)
    return {"success": True, "message": "Queued for Discord batch"}

async def send_slack_alert(prediction, hype_data):
    product_name = prediction['product'].get('name', 'Unknown Product')
    category = prediction['product'].get('category', 'Unknown')

    if not await is_product_marked(product_name, category):
        logger.info("Product %s not marked – skipping Slack", product_name)
        return {"success": True, "message": "Product not marked, alert skipped"}

    alert = (
        f"*{product_name}* ({category})\n"
        f"Uplift: {prediction['uplift']:.2f}% | "
        f"Confidence: {prediction['confidence']:.2f} | "
        f"Strategy: {prediction['strategy']} | "
        f"Hype: {hype_data['averageScore']:.2f} | "
        f"Sentiment Δ: {hype_data['hourly_sentiment_change']:.2f}%"
    )
    if hype_data.get("change_detected"):
        alert += f" ⚠️ Hype changed by {hype_data['change_percent']:.2f}%!"
    slack_alerts.append(alert)
    return {"success": True, "message": "Queued for Slack batch"}

async def send_email_alert(prediction, hype_data):
    product_name = prediction['product'].get('name', 'Unknown Product')
    category = prediction['product'].get('category', 'Unknown')

    if not await is_product_marked(product_name, category):
        logger.info("Product %s not marked – skipping Email", product_name)
        return {"success": True, "message": "Product not marked, alert skipped"}

    body = (
        f"Product: {product_name}\n"
        f"Category: {category}\n"
        f"Demand Uplift: {prediction['uplift']:.2f}%\n"
        f"Confidence: {prediction['confidence']:.2f}%\n"
        f"Strategy: {prediction['strategy']}\n"
        f"Hype Score: {hype_data['averageScore']:.2f}\n"
        f"Hourly Sentiment Change: {hype_data['hourly_sentiment_change']:.2f}%"
    )
    if hype_data.get("change_detected"):
        body += f"\n⚠️ Hype score changed by {hype_data['change_percent']:.2f}%!"
    email_alerts.append(body)
    return {"success": True, "message": "Queued for Email batch"}

# ------------------------------------------------------------------
async def send_alert(prediction, hype_data):
    await send_discord_alert(prediction, hype_data)
    await send_slack_alert(prediction, hype_data)
    await send_email_alert(prediction, hype_data)

    # Flush all queues
    _flush_discord()
    _flush_slack()
    _flush_email()

    # Summaries
    successes = [bool(discord_alerts), bool(slack_alerts), bool(email_alerts)]
    return {"success": any(successes),
            "message": "Alerts batched and flushed"}

# ------------------------------------------------------------------
# NEW ASYNC WRAPPER
# ------------------------------------------------------------------
async def send_alert_async(prediction, hype_data):
    return await send_alert(prediction, hype_data)

async def init_discord_service():
    global pg_pool
    try:
        pg_pool = await asyncpg.create_pool(POSTGRES_URL, min_size=1, max_size=10)
        async with pg_pool.acquire() as conn:
            await conn.execute(
                """
                CREATE TABLE IF NOT EXISTS marked_products (
                    product_name TEXT PRIMARY KEY,
                    category TEXT NOT NULL
                );
                """
            )
        logger.info("PostgreSQL connected and marked_products table ensured.")
    except Exception as e:
        logger.error(f"Failed to connect to PostgreSQL or create marked_products table: {e}")
        pg_pool = None