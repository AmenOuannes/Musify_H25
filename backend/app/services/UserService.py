from backend.app.infrastructure.UserRepository import UserRepository
from backend.app.domain.User import User

class UserService:
    def __init__(self):
        self.repository = UserRepository()

    def getUsers(self, limit):
        return [user.to_dict() for user in self.repository.getAllUsers(limit)]

    def createUser(self, username, first_name, last_name, email, password, birth_date):
        try:
            user = User().fromRequest(username, first_name, last_name, email, password, birth_date)
            self.repository.addUser(user)
        except (Exception) as e:
            raise e

    def login(self, username, password):
        user = self.repository.getUser(username)
        if not user:
            raise Exception('User not found')
        if user.password == password:
            return True
        else:
            raise Exception('Wrong password')

    def retrieveUser(self, username):
        user = self.repository.getUser(username)
        if not user:
            raise Exception('User not found')
        return user.to_dict()

    def updateUser(self,current_username, user_name, first_name, last_name, email, password, birth_date):
        self.repository.updateUser(current_username,user_name, first_name, last_name, email, password, birth_date)

    def getLikedArtists(self, current_user, research):
        try:
            artists = self.repository.getLikedArtists(current_user, research)
            return [artist.to_dict() for artist in artists]
        except (Exception) as e:
            raise e

    def addArtistTolikes(self, current_user, artist_name):
        try:
            self.repository.addLikedArtist(current_user, artist_name)
        except (Exception) as e:
            raise e

    def unlikeArtist(self, current_user, artist_name):
        try:
            self.repository.unlikeArtist(current_user, artist_name)
        except (Exception) as e:
            raise e

    def getLikedPlaylists(self, current_user, research):
        try:
            playlists = self.repository.getLikedPlaylists(current_user, research)
            return [playlist.to_dict() for playlist in playlists]
        except (Exception) as e:
            raise e

    def unlikePlaylist(self, current_user, playlist_name):
        try:
            self.repository.unlikePlaylist(current_user, playlist_name)
        except (Exception) as e:
            raise e

    def likePlaylist(self, current_user, playlist_name):
        try:
            self.repository.likePlaylist(current_user, playlist_name)
        except (Exception) as e:
            raise e

