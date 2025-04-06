from sqlalchemy import text

from backend.app.domain.Artist import Artist
from backend.app.infrastructure.ArtistSQL import ArtistSQL
from backend.app.infrastructure.Queries import get_all_artists_query, get_artist_by_name_query, insert_artist_query
from backend.__init__ import db


class ArtistRepository():
    def __init__(self):
        self.artists = []

    def addArtist(self, artist):
        artist_exists = get_artist_by_name_query(artist.artist_name)
        result = db.session.execute(text(artist_exists))
        count = result.scalar() or 0

        if count>0:
            raise Exception("Artist already exists")
        else:

            query = insert_artist_query(artist.artist_id, artist.artist_name, artist.genre, artist.followers, artist.profile_url, artist.image)
            db.session.execute(text(query))
            db.session.commit()


    def getAllArtists(self, limit,research):
        self.artists=[]
        query = get_all_artists_query(limit,research)

        result = db.session.execute(text(query))
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
        query = get_artist_by_name_query(artist_name)
        result = db.session.execute(text(query))
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


