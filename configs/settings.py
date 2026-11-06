# configs/settings.py
# App-wide settings live here so they are easy to find and change in one place.
# Values are read from the .env file. If a value is missing, the default is used.

import os

from dotenv import load_dotenv

load_dotenv()  # reads the .env file and adds its values to the environment

APP_NAME = os.getenv("APP_NAME", "Todo API")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
APP_DESCRIPTION = os.getenv("APP_DESCRIPTION", "A simple Todo API built with FastAPI for learning.")
