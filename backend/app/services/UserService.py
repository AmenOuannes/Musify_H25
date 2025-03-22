from backend.app.infrastructure.Repository import Repository
from backend.app.utils.User import User

class UserService:
    def __init__(self):
        self.repository = Repository()

    def getUsers(self):
        return [user.to_dict() for user in self.repository.users]

    def createUser(self, username, first_name, last_name, email, password):
        self.repository.addUser(User(username, first_name, last_name, email, password))

    def retriveUser(self, username, password):
        user = self.repository.getUser(username)
        if not user:
            raise Exception('User not found')
        if user.password == password:
            return user.to_dict()
        else:
            raise Exception('Wrong password')
