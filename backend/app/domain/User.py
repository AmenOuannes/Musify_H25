import hashlib
from collections import OrderedDict

from backend.app.domain.encryption import encrypt_password, KEY, decrypt_password


class User:
    def __init__(self):
        self.username = ""
        self.password = ""
        self.email = ""
        self.firstName = ""
        self.lastName = ""
        self.birth_date = ""

    def fromRequest(self, username, first_name, last_name, email, password, birth_date):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = encrypt_password(password, KEY)
        self.birth_date = birth_date
        return self

    def fromUserSQL(self, userSQL):
        self.username = userSQL.username
        self.first_name = userSQL.first_name
        self.last_name = userSQL.last_name
        self.email = userSQL.email
        self.password = decrypt_password(userSQL.password_hash, KEY)
        self.birth_date = userSQL.birth_date
        return self

    def to_dict(self):
        return OrderedDict([
            ("username", self.username),
            ("first_name", self.first_name),
            ("last_name", self.last_name),
            ("email", self.email),
            ("birth_date", self.birth_date.isoformat()),
            ("password", self.password)
        ])
