from backend.app.infrastructure.repositories.PlaylistRepository import PlaylistRepository


class PlaylistService:
    def __init__(self):
        self.playlistRepository = PlaylistRepository()

    def get_playlists(self, private, limit=-1, research="", owner=""):
        return [playlist.to_dict() for playlist in self.playlistRepository.get_playlists(limit, research, owner, private)]

    def get_playlist(self, playlist_name):
        try:
            return self.playlistRepository.get_playlist(playlist_name).to_dict()
        except Exception as e:
            raise e

    def create_playlist(self, playlist_name, current_user, private):

        try:
            self.playlistRepository.create_playlist(
                playlist_name, current_user, private)
        except Exception as e:
            raise e

    def delete_playlist(self, playlist_name):
        try:
            self.playlistRepository.deletePlaylist(playlist_name)
        except Exception as e:
            raise e

    def get_song_from_playlist(self, playlist_name, song_name):
        try:
            song = self.playlistRepository.getSongFromPlaylist(
                playlist_name, song_name)
            return song.to_dict()
        except Exception as e:
            raise e

    def get_all_songs_from_playlist(self, playlist_name, owner):
        try:
            print("service",playlist_name, owner)
            songs = self.playlistRepository.get_all_songs_from_playlist(
                playlist_name, owner)
            return [song.to_dict() for song in songs]
        except Exception as e:
            raise e

    def add_song_to_playlist(self, playlist_name, song_name):
        try:
            print(playlist_name, song_name)
            self.playlistRepository.add_song_to_playlist(
                playlist_name, song_name)

        except Exception as e:
            print("exception addSongToPlaylist")
            raise e

    def delete_song_from_playlist(self, playlist_name, song_name):
        try:
            self.playlistRepository.deleteSongToPlaylist(
                playlist_name, song_name)
        except Exception as e:
            raise e
