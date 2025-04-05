from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from backend.app.routes.ArtistRoute import artist_bp
from backend.app.routes.PlaylistRoute import playlist_bp
from backend.app.routes.SongRoute import song_bp
from backend.app.routes.UserRoute import user_bp

app = Flask(__name__)
app.register_blueprint(user_bp, url_prefix='/')
app.register_blueprint(song_bp, url_prefix='/')
app.register_blueprint(artist_bp, url_prefix='/')
app.register_blueprint(playlist_bp, url_prefix='/')
CORS(app)

app.config["JWT_SECRET_KEY"] = "HS256"
jwt = JWTManager(app)

@app.route("/")
def main():

    return "musify_h25 API"


if __name__ == "__main__":

    app.run()


