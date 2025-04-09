from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from urllib.parse import unquote

from backend.app.routes.ResponseFormat import responseFormat
from backend.app.services.PlaylistService import PlaylistService

playlist_bp = Blueprint('playlist_bp', __name__)
playlistService = PlaylistService()
@playlist_bp.route('/playlists', methods=['GET'])
def get_playlists():
    limit = request.args.get('limit', type=int) if 'limit' in request.args else -1
    research = unquote(request.args.get('research', type=str)) if 'research' in request.args else ""
    owner = unquote(request.args.get('owner', type=str)) if 'owner' in request.args else ""
    playlists = playlistService.getPlaylists(limit, research, owner)
    return responseFormat({"playlists":playlists}), 200

@playlist_bp.route('/playlists/<playlist_name>', methods=['GET'])
def get_playlist(playlist_name):
    try:
        playlist = playlistService.getPlaylist(playlist_name)
        return responseFormat(playlist), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@playlist_bp.route('/playlists', methods=['POST'])
@jwt_required()
def create_playlist():
    try:
        current_user = get_jwt_identity()
        playlist_name = unquote(request.json.get('playlist_name'))
        private = request.json.get('private', 0)

        playlistService.createPlaylist(playlist_name, current_user, private)
        return jsonify({"message": "Playlist created"}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 400


@playlist_bp.route('/playlists/<playlist_name>', methods=['DELETE'])
@jwt_required()
def delete_playlist(playlist_name):
    try:
        playlistService.deletePlaylist(playlist_name)
        return jsonify({"message": "Playlist deleted"}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@playlist_bp.route('/playlists/<playlist_name>/songs/<song_name>', methods=['GET'])
def get_song(playlist_name, song_name):
    try:
        song = playlistService.getSongFromPlaylist(playlist_name, song_name)
        return responseFormat({"song":song}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 404


@playlist_bp.route('/playlists/<playlist_name>/songs', methods=['GET'])
def get_songs(playlist_name):
    try:
        owner = unquote(request.args.get('owner', type=str)) if 'owner' in request.args else ""
        songs = playlistService.getAllSongsFromPlaylist(unquote(playlist_name), owner)
        return responseFormat({"songs":songs}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 404


@playlist_bp.route('/playlists/<playlist_name>/songs/<song_name>', methods=['POST'])
@jwt_required()
def create_song(playlist_name, song_name):
    try:
        current_user = get_jwt_identity()
        playlistService.addSongToPlaylist(unquote(playlist_name), unquote(song_name))
        return jsonify({"message": "Song added"}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@playlist_bp.route('/playlists/<playlist_name>/songs/<song_name>', methods=['DELETE'])
@jwt_required()
def delete_song(playlist_name, song_name):
    try:
        current_user = get_jwt_identity()
        playlistService.deleteSongFromPlaylist(unquote(playlist_name), unquote(song_name))
        return jsonify({"message": "Song deleted"}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 404