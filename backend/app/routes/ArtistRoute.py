from urllib.parse import unquote

from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

from backend.app.routes.RequestFormat import get_limit_argument, get_research_argument, get_artist_credentials
from backend.app.routes.ResponseFormat import responseFormat
from backend.app.services.ArtistService import ArtistService

artist_bp = Blueprint('artist_bp', __name__)
artistService = ArtistService()

@artist_bp.route('/artists', methods=['GET'])
def get_artists():
    limit = get_limit_argument()
    research = get_research_argument()
    artists = artistService.get_artists(limit, research)
    return responseFormat({"artists": artists}), 200

@artist_bp.route('/artists', methods=['POST'])
@jwt_required()
def add_artist():
    try:
        current_user = get_jwt_identity()
        artist_name, genre, profile_url, followers, image = get_artist_credentials()
        artistService.add_artist(artist_name, genre, profile_url, image, followers)
        return jsonify({"message": "artist created"}), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 400

@artist_bp.route('/artists/<artist_name>', methods=['GET'])
def get_artist_by_name(artist_name):
    try:
        artist_json = artistService.get_artist(unquote(artist_name))
        return responseFormat(artist_json), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400



