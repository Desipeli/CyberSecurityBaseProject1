import secrets
from werkzeug.security import check_password_hash, generate_password_hash
from repositories.user_repository import user_repository as default_user_repository
from flask import session
import string


class UserService:
    def __init__(self, user_repository=default_user_repository):
        self.user_repository = user_repository

    def login(self, username, password):
        user = self.user_repository.get_user(username)
        if user and check_password_hash(user["password"], password):
            session.clear()
            session["username"] = user["username"]
            session["user_id"] = user["id"]
            session["csrf_token"] = secrets.token_hex(16)
            # self.check_and_update_password_hash(user["password"], password)
            return True

    def register_user(self, username, password):

        passwordhash = generate_password_hash(password, method="md5")

        return self.user_repository.register_user(username, passwordhash)

    def validate_passwords(self, password1, password2):
        if password1 != password2:
            return "Passwords do not match"
        if len(password1) < 12:
            return "Password must have at least 12 characters"

    def validate_username(self, username):
        if len(username) < 1:
            return "Username can not be empty"

    def get_users(self):
        users = self.user_repository.get_users()
        return [dict(row) for row in users]

    def logout(self):
        session.clear()

    # def check_and_update_password_hash(self, stored_hash, password):
    #     if stored_hash[:3].lower() == "md5":
    #         new_secure_hash = generate_password_hash(password)
    #         self.user_repository.update_password(
    #             session["user_id"], new_secure_hash)


user_service = UserService()
