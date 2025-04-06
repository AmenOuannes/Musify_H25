
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
    return f"SELECT artist_id, artist_name, genre, followers, celebrity, profile_url, image FROM Artists WHERE artist_name = '{artist_name}';"

def find_similar_artists_query(artist_name):
    return f"SELECT COUNT(*) AS count FROM Artists WHERE artist_name = '{artist_name}';"

def insert_artist_query(artist_id, artist_name, genre, followers, profile_url, image):

    return f"""
        INSERT INTO Artists (artist_id, artist_name, genre, followers, profile_url, image)
        VALUES ({artist_id}, '{artist_name}', '{genre}', {followers}, '{profile_url}', '{image}');
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

def insert_song_query(song_id, song_name, genre, release_date, url):
    # Safely escape single quotes in string values
    song_name = song_name.replace("'", "''")
    genre = genre.replace("'", "''")
    url = url.replace("'", "''")

    return f"""
        INSERT INTO Songs (song_id, song_name, genre, release_date, url)
        VALUES ({song_id}, '{song_name}', '{genre}', '{release_date}', '{url}');
    """