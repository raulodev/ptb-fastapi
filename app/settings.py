from decouple import config

DATABASE_URL = config("DATABASE_URL", default="sqlite:///database.db")
LANGUAGE_CODE = config("LANGUAGE_CODE", default="en")

BOT_FATHER_TOKEN = config("BOT_FATHER_TOKEN")
TG_SECRET_TOKEN = config("TG_SECRET_TOKEN")
