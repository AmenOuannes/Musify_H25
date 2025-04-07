from backend.app.domain.Artist import Artist
from backend.app.domain.Playlist import Playlist
from backend.app.domain.User import User
from backend.__init__ import db
from sqlalchemy import text

from backend.app.infrastructure.ArtistSQL import ArtistSQL
from backend.app.infrastructure.PlaylistSQL import PlaylistSQL
from backend.app.infrastructure.Queries import get_all_users_query, find_similar_users_query, insert_user_query, \
    get_user_with_username_query, update_user_query, get_liked_artists_query, get_artist_by_name_query, \
    add_artist_to_likes, unlike_artist, get_liked_playlists_query, get_playlist_by_name_query, unlike_playlist_query, \
    like_playlist_query, get_liked_playlist_count_query
from backend.app.infrastructure.UserSQL import UserSQL
from backend.app.routes.ArtistRoute import add_artist


class UserRepository:
    def __init__(self):
        self.users = []

    def addUser(self, user):
        user_exists = find_similar_users_query(user.username)
        count = db.session.execute(text(user_exists))
        if count.scalar()>0:
            raise Exception('User already exists')

        add_query = insert_user_query(user.username, user.last_name, user.first_name, user.email, user.password, user.birth_date)
        db.session.execute(text(add_query))
        db.session.commit()

    def getUser(self, username):
        self.users = []
        user_exists = find_similar_users_query(username)
        count = db.session.execute(text(user_exists))

        if count.scalar()>0:
            query = get_user_with_username_query(username)
            result_user = db.session.execute(text(query))
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

    def getAllUsers(self, limit):
        self.users = []
        query = get_all_users_query(limit)
        result = db.session.execute(text(query))

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

    def updateUser(self,current_username, user_name, first_name, last_name, email, password, birth_date):
        query = update_user_query(current_username,user_name, first_name, last_name, email, password, birth_date)
        db.session.execute(text(query))
        db.session.commit()

    def getLikedArtists(self, current_user):
        self.artists = []
        query = get_liked_artists_query(current_user)
        result = db.session.execute(text(query))
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

    def addLikedArtist(self, current_user, artist_name):
        artist_id_query = get_artist_by_name_query(artist_name)
        artist_id = db.session.execute(text(artist_id_query)).fetchone()._mapping["artist_id"]
        query = add_artist_to_likes(current_user, artist_id)
        db.session.execute(text(query))
        db.session.commit()

    def unlikeArtist(self, current_user, artist_name):
        artist_id_query = get_artist_by_name_query(artist_name)
        artist_id = db.session.execute(text(artist_id_query)).fetchone()._mapping["artist_id"]
        query = unlike_artist(current_user, artist_id)
        db.session.execute(text(query))
        db.session.commit()

    def getLikedPlaylists(self, current_user):
        self.playlists = []
        query = get_liked_playlists_query(current_user)
        result = db.session.execute(text(query))

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

    def unlikePlaylist(self, current_user, playlist_name):
        playlist_result = db.session.execute(text(get_playlist_by_name_query(playlist_name))).fetchone()
        if not playlist_result:
            raise Exception(f"No playlist found with name '{playlist_name}'")

        playlist_id = playlist_result._mapping["playlist_id"]

        # 2. Build and execute the unlike query
        query = unlike_playlist_query(current_user, playlist_id)
        db.session.execute(text(query))
        db.session.commit()

    def likePlaylist(self, current_user, playlist_name):
        playlist_result = db.session.execute(text(get_playlist_by_name_query(playlist_name))).fetchone()
        if not playlist_result:
            raise Exception(f"No playlist found with name '{playlist_name}'")

        playlist_id = playlist_result._mapping["playlist_id"]

        # 2. Check if playlist is already liked by the user
        check_query = get_liked_playlist_count_query(current_user, playlist_id)
        exists_result = db.session.execute(text(check_query)).fetchone()
        count = exists_result[0] if exists_result else 0
        if count > 0:
            raise Exception(f"Playlist '{playlist_name}' is already liked by '{current_user}'")

        # 3. Insert the like record into LikedPlaylists
        insert_query = like_playlist_query(current_user, playlist_id)
        db.session.execute(text(insert_query))
        db.session.commit()
