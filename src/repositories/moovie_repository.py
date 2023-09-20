from db import db as default_db
from sqlalchemy import text


class MoovieRepository:

    def __init__(self, db=default_db):
        self.db = db

    def get_moovies(self):
        sql = "SELECT * FROM Moovies"
        return self.db.session.execute(text(sql)).mappings().all()

    def get_moovie_by_id(self, id):
        sql = "SELECT * FROM Moovies WHERE id=:id"
        return self.db.session.execute(
            text(sql), {"id": id}).mappings().first()


moovie_repository = MoovieRepository()
