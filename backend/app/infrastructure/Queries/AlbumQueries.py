from sqlalchemy import text


def get_all_albums_query(limit, research):
    if research == "":
        if int(limit) == -1:
            return text("SELECT * FROM Albums")
        return text("SELECT * FROM Albums LIMIT :limit")

    if int(limit) == -1:
        return text("SELECT * FROM Albums WHERE LOWER(album_name) LIKE :research")

    return text("SELECT * FROM Albums WHERE LOWER(album_name) LIKE :research LIMIT :limit")


def get_album_owner_query():
    return text("""
        SELECT A.artist_name
        FROM Artists A, Albums S, Creates R
        WHERE LOWER(S.album_name) = LOWER(:name)
          AND S.album_id = R.album_id
          AND A.artist_id = R.artist_id
    """)


def get_album_by_name_query():
    return text("""
        SELECT *
        FROM Albums
        WHERE LOWER(album_name) = LOWER(:name)
        LIMIT 1
    """)


def insert_album_query():
    return text("""
        INSERT INTO Albums (album_name, genre, release_date, cover_image)
        VALUES (:name, :genre, :date, :cover)
    """)


def insert_creates():
    return text("""
        INSERT INTO Creates (album_id, artist_id)
        VALUES (:album_id, :artist_id)
    """)


def get_album_id_query():
    return text("SELECT album_id FROM Albums WHERE LOWER(album_name) = LOWER(:name)")


def get_songs_of_album():
    return text("""
        SELECT * FROM Songs 
        WHERE song_id IN (
            SELECT song_id FROM Has WHERE album_id = :album_id
        )
    """)


def insert_song_into_album_query():
    return text("""
        INSERT INTO Has (song_id, album_id)
        VALUES (:song_id, :album_id)
    """)


def delete_song_from_album_query():
    return text("""
        DELETE FROM Has
        WHERE song_id = :song_id AND album_id = :album_id
    """)
