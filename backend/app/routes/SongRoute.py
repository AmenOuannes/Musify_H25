from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from urllib.parse import unquote

from backend.app.routes.ResponseFormat import responseFormat
from backend.app.services.SongService import SongService

song_bp = Blueprint('song_bp', __name__)
songService = SongService()
@song_bp.route('/songs', methods=['GET'])
def get_songs():
    limit = request.args.get('limit') if 'limit' in request.args else -1
    research = request.args.get('research') if 'research' in request.args else ""
    songs = songService.getAllSongs(limit, research)
    return responseFormat({"songs": songs}), 200

@song_bp.route('/songs/<song_name>', methods=['GET'])
def get_song(song_name):
    try:
        decoded_name = unquote(song_name)
        song = songService.getSong(decoded_name)
        return responseFormat(song),200
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@song_bp.route('/songs', methods=['POST'])
@jwt_required()
def create_song():
    try:
        current_user = get_jwt_identity()

        song_name = unquote(request.json.get('song_name'))
        genre = unquote(request.json.get('genre'))
        artist = unquote(request.json.get('artist_name'))
        release_date = unquote(request.json.get('release_date'))
        url = unquote(request.json.get('url'))

        songService.createSong(song_name, genre, artist, release_date, url)
        return jsonify({"message": "created"}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400