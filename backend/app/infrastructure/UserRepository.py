from backend.app.domain.User import User
from backend.__init__ import db
from sqlalchemy import text

from backend.app.infrastructure.Queries import get_all_users_query, find_similar_users_query, insert_user_query, \
    get_user_with_username_query
from backend.app.infrastructure.UserSQL import UserSQL


class UserRepository:
    def __init__(self):
        self.users = []

    def addUser(self, user):
        user_exists = find_similar_users_query(user.username)
        count = db.session.execute(text(user_exists))
        if count.scalar()>0:
            raise Exception('User already exists')

        add_query = insert_user_query(user.username, user.last_name, user.first_name, user.email, user.password, user.birth_date)
        db.session.execute(text(add_query))
        db.session.commit()

    def getUser(self, username):
        user_exists = find_similar_users_query(username)
        count = db.session.execute(text(user_exists))

        if count.scalar()>0:
            query = get_user_with_username_query(username)
            result_user = db.session.execute(text(query))
            row = result_user.fetchone()
            row_data = row._mapping

            userSQL = UserSQL(
                username=row_data["username"],
                password_hash=row_data["password_hash"],
                email=row_data["email"],
                first_name=row_data["first_name"],
                last_name=row_data["last_name"],
                birth_date=row_data["birth_date"]
            )
            return User().fromUserSQL(userSQL)
        else:
            return None

    def getAllUsers(self, limit):
        query = get_all_users_query(limit)
        result = db.session.execute(text(query))

        for row in result:
            row_data = row._mapping
            userSQL = UserSQL(
                username=row_data["username"],
                password_hash=row_data["password_hash"],
                email=row_data["email"],
                first_name=row_data["first_name"],
                last_name=row_data["last_name"],
                birth_date=row_data["birth_date"]
            )
            self.users.append(User().fromUserSQL(userSQL))

        return self.users

    def emailExists(self, email):
        return next((u for u in self.users if u.email == email), None)