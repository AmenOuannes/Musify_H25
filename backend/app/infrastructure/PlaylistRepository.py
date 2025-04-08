from sqlalchemy import text

from backend.__init__ import db
from backend.app.domain.Playlist import Playlist
from backend.app.domain.Song import Song
from backend.app.infrastructure.PlaylistSQL import PlaylistSQL
from backend.app.infrastructure.Queries import get_playlist_by_name_query, get_all_playlists_query, \
    insert_playlist_query, delete_playlist_query, get_song_count_from_playlist_query, get_songs_from_playlist_query, \
    get_singer_query, get_song_by_name_query, insert_song_into_playlist_query, delete_song_from_playlist_query
from backend.app.infrastructure.SongRepository import SongRepository
from backend.app.infrastructure.songSQL import SongSQL

class PlaylistRepository():
    def __init__(self):
        self.playlists = []

    def getPlaylists(self, limit, research, owner):
        self.playlists = []
        query = get_all_playlists_query(limit, research, owner)
        result = db.session.execute(text(query))

        for row in result:
            row_data = row._mapping

            playlistSQL = PlaylistSQL(
                playlist_id=row_data["playlist_id"],
                playlist_name=row_data["playlist_name"],
                owner=row_data["owner"],
                private=row_data["private"]
            )

            self.playlists.append(Playlist().fromSQL(playlistSQL))

        return self.playlists

    def getPlaylist(self, playlist_name):
        query = get_playlist_by_name_query(playlist_name)
        result = db.session.execute(text(query)).fetchone()
        if not result:
            raise Exception(f"No playlist found with name '{playlist_name}'")

        row_data = result._mapping

        playlistSQL = PlaylistSQL(
            playlist_id=row_data["playlist_id"],
            playlist_name=row_data["playlist_name"],
            owner=row_data["owner"],
            private=row_data["private"]
        )

        return Playlist().fromSQL(playlistSQL)

    def createPlaylist(self, playlist_name, current_user, private):
        query = insert_playlist_query(playlist_name, current_user, private)
        db.session.execute(text(query))
        db.session.commit()

    def deletePlaylist(self, playlist_name):
        query = delete_playlist_query(playlist_name)
        db.session.execute(text(query))
        db.session.commit()

    def getSongFromPlaylist(self, playlist_name, song_name):
        query = get_playlist_by_name_query(playlist_name)
        result = db.session.execute(text(query)).fetchone()
        if not result:
            raise Exception(f"No playlist found with name '{playlist_name}'")

        song_query = get_song_count_from_playlist_query(playlist_name, song_name)
        count_result  = db.session.execute(text(song_query)).fetchone()
        count = count_result[0] if count_result else 0
        if count==0:
            raise Exception(f"No song found with name '{song_name}'")

        return SongRepository().getSong(song_name)

    def getAllSongsFromPlaylist(self, playlist_name, owner):
        query = get_playlist_by_name_query(playlist_name)
        result = db.session.execute(text(query)).fetchone()
        if not result:
            raise Exception(f"No playlist found with name '{playlist_name}'")

        songs_query = get_songs_from_playlist_query(playlist_name, owner)
        result = db.session.execute(text(songs_query))
        self.songs = []
        for row in result:
            row_data = row._mapping
            sing_query = get_singer_query(row_data["song_name"])
            singer = db.session.execute(text(sing_query)).fetchone()
            songSQL = SongSQL(
                song_id=row_data["song_id"],
                song_name=row_data["song_name"],
                genre=row_data["genre"],
                artist_name=singer._mapping["artist_name"],
                release_date=row_data["release_date"],
                url=row_data["url"]
            )
            self.songs.append(Song().fromSQL(songSQL))

        return self.songs

    def addSongToPlaylist(self, playlist_name, song_name):
        # 1. Get playlist by name
        playlist_result = db.session.execute(text(get_playlist_by_name_query(playlist_name))).fetchone()
        if not playlist_result:
            raise Exception(f"No playlist found with name '{playlist_name}'")

        playlist_id = playlist_result._mapping["playlist_id"]

        # 2. Get song by name
        song_result = db.session.execute(text(get_song_by_name_query(song_name))).fetchone()
        if not song_result:
            raise Exception(f"No song found with name '{song_name}'")


        song_id = song_result._mapping["song_id"]

        # 3. Check if song is already in playlist
        check_query = get_song_count_from_playlist_query(playlist_name, song_name)
        count_result = db.session.execute(text(check_query)).fetchone()
        count = count_result[0] if count_result else 0
        if count > 0:
            raise Exception(f"Song '{song_name}' is already in the playlist '{playlist_name}'")

        print("Adding song to playlist")
        # 4. Insert song into playlist
        insert_query = insert_song_into_playlist_query(playlist_id, song_id)
        db.session.execute(text(insert_query))
        db.session.commit()

    def deleteSongToPlaylist(self, playlist_name, song_name):
        # 1. Get playlist by name
        playlist_result = db.session.execute(text(get_playlist_by_name_query(playlist_name))).fetchone()
        if not playlist_result:
            raise Exception(f"No playlist found with name '{playlist_name}'")

        playlist_id = playlist_result._mapping["playlist_id"]

        # 2. Get song by name
        song_result = db.session.execute(text(get_song_by_name_query(song_name))).fetchone()
        if not song_result:
            raise Exception(f"No song found with name '{song_name}'")

        song_id = song_result._mapping["song_id"]

        # 3. Check if song is actually in the playlist
        check_query = get_song_count_from_playlist_query(playlist_name, song_name)
        count_result = db.session.execute(text(check_query)).fetchone()
        count = count_result[0] if count_result else 0

        if count == 0:
            raise Exception(f"Song '{song_name}' is not in the playlist '{playlist_name}'")

        # 4. Delete the song from the playlist
        delete_query = delete_song_from_playlist_query(playlist_id, song_id)
        db.session.execute(text(delete_query))
        db.session.commit()




