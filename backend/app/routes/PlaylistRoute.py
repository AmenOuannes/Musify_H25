from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from backend.app.routes.ResponseFormat import responseFormat
from backend.app.services.PlaylistService import PlaylistService
from backend.app.services.SongService import SongService

playlist_bp = Blueprint('playlist_bp', __name__)
playlistService = PlaylistService()
@playlist_bp.route('/playlists', methods=['GET'])
def get_playlists():
    limit = request.args.get('limit', type=int)
    playlists = playlistService.getPlaylists(limit)
    return responseFormat({"playlists":playlists}), 200

@playlist_bp.route('/playlists/<playlist_name>', methods=['GET'])
def get_playlist(playlist_name):
    try:
        playlist = playlistService.getPlaylist(playlist_name)
        return responseFormat(playlist), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 404