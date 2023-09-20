from db import db as default_db
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError


class UserRepository:

    def __init__(self, db=default_db):
        self.db = db

    def get_users(self):
        sql = "SELECT id, username FROM Users"
        return self.db.session.execute(text(sql)).mappings().all()

    def get_user(self, username):
        sql = "SELECT id, username, password FROM Users WHERE username=:username"
        return self.db.session.execute(
            text(sql), {"username": username}).mappings().first()

    def register_user(self, username, password):
        sql = "INSERT INTO users(username, password) VALUES (:username, :password)"
        try:
            self.db.session.execute(
                text(sql), {"username": username, "password": password})
            self.db.session.commit()
            return True
        except IntegrityError:
            self.db.session.rollback()
            return False

    # def update_password(self, user_id, password_hash):
    #     sql = "UPDATE Users SET password=:password_hash WHERE id=:user_id"
    #     res = self.db.session.execute(
    #         text(sql), {"password_hash": password_hash, "user_id": user_id})
    #     self.db.session.commit()


user_repository = UserRepository()
