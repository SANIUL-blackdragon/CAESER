import os
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

import asyncio
import logging
from datetime import datetime, timedelta

import pandas as pd
import requests
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine


# ... (rest of the file)
