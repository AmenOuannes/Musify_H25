from backend.app.utils.User import User


class UserRepository:
    def __init__(self):
        self.users = []
        self.users.append(User(username= "name", password = "password", email = "email", first_name = "first_name", last_name = "last_name"))


    def addUser(self, user):
        if self.getUser(user.username) is None and self.emailExists(user.email) is None:
            self.users.append(user)
        else:
            raise Exception("User exists")

    def getUser(self, username):
        return next((u for u in self.users if u.username == username), None)

    def getAllUsers(self, limit):
        if limit == -1:
            return self.users
        else:
            return self.users[:limit]

    def emailExists(self, email):
        return next((u for u in self.users if u.email == email), None)