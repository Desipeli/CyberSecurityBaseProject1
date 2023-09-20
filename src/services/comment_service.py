from flask import session, abort
from repositories.comment_repository import comment_repository as default_comment_repository


class CommentService:
    def __init__(self, comment_repository=default_comment_repository):
        self.comment_repository = comment_repository

    def get_comment_by_moovie(self, id):
        res = self.comment_repository.get_comments_by_moovie(id)
        return res

    def get_comments(self):
        return self.comment_repository.get_comments()

    def add_comment(self, comment, moovie):
        return self.comment_repository.add_comment(
            comment, session["user_id"], moovie)

    def delete_comment(self, id):
        # comment_user_id = self.comment_repository.get_comment(id)["user"]
        # if session["user_id"] != comment_user_id:
        #     abort(401)
        return self.comment_repository.delete_comment(id)


comment_service = CommentService()
