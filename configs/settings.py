# configs/settings.py
# App-wide settings live here so they are easy to find and change in one place.
# Values are read from the .env file. If a value is missing, the default is used.

import os

from dotenv import load_dotenv

load_dotenv()  # reads the .env file and adds its values to the environment

APP_NAME = os.getenv("APP_NAME", "Todo API")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
APP_DESCRIPTION = os.getenv("APP_DESCRIPTION", "A simple Todo API built with FastAPI for learning.")

# Database settings
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("DB_PORT", "3306"))  # .env values are strings, so convert to int
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "todo_db")
