from collections import OrderedDict


class Playlist:

    def __init__(self):
        self.init = None

    def fromRequest(self, playlist_name, owner):
        self.playlist_name = playlist_name
        self.owner = owner
        return self

    def fromSQL(self, playlistSQL):
        self.playlist_name = playlistSQL.playlist_name
        self.owner = playlistSQL.owner
        self.private = playlistSQL.private
        self.playlist_id = playlistSQL.playlist_id
        return self

    def to_dict(self):
        return OrderedDict([
            ("playlist_name", self.playlist_name),
            ("owner", self.owner),
            ("private", self.private),
        ])