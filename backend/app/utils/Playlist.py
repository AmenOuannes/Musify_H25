from collections import OrderedDict


class Playlist:
    def __init__(self, playlist_name, owner, private):
        self.playlist_name = playlist_name
        self.owner = owner
        self.private = private

    def to_dict(self):
        return OrderedDict([
            ("playlist_name", self.playlist_name),
            ("owner", self.owner),
            ("private", self.private),
        ])