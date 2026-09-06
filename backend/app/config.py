import os
import ssl
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from dotenv import load_dotenv

load_dotenv()


def _database_uri():
    url = os.getenv("DATABASE_URL")
    if url:
        if url.startswith("mysql://"):
            url = url.replace("mysql://", "mysql+pymysql://", 1)
        return _strip_ssl_query(url)
    db_name = os.getenv("DB_NAME")
    db_password = os.getenv("DB_PASSWORD")
    db_user = os.getenv("DB_USER", "root")
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "3306")
    return f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"


def _strip_ssl_query(url):
    parts = urlsplit(url)
    query = [
        (key, value)
        for key, value in parse_qsl(parts.query, keep_blank_values=True)
        if not key.lower().startswith("ssl")
    ]
    return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))


def _mysql_ssl_args():
    ca = os.getenv("MYSQL_SSL_CA")
    if ca:
        if "BEGIN CERTIFICATE" in ca:
            path = "/tmp/mysql-ca.pem"
            with open(path, "w") as file:
                file.write(ca)
        else:
            path = ca
        return {"ssl": {"ca": path}}

    if os.getenv("DATABASE_URL"):
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        return {"ssl": context}

    return {}


class Config:
    SQLALCHEMY_DATABASE_URI = _database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {"connect_args": _mysql_ssl_args()}
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", os.getenv("SECRET_KEY", "supersecretkey"))
    DEBUG = os.getenv("FLASK_ENV", "production") == "development"
    FRONTEND_ORIGINS = [
        origin.strip()
        for origin in os.getenv("FRONTEND_ORIGIN", "http://localhost:5500").split(",")
        if origin.strip()
    ]
    EMAIL_CONFIRM_SECRET = os.getenv("EMAIL_CONFIRM_SECRET", os.getenv("SECRET_KEY", "supersecretkey"))
