import os
import json
import requests
import logging
import sqlite3
import backoff
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.service_account import Credentials
from functools import lru_cache
import asyncio

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ------------------------------------------------------------------
# 0. Secrets helper
# ------------------------------------------------------------------
def _get_secret(secret_name: str, default=None):
    """
    Fetch secret from environment variables.
    """
    return os.getenv(secret_name, default)

# ------------------------------------------------------------------
# 1. Configuration
# ------------------------------------------------------------------
GOOGLE_SHEETS_CREDENTIALS = _get_secret("GOOGLE_SHEETS_CREDENTIALS")
SPREADSHEET_ID          = _get_secret("SPREADSHEET_ID")
SALESFORCE_CLIENT_ID    = _get_secret("SALESFORCE_CLIENT_ID")
SALESFORCE_CLIENT_SECRET= _get_secret("SALESFORCE_CLIENT_SECRET")
SALESFORCE_USERNAME     = _get_secret("SALESFORCE_USERNAME")
SALESFORCE_PASSWORD     = _get_secret("SALESFORCE_PASSWORD")
SALESFORCE_TOKEN        = _get_secret("SALESFORCE_TOKEN")
SALESFORCE_INSTANCE_URL = _get_secret("SALESFORCE_INSTANCE_URL")
DISCORD_WEBHOOK_SECRET_NAME = "discord_webhook"   # env var name
DB_PATH = os.getenv("DB_PATH", "./data/caeser.db")

# ------------------------------------------------------------------
# 2. Google Sheets helpers
# ------------------------------------------------------------------
@lru_cache(maxsize=1)
def get_google_sheets_service():
    """
    Returns a cached Google Sheets service object.
    """
    try:
        creds_json = GOOGLE_SHEETS_CREDENTIALS
        if not creds_json:
            raise ValueError("Google Sheets credentials are not set.")
        creds = Credentials.from_service_account_info(json.loads(creds_json))
        service = build('sheets', 'v4', credentials=creds, cache_discovery=False)
        logger.info("Google Sheets service initialized successfully")
        return service
    except (ValueError, json.JSONDecodeError, HttpError) as e:
        logger.error(f"Failed to initialize Google Sheets service: {str(e)}")
        return None

@backoff.on_exception(backoff.expo, HttpError, max_tries=5)
def append_to_google_sheets(prediction, hype_data):
    if not GOOGLE_SHEETS_CREDENTIALS or not SPREADSHEET_ID:
        logger.error("Google Sheets configuration missing")
        return {"success": False, "message": "Google Sheets configuration missing"}

    service = get_google_sheets_service()
    if not service:
        return {"success": False, "message": "Failed to initialize Google Sheets service"}

    values = [[
        prediction.get('product', {}).get('name', 'Unknown'),
        prediction.get('product', {}).get('category', 'Unknown'),
        prediction.get('uplift', 0.0),
        prediction.get('confidence', 0.0),
        prediction.get('strategy', 'Unknown'),
        hype_data.get('averageScore', 0.0),
        hype_data.get('change_percent', 0.0) if hype_data.get('change_detected') else 0.0
    ]]

    body = {'values': values}
    try:
        service.spreadsheets().values().append(
            spreadsheetId=SPREADSHEET_ID,
            range="Sheet1!A:G",
            valueInputOption="RAW",
            body=body
        ).execute()
        logger.info("Data appended to Google Sheets successfully")
        return {"success": True, "message": "Data appended to Google Sheets successfully"}
    except HttpError as e:
        logger.error(f"Failed to append to Google Sheets: {str(e)}")
        return {"success": False, "message": f"Failed to append to Google Sheets: {str(e)}"}

