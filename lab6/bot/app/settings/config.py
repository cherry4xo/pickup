import os

from decouple import config

import string
import random


class Settings:
    TELEGRAM_BOT_TOKEN = config("TELEGRAM_BOT_TOKEN")
    PROVIDER_TOKEN = config("PROVIDER_TOKEN")

    DB_NAME = config("DB_NAME")
    DB_USER = config("DB_USER")
    DB_PASS = config("DB_PASS")
    DB_HOST = config("DB_HOST")
    DB_PORT = config("DB_PORT")

    REDIS_HOST = config("REDIS_HOST")
    REDIS_PORT = config("REDIS_PORT")

    DB_URL = f"postgres://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    APPLICATIONS = [
        "db"
    ]

    APPLICATIONS_MODULE = "app"

    DEFAULT_ADMIN_TG_ID = config("DEFAULT_ADMIN_TG_ID")
    DEFAULT_ADMIN_USERNAME = config("DEFAULT_ADMIN_USERNAME")
    DEFAULT_ADMIN_FIRST_NAME = config("DEFAULT_ADMIN_FIRST_NAME")

    SHOP_ID = config("SHOP_ID")
    YOO_SECRET = config("YOO_SECRET")


settings = Settings()