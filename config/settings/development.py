from .base import *
import os
import sys
import ast
import pytz
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv('.env')

DEBUG = True

ALLOWED_HOSTS = ["*"]

# PostgreSQL local development database

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

