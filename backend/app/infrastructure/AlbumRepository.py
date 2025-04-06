from sqlalchemy import text
from backend.__init__ import db


from backend.app.domain.Album import Album
from backend.app.domain.Song import Song
from backend.app.infrastructure.AlbumSQL import AlbumSQL
from backend.app.infrastructure.Queries import get_all_albums_query, get_singer_query, get_album_owner_query, \
    get_album_by_name_query, insert_album_query, insert_creates, get_album_id_query, get_songs_of_album, \
    insert_song_into_album_query, get_song_by_name_query, delete_song_from_album_query
from backend.app.infrastructure.songSQL import SongSQL
from backend.app.routes.ArtistRoute import add_artist


class AlbumRepository:
    def __init__(self):
        self.albums = []
        self.songs = []

    def getAlbums(self, limit, research):
        self.albums = []
        query = get_all_albums_query(limit, research)
        result = db.session.execute(text(query))
        for row in result:
            row_data = row._mapping
            owner_query = get_album_owner_query(row_data["album_name"])
            owner = db.session.execute(text(owner_query)).fetchone()._mapping
            albumSQL = AlbumSQL(
                album_id=row_data["album_id"],
                album_name=row_data["album_name"],
                genre=row_data["genre"],
                release_date=row_data["release_date"],
                cover_image=row_data["cover_image"],
                artist_name=owner["artist_name"]
            )

            self.albums.append(Album().fromSQL(albumSQL))

        return self.albums

    def get_album(self, album_name):
        query = get_album_by_name_query(album_name)
        result = db.session.execute(text(query))
        row = result.fetchone()
        if row:
            row_data = row._mapping
            owner_query = get_album_owner_query(row_data["album_name"])
            owner = db.session.execute(text(owner_query)).fetchone()._mapping
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
        album_exists = get_album_by_name_query(album.album_name)
        result = db.session.execute(text(album_exists))
        count = result.scalar() or 0

        if count > 0:
            raise Exception("Album already exists")
        else:
            album_query = insert_album_query(
                album.album_name,
                album.genre,
                album.release_date,
                album.cover_image
            )

            db.session.execute(text(album_query))
            db.session.commit()
            print('inserted')
            id_query = get_album_id_query(album.album_name)
            id =db.session.execute(text(id_query)).fetchone()._mapping["album_id"]
            print(id)
            creates_query = insert_creates(id, artist.artist_id)
            db.session.execute(text(creates_query))
            db.session.commit()

    def get_album_songs(self, album_name):
        self.songs = []
        album_id_query = get_album_id_query(album_name)
        album_id = db.session.execute(text(album_id_query)).fetchone()._mapping["album_id"]

        owner_query = get_album_owner_query(album_name)
        owner = db.session.execute(text(owner_query)).fetchone()._mapping

        songs_query = get_songs_of_album(album_id)
        result = db.session.execute(text(songs_query))
        count = result.scalar() or 0


        if count > 0:
            for row in result:
                row_data = row._mapping

                songSQL = SongSQL(
                    song_id=row_data["song_id"],
                    song_name=row_data["song_name"],
                    genre=row_data["genre"],
                    artist_name=owner["artist_name"],
                    release_date=row_data["release_date"],
                    url=row_data["url"]
                )

                self.songs.append(Song().fromSQL(songSQL))

            return self.songs
        return None

    def addSongToAlbum(self, album_name, song_name):
        get_song_id = get_song_by_name_query(song_name)
        song_id = db.session.execute(text(get_song_id)).fetchone()._mapping["song_id"]

        get_album_id = get_album_id_query(album_name)
        album_id = db.session.execute(text(get_album_id)).fetchone()._mapping["album_id"]

        insert_query = insert_song_into_album_query(song_id,album_id)
        db.session.execute(text(insert_query))
        db.session.commit()

    def deleteSongFromAlbum(self, album_name, song_name):
        get_song_id = get_song_by_name_query(song_name)
        song_id = db.session.execute(text(get_song_id)).fetchone()._mapping["song_id"]

        get_album_id = get_album_id_query(album_name)
        album_id = db.session.execute(text(get_album_id)).fetchone()._mapping["album_id"]

        insert_query = delete_song_from_album_query(song_id, album_id)
        db.session.execute(text(insert_query))
        db.session.commit()




