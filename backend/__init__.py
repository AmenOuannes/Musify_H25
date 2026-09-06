from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from .app.config import Config

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(
        app,
        origins=app.config["FRONTEND_ORIGINS"],
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization"],
    )

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

    @app.route("/")
    def main():
        return "musify_h25 API"

    @app.route("/health")
    def health():
        return {"status": "ok"}, 200

    return app
