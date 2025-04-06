
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