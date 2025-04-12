from backend.app.domain.AiModel import recommend_entities
from backend.app.domain.User import User
from backend.app.infrastructure.repositories.ArtistRepository import ArtistRepository
from backend.app.infrastructure.repositories.UserRepository import UserRepository



class UserService:
    def __init__(self):
        self.repository = UserRepository()

    def getUsers(self, limit):
        return [user.to_dict() for user in self.repository.get_all_users(limit)]

    def createUser(self, username, first_name, last_name, email, password, birth_date):
        try:
            user = User().fromRequest(username, first_name,
                                      last_name, email, password, birth_date)
            self.repository.add_user(user)
        except (Exception) as e:
            raise e

    def login(self, username, password):
        user = self.repository.get_user(username)
        if not user:
            raise Exception('User not found')
        if user.password == password:
            return True
        else:
            raise Exception('Wrong password')

    def retrieveUser(self, username):
        user = self.repository.get_user(username)
        if not user:
            raise Exception('User not found')
        return user.to_dict()

    def update_user_info(self, current_username, user_name, first_name, last_name, email, password, birth_date):
        self.repository.update_user(
            current_username, user_name, first_name, last_name, email, password, birth_date)

    def get_liked_artists(self, current_user, research):
        try:
            artists = self.repository.get_liked_artists(current_user, research)
            return [artist.to_dict() for artist in artists]
        except (Exception) as e:
            raise e

    def like_artist(self, current_user, artist_name):
        try:
            self.repository.add_liked_artist(current_user, artist_name)
        except (Exception) as e:
            raise e

    def unlike_artist(self, current_user, artist_name):
        try:
            self.repository.unlike_artist(current_user, artist_name)
        except (Exception) as e:
            raise e

    def get_liked_playlists(self, current_user, research):
        try:
            playlists = self.repository.get_liked_playlists(
                current_user, research)
            return [playlist.to_dict() for playlist in playlists]
        except (Exception) as e:
            raise e

    def unlike_playlist(self, current_user, playlist_name):
        try:
            self.repository.unlike_playlist(current_user, playlist_name)
        except (Exception) as e:
            raise e

    def like_playlist(self, current_user, playlist_name):
        try:
            self.repository.like_playlist(current_user, playlist_name)
        except (Exception) as e:
            raise e

    def get_recommended_artists(self, current_user):
        try:
            liked_artists = self.repository.get_liked_artists(current_user, '')
            all_artists = ArtistRepository().get_all_artists(-1,"")
            liked_artists_ids = [artist.artist_id for artist in liked_artists]
            all_except_liked = [artist for artist in all_artists if artist.artist_id not in liked_artists_ids]
            recommended_artists = recommend_entities(liked_artists, all_except_liked)
            return [artist.to_dict() for artist in recommended_artists]
        except (Exception) as e:
            raise e
