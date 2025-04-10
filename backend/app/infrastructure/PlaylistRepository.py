from backend.__init__ import db
from backend.app.domain.Playlist import Playlist
from backend.app.domain.Song import Song
from backend.app.infrastructure.Queries.SongQueries import get_singer_query, get_song_by_name_query
from backend.app.infrastructure.SQL.PlaylistSQL import PlaylistSQL
from backend.app.infrastructure.Queries.PlaylistQueries import *
from backend.app.infrastructure.SongRepository import SongRepository
from backend.app.infrastructure.SQL.songSQL import SongSQL

class PlaylistRepository:
    def __init__(self):
        self.playlists = []

    def getPlaylists(self, limit, research, owner, private):
        self.playlists = []
        query = get_all_playlists_query(limit, research, owner, private)
        result = db.session.execute(query, {
            'limit': limit,
            'research': f'%{research.lower()}%' if research else None,
            'owner': owner.lower() if owner else None,
            'private': private if private else 1,
        })

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
        query = get_playlist_by_name_query()
        result = db.session.execute(query, {'playlist_name': playlist_name}).fetchone()
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
        query = insert_playlist_query()
        db.session.execute(query, {
            'playlist_name': playlist_name,
            'owner': current_user,
            'private': private
        })
        db.session.commit()

    def deletePlaylist(self, playlist_name):
        query = delete_playlist_query()
        db.session.execute(query, {'playlist_name': playlist_name})
        db.session.commit()

    def getSongFromPlaylist(self, playlist_name, song_name):
        # Validate playlist exists
        result = db.session.execute(get_playlist_by_name_query(), {'playlist_name': playlist_name}).fetchone()
        if not result:
            raise Exception(f"No playlist found with name '{playlist_name}'")

        # Check if song exists in playlist
        count_result = db.session.execute(get_song_count_from_playlist_query(), {
            'playlist_name': playlist_name,
            'song_name': song_name
        }).fetchone()
        count = count_result[0] if count_result else 0
        if count == 0:
            raise Exception(f"No song found with name '{song_name}' in playlist '{playlist_name}'")

        return SongRepository().getSong(song_name)

    def getAllSongsFromPlaylist(self, playlist_name, owner):
        result = db.session.execute(get_playlist_by_name_query(), {'playlist_name': playlist_name}).fetchone()
        if not result:
            raise Exception(f"No playlist found with name '{playlist_name}'")

        result = db.session.execute(get_songs_from_playlist_query(), {
            'playlist_name': playlist_name,
            'owner': owner
        })

        self.songs = []
        for row in result:
            row_data = row._mapping
            sing_result = db.session.execute(get_singer_query(), {'name': row_data["song_name"]}).fetchone()
            singer = sing_result._mapping["artist_name"] if sing_result else "Unknown"

            songSQL = SongSQL(
                song_id=row_data["song_id"],
                song_name=row_data["song_name"],
                genre=row_data["genre"],
                artist_name=singer,
                release_date=row_data["release_date"],
                url=row_data["url"]
            )
            self.songs.append(Song().fromSQL(songSQL))

        return self.songs

    def addSongToPlaylist(self, playlist_name, song_name):
        playlist_result = db.session.execute(get_playlist_by_name_query(), {'playlist_name': playlist_name}).fetchone()
        if not playlist_result:
            raise Exception(f"No playlist found with name '{playlist_name}'")
        playlist_id = playlist_result._mapping["playlist_id"]

        song_result = db.session.execute(get_song_by_name_query(), {'name': song_name}).fetchone()
        if not song_result:
            raise Exception(f"No song found with name '{song_name}'")
        song_id = song_result._mapping["song_id"]

        count_result = db.session.execute(get_song_count_from_playlist_query(), {
            'playlist_name': playlist_name,
            'song_name': song_name
        }).fetchone()
        count = count_result[0] if count_result else 0
        if count > 0:
            raise Exception(f"Song '{song_name}' is already in the playlist '{playlist_name}'")

        db.session.execute(insert_song_into_playlist_query(), {
            'playlist_id': playlist_id,
            'song_id': song_id
        })
        db.session.commit()

    def deleteSongToPlaylist(self, playlist_name, song_name):
        playlist_result = db.session.execute(get_playlist_by_name_query(), {'playlist_name': playlist_name}).fetchone()
        if not playlist_result:
            raise Exception(f"No playlist found with name '{playlist_name}'")
        playlist_id = playlist_result._mapping["playlist_id"]

        song_result = db.session.execute(get_song_by_name_query(), {'name': song_name}).fetchone()
        if not song_result:
            raise Exception(f"No song found with name '{song_name}'")
        song_id = song_result._mapping["song_id"]

        count_result = db.session.execute(get_song_count_from_playlist_query(), {
            'playlist_name': playlist_name,
            'song_name': song_name
        }).fetchone()
        count = count_result[0] if count_result else 0
        if count == 0:
            raise Exception(f"Song '{song_name}' is not in the playlist '{playlist_name}'")

        db.session.execute(delete_song_from_playlist_query(), {
            'playlist_id': playlist_id,
            'song_id': song_id
        })
        db.session.commit()
