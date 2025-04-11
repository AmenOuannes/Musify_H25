from sqlalchemy import text


def get_all_songs_query(limit, research):
    if research == "":
        if int(limit) == -1:
            return text("SELECT * FROM Songs")
        return text("SELECT * FROM Songs LIMIT :limit")

    if int(limit) == -1:
        return text("""
            SELECT * FROM Songs
            WHERE LOWER(song_name) LIKE LOWER(:research)
        """)
    return text("""
        SELECT * FROM Songs
        WHERE LOWER(song_name) LIKE LOWER(:research)
        LIMIT :limit
    """)


def get_song_by_name_query():
    return text("""
        SELECT song_id, song_name, genre, release_date, url
        FROM Songs
        WHERE LOWER(song_name) = LOWER(:name)
    """)


def insert_song_query():
    return text("""
        INSERT INTO Songs (song_name, genre, release_date, url, artist_id)
        VALUES (:name, :genre, :date, :url, :artist_id)
    """)


def insert_sings():
    return text("""
        INSERT INTO Sings (song_id, artist_id)
        VALUES (:song_id, :artist_id)
    """)


def get_singer_query():
    return text("""
        SELECT A.artist_name
        FROM Artists A
        JOIN Sings R ON A.artist_id = R.artist_id
        JOIN Songs S ON R.song_id = S.song_id
        WHERE LOWER(S.song_name) = LOWER(:name)
    """)
