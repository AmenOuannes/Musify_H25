import os
from urllib.parse import unquote

from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

from backend.app.routes.RequestFormat import get_user_credentials, get_limit_argument, get_research_argument
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


# @user_bp.route('/users', methods=['POST'])
# def sign_up():
#     try:
#         user_name, first_name, last_name, email, password, birth_date = get_user_credentials()
#         userService.createUser(user_name, first_name,
#                                last_name, email, password, birth_date)
#         send_confirmation_email(email, first_name, last_name)
#         return jsonify({"message": "User created"}), 200
#     except Exception as e:
#         return jsonify({"message": str(e)}), 400


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
        research = get_research_argument()
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
        research = get_research_argument()
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

@user_bp.route('/users/likes/artists/recommended', methods=['GET'])
@jwt_required()
def recommend_artists():
    try:
        current_user = get_jwt_identity()
        print(current_user)
        artists = userService.get_recommended_artists(current_user)
        return jsonify({"artists": artists}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400


from itsdangerous import URLSafeTimedSerializer
from flask import url_for

serializer = URLSafeTimedSerializer("your-secret-key")  # keep secret in config or env

@user_bp.route('/users', methods=['POST'])
def sign_up():
    try:
        user_name, first_name, last_name, email, password, birth_date = get_user_credentials()

        # Generate confirmation token
        token = serializer.dumps({
            "user_name": user_name,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": password,
            "birth_date": birth_date
        }, salt='email-confirm')

        confirm_url = url_for('user_bp.confirm_email', token=token, _external=True)

        # Send email
        send_confirmation_email(email, first_name, confirm_url)

        return jsonify({"message": "Please check your email to confirm your account"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400

@user_bp.route('/confirm/<token>', methods=['GET'])
def confirm_email(token):
    try:
        data = serializer.loads(token, salt='email-confirm', max_age=3600)  # 1h limit

        # Save the user now that they confirmed
        userService.createUser(
            data['user_name'],
            data['first_name'],
            data['last_name'],
            data['email'],
            data['password'],
            data['birth_date']
        )
        return "<h2>✅ Your account has been confirmed! You can now log in.</h2>"

    except Exception as e:
        return f"<h2>❌ Invalid or expired token: {str(e)}</h2>"


import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_confirmation_email(receiver_email, first_name, confirm_url):
    sender_email = "amenouannes22@gmail.com"
    sender_password = os.getenv("EMAIL_PASSWORD")

    message = MIMEMultipart("alternative")
    message["Subject"] = "Confirm your Musify account"
    message["From"] = sender_email
    message["To"] = receiver_email

    html = f"""
    <html>
      <body>
        <p>Hi {first_name},<br><br>
           Click the button below to confirm your account:<br><br>
           <a href="{confirm_url}" style="padding: 10px 20px; background-color: #0f0; color: white; text-decoration: none; border-radius: 5px;">
               Confirm Account
           </a><br><br>
           If you didn’t request this, please ignore this email.
        </p>
      </body>
    </html>
    """

    message.attach(MIMEText(html, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message.as_string())


