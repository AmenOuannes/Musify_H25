from sqlalchemy import text

from backend.app.domain.Playlist import Playlist
from backend.app.infrastructure.PlaylistSQL import PlaylistSQL
from backend.app.infrastructure.Queries import get_playlist_by_name_query, get_all_playlists_query, \
    insert_playlist_query
from backend.__init__ import db


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
