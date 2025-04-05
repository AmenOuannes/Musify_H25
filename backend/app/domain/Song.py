from collections import OrderedDict


class Song:
    def __init__(self,song_name, genre, artist, release_date, url):
        self.song_name = song_name
        self.genre = genre
        self.artist = artist
        self.release_date = release_date
        self.url = url

    def to_dict(self):
        return OrderedDict([
            ("song_name", self.song_name),
            ("genre", self.genre),
            ("artist", self.artist),
            ("release_date", self.release_date),
            ("url", self.url),
        ])