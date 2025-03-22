import json

from flask import Blueprint, jsonify, request, Response
from backend.app.services.UserService import UserService

user_bp = Blueprint('user_bp', __name__)
userService = UserService()
@user_bp.route('/users', methods=['GET'])
def users():
    all_users = userService.getUsers()
    return Response(
        json.dumps({"users": all_users}, sort_keys=False, indent=2),
        mimetype='application/json'
    ), 200

@user_bp.route('/users', methods=['POST'])
def signUp():
    user_name = request.json.get('username')
    first_name = request.json.get('first_name')
    last_name = request.json.get('last_name')
    email = request.json.get('email')
    password = request.json.get('password')

    userService.createUser(user_name, first_name, last_name, email, password)
    return jsonify({"message": "User created"}), 200

@user_bp.route('/users/<username>', methods=['GET'])
def signIn(username):
    password = request.json.get('password')
    try:
        user_json = userService.retriveUser(username, password)
        return jsonify(user_json), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400

