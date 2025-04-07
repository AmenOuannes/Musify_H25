from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from backend.app.routes.ResponseFormat import responseFormat
from backend.app.services.PlaylistService import PlaylistService

playlist_bp = Blueprint('playlist_bp', __name__)
playlistService = PlaylistService()
@playlist_bp.route('/playlists', methods=['GET'])
def get_playlists():
    limit = request.args.get('limit', type=int) if 'limit' in request.args else -1
    research = request.args.get('research', type=str) if 'research' in request.args else ""
    owner = request.args.get('owner', type=str) if 'owner' in request.args else ""
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
        playlist_name = request.json.get('playlist_name')
        private = request.json.get('private', 0)

        playlistService.createPlaylist(playlist_name, current_user, private)
        return jsonify({"message": "Playlist created"}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 400