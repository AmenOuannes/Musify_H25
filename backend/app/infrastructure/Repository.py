from backend.app.utils.User import User


class Repository:
    def __init__(self):
        self.users = []
        self.users.append(User(username= "name", password = "password", email = "email", first_name = "first_name", last_name = "last_name"))


    def addUser(self, user):
        self.users.append(user)

    def getUser(self, username):
        return next((u for u in self.users if u.username == username), None)
