from sqlalchemy import text


def get_all_artists_query(limit, research):
    if research == "":
        return text("SELECT * FROM Artists") if limit == -1 else text("SELECT * FROM Artists LIMIT :limit")

    return text("SELECT * FROM Artists WHERE artist_name LIKE :research") if limit == -1 else text("SELECT * FROM Artists WHERE artist_name LIKE :research LIMIT :limit")


def get_artist_by_name_query():
    return text("""
        SELECT artist_id, artist_name, genre, followers, celebrity, profile_url, image 
        FROM Artists 
        WHERE artist_name = :artist_name
    """)


def find_similar_artists_query():
    return text("SELECT COUNT(*) AS count FROM Artists WHERE artist_name = :artist_name")


def insert_artist_query():
    return text("""
        INSERT INTO Artists (artist_name, genre, followers, profile_url, image)
        VALUES (:artist_name, :genre, :followers, :profile_url, :image)
    """)
