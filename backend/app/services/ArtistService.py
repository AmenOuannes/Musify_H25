from werkzeug.exceptions import NotFound

from backend.app.infrastructure.ArtistRepository import ArtistRepository
from backend.app.domain.Artist import Artist


class ArtistService:
    def __init__(self):
        self.artistRepository = ArtistRepository()

    def addArtist(self, artist_name, genre, profile_url):
        try:
            artist = Artist(artist_name, genre, profile_url)
            self.artistRepository.addArtist(artist)
        except Exception as e:
            raise e

    def getArtist(self, artist_name):
        artist = self.artistRepository.getArtistByName(artist_name)
        if artist:
            return artist.to_dict()
        else:
            raise NotFound("Artist not found")

    def getArtists(self, limit=-1):
        return [artist.to_dict() for artist in self.artistRepository.getAllArtists(limit)]