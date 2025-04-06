from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from backend.app.routes.ResponseFormat import responseFormat
from backend.app.services.ArtistService import ArtistService

artist_bp = Blueprint('artist_bp', __name__)
artistService = ArtistService()

@artist_bp.route('/artists', methods=['GET'])
def get_artists():
    limit = request.args.get('limit', type=int) if 'limit' in request.args else -1
    artists = artistService.getArtists(limit)
    return responseFormat({"artists": artists}), 200

@artist_bp.route('/artists', methods=['POST'])
@jwt_required()
def add_artist():
    try:
        current_user = get_jwt_identity()
        artist_name = request.json.get('artist_name')
        genre = request.json.get('genre')
        profile_url = request.json.get('profile_url')
        followers = request.json.get('followers')
        image = request.json.get('image')

        artistService.addArtist(artist_name, genre, profile_url, image, followers)
        return jsonify({"message": "artist created"}), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 400


@artist_bp.route('/artists/<artist_name>', methods=['GET'])
def get_artist_by_name(artist_name):
    try:
        artist_json = artistService.getArtist(artist_name)
        return responseFormat(artist_json), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400



