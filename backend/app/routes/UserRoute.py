from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from backend.app.routes.ResponseFormat import responseFormat
from backend.app.services.UserService import UserService
from urllib.parse import unquote

user_bp = Blueprint('user_bp', __name__)
userService = UserService()

@user_bp.route('/users', methods=['GET'])
def get_users():
    limit = request.args.get('limit', type=int) if 'limit' in request.args else -1
    all_users = userService.getUsers(limit)
    print(all_users)
    usernames = [{'username':user['username']} for user in all_users]
    return {'users':usernames}, 200

@user_bp.route('/users', methods=['POST'])
def signUp():
    user_name = unquote(request.json.get('username'))
    first_name = unquote(request.json.get('first_name'))
    last_name = unquote(request.json.get('last_name'))
    email = unquote(request.json.get('email'))
    password = unquote(request.json.get('password'))
    birth_date = unquote(request.json.get('birth_date'))

    try:
        userService.createUser(user_name, first_name, last_name, email, password, birth_date)
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
        return responseFormat({"token":access_token}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400


@user_bp.route('/users/user', methods=['GET'])
@jwt_required()
def userProfile():
    current_user = get_jwt_identity()
    user_info = userService.retrieveUser(current_user)
    return responseFormat(user_info), 200

@user_bp.route('/users', methods=['PUT'])
@jwt_required()
def changeUser():
    current_user = get_jwt_identity()
    user_name = unquote(request.json.get('username'))
    first_name = unquote(request.json.get('first_name'))
    last_name = unquote(request.json.get('last_name'))
    email = unquote(request.json.get('email'))
    password = unquote(request.json.get('password'))
    birth_date = unquote(request.json.get('birth_date'))
    try:
        userService.updateUser(current_user,user_name, first_name, last_name, email, password, birth_date)
        return responseFormat({"user_name":user_name, "password":password}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400

@user_bp.route('/users/likes/artists/<artist_name>', methods=['POST'])
@jwt_required()
def likeArtist(artist_name):
    try:
        current_user = get_jwt_identity()
        userService.addArtistTolikes(current_user, unquote(artist_name))
        return jsonify({"message": "Artist liked"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400


@user_bp.route('/users/likes/artists', methods=['GET'])
@jwt_required()
def likedArtists():
    try:
        current_user = get_jwt_identity()
        artists = userService.getLikedArtists(current_user)
        return jsonify({"artists":artists}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400


@user_bp.route('/users/likes/artists/<artist_name>', methods=['DELETE'])
@jwt_required()
def unlikeArtist(artist_name):
    try:
        current_user = get_jwt_identity()
        userService.unlikeArtist(current_user, unquote(artist_name))
        return jsonify({"message": "Artist unliked"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400


@user_bp.route('/users/likes/playlists', methods=['GET'])
@jwt_required()
def likePlaylists():
    try:
        current_user = get_jwt_identity()
        playlists = userService.getLikedPlaylists(current_user)
        return jsonify({"playlists":playlists}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400

@user_bp.route('/users/likes/playlists/<playlist_name>', methods=['DELETE'])
@jwt_required()
def unlikePlaylists(playlist_name):
    try:
        current_user = get_jwt_identity()
        userService.unlikePlaylist(current_user, unquote(playlist_name))
        return jsonify({"message": "Playlist unliked"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400

@user_bp.route('/users/likes/playlists/<playlist_name>', methods=['POST'])
@jwt_required()
def likeAPlaylist(playlist_name):
    try:
        current_user = get_jwt_identity()
        userService.likePlaylist(current_user, unquote(playlist_name))
        return jsonify({"message": "Playlist liked"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400