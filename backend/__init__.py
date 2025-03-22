from flask import Flask
from flask_cors import CORS
from backend.app.routes.userRoute import user_bp

app = Flask(__name__)
app.register_blueprint(user_bp, url_prefix='/')
CORS(app)
@app.route("/")
def main():

    return "musify_h25 API"


if __name__ == "__main__":

    app.run()


