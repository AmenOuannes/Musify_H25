from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from urllib.parse import unquote

from backend.app.routes.ResponseFormat import responseFormat
from backend.app.services.AlbumService import AlbumService

album_bp = Blueprint('album_bp', __name__)
albumService = AlbumService()

@album_bp.route('/albums', methods=['GET'])
def get_albums():
    limit = request.args.get('limit', type=int) if 'limit' in request.args else -1
    research = unquote(request.args.get('research', type=str)) if 'research' in request.args else ""
    albums = albumService.getAlbums(limit,research)
    return responseFormat({"albums": albums}), 200

@album_bp.route('/albums/<album_name>', methods=['GET'])
def get_album(album_name):
    try:
        song = albumService.getAlbum(unquote(album_name))
        return responseFormat(song),200
    except Exception as e:
        return jsonify({'error': str(e)}), 404


@album_bp.route('/albums/', methods=['POST'])
@jwt_required()
def create_album():
    try:
        current_user = get_jwt_identity()
        album_name = unquote(request.json.get('album_name'))
        genre = unquote(request.json.get('genre'))
        artist_name = unquote(request.json.get('artist_name'))
        release_date = unquote(request.json.get('release_date'))
        image = unquote(request.json.get('image'))

        albumService.createAlbum(album_name, genre, artist_name, release_date, image)
        return jsonify({"message": "created"}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@album_bp.route('/albums/<album_name>/songs', methods=['GET'])
def getAlbumSongs(album_name):
    songs = albumService.getSongsFromAlbum(unquote(album_name))
    return responseFormat({"songs": songs}), 200

@album_bp.route('/albums/<album_name>/songs/<song_name>', methods=['POST'])
@jwt_required()
def createSong(album_name, song_name):
    try:
        current_user = get_jwt_identity()
        albumService.addSongToAlbum(unquote(album_name), unquote(song_name))
        return jsonify({"message": "created"}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@album_bp.route('/albums/<album_name>/songs/<song_name>', methods=['DELETE'])
@jwt_required()
def deleteSong(album_name, song_name):
    try:
        current_user = get_jwt_identity()
        albumService.deleteSongFromAlbum(unquote(album_name), unquote(song_name))
        return jsonify({"message": "deleted"}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
