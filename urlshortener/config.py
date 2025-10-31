# core/config.py
import environ
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env(BASE_DIR / ".env")

class Settings:
    DEBUG = env.bool("DEBUG", False)
    SECRET_KEY = env("SECRET_KEY", default="change-me")
    DATABASE_URL = env("DATABASE_URL", default="")
    REDIS_URL = env("REDIS_URL", default="")
    ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["localhost"])

settings = Settings()