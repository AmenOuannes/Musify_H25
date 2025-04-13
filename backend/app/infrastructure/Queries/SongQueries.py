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
        INSERT INTO Songs (song_name, genre, release_date, url)
        VALUES (:name, :genre, :date, :url)
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

def song_exists_query():
    return text("SELECT DoesSongExist(:song_name) AS exists_flag")

def insert_sings_query():
    return text("CALL InsertIntoSings(:song_id, :artist_id)")

def get_songs_with_artist_ids():
    return text("""
        SELECT s.song_id, s.song_name, s.genre, s.release_date, s.url, sg.artist_id
        FROM Songs s
        JOIN Sings sg ON s.song_id = sg.song_id
        WHERE SG.artist_id = :artist_id
    """)
