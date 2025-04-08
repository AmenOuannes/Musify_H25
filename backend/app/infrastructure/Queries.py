from sqlalchemy import text

def get_all_users_query(limit):
    return "SELECT * FROM Users;" if limit == -1 else f"SELECT * FROM Users LIMIT {limit};"

def insert_user_query(username, last_name, first_name, email, password_hash, birth_date):
    return f"INSERT INTO Users (username, last_name, first_name, email, password_hash, birth_date) VALUES ('{username}', '{last_name}', '{first_name}', '{email}', '{password_hash}', '{birth_date}');"

def find_similar_users_query(username):
    return f"SELECT COUNT(*) AS count FROM Users WHERE username = '{username}';"

def get_user_with_username_query(username):
    return f"SELECT * FROM Users WHERE username = '{username}';"

def get_all_artists_query(limit, research):
    if research == "":
        return "SELECT * FROM Artists;" if limit == -1 else f"SELECT * FROM Artists LIMIT {limit};"
    safe_research = research.replace("'", "''")
    base_query = f"SELECT * FROM Artists WHERE artist_name LIKE '{safe_research}%'"
    return f"{base_query};" if limit == -1 else f"{base_query} LIMIT {limit};"


def get_artist_by_name_query(artist_name):
    return f"SELECT artist_id, artist_name, genre, followers, celebrity, profile_url, image FROM Artists WHERE artist_name='{artist_name}';"

def find_similar_artists_query(artist_name):
    return f"SELECT COUNT(*) AS count FROM Artists WHERE artist_name = '{artist_name}';"

def insert_artist_query(artist_name, genre, followers, profile_url, image):

    return f"""
        INSERT INTO Artists (artist_name, genre, followers, profile_url, image)
        VALUES ('{artist_name}', '{genre}', {followers}, '{profile_url}', '{image}');
    """

def update_user_query(current_username, username, first_name, last_name, email, password_hash, birth_date):
    return f"""
        UPDATE Users
        SET username = '{username}',
            first_name = '{first_name}',
            last_name = '{last_name}',
            email = '{email}',
            password_hash = '{password_hash}',
            birth_date = '{birth_date}'

        WHERE username = '{current_username}';
        """


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

def insert_sings(song_id, artist_id):
    return text(f"INSERT INTO Sings (song_id, artist_id) VALUES ('{song_id}', '{artist_id}');")

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
        return text("SELECT * FROM Albums WHERE LOWER(album_name) LIKE LOWER(:research)")
    return text("SELECT * FROM Albums WHERE LOWER(album_name) LIKE LOWER(:research) LIMIT :limit")

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

def insert_song_into_album_query(song_id, album_id):
    return text(f"""
        INSERT INTO Has (song_id, album_id)
        VALUES ({song_id}, {album_id});
    """)

def delete_song_from_album_query(song_id, album_id):
    return text(f"""
        DELETE FROM Has
        WHERE song_id = {song_id} AND album_id = {album_id};
    """)

def get_playlist_by_name_query(playlist_name):
    return text(f"""
        SELECT playlist_id, playlist_name, owner, private
        FROM Playlists
        WHERE playlist_name = '{playlist_name}';
    """)

def get_all_playlists_query(limit, research, owner):
    conditions = []

    if research:
        safe_research = research.replace("'", "''")
        conditions.append(f"playlist_name LIKE '{safe_research}%'")

    if owner:
        safe_owner = owner.replace("'", "''")
        conditions.append(f"owner = '{safe_owner}'")

    where_clause = " WHERE " + " AND ".join(conditions) if conditions else ""
    limit_clause = f" LIMIT {limit}" if limit != -1 else ""

    return text(f"SELECT * FROM Playlists{where_clause}{limit_clause};")

def insert_playlist_query(playlist_name, owner, private):
    return text(f"""
        INSERT INTO Playlists (playlist_name, owner, private)
        VALUES ('{playlist_name}', '{owner}', {private});
    """)

def delete_playlist_query(playlist_name):
    safe_name = playlist_name.replace("'", "''")
    return text(f"""
            DELETE FROM Playlists
            WHERE playlist_name = '{safe_name}';
        """)

def get_song_count_from_playlist_query(playlist_name, song_name):
    safe_playlist_name = playlist_name.replace("'", "''")
    safe_song_name = song_name.replace("'", "''")

    return text(f"""
        SELECT COUNT(*) 
        FROM Playlists P
        JOIN ConsistsOf C ON P.playlist_id = C.playlist_id
        JOIN Songs S ON C.song_id = S.song_id
        WHERE P.playlist_name = '{safe_playlist_name}'
          AND S.song_name = '{safe_song_name}';
    """)

def get_songs_from_playlist_query(playlist_name, owner):
    safe_name = playlist_name.replace("'", "''")

    query = f"""
        SELECT S.song_id, S.song_name, S.genre, S.release_date, S.url
        FROM Playlists P
        JOIN ConsistsOf C ON P.playlist_id = C.playlist_id
        JOIN Songs S ON C.song_id = S.song_id
        WHERE P.playlist_name = '{safe_name}'
    """

    if owner:
        safe_owner = owner.replace("'", "''")
        query += f" AND P.owner = '{safe_owner}'"

    return query + ";"

def insert_song_into_playlist_query(playlist_id, song_id):
    return text(f"""
        INSERT INTO ConsistsOf (playlist_id, song_id)
        VALUES ({playlist_id}, {song_id});
    """)

def delete_song_from_playlist_query(playlist_id, song_id):
    return text(f"""
        DELETE FROM ConsistsOf
        WHERE playlist_id = {playlist_id} AND song_id = {song_id};
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