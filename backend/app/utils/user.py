class User:
    def __init__(self, username, first_name, last_name, email, password ):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password_hash = password
