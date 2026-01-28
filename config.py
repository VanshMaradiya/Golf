import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    # Secret key (from .env or fallback)
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")

    # Database URL (env first, fallback to SQLite)
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///" + os.path.join(BASE_DIR, "golf.db")
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
