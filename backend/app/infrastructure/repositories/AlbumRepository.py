from sqlalchemy import text
from backend.__init__ import db


from backend.app.domain.Album import Album
from backend.app.domain.Song import Song
from backend.app.infrastructure.Queries.SongQueries import get_song_by_name_query
from backend.app.infrastructure.SQL.AlbumSQL import AlbumSQL
from backend.app.infrastructure.Queries.AlbumQueries import *
from backend.app.infrastructure.SQL.songSQL import SongSQL


class AlbumRepository:
    def __init__(self):
        self.albums = []
        self.songs = []

    def getAlbums(self, limit, research):
        self.albums = []
        query = get_all_albums_query(limit, research)
        params = {}
        if research:
            params["research"] = f"{research.lower()}%"
        if int(limit) != -1:
            params["limit"] = int(limit)

        result = db.session.execute(query, params)

        for row in result:
            row_data = row._mapping

            owner_query = get_album_owner_query()
            owner_result = db.session.execute(owner_query, {"name": row_data["album_name"]}).fetchone()
            artist_name = owner_result._mapping["artist_name"] if owner_result else "Unknown"

            albumSQL = AlbumSQL(
                album_id=row_data["album_id"],
                album_name=row_data["album_name"],
                genre=row_data["genre"],
                release_date=row_data["release_date"],
                cover_image=row_data["cover_image"],
                artist_name=artist_name
            )

            self.albums.append(Album().fromSQL(albumSQL))

        return self.albums

    def get_album(self, album_name):
        query = get_album_by_name_query()
        result = db.session.execute(query, {"name": album_name}).fetchone()

        if result:
            row_data = result._mapping

            owner_query = get_album_owner_query()
            owner = db.session.execute(owner_query, {"name": row_data["album_name"]}).fetchone()._mapping

            albumSQL = AlbumSQL(
                album_id=row_data["album_id"],
                album_name=row_data["album_name"],
                genre=row_data["genre"],
                release_date=row_data["release_date"],
                cover_image=row_data["cover_image"],
                artist_name=owner["artist_name"]
            )

            return Album().fromSQL(albumSQL)
        return None

    def addAlbum(self, album, artist):
        exists_query = get_album_by_name_query()
        result = db.session.execute(exists_query, {"name": album.album_name}).fetchone()
        if result:
            raise Exception("Album already exists")

        insert_query = insert_album_query()
        db.session.execute(insert_query, {
            "name": album.album_name,
            "genre": album.genre,
            "date": album.release_date,
            "cover": album.cover_image
        })
        db.session.commit()

        id_query = get_album_id_query()
        id_result = db.session.execute(id_query, {"name": album.album_name}).fetchone()
        album_id = id_result._mapping["album_id"]

        creates_query = insert_creates()
        db.session.execute(creates_query, {
            "album_id": album_id,
            "artist_id": artist.artist_id
        })
        db.session.commit()

    def get_album_songs(self, album_name):
        self.songs = []

        album_id_query = get_album_id_query()
        album_id_result = db.session.execute(album_id_query, {"name": album_name}).fetchone()
        if not album_id_result:
            return []

        album_id = album_id_result._mapping["album_id"]

        owner_query = get_album_owner_query()
        owner_result = db.session.execute(owner_query, {"name": album_name}).fetchone()
        artist_name = owner_result._mapping["artist_name"] if owner_result else "Unknown"

        songs_query = get_songs_of_album()
        result = db.session.execute(songs_query, {"album_id": album_id})

        for row in result:
            row_data = row._mapping
            songSQL = SongSQL(
                song_id=row_data["song_id"],
                song_name=row_data["song_name"],
                genre=row_data["genre"],
                artist_name=artist_name,
                release_date=row_data["release_date"],
                url=row_data["url"]
            )
            self.songs.append(Song().fromSQL(songSQL))

        return self.songs

    def addSongToAlbum(self, album_name, song_name):
        song_query = get_song_by_name_query()
        song_result = db.session.execute(song_query, {"name":song_name}).fetchone()
        song_id = song_result._mapping["song_id"]

        album_id_query = get_album_id_query()
        album_result = db.session.execute(album_id_query, {"name": album_name}).fetchone()
        album_id = album_result._mapping["album_id"]

        insert_query = insert_song_into_album_query()
        db.session.execute(insert_query, {
            "song_id": song_id,
            "album_id": album_id
        })
        db.session.commit()

    def deleteSongFromAlbum(self, album_name, song_name):
        song_query = get_song_by_name_query()
        song_result = db.session.execute(  song_query, {"name":song_name}).fetchone()
        if not song_result:
            raise Exception("Song not found in album")
        song_id = song_result._mapping["song_id"]

        album_id_query = get_album_id_query()
        album_result = db.session.execute(album_id_query, {"name": album_name}).fetchone()
        if not album_result:
            raise Exception("album not found")
        album_id = album_result._mapping["album_id"]

        delete_query = delete_song_from_album_query()
        db.session.execute(delete_query, {
            "song_id": song_id,
            "album_id": album_id
        })
        db.session.commit()
