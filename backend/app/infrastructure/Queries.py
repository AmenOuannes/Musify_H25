from sqlalchemy import text

def get_all_users_query(limit):
    return text("SELECT * FROM Users") if limit == -1 else text("SELECT * FROM Users LIMIT :limit")

def insert_user_query():
    return text("""
        INSERT INTO Users (username, last_name, first_name, email, password_hash, birth_date)
        VALUES (:username, :last_name, :first_name, :email, :password_hash, :birth_date)
    """)

def find_similar_users_query():
    return text("SELECT COUNT(*) AS count FROM Users WHERE username = :username")

def get_user_with_username_query():
    return text("SELECT * FROM Users WHERE username = :username")

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

def update_user_query():
    return text("""
        UPDATE Users
        SET username = :username,
            first_name = :first_name,
            last_name = :last_name,
            email = :email,
            password_hash = :password_hash,
            birth_date = :birth_date
        WHERE username = :current_username
    """)


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

def get_playlist_by_name_query():
    return text("""
        SELECT playlist_id, playlist_name, owner, private
        FROM Playlists
        WHERE LOWER(playlist_name) = LOWER(:playlist_name)
        LIMIT 1
    """)


def get_all_playlists_query(limit, research, owner):
    if not research and not owner:
        if int(limit) == -1:
            return text("SELECT * FROM Playlists")
        return text("SELECT * FROM Playlists LIMIT :limit")

    base_query = "SELECT * FROM Playlists WHERE"
    conditions = []

    if research:
        conditions.append("LOWER(playlist_name) LIKE :research")
    if owner:
        conditions.append("LOWER(owner) = LOWER(:owner)")

    where_clause = " AND ".join(conditions)

    if int(limit) == -1:
        return text(f"{base_query} {where_clause}")

    return text(f"{base_query} {where_clause} LIMIT :limit")


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


def get_liked_artists_query(username):
    return text(f"""
    SELECT *
    FROM Artists A
    INNER JOIN LikedArtists L ON A.artist_id = L.artist_id
    WHERE L.user_id = '{username}';
    """)

def add_artist_to_likes(username, artist_id):
    return text(f"""
    INSERT INTO LikedArtists (artist_id, user_id) VALUES ({artist_id},'{username}');
    """)
def unlike_artist(username, artist_id):
    return text(f"""
    DELETE FROM LikedArtists 
    WHERE artist_id = {artist_id} AND user_id = '{username}';
    """)

def get_liked_playlists_query(user_id):
    return text(f"""
        SELECT *
        FROM Playlists P
        JOIN LikedPlaylists L ON P.playlist_id = L.playlist_id  -- This is just an example, update if you have a real playlist-like table
        WHERE L.user_id = '{user_id}';
    """)

def unlike_playlist_query(user_id, playlist_id):
    return text(f"""
        DELETE FROM LikedPlaylists
        WHERE user_id = '{user_id}' AND playlist_id = {playlist_id};
    """)
def like_playlist_query(user_id, playlist_id):
    return text(f"""
        INSERT INTO LikedPlaylists (user_id, playlist_id)
        VALUES ('{user_id}', {playlist_id});
    """)
def get_liked_playlist_count_query(user_id, playlist_id):
    return text(f"""
        SELECT COUNT(*) 
        FROM LikedPlaylists
        WHERE user_id = '{user_id}' AND playlist_id = {playlist_id};
    """)