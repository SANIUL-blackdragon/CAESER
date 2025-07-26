import os
import requests
import logging
import sqlite3
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.service_account import Credentials

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

GOOGLE_SHEETS_CREDENTIALS = os.getenv("GOOGLE_SHEETS_CREDENTIALS")
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
SALESFORCE_CLIENT_ID = os.getenv("SALESFORCE_CLIENT_ID")
SALESFORCE_CLIENT_SECRET = os.getenv("SALESFORCE_CLIENT_SECRET")
SALESFORCE_USERNAME = os.getenv("SALESFORCE_USERNAME")
SALESFORCE_PASSWORD = os.getenv("SALESFORCE_PASSWORD")
SALESFORCE_TOKEN = os.getenv("SALESFORCE_TOKEN")
SALESFORCE_INSTANCE_URL = os.getenv("SALESFORCE_INSTANCE_URL")

DB_PATH = os.getenv("DB_PATH", "./data/caeser.db")

def get_google_sheets_service():
    try:
        creds = Credentials.from_service_account_info(json.loads(GOOGLE_SHEETS_CREDENTIALS))
        service = build('sheets', 'v4', credentials=creds)
        return service
    except Exception as e:
        logger.error(f"Failed to initialize Google Sheets service: {str(e)}")
        return None

def append_to_google_sheets(prediction, hype_data):
    if not GOOGLE_SHEETS_CREDENTIALS or not SPREADSHEET_ID:
        logger.error("Google Sheets configuration missing")
        return {"success": False, "message": "Google Sheets configuration missing"}
    
    service = get_google_sheets_service()
    if not service:
        return {"success": False, "message": "Failed to initialize Google Sheets service"}
    
    values = [
        [
            prediction['product'].get('name', 'Unknown'),
            prediction['product'].get('category', 'Unknown'),
            prediction.get('uplift', 0.0),
            prediction.get('confidence', 0.0),
            prediction.get('strategy', 'Unknown'),
            hype_data.get('averageScore', 0.0),
            hype_data.get('change_percent', 0.0) if hype_data.get('change_detected') else 0.0
        ]
    ]
    
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

def get_salesforce_access_token():
    auth_url = f"{SALESFORCE_INSTANCE_URL}/services/oauth2/token"
    payload = {
        'grant_type': 'password',
        'client_id': SALESFORCE_CLIENT_ID,
        'client_secret': SALESFORCE_CLIENT_SECRET,
        'username': SALESFORCE_USERNAME,
        'password': SALESFORCE_PASSWORD + SALESFORCE_TOKEN
    }
    try:
        response = requests.post(auth_url, data=payload, timeout=5)
        response.raise_for_status()
        return response.json().get('access_token')
    except requests.RequestException as e:
        logger.error(f"Failed to get Salesforce access token: {str(e)}")
        return None

def create_salesforce_record(prediction, hype_data):
    if not all([SALESFORCE_CLIENT_ID, SALESFORCE_CLIENT_SECRET, SALESFORCE_USERNAME, SALESFORCE_PASSWORD, SALESFORCE_TOKEN, SALESFORCE_INSTANCE_URL]):
        logger.error("Salesforce configuration missing")
        return {"success": False, "message": "Salesforce configuration missing"}
    
    access_token = get_salesforce_access_token()
    if not access_token:
        return {"success": False, "message": "Failed to get Salesforce access token"}
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    data = {
        'Name': prediction['product'].get('name', 'Unknown Product'),
        'Category__c': prediction['product'].get('category', 'Unknown'),
        'Demand_Uplift__c': prediction.get('uplift', 0.0),
        'Confidence__c': prediction.get('confidence', 0.0),
        'Strategy__c': prediction.get('strategy', 'Unknown'),
        'Hype_Score__c': hype_data.get('averageScore', 0.0),
        'Hype_Change_Percent__c': hype_data.get('change_percent', 0.0) if hype_data.get('change_detected') else 0.0
    }
    try:
        response = requests.post(
            f"{SALESFORCE_INSTANCE_URL}/services/data/v52.0/sobjects/Opportunity",
            headers=headers,
            json=data,
            timeout=5
        )
        response.raise_for_status()
        logger.info("Salesforce record created successfully")
        return {"success": True, "message": "Salesforce record created successfully"}
    except requests.RequestException as e:
        logger.error(f"Failed to create Salesforce record: {str(e)}")
        return {"success": False, "message": f"Failed to create Salesforce record: {str(e)}"}

def send_integrations(prediction, hype_data):
    results = [
        append_to_google_sheets(prediction, hype_data),
        create_salesforce_record(prediction, hype_data)
    ]
    successes = [r["success"] for r in results]
    messages = [r["message"] for r in results]
    return {"success": any(successes), "message": "; ".join(messages)}