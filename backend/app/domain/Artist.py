from collections import OrderedDict


class Artist:
    def __init__(self, artist_name, genre, profile_url):
        self.artist_name = artist_name
        self.genre = genre
        self.profile_url = profile_url
        self.followers = 0
        self.celebrity = False

    def to_dict(self):
        return OrderedDict([
            ("artist_name", self.artist_name),
            ("genre", self.genre),
            ("profile_url", self.profile_url),
            ("followers", self.followers),
            ("celebrity", self.celebrity),
        ])