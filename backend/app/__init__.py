from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Load Config
    app.config.from_object("app.config.Config")

    # Initialize Extensions
    db.init_app(app)
    Migrate(app, db)
    CORS(app)

    # Register Blueprints (routes)
    from app.routes.user_routes import user_bp
    from app.routes.product_routes import product_bp

    app.register_blueprint(user_bp, url_prefix="/api/users")
    app.register_blueprint(product_bp, url_prefix="/api/products")

    return app
