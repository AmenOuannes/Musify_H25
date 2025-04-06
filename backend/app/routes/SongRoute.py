from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

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
        song = songService.getSong(song_name)
        return responseFormat(song),200
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@song_bp.route('/songs', methods=['POST'])
@jwt_required()
def create_song():
    try:
        current_user = get_jwt_identity()
        song_name = request.json.get('song_name')
        genre = request.json.get('genre')
        artist = request.json.get('artist')
        release_date = request.json.get('release_date')
        url = request.json.get('url')

        songService.createSong(song_name, genre, artist, release_date, url)
        return jsonify({"message": "created"}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400