from sqlalchemy import text
from backend.__init__ import db

from backend.app.domain.Song import Song
from backend.app.infrastructure.Queries import get_all_songs_query, get_song_by_name_query, insert_song_query
from backend.app.infrastructure.songSQL import SongSQL


class SongRepository:
    def __init__(self):
        self.songs = []

    def addSong(self, song):
        song_exists = get_song_by_name_query(song.song_name)
        result = db.session.execute(text(song_exists))
        count = result.scalar() or 0
        print("Song inserted")

        if count > 0:
            raise Exception("Song already exists")
        else:
            query = insert_song_query(
                song.song_id,
                song.song_name,
                song.genre,
                song.release_date,
                song.url
            )

            db.session.execute(text(query))
            db.session.commit()

    def getSong(self, song_name):
        query = get_song_by_name_query(song_name)
        result = db.session.execute(text(query))
        row = result.fetchone()
        if row:
            row_data = row._mapping

            songSQL = SongSQL(
                song_id=row_data["song_id"],
                song_name=row_data["song_name"],
                genre=row_data["genre"],
                release_date=row_data["release_date"],
                url=row_data["url"]
            )

            return Song().fromSQL(songSQL)
        else:
            return None

    def getAllSongs(self, limit, research):
        query = get_all_songs_query(limit,research)
        result = db.session().execute(text(query))
        self.songs = []
        for row in result:
            row_data = row._mapping
            songSQL = SongSQL(
                song_id=row_data["song_id"],
                song_name=row_data["song_name"],
                genre=row_data["genre"],
                release_date=row_data["release_date"],
                url=row_data["url"]
            )
            self.songs.append(Song().fromSQL(songSQL))

        return self.songs

