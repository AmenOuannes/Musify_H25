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

def add_artist_to_likes():
    return text(f"""
    INSERT INTO LikedArtists (artist_id, user_id) VALUES (':artist_id', :username);
    """)

def unlike_artist():
    return text(f"""
    DELETE FROM LikedArtists 
    WHERE artist_id = :artist_id AND user_id = :username;
    """)

def get_liked_playlists_query(research=False):
    base_query = """
        SELECT *
        FROM Playlists P
        JOIN LikedPlaylists L ON P.playlist_id = L.playlist_id
        WHERE L.user_id = :user_id
    """

    if research:
        base_query += " AND LOWER(P.playlist_name) LIKE :research"

    return text(base_query)

def unlike_playlist_query():
    return text(f"""
        DELETE FROM LikedPlaylists
        WHERE user_id = :user_id AND playlist_id = :playlist_id;
    """)
def like_playlist_query():
    return text(f"""
        INSERT INTO LikedPlaylists (user_id, playlist_id)
        VALUES (:user_id, :playlist_id);
    """)
def get_liked_playlist_count_query():
    return text(f"""
        SELECT COUNT(*) 
        FROM LikedPlaylists
        WHERE user_id = :user_id AND playlist_id = :playlist_id;
    """)