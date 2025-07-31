import os
import boto3
import requests
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import logging
import sqlite3

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ------------------------------------------------------------------
# AWS Secrets Manager client
secrets_client = boto3.client('secretsmanager', region_name=os.getenv("AWS_REGION", "us-east-1"))

def _get_secret(secret_id: str) -> str:
    return secrets_client.get_secret_value(SecretId=secret_id)['SecretString']

# Pull secrets once at import time
DISCORD_WEBHOOK_URL = _get_secret("discord_webhook")
SLACK_WEBHOOK_URL   = _get_secret("slack_webhook")

EMAIL_HOST      = _get_secret("email_host")      # e.g. "smtp.gmail.com"
EMAIL_PORT      = int(_get_secret("email_port")) # e.g. 587
EMAIL_USER      = _get_secret("email_user")
EMAIL_PASSWORD  = _get_secret("email_password")
EMAIL_RECIPIENT = _get_secret("email_recipient")

DB_PATH = os.getenv("DB_PATH", "./data/caeser.db")

# ------------------------------------------------------------------
def is_product_marked(product_name, category):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*) FROM marked_products
        WHERE product_name = ? AND category = ?
    """, (product_name, category))
    count = cursor.fetchone()[0]
    conn.close()
    return count > 0

# ------------------------------------------------------------------
# Batched alert queues
discord_alerts = []
slack_alerts   = []
email_alerts   = []

def _flush_discord():
    if not discord_alerts:
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
def send_discord_alert(prediction, hype_data):
    product_name = prediction['product'].get('name', 'Unknown Product')
    category = prediction['product'].get('category', 'Unknown')

    if not is_product_marked(product_name, category):
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

def send_slack_alert(prediction, hype_data):
    product_name = prediction['product'].get('name', 'Unknown Product')
    category = prediction['product'].get('category', 'Unknown')

    if not is_product_marked(product_name, category):
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

def send_email_alert(prediction, hype_data):
    product_name = prediction['product'].get('name', 'Unknown Product')
    category = prediction['product'].get('category', 'Unknown')

    if not is_product_marked(product_name, category):
        logger.info("Product %s not marked – skipping Email", product_name)
        return {"success": True, "message": "Product not marked, alert skipped"}

    body = (
        f"Product: {product_name}\n"
        f"Category: {category}\n"
        f"Demand Uplift: {prediction['uplift']:.2f}%\n"
        f"Confidence: {prediction['confidence']:.2f}\n"
        f"Strategy: {prediction['strategy']}\n"
        f"Hype Score: {hype_data['averageScore']:.2f}\n"
        f"Hourly Sentiment Change: {hype_data['hourly_sentiment_change']:.2f}%"
    )
    if hype_data.get("change_detected"):
        body += f"\n⚠️ Hype score changed by {hype_data['change_percent']:.2f}%!"
    email_alerts.append(body)
    return {"success": True, "message": "Queued for Email batch"}

# ------------------------------------------------------------------
def send_alert(prediction, hype_data):
    send_discord_alert(prediction, hype_data)
    send_slack_alert(prediction, hype_data)
    send_email_alert(prediction, hype_data)

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
import asyncio
async def send_alert_async(prediction, hype_data):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, send_alert, prediction, hype_data)