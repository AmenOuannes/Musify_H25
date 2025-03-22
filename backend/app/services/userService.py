from backend.app.utils import user
from backend.app.utils.user import User

class userService:
    def __init__(self):
        pass

    def getUser(self):
        return [{"id": 1, "name": "John Doe"},
    {"id": 2, "name": "Jane Doe"}]

    def createUser(self, username, first_name, last_name, email, password):
        self.user = User(username, first_name, last_name, email, password)
        self.repository.addUser(self.user)
