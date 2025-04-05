
def get_all_users_query(limit):
    return "SELECT * FROM Users;" if limit == -1 else f"SELECT * FROM Users LIMIT {limit};"

def insert_user_query(username, last_name, first_name, email, password_hash, date_naissance):
    return f"INSERT INTO Users (username, last_name, first_name, email, password_hash, date_naissance) VALUES ('{username}', '{last_name}', '{first_name}', '{email}', '{password_hash}', '{date_naissance}');"

def find_similar_users_query(username):
    return f"SELECT COUNT(*) AS count FROM Users WHERE username = '{username}';"

def get_user_with_username_query(username):
    return f"SELECT * FROM Users WHERE username = '{username}';"