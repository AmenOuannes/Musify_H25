from datetime import datetime

from backend.app.domain.Album import Album
from backend.app.infrastructure.repositories.AlbumRepository import AlbumRepository
from backend.app.infrastructure.repositories.ArtistRepository import ArtistRepository
from backend.app.services.SongService import artist_repository

artist_repository = ArtistRepository()

class AlbumService:
    def __init__(self):
        self.album_repository = AlbumRepository()

    def get_albums(self, limit, research):
        return [album.to_dict() for album in self.album_repository.getAlbums(limit, research)]

    def get_album(self, album_name):
        album = self.album_repository.get_album(album_name)
        if album:
           return album.to_dict()
        else:
            raise Exception(f"album not found:{album_name}")

    def create_album(self, album_name, genre, artist_name, release_date, image):
        try:
            artist = artist_repository.getArtistByName(artist_name)
            date = datetime.strptime(release_date, "%Y-%m-%d")
            if artist is  not None:
                self.album_repository.addAlbum(Album().fromRequest(album_name, genre, release_date, image, artist_name), artist)
            else:
                raise Exception("Artist not found")
        except Exception as e:
            raise e

    def get_songs_from_album(self, album_name):
        songs = self.album_repository.get_album_songs(album_name)
        return [song.to_dict() for song in songs] if songs else []

    def add_song_to_album(self, album_name, song_name):
        self.album_repository.addSongToAlbum(album_name, song_name)

    def delete_song_from_album(self, album_name, song_name):
        self.album_repository.deleteSongFromAlbum(album_name, song_name)