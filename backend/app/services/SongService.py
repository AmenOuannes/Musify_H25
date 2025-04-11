from datetime import datetime

from werkzeug.exceptions import NotFound
from backend.app.infrastructure.repositories.ArtistRepository import ArtistRepository
from backend.app.infrastructure.repositories.SongRepository import SongRepository
from backend.app.domain.Song import Song
from backend.app.services.ArtistService import ArtistService

artist_repository = ArtistRepository()
artist_service = ArtistService()


class SongService:
    def __init__(self):
        self.songRepository = SongRepository()

    def create_song(self, song_name, genre, artist_name, release_date, url):
        try:
            artist = artist_repository.getArtistByName(artist_name)
            date = datetime.strptime(release_date, "%Y-%m-%d")
            if artist is not None:
                self.songRepository.addSong(Song().fromRequest(
                    song_name, genre, artist_name, release_date, url), artist)
            else:
                raise NotFound("Artist not found")
        except Exception as e:
            raise e

    def get_song(self, song_name):
        song = self.songRepository.getSong(song_name)
        if song:
            return song.to_dict()
        else:
            raise NotFound(song_name)

    def get_all_songs(self, limit=-1, research=""):
        return [song.to_dict() for song in self.songRepository.getAllSongs(limit, research)]
