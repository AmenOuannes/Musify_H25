from sqlalchemy.exc import DBAPIError

from backend.__init__ import db
from backend.app.domain.Album import Album
from backend.app.domain.Artist import Artist
from backend.app.domain.Song import Song
from backend.app.infrastructure.Queries.AlbumQueries import get_albums_with_artist_ids
from backend.app.infrastructure.Queries.ArtistQueries import *
from backend.app.infrastructure.Queries.SongQueries import get_songs_with_artist_ids
from backend.app.infrastructure.SQL.AlbumSQL import AlbumSQL
from backend.app.infrastructure.SQL.ArtistSQL import ArtistSQL
from backend.app.infrastructure.SQL.songSQL import SongSQL


class ArtistRepository:
    def __init__(self):
        self.artists = []

    def addArtist(self, artist):
        query = artist_exists_query()
        result = db.session.execute(query, {"artist_name": artist.artist_name})
        row = result.fetchone()

        if row._mapping['exists_flag'] == 1:
            raise Exception("Artist already exists")
        else:
            try:
                insert_query = insert_artist_query()
                db.session.execute(insert_query, {
                    "artist_name": artist.artist_name,
                    "genre": artist.genre,
                    "followers": artist.followers,
                    "profile_url": artist.profile_url,
                    "image": artist.image
                })
                db.session.commit()
            except DBAPIError as e:
                db.session.rollback()
                if e.orig:
                    raise Exception(f"Database error: {str(e.orig)}")
                else:
                    raise Exception("An unknown database error occurred.")

    def get_all_artists(self, limit, research):
        self.artists = []
        query = get_all_artists_query(limit, research)
        params = {}
        if research!="":
            params["research"] = f"{research}%"
        if int(limit) != -1:
            params["limit"] = int(limit)

        result = db.session.execute(query, params)
        for row in result:
            row_data = row._mapping

            artistSQL = ArtistSQL(
                artist_id=row_data["artist_id"],
                artist_name=row_data["artist_name"],
                genre=row_data["genre"],
                followers=row_data["followers"],
                celebrity=row_data["celebrity"],
                profile_url=row_data["profile_url"],
                image=row_data["image"]
            )

            self.artists.append(Artist().fromArtistSQL(artistSQL))

        return self.artists

    def getArtistByName(self, artist_name):
        query = get_artist_by_name_query()
        result = db.session.execute(query, {"artist_name": artist_name})
        row = result.fetchone()
        if row:
            row_data = row._mapping

            artistSQL = ArtistSQL(
                artist_id=row_data["artist_id"],
                artist_name=row_data["artist_name"],
                genre=row_data["genre"],
                followers=row_data["followers"],
                celebrity=row_data["celebrity"],
                profile_url=row_data["profile_url"],
                image=row_data["image"]
            )

            return Artist().fromArtistSQL(artistSQL)
        else:
            return None

    def get_songs_of_artist(self, artist_name):
        artist_query = get_artist_by_name_query()
        result = db.session.execute(artist_query, {"artist_name": artist_name})
        artist_id = result.fetchone()._mapping["artist_id"]
        
        songs_query = get_songs_with_artist_ids()
        result = db.session.execute(songs_query, {"artist_id": artist_id})
        songs = []
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
            songs.append(Song().fromSQL(songSQL))

        return songs

    def get_albums_of_artist(self, artist_name):
        artist_query = get_artist_by_name_query()
        result = db.session.execute(artist_query, {"artist_name": artist_name})
        artist_id = result.fetchone()._mapping["artist_id"]
        print("query done")

        albums_query = get_albums_with_artist_ids()
        result = db.session.execute(albums_query, {"artist_id": artist_id})
        print("query done")
        albums = []
        for row in result:
            row_data = row._mapping
            albumSQL = AlbumSQL(
                album_id=row_data["album_id"],
                album_name=row_data["album_name"],
                genre=row_data["genre"],
                release_date=row_data["release_date"],
                cover_image=row_data["cover_image"],
                artist_name=artist_name
            )
            albums.append(Album().fromSQL(albumSQL))

        return albums



