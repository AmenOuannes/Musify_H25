from backend.app.utils.Playlist import Playlist


class PlaylistRepository():
    def __init__(self):
        self.playlists = []
        self.playlists.append(Playlist("my_hits", "kiko", True))

    def getPlaylists(self, limit):
        if limit == -1:
            return self.playlists
        else:
            return self.playlists[:limit]

    def getPlaylist(self, playlist_name):
        playlist = next((u for u in self.playlists if u.playlist_name == playlist_name), None)
        if playlist is None:
            raise Exception("Playlist not found")
        return playlist.to_dict()