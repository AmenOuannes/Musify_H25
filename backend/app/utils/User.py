from collections import OrderedDict



class User:
    def __init__(self, username, first_name, last_name, email, password ):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

    def to_dict(self):
        return OrderedDict([
            ("username", self.username),
            ("first_name", self.first_name),
            ("last_name", self.last_name),
            ("email", self.email),
            ("password", self.password)
        ])