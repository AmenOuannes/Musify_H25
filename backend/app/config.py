import os
from dotenv import load_dotenv

load_dotenv()


def _database_uri():
    url = os.getenv("DATABASE_URL")
    if url:
        if url.startswith("mysql://"):
            return url.replace("mysql://", "mysql+pymysql://", 1)
        return url
    db_name = os.getenv("DB_NAME")
    db_password = os.getenv("DB_PASSWORD")
    db_user = os.getenv("DB_USER", "root")
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "3306")
    return f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"


class Config:
    SQLALCHEMY_DATABASE_URI = _database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", os.getenv("SECRET_KEY", "supersecretkey"))
    DEBUG = os.getenv("FLASK_ENV", "production") == "development"
    FRONTEND_ORIGINS = [
        origin.strip()
        for origin in os.getenv("FRONTEND_ORIGIN", "http://localhost:5500").split(",")
        if origin.strip()
    ]
    EMAIL_CONFIRM_SECRET = os.getenv("EMAIL_CONFIRM_SECRET", os.getenv("SECRET_KEY", "supersecretkey"))
