# tests/__init__.py
import os, sys, dotenv
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
dotenv.load_dotenv(dotenv.find_dotenv())