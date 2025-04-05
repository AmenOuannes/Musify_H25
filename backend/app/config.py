import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables

db_name = os.getenv("DB_NAME")
db_password = os.getenv("DB_PASSWORD")
class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", f"mysql+pymysql://root:{db_password}@localhost/{db_name}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
    DEBUG = os.getenv("FLASK_ENV", "development") == "development"
