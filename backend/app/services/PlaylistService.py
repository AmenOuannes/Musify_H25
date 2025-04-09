from os import add_dll_directory

from backend.app.infrastructure.PlaylistRepository import PlaylistRepository


class PlaylistService:
    def __init__(self):
        self.playlistRepository = PlaylistRepository()

    def getPlaylists(self, limit=-1, research="", owner=""):
        return [playlist.to_dict() for playlist in self.playlistRepository.getPlaylists(limit,research,owner)]

    def getPlaylist(self, playlist_name):
        try:
            return self.playlistRepository.getPlaylist(playlist_name).to_dict()
        except Exception as e:
            raise e

    def createPlaylist(self, playlist_name, current_user, private):

        try:
            playlist = self.playlistRepository.getPlaylist(playlist_name)
            if playlist:
                raise Exception('Duplicate playlist')
        except:
            self.playlistRepository.createPlaylist(playlist_name, current_user, private)

    def deletePlaylist(self, playlist_name):
        try:
            self.playlistRepository.deletePlaylist(playlist_name)
        except Exception as e:
            raise e

    def getSongFromPlaylist(self, playlist_name, song_name):
        try:
            song = self.playlistRepository.getSongFromPlaylist(playlist_name, song_name)
            return song.to_dict()
        except Exception as e:
            raise e

    def getAllSongsFromPlaylist(self, playlist_name, owner):
        try:
            songs = self.playlistRepository.getAllSongsFromPlaylist(playlist_name, owner)
            return [song.to_dict() for song in songs]
        except Exception as e:
            raise e

    def addSongToPlaylist(self, playlist_name, song_name):
        try:
            print(playlist_name, song_name)
            self.playlistRepository.addSongToPlaylist(playlist_name, song_name)

        except Exception as e:
            print("exception addSongToPlaylist")
            raise e

    def deleteSongFromPlaylist(self, playlist_name, song_name):
        try:
            self.playlistRepository.deleteSongToPlaylist(playlist_name, song_name)
        except Exception as e:
            raise e



