from backend.__init__ import db

from backend.app.domain.Song import Song
from backend.app.infrastructure.Queries.SongQueries import *
from backend.app.infrastructure.SQL.songSQL import SongSQL


class SongRepository:
    def __init__(self):
        self.songs = []

    def addSong(self, song, artist):
        song_exists = get_song_by_name_query()
        result = db.session.execute(song_exists, {"name": song.song_name})
        row = result.fetchone()

        if row:
            raise Exception("Song already exists")
        else:
            song_query = insert_song_query()
            db.session.execute(song_query, {
                "name": song.song_name,
                "genre": song.genre,
                "date": song.release_date,
                "url": song.url,
                "artist_id": artist.artist_id,
            })
            db.session.commit()
            song_id = db.session.execute(get_song_by_name_query(
            ), {"name": song.song_name}).fetchone()._mapping["song_id"]
            sings_query = insert_sings()
            db.session.execute(sings_query, {
                "song_id": song_id,
                "artist_id": artist.artist_id
            })
            db.session.commit()

    def getSong(self, song_name):
        query = get_song_by_name_query()
        singer_query = get_singer_query()

        result = db.session.execute(query, {"name": song_name})
        row = result.fetchone()
        singer = db.session.execute(
            singer_query, {"name": song_name}).fetchone()

        if row:
            row_data = row._mapping

            songSQL = SongSQL(
                song_id=row_data["song_id"],
                song_name=row_data["song_name"],
                genre=row_data["genre"],
                artist_name=singer._mapping["artist_name"],
                release_date=row_data["release_date"],
                url=row_data["url"]
            )

            return Song().fromSQL(songSQL)
        else:
            return None

    def getAllSongs(self, limit, research):
        query = get_all_songs_query(limit, research)
        params = {}
        if research:
            params["research"] = f"{research.lower()}%"
        if int(limit) != -1:
            params["limit"] = int(limit)

        result = db.session.execute(query, params)
        self.songs = []
        for row in result:
            row_data = row._mapping
            sing_query = get_singer_query()
            singer = db.session.execute(
                sing_query, {"name": row_data["song_name"]}).fetchone()
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
