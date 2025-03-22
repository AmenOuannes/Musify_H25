class Repository:
    def __init__(self):
        self.users = []
        self.songs = []
        self.playlists = []
        self.albums = []

    def addUser(self, user):
        self.users.append(user)