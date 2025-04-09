from collections import OrderedDict
import random


class Song:
    def __init__(self):
        self.init = None

    def fromRequest(self,song_name, genre, artist_name, release_date, url):
        self.song_name = song_name
        self.genre = genre
        self.artist_name = artist_name
        self.release_date = release_date
        self.url = url
        return self
    def fromSQL(self, songSQL):
        self.song_id = songSQL.song_id
        self.song_name = songSQL.song_name
        self.genre = songSQL.genre
        self.artist_name = songSQL.artist_name
        self.release_date = songSQL.release_date
        self.url = songSQL.url
        return self

    def to_dict(self):
        return OrderedDict([
            ("song_name", self.song_name),
            ("genre", self.genre),
            ("artist_name", self.artist_name),
            ("release_date", self.release_date.isoformat()),
            ("url", self.url),
        ])