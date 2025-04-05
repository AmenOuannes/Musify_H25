from backend.app.infrastructure.PlaylistRepository import PlaylistRepository


class PlaylistService:
    def __init__(self):
        self.playlistRepository = PlaylistRepository()

    def getPlaylists(self, limit=-1):
        return [playlist.to_dict() for playlist in self.playlistRepository.getPlaylists(limit)]

    def getPlaylist(self, playlist_name):
        try:
            self.playlistRepository.getPlaylist(playlist_name)
            return playlist_name
        except Exception as e:
            raise e

