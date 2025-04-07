
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
        return "SELECT * FROM Songs;" if limit == -1 else f"SELECT * FROM Songs LIMIT {limit};"
    return "SELECT * FROM Songs;" if limit == -1 else f"SELECT * FROM Songs LIMIT {limit};"
    safe_research = research.replace("'", "''")  # Escape single quotes
    base_query = f"SELECT * FROM Songs WHERE song_name LIKE '{safe_research}%'"
    return f"{base_query};" if limit == -1 else f"{base_query} LIMIT {limit};"


def get_song_by_name_query(song_name):
    return f"""
        SELECT song_id, song_name, genre, release_date, url
        FROM Songs
        WHERE song_name = '{song_name}';
    """

def insert_song_query( song_name, genre, release_date, url):
    return f"""
        INSERT INTO Songs (song_name, genre, release_date, url)
        VALUES ('{song_name}', '{genre}', '{release_date}', '{url}');
    """

def insert_sings(song_id, artist_id):
    return f"INSERT INTO Sings (song_id, artist_id) VALUES ('{song_id}', '{artist_id}');"

def get_singer_query(song_name):
    return f"SELECT A.artist_name FROM Artists A, Songs S, Sings R WHERE S.song_name='{song_name}' and S.song_id=R.song_id and A.artist_id=R.artist_id;"

def get_all_albums_query(limit, research):
    if research == "":
        return "SELECT * FROM Albums;" if limit == -1 else f"SELECT * FROM Albums LIMIT {limit};"
    safe_research = research.replace("'", "''")
    base_query = f"SELECT * FROM Albums WHERE album_name LIKE '{safe_research}%'"
    return f"{base_query};" if limit == -1 else f"{base_query} LIMIT {limit};"

def get_album_owner_query(album_name):
    return f"SELECT A.artist_name FROM Artists A, Albums S, Creates R WHERE S.album_name='{album_name}' and S.album_id=R.album_id and A.artist_id=R.artist_id;"

def get_album_by_name_query(album_name):
    return f"""
            SELECT *
            FROM Albums
            WHERE album_name = '{album_name}' LIMIT 1;"""

def insert_album_query(album_name, genre, release_date, cover_image):
    return f"""
        INSERT INTO Albums (album_name, genre, release_date, cover_image)
        VALUES ('{album_name}', '{genre}', '{release_date}', '{cover_image}')
    """

def insert_creates(album_id, artist_id):
    return f"""
        INSERT INTO Creates (album_id, artist_id)
        VALUES ('{album_id}', '{artist_id}')
    """

def get_album_id_query(album_name):
    return f"SELECT album_id FROM Albums WHERE album_name='{album_name}';"

def get_songs_of_album(album_id):
    return f"""
            SELECT * FROM Songs 
            WHERE song_id IN (
                SELECT song_id FROM Has WHERE album_id = '{album_id}'
            );
        """

def insert_song_into_album_query(song_id, album_id):
    return f"""
        INSERT INTO Has (song_id, album_id)
        VALUES ({song_id}, {album_id});
    """

def delete_song_from_album_query(song_id, album_id):
    return f"""
        DELETE FROM Has
        WHERE song_id = {song_id} AND album_id = {album_id};
    """

def get_playlist_by_name_query(playlist_name):
    return f"""
        SELECT playlist_id, playlist_name, owner, private
        FROM Playlists
        WHERE playlist_name = '{playlist_name}';
    """

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

    return f"SELECT * FROM Playlists{where_clause}{limit_clause};"

def insert_playlist_query(playlist_name, owner, private):
    return f"""
        INSERT INTO Playlists (playlist_name, owner, private)
        VALUES ('{playlist_name}', '{owner}', {private});
    """

def delete_playlist_query(playlist_name):
    safe_name = playlist_name.replace("'", "''")
    return f"""
            DELETE FROM Playlists
            WHERE playlist_name = '{safe_name}';
        """

def get_song_count_from_playlist_query(playlist_name, song_name):
    safe_playlist_name = playlist_name.replace("'", "''")
    safe_song_name = song_name.replace("'", "''")

    return f"""
        SELECT COUNT(*) 
        FROM Playlists P
        JOIN ConsistsOf C ON P.playlist_id = C.playlist_id
        JOIN Songs S ON C.song_id = S.song_id
        WHERE P.playlist_name = '{safe_playlist_name}'
          AND S.song_name = '{safe_song_name}';
    """

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
    return f"""
        INSERT INTO ConsistsOf (playlist_id, song_id)
        VALUES ({playlist_id}, {song_id});
    """

def delete_song_from_playlist_query(playlist_id, song_id):
    return f"""
        DELETE FROM ConsistsOf
        WHERE playlist_id = {playlist_id} AND song_id = {song_id};
    """

def get_liked_artists_query(username):
    return f"""
    SELECT *
    FROM Artists A
    INNER JOIN LikedArtists L ON A.artist_id = L.artist_id
    WHERE L.user_id = '{username}';
    """

def add_artist_to_likes(username, artist_id):
    return f"""
    INSERT INTO LikedArtists (artist_id, user_id) VALUES ({artist_id},'{username}');
    """
def unlike_artist(username, artist_id):
    return f"""
    DELETE FROM LikedArtists 
    WHERE artist_id = {artist_id} AND user_id = '{username}';
    """

def get_liked_playlists_query(user_id):
    return f"""
        SELECT *
        FROM Playlists P
        JOIN LikedPlaylists L ON P.playlist_id = L.playlist_id  -- This is just an example, update if you have a real playlist-like table
        WHERE L.user_id = '{user_id}';
    """

def unlike_playlist_query(user_id, playlist_id):
    return f"""
        DELETE FROM LikedPlaylists
        WHERE user_id = '{user_id}' AND playlist_id = {playlist_id};
    """
def like_playlist_query(user_id, playlist_id):
    return f"""
        INSERT INTO LikedPlaylists (user_id, playlist_id)
        VALUES ('{user_id}', {playlist_id});
    """
def get_liked_playlist_count_query(user_id, playlist_id):
    return f"""
        SELECT COUNT(*) 
        FROM LikedPlaylists
        WHERE user_id = '{user_id}' AND playlist_id = {playlist_id};
    """