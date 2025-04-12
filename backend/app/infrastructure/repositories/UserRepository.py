from sqlalchemy.exc import DBAPIError

from backend.app.domain.Artist import Artist
from backend.app.domain.Playlist import Playlist
from backend.app.domain.User import User
from backend.__init__ import db
from backend.app.domain.encryption import encrypt_password, KEY
from backend.app.infrastructure.Queries.ArtistQueries import get_artist_by_name_query
from backend.app.infrastructure.Queries.PlaylistQueries import get_liked_artists_query, get_playlist_by_name_query
from backend.app.infrastructure.Queries.UserQueries import *


from backend.app.infrastructure.SQL.ArtistSQL import ArtistSQL
from backend.app.infrastructure.SQL.PlaylistSQL import PlaylistSQL

from backend.app.infrastructure.SQL.UserSQL import UserSQL


class UserRepository:
    def __init__(self):
        self.users = []

    def add_user(self, user):
        query = user_exists_query()
        result = db.session.execute(query, {"username": user.username})
        row = result.fetchone()

        if row._mapping["exists_flag"]:
            raise Exception('User already exists')

        try:
            query = insert_user_query()
            db.session.execute(query, {
                "username": user.username,
                "last_name": user.last_name,
                "first_name": user.first_name,
                "email": user.email,
                "password_hash": user.password,
                "birth_date": user.birth_date
            })
            db.session.commit()
        except DBAPIError as e:
            db.session.rollback()
            # Extract and raise SQL trigger's custom error message
            if e.orig:
                raise Exception(f"Database error: {str(e.orig)}")
            else:
                raise Exception("An unknown database error occurred.")

    def get_user(self, username):
        self.users = []
        user_exists = find_similar_users_query()
        count = db.session.execute(user_exists, {"username": username})

        if count.scalar() > 0:
            query = get_user_with_username_query()
            result_user = db.session.execute(query, {"username": username})
            row = result_user.fetchone()
            row_data = row._mapping

            userSQL = UserSQL(
                username=row_data["username"],
                password_hash=row_data["password_hash"],
                email=row_data["email"],
                first_name=row_data["first_name"],
                last_name=row_data["last_name"],
                birth_date=row_data["birth_date"]
            )
            return User().fromUserSQL(userSQL)
        else:
            return None

    def get_all_users(self, limit):
        self.users = []
        query = get_all_users_query(limit)
        params = {} if limit == -1 else {"limit": limit}
        result = db.session.execute(query, params)

        for row in result:
            row_data = row._mapping
            userSQL = UserSQL(
                username=row_data["username"],
                password_hash=row_data["password_hash"],
                email=row_data["email"],
                first_name=row_data["first_name"],
                last_name=row_data["last_name"],
                birth_date=row_data["birth_date"]
            )
            self.users.append(User().fromUserSQL(userSQL))

        return self.users

    def update_user(self, current_username, user_name, first_name, last_name, email, password, birth_date):
        query = update_user_query()
        try:
            db.session.execute(query, {
                "current_username": current_username,
                "username": user_name,
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "password_hash": encrypt_password(password, KEY),
                "birth_date": birth_date
            })
            db.session.commit()
        except DBAPIError as e:
            db.session.rollback()
            if e.orig:
                raise Exception(f"Database error: {str(e.orig)}")
            else:
                raise Exception("An unknown database error occurred.")

    def get_liked_artists(self, current_user, research):
        self.artists = []
        query = get_liked_artists_query(research)
        result = db.session.execute(query, {
                                    "username": current_user, "research": f'%{research.lower()}%' if research else None})
        for row in result:
            row_data = row._mapping

            artistSQL = ArtistSQL(
                artist_id=row_data["artist_id"],
                artist_name=row_data["artist_name"],
                genre=row_data["genre"],
                followers=row_data["followers"],
                celebrity=row_data["celebrity"],
                profile_url=row_data["profile_url"],
                image=row_data["image"]
            )

            self.artists.append(Artist().fromArtistSQL(artistSQL))

        return self.artists

    def add_liked_artist(self, current_user, artist_name):
        query = get_artist_by_name_query()
        artist_id = db.session.execute(
            query, {"artist_name": artist_name}).fetchone()._mapping["artist_id"]
        insert_query = add_artist_to_likes()
        db.session.execute(insert_query, {
            "username": current_user,
            "artist_id": artist_id
        })
        db.session.commit()

    def unlike_artist(self, current_user, artist_name):
        query = get_artist_by_name_query()
        artist_id = db.session.execute(
            query, {"artist_name": artist_name}).fetchone()._mapping["artist_id"]
        unlike_query = unlike_artist()
        db.session.execute(unlike_query, {
            "username": current_user,
            "artist_id": artist_id
        })
        db.session.commit()

    def get_liked_playlists(self, current_user, research):
        self.playlists = []
        query = get_liked_playlists_query(research)
        result = db.session.execute(query, {"user_id": current_user,
                                            "research": f'%{research.lower()}%' if research else None})

        for row in result:
            row_data = row._mapping

            playlistSQL = PlaylistSQL(
                playlist_id=row_data["playlist_id"],
                playlist_name=row_data["playlist_name"],
                owner=row_data["owner"],
                private=row_data["private"]
            )

            self.playlists.append(Playlist().fromSQL(playlistSQL))

        return self.playlists

    def unlike_playlist(self, current_user, playlist_name):
        query = get_playlist_by_name_query()
        playlist_result = db.session.execute(
            query, {"playlist_name": playlist_name}).fetchone()
        if not playlist_result:
            raise Exception(f"No playlist found with name '{playlist_name}'")

        playlist_id = playlist_result._mapping["playlist_id"]

        unlike_query = unlike_playlist_query()
        db.session.execute(unlike_query, {
            "user_id": current_user,
            "playlist_id": playlist_id
        })
        db.session.commit()

    def like_playlist(self, current_user, playlist_name):
        query = get_playlist_by_name_query()
        playlist_result = db.session.execute(
            query, {"playlist_name": playlist_name}).fetchone()
        if not playlist_result:
            raise Exception(f"No playlist found with name '{playlist_name}'")

        playlist_id = playlist_result._mapping["playlist_id"]

        check_query = get_liked_playlist_count_query()
        exists_result = db.session.execute(check_query, {
            "user_id": current_user,
            "playlist_id": playlist_id
        }).fetchone()
        count = exists_result[0] if exists_result else 0
        if count > 0:
            raise Exception(
                f"Playlist '{playlist_name}' is already liked by '{current_user}'")

        insert_query = like_playlist_query()
        db.session.execute(insert_query, {
            "user_id": current_user,
            "playlist_id": playlist_id
        })
        db.session.commit()
