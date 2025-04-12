from werkzeug.exceptions import NotFound

from backend.app.infrastructure.repositories.ArtistRepository import ArtistRepository
from backend.app.domain.Artist import Artist


class ArtistService:
    def __init__(self):
        self.artistRepository = ArtistRepository()

    def add_artist(self, artist_name, genre, profile_url, image, followers):
        try:
            self.artistRepository.addArtist(Artist().fromRequest(
                artist_name, genre, profile_url, image, followers))
        except Exception as e:
            raise e

    def get_artist(self, artist_name):
        artist = self.artistRepository.getArtistByName(artist_name)
        if artist:
            return artist.to_dict()
        else:
            raise NotFound("Artist not found")

    def get_artists(self, limit=-1, research=""):
        return [artist.to_dict() for artist in self.artistRepository.get_all_artists(limit, research)]
