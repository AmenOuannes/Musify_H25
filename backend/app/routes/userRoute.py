from flask import Blueprint, jsonify
from backend.app.services.userService import userService

user_bp = Blueprint('user_bp', __name__)
user = userService()
@user_bp.route('/users', methods=['GET'])
def users():
    all_users = user.getUser()
    return jsonify({"users": all_users}), 200
