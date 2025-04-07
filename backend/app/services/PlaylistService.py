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



