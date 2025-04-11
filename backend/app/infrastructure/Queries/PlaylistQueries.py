from sqlalchemy.sql import text

def get_playlist_by_name_query():
    return text("""
        SELECT playlist_id, playlist_name, owner, private
        FROM Playlists
        WHERE LOWER(playlist_name) = LOWER(:playlist_name)
        LIMIT 1
    """)


def get_all_playlists_query(limit, research, owner, private):
    conditions = []

    if private == 0:
        conditions.append("private = 0")

    if research:
        conditions.append("LOWER(playlist_name) LIKE :research")

    if owner:
        conditions.append("LOWER(owner) = LOWER(:owner)")

    query = "SELECT * FROM Playlists"

    if conditions:
        where_clause = " AND ".join(conditions)
        query += f" WHERE {where_clause}"

    if int(limit) != -1:
        query += " LIMIT :limit"

    return text(query)


def insert_playlist_query():
    return text("""
        INSERT INTO Playlists (playlist_name, owner, private)
        VALUES (:playlist_name, :owner, :private)
    """)


def delete_playlist_query():
    return text("""
        DELETE FROM Playlists
        WHERE LOWER(playlist_name) = LOWER(:playlist_name)
    """)


def get_song_count_from_playlist_query():
    return text("""
        SELECT COUNT(*) 
        FROM Playlists P
        JOIN ConsistsOf C ON P.playlist_id = C.playlist_id
        JOIN Songs S ON C.song_id = S.song_id
        WHERE LOWER(P.playlist_name) = LOWER(:playlist_name)
          AND LOWER(S.song_name) = LOWER(:song_name)
    """)


def get_songs_from_playlist_query():
    return text("""
        SELECT S.song_id, S.song_name, S.genre, S.release_date, S.url
        FROM Playlists P
        JOIN ConsistsOf C ON P.playlist_id = C.playlist_id
        JOIN Songs S ON C.song_id = S.song_id
        WHERE LOWER(P.playlist_name) = LOWER(:playlist_name)
          AND LOWER(P.owner) = LOWER(:owner)
    """)


def insert_song_into_playlist_query():
    return text("""
        INSERT INTO ConsistsOf (playlist_id, song_id)
        VALUES (:playlist_id, :song_id)
    """)


def delete_song_from_playlist_query():
    return text("""
        DELETE FROM ConsistsOf
        WHERE playlist_id = :playlist_id AND song_id = :song_id
    """)


def get_liked_artists_query(research):
    base_query = """
    SELECT *
    FROM Artists A
    INNER JOIN LikedArtists L ON A.artist_id = L.artist_id
    WHERE L.user_id = :username
    """

    if research:
        base_query += " AND LOWER(A.artist_name) LIKE :research"

    return text(base_query)

