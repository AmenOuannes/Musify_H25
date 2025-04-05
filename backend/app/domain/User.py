from collections import OrderedDict


class User:
    def __init__(self):
        self.username = ""
        self.password = ""
        self.email = ""
        self.firstName = ""
        self.lastName = ""
        self.date_naissance=""

    def fromRequest(self, username, first_name, last_name, email, password, date_naissance):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.date_naissance = date_naissance
        return self

    def fromUserSQL(self, userSQL):
        self.username = userSQL.username
        self.first_name = userSQL.first_name
        self.last_name = userSQL.last_name
        self.email = userSQL.email
        self.password = userSQL.password_hash ##unhash
        self.date_naissance = userSQL.date_naissance
        return self


    def to_dict(self):
        return OrderedDict([
            ("username", self.username),
            ("first_name", self.first_name),
            ("last_name", self.last_name),
            ("email", self.email),
            ("password", self.password)
        ])