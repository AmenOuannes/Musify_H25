from collections import OrderedDict


class Artist:
    def __init__(self):
        self.init = None

    def fromRequest(self, artist_name, genre, profile_url, image, followers):
        self.artist_name = artist_name
        self.genre = genre
        self.profile_url = profile_url
        self.followers = followers
        self.celebrity = False
        self.image=image
        return self

    def fromArtistSQL(self, artistSQL):
        self.artist_id = artistSQL.artist_id
        self.artist_name = artistSQL.artist_name
        self.genre = artistSQL.genre
        self.profile_url = artistSQL.profile_url
        self.celebrity = artistSQL.celebrity
        self.followers = artistSQL.followers
        self.image = artistSQL.image
        return self

    def to_dict(self):
        return OrderedDict([
            ("artist_name", self.artist_name),
            ("genre", self.genre),
            ("profile_url", self.profile_url),
            ("followers", self.followers),
            ("celebrity", self.celebrity),
            ("image", self.image)
        ])