# ------------------------------------------------------------------
# 3. Salesforce helpers
# ------------------------------------------------------------------
@backoff.on_exception(backoff.expo, requests.exceptions.RequestException, max_tries=5)
def get_salesforce_access_token():
    required = [SALESFORCE_CLIENT_ID, SALESFORCE_CLIENT_SECRET, SALESFORCE_USERNAME,
                SALESFORCE_PASSWORD, SALESFORCE_TOKEN, SALESFORCE_INSTANCE_URL]
    if not all(required):
        logger.error("Salesforce configuration missing")
        return None

    auth_url = f"{SALESFORCE_INSTANCE_URL}/services/oauth2/token"
    password = (SALESFORCE_PASSWORD or "") + (SALESFORCE_TOKEN or "")
    payload = {
        'grant_type': 'password',
        'client_id': SALESFORCE_CLIENT_ID,
        'client_secret': SALESFORCE_CLIENT_SECRET,
        'username': SALESFORCE_USERNAME,
        'password': password
    }
    response = requests.post(auth_url, data=payload, timeout=10)
    response.raise_for_status()
    access_token = response.json().get("access_token")
    if not access_token:
        logger.error("No access token in Salesforce response")
        return None
    logger.info("Salesforce access token obtained successfully")
    return access_token

@backoff.on_exception(backoff.expo, requests.exceptions.RequestException, max_tries=5)
def create_salesforce_record(prediction, hype_data):
    access_token = get_salesforce_access_token()
    if not access_token:
        return {"success": False, "message": "Failed to get Salesforce access token"}

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    data = {
        'Name': prediction.get('product', {}).get('name', 'Unknown Product'),
        'Category__c': prediction.get('product', {}).get('category', 'Unknown'),
        'Demand_Uplift__c': prediction.get('uplift', 0.0),
        'Confidence__c': prediction.get('confidence', 0.0),
        'Strategy__c': prediction.get('strategy', 'Unknown'),
        'Hype_Score__c': hype_data.get('averageScore', 0.0),
        'Hype_Change_Percent__c': hype_data.get('change_percent', 0.0) if hype_data.get('change_detected') else 0.0
    }
    response = requests.post(
        f"{SALESFORCE_INSTANCE_URL}/services/data/v58.0/sobjects/Opportunity",
        headers=headers,
        json=data,
        timeout=10
    )
    response.raise_for_status()
    logger.info("Salesforce record created successfully")
    return {"success": True, "message": "Salesforce record created successfully"}

# ------------------------------------------------------------------
# 4. Discord helper (new) – batched alerts
# ------------------------------------------------------------------
_discord_alerts_buffer = []

def queue_discord_alert(message: str):
    """
    Add message to the in-memory buffer for Discord.
    """
    _discord_alerts_buffer.append(message)

@backoff.on_exception(backoff.expo, requests.exceptions.RequestException, max_tries=5)
def flush_discord_alerts():
    """
    Send all queued alerts in one batched POST.
    """
    global _discord_alerts_buffer
    if not _discord_alerts_buffer:
        return

    webhook_url = _get_secret(DISCORD_WEBHOOK_SECRET_NAME)
    if not webhook_url:
        logger.warning("Discord webhook URL not found; skipping alerts.")
        _discord_alerts_buffer.clear()
        return

    payload = {"content": "\n".join(_discord_alerts_buffer)}
    response = requests.post(webhook_url, json=payload, timeout=10)
    response.raise_for_status()
    logger.info(f"Sent {len(_discord_alerts_buffer)} Discord alerts")
    _discord_alerts_buffer.clear()

# ------------------------------------------------------------------
# 5. Main orchestrator
# ------------------------------------------------------------------
def send_integrations(prediction, hype_data):
    """
    Push data to Google Sheets, Salesforce, and queue Discord alerts.
    """
    # Queue a short Discord message for each prediction
    product_name = prediction.get('product', {}).get('name', 'Unknown')
    uplift = prediction.get('uplift', 0.0)
    queue_discord_alert(f"📈 {product_name}: predicted uplift {uplift:.2%}")

    results = [
        append_to_google_sheets(prediction, hype_data),
        create_salesforce_record(prediction, hype_data)
    ]
    flush_discord_alerts()  # send batched alerts

    successes = [r["success"] for r in results]
    messages = [r["message"] for r in results]
    return {"success": any(successes), "message": "; ".join(messages)}

# ------------------------------------------------------------------
# NEW ASYNC WRAPPER
# ------------------------------------------------------------------
async def send_integrations_async(prediction, hype_data):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, send_integrations, prediction, hype_data)
