from urllib.parse import unquote

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from backend.app.routes.RequestFormat import get_album_credentials, get_limit_argument, get_research_argument
from backend.app.routes.ResponseFormat import responseFormat
from backend.app.services.AlbumService import AlbumService

album_bp = Blueprint('album_bp', __name__)
albumService = AlbumService()

@album_bp.route('/albums', methods=['GET'])
def get_albums():
    limit = get_limit_argument()
    research = get_research_argument()
    albums = albumService.get_albums(limit, research)
    return responseFormat({"albums": albums}), 200

@album_bp.route('/albums/<album_name>', methods=['GET'])
def get_album(album_name):
    try:
        song = albumService.get_album(unquote(album_name))
        return responseFormat(song),200
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@album_bp.route('/albums/', methods=['POST'])
@jwt_required()
def create_album():
    try:
        current_user = get_jwt_identity()
        album_name, genre, artist_name, release_date, image = get_album_credentials()
        albumService.create_album(album_name, genre, artist_name, release_date, image)
        return jsonify({"message": "created"}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@album_bp.route('/albums/<album_name>/songs', methods=['GET'])
def get_album_songs(album_name):
    songs = albumService.get_songs_from_album(unquote(album_name))
    return responseFormat({"songs": songs}), 200

@album_bp.route('/albums/<album_name>/songs/<song_name>', methods=['POST'])
@jwt_required()
def create_song(album_name, song_name):
    try:
        current_user = get_jwt_identity()
        albumService.add_song_to_album(unquote(album_name), unquote(song_name))
        return jsonify({"message": "created"}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@album_bp.route('/albums/<album_name>/songs/<song_name>', methods=['DELETE'])
@jwt_required()
def delete_song(album_name, song_name):
    try:
        current_user = get_jwt_identity()
        albumService.delete_song_from_album(unquote(album_name), unquote(song_name))
        return jsonify({"message": "deleted"}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
