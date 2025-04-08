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
        # Vérifie si la chanson existe déjà
        exists_query = get_song_by_name_query()
        result = db.session.execute(exists_query, {"name": song.song_name})
        count = result.scalar() or 0

        if count > 0:
            raise Exception("Song already exists")

        # Insère la chanson avec paramètres sécurisés
        insert_query = insert_song_query()
        db.session.execute(insert_query, {
            "name": song.song_name,
            "genre": song.genre,
            "date": song.release_date,
            "url": song.url
        })
        db.session.commit()

        # Récupère son ID
        song_id = db.session.execute(get_song_by_name_query(), {"name": song.song_name}).fetchone()._mapping["song_id"]

        # Ajoute dans Sings
        sings_query = insert_sings(song_id, artist.artist_id)
        db.session.execute(sings_query)
        db.session.commit()

    def getSong(self, song_name):
        query = get_song_by_name_query()
        singer_query = get_singer_query()

        result = db.session.execute(query, {"name": song_name}).fetchone()
        singer = db.session.execute(singer_query, {"name": song_name}).fetchone()

        if result:
            row_data = result._mapping
            songSQL = SongSQL(
                song_id=row_data["song_id"],
                song_name=row_data["song_name"],
                genre=row_data["genre"],
                artist_name=singer._mapping["artist_name"] if singer else "Unknown",
                release_date=row_data["release_date"],
                url=row_data["url"]
            )
            return Song().fromSQL(songSQL)
        else:
            return None

    def getAllSongs(self, limit, research):
        try:
            query = get_all_songs_query(limit, research)

            params = {}
            if research:
                params["research"] = f"{research}%"
            if int(limit) != -1:
                params["limit"] = int(limit)

            result = db.session.execute(query, params)

            self.songs = []
            for row in result:
                row_data = row._mapping

                # secure query for artist name
                artist_query = text("""
                    SELECT A.artist_name FROM Artists A
                    JOIN Sings R ON A.artist_id = R.artist_id
                    WHERE R.song_id = :song_id
                """)
                artist = db.session.execute(artist_query, {"song_id": row_data["song_id"]}).fetchone()

                songSQL = SongSQL(
                    song_id=row_data["song_id"],
                    song_name=row_data["song_name"],
                    genre=row_data["genre"],
                    artist_name=artist._mapping["artist_name"] if artist else "Unknown",
                    release_date=row_data["release_date"],
                    url=row_data["url"]
                )
                self.songs.append(Song().fromSQL(songSQL))

            return self.songs

        except Exception as e:
            print("Error in getAllSongs:", e)
            raise e


