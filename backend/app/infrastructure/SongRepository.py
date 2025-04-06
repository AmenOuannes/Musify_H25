from sqlalchemy import text
from backend.__init__ import db

from backend.app.domain.Song import Song
from backend.app.infrastructure.Queries import get_all_songs_query, get_song_by_name_query, insert_song_query, \
    insert_sings, get_singer_query
from backend.app.infrastructure.songSQL import SongSQL


class SongRepository:
    def __init__(self):
        self.songs = []

    def addSong(self, song, artist):
        song_exists = get_song_by_name_query(song.song_name)
        result = db.session.execute(text(song_exists))
        count = result.scalar() or 0
        print("Song inserted")

        if count > 0:
            raise Exception("Song already exists")
        else:
            song_query = insert_song_query(
                song.song_name,
                song.genre,
                song.release_date,
                song.url
            )

            db.session.execute(text(song_query))
            db.session.commit()

            song_id = db.session.execute(text(get_song_by_name_query(song.song_name))).fetchone()._mapping["song_id"]

            sings_query = insert_sings(song_id, artist.artist_id)
            db.session.execute(text(sings_query))
            db.session.commit()


    def getSong(self, song_name):
        query = get_song_by_name_query(song_name)
        singer_query = get_singer_query(song_name)
        result = db.session.execute(text(query))
        row = result.fetchone()
        singer = db.session.execute(text(singer_query)).fetchone()
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
        query = get_all_songs_query(limit,research)
        result = db.session.execute(text(query))
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

