from werkzeug.exceptions import NotFound
from backend.app.infrastructure.ArtistRepository import ArtistRepository
from backend.app.infrastructure.SongRepository import SongRepository
from backend.app.utils.Song import Song
artist_repository = ArtistRepository()

class SongService:
    def __init__(self):
        self.songRepository = SongRepository()


    def createSong(self, song_name, artist_name, genre, release_date, url):
        try:
            artist = artist_repository.getArtistByName(artist_name)
            if artist is  not None:
                song = Song(song_name, genre, artist_name, release_date, url)
                self.songRepository.addSong(song)
        except Exception as e:
            raise e


    def getSong(self, song_name):
        song = self.songRepository.getSong(song_name)
        if song:
           return song.to_dict()
        else:
            raise NotFound(song_name)

    def getAllSongs(self, limit=-1):
        return [song.to_dict() for song in self.songRepository.getAllSongs(limit)]


