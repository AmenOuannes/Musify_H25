from urllib.parse import unquote

from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

from backend.app.routes.RequestFormat import get_user_credentials, get_limit_argument
from backend.app.routes.ResponseFormat import responseFormat, usernames_response
from backend.app.services.UserService import UserService

user_bp = Blueprint('user_bp', __name__)
userService = UserService()


@user_bp.route('/users', methods=['GET'])
def get_users():
    limit = get_limit_argument()
    all_users = userService.getUsers(limit)
    usernames = usernames_response(all_users)
    return {'users': usernames}, 200


@user_bp.route('/users', methods=['POST'])
def sign_up():
    try:
        user_name, first_name, last_name, email, password, birth_date = get_user_credentials()
        userService.createUser(user_name, first_name,
                               last_name, email, password, birth_date)
        return jsonify({"message": "User created"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400


@user_bp.route('/users/login', methods=['POST'])
def login():
    username = unquote(request.json.get('username'))
    password = unquote(request.json.get('password'))
    try:
        userService.login(username, password)
        access_token = create_access_token(identity=username)
        return responseFormat({"token": access_token}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400


@user_bp.route('/users/user', methods=['GET'])
@jwt_required()
def get_user_profile():
    try:
        current_user = get_jwt_identity()
        user_info = userService.retrieveUser(current_user)
        return responseFormat(user_info), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400


@user_bp.route('/users', methods=['PUT'])
@jwt_required()
def update_user_info():
    try:
        user_name, first_name, last_name, email, password, birth_date = get_user_credentials()
        current_user = get_jwt_identity()
        userService.update_user_info(
            current_user, user_name, first_name, last_name, email, password, birth_date)
        return responseFormat({"user_name": user_name, "password": password}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400


@user_bp.route('/users/likes/artists/<artist_name>', methods=['POST'])
@jwt_required()
def like_artist(artist_name):
    try:
        current_user = get_jwt_identity()
        userService.like_artist(current_user, unquote(artist_name))
        return jsonify({"message": "Artist liked"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400


@user_bp.route('/users/likes/artists', methods=['GET'])
@jwt_required()
def get_liked_artists():
    try:
        current_user = get_jwt_identity()
        research = unquote(request.args.get('research', type=str)
                           ) if 'research' in request.args else None
        artists = userService.get_liked_artists(current_user, research)
        return jsonify({"artists": artists}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400


@user_bp.route('/users/likes/artists/<artist_name>', methods=['DELETE'])
@jwt_required()
def unlike_artist(artist_name):
    try:
        current_user = get_jwt_identity()
        userService.unlike_artist(current_user, unquote(artist_name))
        return jsonify({"message": "Artist unliked"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400


@user_bp.route('/users/likes/playlists', methods=['GET'])
@jwt_required()
def get_liked_playlists():
    try:
        current_user = get_jwt_identity()
        research = unquote(request.args.get('research', type=str)
                           ) if 'research' in request.args else None
        playlists = userService.get_liked_playlists(current_user, research)
        return jsonify({"playlists": playlists}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400


@user_bp.route('/users/likes/playlists/<playlist_name>', methods=['DELETE'])
@jwt_required()
def unlike_playlists(playlist_name):
    try:
        current_user = get_jwt_identity()
        userService.unlike_playlist(current_user, unquote(playlist_name))
        return jsonify({"message": "Playlist unliked"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400


@user_bp.route('/users/likes/playlists/<playlist_name>', methods=['POST'])
@jwt_required()
def like_a_playlist(playlist_name):
    try:
        current_user = get_jwt_identity()
        userService.like_playlist(current_user, unquote(playlist_name))
        return jsonify({"message": "Playlist liked"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400
