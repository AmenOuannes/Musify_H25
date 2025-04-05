from backend.app.utils.Song import Song


class SongRepository:
    def __init__(self):
        self.songs = []
        self.songs.append(Song('darjin', 'rap', 'klay', '2020', 'ifjurfhru'))

    def addSong(self, song):
        if self.getSong(song.song_name) is None:
            self.songs.append(song)
        else:
            raise Exception('Already added')

    def getSong(self, song_name):
        return next((u for u in self.songs if u.song_name == song_name), None)

    def getAllSongs(self, limit):
        if limit == -1:
            return self.songs
        else:
            return self.songs[:limit]