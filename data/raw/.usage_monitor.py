import os
import time
import smtplib
import socket
from email.mime.text import MIMEText
from datetime import datetime

# Configuration
LOG_FILE = '.usage_log.txt'
EMAIL_RECEIVER = 'mdalifsaniul@gmail.com'
EMAIL_SUBJECT = 'CAESER Project Access Notification'

def log_access():
    """Log project access with timestamp"""
    with open(LOG_FILE, 'a') as f:
        f.write(f"Accessed at: {datetime.now()}\n")

def send_notification():
    """Send email notification if online"""
    try:
        # Check internet connection
        socket.create_connection(("8.8.8.8", 53), timeout=5)
        
        msg = MIMEText(f"Project accessed at {datetime.now()}")
        msg['Subject'] = EMAIL_SUBJECT
        msg['From'] = 'monitor@caeser.local'
        msg['To'] = EMAIL_RECEIVER
        
        with smtplib.SMTP('localhost') as server:
            server.send_message(msg)
    except:
        pass  # Skip if offline or email fails

if __name__ == "__main__":
    log_access()
    send_notification()