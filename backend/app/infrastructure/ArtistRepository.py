
class ArtistRepository():
    def __init__(self):
        self.artists = []

    def addArtist(self, artist):
        if self.getArtistByName(artist.artist_name) is None:
            self.artists.append(artist)
        else:
            raise Exception("Artist already exists")

    def getAllArtists(self, limit):
        if limit == -1:
            return self.artists
        else:
            return self.artists[:limit]

    def getArtistByName(self, artist_name):
        return next((u for u in self.artists if u.artist_name == artist_name), None)

