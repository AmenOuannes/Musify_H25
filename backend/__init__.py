from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from .app.config import Config

# Initialize Flask extensions
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)

    # Load config
    app.config.from_object(Config)
    app.config["JWT_SECRET_KEY"] = "HS256"

    # Init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app)

    # Register routes (blueprints)
    from .app.routes.ArtistRoute import artist_bp
    from .app.routes.PlaylistRoute import playlist_bp
    from .app.routes.SongRoute import song_bp
    from .app.routes.UserRoute import user_bp
    from .app.routes.AlbumRoute import album_bp

    app.register_blueprint(user_bp, url_prefix='/')
    app.register_blueprint(song_bp, url_prefix='/')
    app.register_blueprint(artist_bp, url_prefix='/')
    app.register_blueprint(playlist_bp, url_prefix='/')
    app.register_blueprint(album_bp, url_prefix='/')

    # Test route
    @app.route("/")
    def main():
        return "musify_h25 API"

    return app
