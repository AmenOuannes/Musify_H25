
def get_all_users_query(limit):
    return "SELECT * FROM Users;" if limit == -1 else f"SELECT * FROM Users LIMIT {limit};"

def insert_user_query(username, last_name, first_name, email, password_hash, birth_date):
    return f"INSERT INTO Users (username, last_name, first_name, email, password_hash, birth_date) VALUES ('{username}', '{last_name}', '{first_name}', '{email}', '{password_hash}', '{birth_date}');"

def find_similar_users_query(username):
    return f"SELECT COUNT(*) AS count FROM Users WHERE username = '{username}';"

def get_user_with_username_query(username):
    return f"SELECT * FROM Users WHERE username = '{username}';"

def get_all_artists_query(limit):
    return "SELECT * FROM Artists;" if limit == -1 else f"SELECT * FROM Artists LIMIT {limit};"

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