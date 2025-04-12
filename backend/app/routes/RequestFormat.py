from urllib.parse import unquote
from flask import request


def get_user_credentials():
    user_name = unquote(request.json.get('username'))
    first_name = unquote(request.json.get('first_name'))
    last_name = unquote(request.json.get('last_name'))
    email = unquote(request.json.get('email'))
    password = unquote(request.json.get('password'))
    birth_date = unquote(request.json.get('birth_date'))

    return user_name, first_name, last_name, email, password, birth_date


def get_song_credentials():
    song_name = unquote(request.json.get('song_name'))
    genre = unquote(request.json.get('genre'))
    artist = unquote(request.json.get('artist_name'))
    release_date = unquote(request.json.get('release_date'))
    url = unquote(request.json.get('url'))

    return song_name, genre, artist, release_date, url


def get_artist_credentials():
    artist_name = unquote(request.json.get('artist_name'))
    genre = unquote(request.json.get('genre'))
    profile_url = unquote(request.json.get('profile_url'))
    followers = request.json.get('followers') if 'followers' in request.json else 0
    image = unquote(request.json.get('image'))

    print(artist_name, genre, profile_url, followers, image)
    return artist_name, genre, profile_url, followers, image


def get_album_credentials():
    album_name = unquote(request.json.get('album_name'))
    genre = unquote(request.json.get('genre'))
    artist_name = unquote(request.json.get('artist_name'))
    release_date = unquote(request.json.get('release_date'))
    image = unquote(request.json.get('image'))

    return album_name, genre, artist_name, release_date, image


def get_limit_argument():
    return request.args.get('limit', type=int) if 'limit' in request.args else -1


def get_research_argument():
    return unquote(request.args.get('research')) if 'research' in request.args else ""


def get_owner_argument():
    return unquote(request.args.get('owner', type=str)) if 'owner' in request.args else ""


def get_private_argument():
    return request.args.get('private', type=int) if 'private' in request.args else 0
