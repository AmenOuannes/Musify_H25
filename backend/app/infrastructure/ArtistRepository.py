from backend.app.domain.Artist import Artist
from backend.app.infrastructure.ArtistSQL import ArtistSQL
from backend.app.infrastructure.Queries import get_all_artists_query, get_artist_by_name_query, insert_artist_query
from backend.__init__ import db


class ArtistRepository():
    def __init__(self):
        self.artists = []

    def addArtist(self, artist):
        query = get_artist_by_name_query()
        result = db.session.execute(query, {"artist_name": artist.artist_name})
        count = result.scalar() or 0

        if count > 0:
            raise Exception("Artist already exists")
        else:
            insert_query = insert_artist_query()
            db.session.execute(insert_query, {
                "artist_name": artist.artist_name,
                "genre": artist.genre,
                "followers": artist.followers,
                "profile_url": artist.profile_url,
                "image": artist.image
            })
            db.session.commit()

    def getAllArtists(self, limit, research):
        self.artists = []
        query = get_all_artists_query(limit, research)
        params = {}
        if research:
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
