import os
import requests
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import logging
import sqlite3

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = os.getenv("EMAIL_PORT", 587)
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECIPIENT = os.getenv("EMAIL_RECIPIENT")
DB_PATH = os.getenv("DB_PATH", "./data/caeser.db")

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

def send_discord_alert(prediction, hype_data):
    if not DISCORD_WEBHOOK_URL:
        logger.error("DISCORD_WEBHOOK_URL not configured")
        return {"success": False, "message": "DISCORD_WEBHOOK_URL not configured"}
    
    product_name = prediction['product'].get('name', 'Unknown Product')
    category = prediction['product'].get('category', 'Unknown')
    
    if not is_product_marked(product_name, category):
        logger.info(f"Product {product_name} not marked, skipping Discord alert")
        return {"success": True, "message": "Product not marked, alert skipped"}
    
    embed = {
        "title": f"New Prediction for {product_name}",
        "description": (
            f"**Category**: {category}\n"
            f"**Uplift**: {prediction['uplift']:.2f}%\n"
            f"**Confidence**: {prediction['confidence']:.2f}\n"
            f"**Strategy**: {prediction['strategy']}\n"
            f"**Hype Score**: {hype_data['averageScore']:.2f}\n"
            f"**Hourly Sentiment Change**: {hype_data['hourly_sentiment_change']:.2f}%"
        ),
        "color": 0x667eea if not hype_data.get("change_detected") else 0xff0000,
        "footer": {"text": "CÆSER System"}
    }
    
    if hype_data.get("change_detected", False):
        embed["description"] += f"\n**Alert**: Hype score changed by {hype_data['change_percent']:.2f}%!"
    
    payload = {"embeds": [embed]}
    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=5)
        response.raise_for_status()
        return {"success": True, "message": "Discord alert sent successfully"}
    except requests.RequestException as e:
        logger.error(f"Failed to send Discord alert: {str(e)}")
        return {"success": False, "message": f"Failed to send Discord alert: {str(e)}"}

def send_email_alert(prediction, hype_data):
    if not all([EMAIL_HOST, EMAIL_USER, EMAIL_PASSWORD, EMAIL_RECIPIENT]):
        logger.error("Email configuration missing")
        return {"success": False, "message": "Email configuration missing"}
    
    product_name = prediction['product'].get('name', 'Unknown Product')
    category = prediction['product'].get('category', 'Unknown')
    
    if not is_product_marked(product_name, category):
        logger.info(f"Product {product_name} not marked, skipping email alert")
        return {"success": True, "message": "Product not marked, alert skipped"}
    
    subject = f"CÆSER Alert: {product_name}"
    body = (
        f"Category: {category}\n"
        f"Demand Uplift: {prediction['uplift']:.2f}%\n"
        f"Confidence: {prediction['confidence']:.2f}\n"
        f"Strategy: {prediction['strategy']}\n"
        f"Hype Score: {hype_data['averageScore']:.2f}\n"
        f"Hourly Sentiment Change: {hype_data['hourly_sentiment_change']:.2f}%"
    )
    if hype_data.get("change_detected", False):
        body += f"\nAlert: Hype score changed by {hype_data['change_percent']:.2f}%!"
    
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_USER
    msg["To"] = EMAIL_RECIPIENT
    
    try:
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            server.send_message(msg)
        logger.info("Email alert sent successfully")
        return {"success": True, "message": "Email alert sent successfully"}
    except Exception as e:
        logger.error(f"Failed to send email alert: {str(e)}")
        return {"success": False, "message": f"Failed to send email alert: {str(e)}"}

def send_slack_alert(prediction, hype_data):
    if not SLACK_WEBHOOK_URL:
        logger.error("SLACK_WEBHOOK_URL not configured")
        return {"success": False, "message": "SLACK_WEBHOOK_URL not configured"}
    
    product_name = prediction['product'].get('name', 'Unknown Product')
    category = prediction['product'].get('category', 'Unknown')
    
    if not is_product_marked(product_name, category):
        logger.info(f"Product {product_name} not marked, skipping Slack alert")
        return {"success": True, "message": "Product not marked, alert skipped"}
    
    text = (
        f"*New Prediction for {product_name}*\n"
        f"Category: {category}\n"
        f"Demand Uplift: {prediction['uplift']:.2f}%\n"
        f"Confidence: {prediction['confidence']:.2f}\n"
        f"Strategy: {prediction['strategy']}\n"
        f"Hype Score: {hype_data['averageScore']:.2f}\n"
        f"Hourly Sentiment Change: {hype_data['hourly_sentiment_change']:.2f}%"
    )
    if hype_data.get("change_detected", False):
        text += f"\n*Alert*: Hype score changed by {hype_data['change_percent']:.2f}%!"
    
    payload = {"text": text}
    try:
        response = requests.post(SLACK_WEBHOOK_URL, json=payload, timeout=5)
        response.raise_for_status()
        return {"success": True, "message": "Slack alert sent successfully"}
    except requests.RequestException as e:
        logger.error(f"Failed to send Slack alert: {str(e)}")
        return {"success": False, "message": f"Failed to send Slack alert: {str(e)}"}

def send_alert(prediction, hype_data):
    results = [
        send_discord_alert(prediction, hype_data),
        send_email_alert(prediction, hype_data),
        send_slack_alert(prediction, hype_data)
    ]
    successes = [r["success"] for r in results]
    messages = [r["message"] for r in results]
    return {"success": any(successes), "message": "; ".join(messages)}