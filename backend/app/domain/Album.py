from collections import OrderedDict


class Album:
    def __init__(self):
        self.a=""

    def fromRequest(self, album_name,genre, release_date,cover_image, artist_name):
        self.album_name = album_name
        self.genre = genre
        self.release_date = release_date
        self.cover_image = cover_image
        self.artist_name = artist_name
        return self

    def fromSQL(self, albumSQL):
        self.album_id = albumSQL.album_id
        self.album_name = albumSQL.album_name
        self.genre = albumSQL.genre
        self.release_date = albumSQL.release_date
        self.cover_image = albumSQL.cover_image
        self.artist_name = albumSQL.artist_name
        return self

    def to_dict(self):
        return OrderedDict([
            ("album_name", self.album_name),
            ("genre", self.genre),
            ("artist_name", self.artist_name),
            ("release_date", self.release_date.isoformat()),
            ("cover_image", self.cover_image),
        ])