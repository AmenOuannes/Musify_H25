from backend.app.infrastructure.UserRepository import UserRepository
from backend.app.utils.User import User

class UserService:
    def __init__(self):
        self.repository = UserRepository()

    def getUsers(self, limit=-1):
        return [user.to_dict() for user in self.repository.getAllUsers(limit)]

    def createUser(self, username, first_name, last_name, email, password):
        try:
            self.repository.addUser(User(username, first_name, last_name, email, password))
        except (Exception) as e:
            raise e

    def login(self, username, password):
        user = self.repository.getUser(username)
        if not user:
            raise Exception('User not found')
        if user.password == password:
            return True
        else:
            raise Exception('Wrong password')

    def retrieveUser(self, username):
        user = self.repository.getUser(username)
        if not user:
            raise Exception('User not found')
        return user.to_dict()