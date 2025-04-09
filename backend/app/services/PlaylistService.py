from os import add_dll_directory

from backend.app.infrastructure.PlaylistRepository import PlaylistRepository


class PlaylistService:
    def __init__(self):
        self.playlistRepository = PlaylistRepository()

    def get_playlists(self, limit=-1, research="", owner="", private=0):
        return [playlist.to_dict() for playlist in self.playlistRepository.getPlaylists(limit,research,owner,private)]

    def get_playlist(self, playlist_name):
        try:
            return self.playlistRepository.getPlaylist(playlist_name).to_dict()
        except Exception as e:
            raise e

    def create_playlist(self, playlist_name, current_user, private):

        try:
            playlist = self.playlistRepository.getPlaylist(playlist_name)
            if playlist:
                raise Exception('Duplicate playlist')
        except:
            self.playlistRepository.createPlaylist(playlist_name, current_user, private)

    def delete_playlist(self, playlist_name):
        try:
            self.playlistRepository.deletePlaylist(playlist_name)
        except Exception as e:
            raise e

    def get_song_from_playlist(self, playlist_name, song_name):
        try:
            song = self.playlistRepository.getSongFromPlaylist(playlist_name, song_name)
            return song.to_dict()
        except Exception as e:
            raise e

    def get_all_songs_from_playlist(self, playlist_name, owner):
        try:
            songs = self.playlistRepository.getAllSongsFromPlaylist(playlist_name, owner)
            return [song.to_dict() for song in songs]
        except Exception as e:
            raise e

    def add_song_to_playlist(self, playlist_name, song_name):
        try:
            print(playlist_name, song_name)
            self.playlistRepository.addSongToPlaylist(playlist_name, song_name)

        except Exception as e:
            print("exception addSongToPlaylist")
            raise e

    def delete_song_from_playlist(self, playlist_name, song_name):
        try:
            self.playlistRepository.deleteSongToPlaylist(playlist_name, song_name)
        except Exception as e:
            raise e



