from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from backend.app.routes.ResponseFormat import responseFormat
from backend.app.services.UserService import UserService


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
    user_name = request.json.get('username')
    first_name = request.json.get('first_name')
    last_name = request.json.get('last_name')
    email = request.json.get('email')
    password = request.json.get('password')
    birth_date = request.json.get('birth_date')

    try:
        userService.createUser(user_name, first_name, last_name, email, password, birth_date)
        return jsonify({"message": "User created"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400


@user_bp.route('/users/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

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
    user_name = request.json.get('username')
    first_name = request.json.get('first_name')
    last_name = request.json.get('last_name')
    email = request.json.get('email')
    password = request.json.get('password')
    birth_date = request.json.get('birth_date')
    try:
        userService.updateUser(current_user,user_name, first_name, last_name, email, password, birth_date)
        return responseFormat({"user_name":user_name, "password":password}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400


