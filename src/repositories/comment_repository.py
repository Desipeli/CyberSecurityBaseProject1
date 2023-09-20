from db import db as default_db
from sqlalchemy import text


class CommentRepository:

    def __init__(self, db=default_db):
        self.db = db

    def get_comments(self):
        sql = "SELECT * FROM Comments"
        return self.db.session.execute(text(sql)).mappings().all()

    def get_comment(self, id):
        sql = "SELECT * FROM Comments WHERE id=:id"
        return self.db.session.execute(text(sql), {"id": id}).mappings().first()

    def get_comments_by_moovie(self, id):
        sql = "SELECT C.*, U.username FROM Comments AS C JOIN Users AS U ON C.user = U.id WHERE C.moovie=:id"
        return self.db.session.execute(
            text(sql), {"id": id}).mappings().all()

    def add_comment(self, comment, user, moovie):
        # sql = "INSERT INTO Comments(comment, user, moovie) VALUES(:comment, :user, :moovie)"
        # self.db.session.execute(
        #     text(sql), {"comment": comment, "user": user, "moovie": moovie}
        # )
        # self.db.session.commit()
        try:
            sql = f"INSERT INTO Comments(comment, user, moovie) VALUES('{comment}', {user}, {moovie})"
            print(sql)
            self.db.session.execute(
                text(sql))
            self.db.session.commit()
            return True
        except Exception:
            return False

    def delete_comment(self, id):
        sql = "DELETE FROM Comments WHERE id=:id"
        try:
            self.db.session.execute(
                text(sql), {"id": id})
            self.db.session.commit()
            return True
        except Exception:
            return False


comment_repository = CommentRepository()
