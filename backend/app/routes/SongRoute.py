from urllib.parse import unquote

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from backend.app.routes.RequestFormat import get_limit_argument, get_research_argument, get_song_credentials
from backend.app.routes.ResponseFormat import responseFormat
from backend.app.services.SongService import SongService

song_bp = Blueprint('song_bp', __name__)
songService = SongService()
@song_bp.route('/songs', methods=['GET'])
def get_songs():
    limit = get_limit_argument()
    research = get_research_argument()
    songs = songService.get_all_songs(limit, research)
    return responseFormat({"songs": songs}), 200

@song_bp.route('/songs/<song_name>', methods=['GET'])
def get_song(song_name):
    try:
        song = songService.get_song(unquote(song_name))
        return responseFormat(song), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@song_bp.route('/songs', methods=['POST'])
@jwt_required()
def create_song():
    try:
        current_user = get_jwt_identity()
        song_name, genre, artist,release_date, url = get_song_credentials()
        songService.create_song(song_name, genre, artist, release_date, url)
        return jsonify({"message": "created"}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400