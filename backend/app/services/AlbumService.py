from datetime import datetime

from werkzeug.exceptions import NotFound

from backend.app.domain.Album import Album
from backend.app.infrastructure.AlbumRepository import AlbumRepository
from backend.app.infrastructure.ArtistRepository import ArtistRepository
from backend.app.services.SongService import artist_repository

artist_repository = ArtistRepository()

class AlbumService:
    def __init__(self):
        self.album_repository = AlbumRepository()

    def getAlbums(self, limit, research):
        return [album.to_dict() for album in self.album_repository.getAlbums(limit, research)]

    def getAlbum(self, album_name):
        album = self.album_repository.get_album(album_name)
        if album:
           return album.to_dict()
        else:
            raise Exception(f"album not found:{album_name}")

    def createAlbum(self, album_name, genre, artist_name, release_date, image):
        try:
            artist = artist_repository.getArtistByName(artist_name)
            date = datetime.strptime(release_date, "%Y-%m-%d")
            if artist is  not None:
                self.album_repository.addAlbum(Album().fromRequest(album_name, genre, release_date, image, artist_name), artist)
            else:
                raise Exception("Artist not found")
        except Exception as e:
            raise e

    def getSongsFromAlbum(self, album_name):
        songs = self.album_repository.get_album_songs(album_name)
        return [song.to_dict() for song in songs] if songs else []

    def addSongToAlbum(self, album_name, song_name):
        self.album_repository.addSongToAlbum(album_name, song_name)

    def deleteSongFromAlbum(self, album_name, song_name):
        self.album_repository.deleteSongFromAlbum(album_name, song_name)